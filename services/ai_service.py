"""
Multimodal AI Service
Provides unified multimodal vision & text generation across Google Gemini 1.5/2.0
and Groq Vision/LLM models, with bulletproof structured JSON validation,
dynamic ModelService discovery, and demo fallback.
"""

import json
import re
import base64
import io
from typing import Dict, Any, List, Optional
from PIL import Image

from config import (
    PROVIDER_GEMINI,
    PROVIDER_GROQ,
    GEMINI_MODELS,
    GROQ_MODELS
)
from services.demo_data import (
    get_demo_food_recognition,
    get_demo_food_freshness,
    get_demo_kitchen_hygiene,
    get_demo_recipes,
    get_demo_meal_plan
)


def _clean_json_response(raw_text: str) -> Dict[str, Any]:
    """Extracts and parses JSON object or array from markdown code fences or raw string."""
    cleaned = raw_text.strip()
    # Strip markdown codeblocks
    if "```json" in cleaned:
        match = re.search(r"```json\s*(.*?)\s*```", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(1).strip()
    elif "```" in cleaned:
        match = re.search(r"```\s*(.*?)\s*```", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(1).strip()
    
    # Try parsing
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback regex search for { ... } or [ ... ]
        curly = re.search(r"(\{.*\})", cleaned, re.DOTALL)
        if curly:
            return json.loads(curly.group(1))
        square = re.search(r"(\[.*\])", cleaned, re.DOTALL)
        if square:
            return json.loads(square.group(1))
        raise


def _pil_to_base64_data_uri(image: Image.Image) -> str:
    """Encodes PIL Image into a base64 data URI for Groq/OpenAI compatible vision endpoints."""
    buffered = io.BytesIO()
    image.convert("RGB").save(buffered, format="JPEG", quality=85)
    img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{img_b64}"


NON_VISION_PATTERNS = [
    "tts", "audio", "embed", "imagen", "whisper", "speech", "bison", "learnlm", "robotics"
]


def is_valid_multimodal_model(name: str) -> bool:
    """Checks if a model is capable of multimodal vision (not TTS, embedding, or audio only)."""
    nl = name.lower()
    for pat in NON_VISION_PATTERNS:
        if pat in nl:
            return False
    return True


def get_available_gemini_models(api_key: str) -> List[str]:
    """Dynamically queries Google Gemini ModelService for multimodal vision-capable models."""
    if not api_key or not api_key.strip():
        return [m for m in GEMINI_MODELS if is_valid_multimodal_model(m)]
    
    discovered_models = []
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key.strip())
        for m in genai.list_models():
            if hasattr(m, "supported_generation_methods") and "generateContent" in m.supported_generation_methods:
                clean_name = m.name.replace("models/", "").strip()
                if is_valid_multimodal_model(clean_name):
                    discovered_models.append(clean_name)
    except Exception:
        pass

    if discovered_models:
        def vision_priority(name: str):
            n = name.lower()
            if "2.0-flash" in n:
                return (0, n)
            if "1.5-flash-latest" in n:
                return (1, n)
            if "1.5-flash-002" in n:
                return (2, n)
            if "1.5-flash" in n:
                return (3, n)
            if "1.5-pro-latest" in n:
                return (4, n)
            if "1.5-pro" in n:
                return (5, n)
            if "2.5-flash" in n:
                return (6, n)
            return (7, n)

        # Deduplicate while preserving order
        deduped = list(dict.fromkeys(discovered_models))
        deduped.sort(key=vision_priority)
        return deduped

    return [m for m in GEMINI_MODELS if is_valid_multimodal_model(m)]


def call_gemini_multimodal(api_key: str, requested_model: Optional[str], contents: list) -> str:
    """
    Executes a multimodal Gemini generation request with intelligent model name resolution,
    strict exclusion of non-vision/TTS models, and automatic fallback.
    """
    clean_api_key = api_key.strip()
    has_image = any(isinstance(c, Image.Image) or isinstance(c, (bytes, bytearray)) for c in contents)

    req = (requested_model or "gemini-2.0-flash").replace("models/", "").strip()

    # 1. Build initial candidate list
    raw_candidates = [req]
    for alias in [
        f"{req}-latest",
        f"{req}-002",
        f"{req}-001",
        "gemini-2.0-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash-002",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash",
        "gemini-1.5-pro-latest",
        "gemini-1.5-pro",
        "gemini-2.5-flash"
    ]:
        if alias not in raw_candidates:
            raw_candidates.append(alias)

    # 2. Query ModelService for verified models
    try:
        import google.generativeai as genai
        genai.configure(api_key=clean_api_key)
        discovered = [
            m.name.replace("models/", "").strip()
            for m in genai.list_models()
            if hasattr(m, "supported_generation_methods") and "generateContent" in m.supported_generation_methods
        ]
        if discovered:
            for d in reversed(discovered):
                if d in raw_candidates:
                    raw_candidates.remove(d)
                raw_candidates.insert(1, d)
    except Exception:
        pass

    # 3. Filter candidates: if request includes an image, strictly reject non-vision/TTS models
    if has_image:
        candidates = [c for c in raw_candidates if is_valid_multimodal_model(c)]
    else:
        candidates = raw_candidates

    if not candidates:
        candidates = ["gemini-2.0-flash", "gemini-1.5-flash-latest", "gemini-1.5-flash", "gemini-1.5-pro"]

    last_error = None

    # 4. Attempt candidates sequentially with google.generativeai
    import google.generativeai as genai
    genai.configure(api_key=clean_api_key)

    for model_id in candidates:
        try:
            model = genai.GenerativeModel(model_id)
            response = model.generate_content(contents)
            if response and response.text:
                return response.text
        except Exception as e:
            err_msg = str(e).lower()
            last_error = e

            # Check if this error indicates an unsupported model or modality
            is_skippable = (
                "404" in err_msg or
                "not found" in err_msg or
                "not supported for generatecontent" in err_msg or
                "is not found" in err_msg or
                "modality is not enabled" in err_msg or
                "image input modality" in err_msg or
                "invalid model" in err_msg
            )
            if is_skippable:
                continue

            # Check if the new google-genai SDK can succeed
            try:
                from google import genai as new_genai
                client = new_genai.Client(api_key=clean_api_key)
                new_resp = client.models.generate_content(model=model_id, contents=contents)
                if new_resp and new_resp.text:
                    return new_resp.text
            except Exception:
                pass

            # If it's a critical auth or quota error, re-raise immediately
            raise e

    # 5. Final attempt with new google-genai SDK using primary models
    try:
        from google import genai as new_genai
        client = new_genai.Client(api_key=clean_api_key)
        for m_id in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]:
            try:
                new_resp = client.models.generate_content(model=m_id, contents=contents)
                if new_resp and new_resp.text:
                    return new_resp.text
            except Exception:
                continue
    except Exception:
        pass

    if last_error:
        raise last_error
    raise RuntimeError(f"Could not generate content with model '{requested_model}' or any available fallback.")


# =====================================================================
# 1. Food Recognition and Nutrition Audit
# =====================================================================
def analyze_food_image(
    image: Image.Image,
    provider: str,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> Dict[str, Any]:
    """Analyzes a food dish photograph for dish identity, ingredients, portion, and nutrition."""
    if not api_key or not api_key.strip():
        demo = get_demo_food_recognition()
        demo["is_demo"] = True
        demo["demo_notice"] = "Displaying demonstration data (no API key configured)."
        return demo

    prompt = (
        "You are an expert food scientist, certified dietitian, and computer vision AI. "
        "Analyze this food dish photograph and return ONLY a valid JSON object strictly matching this schema:\n"
        "{\n"
        '  "dish_name": "Name of the dish",\n'
        '  "cuisine_type": "Cuisine category",\n'
        '  "visible_ingredients": ["list", "of", "ingredients"],\n'
        '  "portion_size": "Estimated portion in grams and description",\n'
        '  "calories_kcal": 450,\n'
        '  "protein_g": 25.0,\n'
        '  "carbs_g": 45.0,\n'
        '  "fats_g": 15.0,\n'
        '  "fiber_g": 6.0,\n'
        '  "micronutrients": {"Calcium": "300 mg", "Iron": "3 mg", "Vitamin C": "25 mg"},\n'
        '  "allergen_alerts": ["Potential allergens e.g. Dairy, Nuts, Gluten"],\n'
        '  "health_score": 85,\n'
        '  "health_badge": "Brief 3-word badge",\n'
        '  "health_analysis": "Scientific nutritional breakdown of nutritional quality."\n'
        "}\n"
        "Do not include any conversational text or markdown explanation outside the JSON."
    )

    try:
        if provider == PROVIDER_GEMINI:
            raw_text = call_gemini_multimodal(api_key, model_name, [prompt, image])
            data = _clean_json_response(raw_text)
            data["is_demo"] = False
            return data

        elif provider == PROVIDER_GROQ:
            from groq import Groq
            client = Groq(api_key=api_key)
            model_id = model_name or "llama-3.2-11b-vision-preview"
            data_uri = _pil_to_base64_data_uri(image)
            completion = client.chat.completions.create(
                model=model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": data_uri}}
                        ]
                    }
                ],
                temperature=0.2,
                response_format={"type": "json_object"} if "json_object" in model_id else None
            )
            raw = completion.choices[0].message.content
            data = _clean_json_response(raw)
            data["is_demo"] = False
            return data

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    except Exception as exc:
        demo = get_demo_food_recognition()
        demo["is_demo"] = True
        demo["demo_notice"] = f"AI Provider encountered an error ({str(exc)}). Displaying simulated demonstration data."
        demo["error_details"] = str(exc)
        return demo


# =====================================================================
# 2. Food Freshness and Spoilage Diagnostic
# =====================================================================
def analyze_food_freshness(
    image: Image.Image,
    provider: str,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> Dict[str, Any]:
    """Evaluates raw perishable food items (produce, meat, dairy) for visible freshness and spoilage."""
    if not api_key or not api_key.strip():
        demo = get_demo_food_freshness()
        demo["is_demo"] = True
        demo["demo_notice"] = "Displaying demonstration data (no API key configured)."
        return demo

    prompt = (
        "You are an expert post-harvest food scientist and quality assurance inspector. "
        "Examine this perishable food item image for visible deterioration, surface texture, discoloration, wrinkling, and mold. "
        "Classify into one of 3 categories: 'Fresh', 'Moderately Fresh', or 'Spoiled'. "
        "Assign actionable guidance: 'Safe to consume', 'Consume within 24 hours', or 'Discard immediately'. "
        "Return ONLY a valid JSON object strictly matching this schema:\n"
        "{\n"
        '  "food_item": "Specific name of the food item",\n'
        '  "food_category": "Category e.g. Fresh Fruit, Vegetable, Poultry, Dairy",\n'
        '  "freshness_category": "Fresh",\n'
        '  "actionable_guidance": "Safe to consume",\n'
        '  "confidence_score": 94,\n'
        '  "visual_indicators": [\n'
        '    {"feature": "Surface Texture", "observation": "detailed observation", "status": "Pass"},\n'
        '    {"feature": "Discoloration & Pigmentation", "observation": "detailed observation", "status": "Normal"},\n'
        '    {"feature": "Wrinkling & Turgidity", "observation": "detailed observation", "status": "Firm"},\n'
        '    {"feature": "Visible Mold / Microbial Mycelium", "observation": "detailed observation", "status": "Clear"}\n'
        '  ],\n'
        '  "storage_preservation_tips": [\n'
        '    "Tip 1 on optimal refrigeration or preparation",\n'
        '    "Tip 2 on freezing or preservation",\n'
        '    "Tip 3 on food safety"\n'
        '  ],\n'
        '  "microbial_risk_level": "Low / Moderate / High with biological explanation"\n'
        "}\n"
        "No conversational text outside the JSON."
    )

    try:
        if provider == PROVIDER_GEMINI:
            raw_text = call_gemini_multimodal(api_key, model_name, [prompt, image])
            data = _clean_json_response(raw_text)
            data["is_demo"] = False
            return data

        elif provider == PROVIDER_GROQ:
            from groq import Groq
            client = Groq(api_key=api_key)
            model_id = model_name or "llama-3.2-11b-vision-preview"
            data_uri = _pil_to_base64_data_uri(image)
            completion = client.chat.completions.create(
                model=model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": data_uri}}
                        ]
                    }
                ],
                temperature=0.2
            )
            raw = completion.choices[0].message.content
            data = _clean_json_response(raw)
            data["is_demo"] = False
            return data

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    except Exception as exc:
        demo = get_demo_food_freshness()
        demo["is_demo"] = True
        demo["demo_notice"] = f"AI Provider encountered an error ({str(exc)}). Displaying simulated demonstration data."
        demo["error_details"] = str(exc)
        return demo


# =====================================================================
# 3. Kitchen Hygiene and Food Safety Compliance
# =====================================================================
def analyze_kitchen_hygiene(
    images: List[Image.Image],
    provider: str,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> Dict[str, Any]:
    """Audits commercial kitchen photos or representative video frames for hygiene and HACCP compliance."""
    if not api_key or not api_key.strip():
        demo = get_demo_kitchen_hygiene()
        demo["is_demo"] = True
        demo["demo_notice"] = "Displaying demonstration data (no API key configured)."
        return demo

    prompt = (
        "You are an OSHA and FDA certified Food Safety Inspector and Commercial Kitchen Auditor. "
        "Inspect the provided kitchen image(s) or video keyframes for compliance indicators:\n"
        "1. Chef hat / hairnet compliance\n"
        "2. Glove usage & hand contact\n"
        "3. Surface cleanliness, sanitization & debris\n"
        "4. Cross-contamination hazards (e.g. raw poultry near ready-to-eat produce)\n"
        "5. Waste management and storage\n\n"
        "Return ONLY a valid JSON object strictly matching this schema:\n"
        "{\n"
        '  "overall_compliance_score": 82,\n'
        '  "compliance_rating": "Acceptable (Corrective Action Required)",\n'
        '  "rating_color": "#F59E0B",\n'
        '  "key_observations": "Summary of observations across audited scenes",\n'
        '  "metrics": {\n'
        '    "ppe_compliance": "85%",\n'
        '    "surface_sanitization": "90%",\n'
        '    "cross_contamination_control": "70%",\n'
        '    "waste_management": "95%"\n'
        '  },\n'
        '  "violations": [\n'
        '    {\n'
        '      "id": "VIOL-01",\n'
        '      "title": "Short title",\n'
        '      "description": "Violation description",\n'
        '      "visual_observation": "Exact visual evidence observed",\n'
        '      "severity": "High",\n'
        '      "severity_badge": "🔴 High Priority",\n'
        '      "corrective_action": "Mandatory standard action plan"\n'
        '    }\n'
        '  ],\n'
        '  "good_practices_observed": ["Practice 1", "Practice 2"],\n'
        '  "action_checklist": ["Action 1", "Action 2"]\n'
        "}\n"
        "No conversational text outside the JSON."
    )

    try:
        if provider == PROVIDER_GEMINI:
            contents = [prompt] + images[:4]
            raw_text = call_gemini_multimodal(api_key, model_name, contents)
            data = _clean_json_response(raw_text)
            data["is_demo"] = False
            return data

        elif provider == PROVIDER_GROQ:
            from groq import Groq
            client = Groq(api_key=api_key)
            model_id = model_name or "llama-3.2-11b-vision-preview"
            primary_img = images[0]
            data_uri = _pil_to_base64_data_uri(primary_img)
            completion = client.chat.completions.create(
                model=model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": data_uri}}
                        ]
                    }
                ],
                temperature=0.2
            )
            raw = completion.choices[0].message.content
            data = _clean_json_response(raw)
            data["is_demo"] = False
            return data

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    except Exception as exc:
        demo = get_demo_kitchen_hygiene()
        demo["is_demo"] = True
        demo["demo_notice"] = f"AI Provider encountered an error ({str(exc)}). Displaying simulated demonstration data."
        demo["error_details"] = str(exc)
        return demo


# =====================================================================
# 4. Smart Kitchen Recipe Assistant
# =====================================================================
def generate_smart_recipes(
    ingredients: List[str],
    dietary_pref: str = "Standard",
    provider: str = PROVIDER_GEMINI,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Generates creative, nutritious recipes maximizing available user ingredients."""
    if not api_key or not api_key.strip():
        demo = get_demo_recipes(ingredients)
        for r in demo:
            r["is_demo"] = True
            r["demo_notice"] = "Displaying demonstration recipes (no API key configured)."
        return demo

    ings_list = ", ".join(ingredients)
    prompt = (
        f"You are a master culinary chef and nutritionist. The user has the following ingredients available in their kitchen: {ings_list}. "
        f"Their dietary preference is: '{dietary_pref}'. "
        "Generate 2 to 3 creative, highly nutritious, and delicious recipes that prioritize these ingredients. "
        "Return ONLY a valid JSON array of recipe objects matching this exact structure:\n"
        "[\n"
        "  {\n"
        '    "recipe_name": "Recipe Title",\n'
        '    "description": "Appetizing description highlighting nutritional benefits",\n'
        '    "cuisine": "Cuisine type",\n'
        '    "difficulty": "Easy / Intermediate / Advanced",\n'
        '    "prep_time_minutes": 10,\n'
        '    "cook_time_minutes": 15,\n'
        '    "total_time_minutes": 25,\n'
        '    "servings": 2,\n'
        '    "calories_per_serving": 380,\n'
        '    "macros": {"protein_g": 20, "carbs_g": 35, "fats_g": 14, "fiber_g": 6.0},\n'
        '    "ingredients_used": ["Item with quantity"],\n'
        '    "pantry_staples_needed": ["Oil", "Salt", "Spices"],\n'
        '    "step_by_step_instructions": ["Step 1", "Step 2", "Step 3"],\n'
        '    "ingredient_substitutions": [\n'
        '      {"original": "Original item", "substitute": "Healthy/Vegan alternative", "reason": "Rationale"}\n'
        '    ],\n'
        '    "healthy_cooking_tips": "Practical tip on temperature, preservation of micronutrients, or digestion"\n'
        "  }\n"
        "]\n"
        "Do not include markdown or explanations outside the JSON."
    )

    try:
        if provider == PROVIDER_GEMINI:
            raw_text = call_gemini_multimodal(api_key, model_name, [prompt])
            data = _clean_json_response(raw_text)
            if isinstance(data, dict) and "recipes" in data:
                data = data["recipes"]
            for r in data:
                r["is_demo"] = False
            return data

        elif provider == PROVIDER_GROQ:
            from groq import Groq
            client = Groq(api_key=api_key)
            model_id = model_name or "llama-3.3-70b-versatile"
            completion = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            raw = completion.choices[0].message.content
            data = _clean_json_response(raw)
            if isinstance(data, dict) and "recipes" in data:
                data = data["recipes"]
            for r in data:
                r["is_demo"] = False
            return data

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    except Exception as exc:
        demo = get_demo_recipes(ingredients)
        for r in demo:
            r["is_demo"] = True
            r["demo_notice"] = f"AI Provider encountered an error ({str(exc)}). Displaying demonstration recipes."
        return demo


# =====================================================================
# 5. Personalized Meal Planner
# =====================================================================
def generate_personalized_meal_plan(
    profile: Dict[str, Any],
    provider: str = PROVIDER_GEMINI,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> Dict[str, Any]:
    """Generates an adaptive 7-day meal plan and consolidated grocery list."""
    target_cals = profile.get("target_calories", 2000)
    constraint = profile.get("dietary_constraint", "Standard")
    goal = profile.get("fitness_goal", "Maintenance")

    if not api_key or not api_key.strip():
        demo = get_demo_meal_plan(target_cals, constraint, goal)
        demo["is_demo"] = True
        demo["demo_notice"] = "Displaying demonstration meal plan (no API key configured)."
        return demo

    prompt = (
        f"You are a clinical sports dietitian and metabolic nutrition planner. "
        f"Create an adaptive 7-day meal plan (Monday to Sunday) for a user with the following profile:\n"
        f"- Target Daily Energy: {target_cals} kcal\n"
        f"- Dietary Constraint: {constraint}\n"
        f"- Fitness Goal: {goal}\n"
        f"- Age: {profile.get('age', 28)}, Gender: {profile.get('gender', 'Unspecified')}, Weight: {profile.get('weight_kg', 70)}kg\n\n"
        "Requirements:\n"
        "1. Every day must contain Breakfast, Lunch, Dinner, and Snacks that sum to approximately the target calories.\n"
        "2. Provide meal names, estimated ingredients, portions, calories, and macros (protein, carbs, fats).\n"
        "3. Provide a consolidated, non-duplicate grocery shopping list categorized into aisles (Produce, Proteins, Dairy/Alternatives, Whole Grains/Pantry, Healthy Fats).\n"
        "Return ONLY a valid JSON object strictly matching this schema:\n"
        "{\n"
        '  "target_calories": 2000,\n'
        '  "dietary_constraint": "Keto",\n'
        '  "fitness_goal": "Fat loss",\n'
        '  "days": [\n'
        '    {\n'
        '      "day": "Monday",\n'
        '      "day_number": 1,\n'
        '      "total_calories": 2000,\n'
        '      "total_protein_g": 130,\n'
        '      "total_carbs_g": 30,\n'
        '      "total_fats_g": 150,\n'
        '      "meals": {\n'
        '        "Breakfast": {"name": "Title", "ingredients": "list", "portion": "300g", "calories": 500, "protein": 30, "carbs": 5, "fats": 40},\n'
        '        "Lunch": {"name": "Title", "ingredients": "list", "portion": "400g", "calories": 700, "protein": 45, "carbs": 10, "fats": 52},\n'
        '        "Dinner": {"name": "Title", "ingredients": "list", "portion": "350g", "calories": 600, "protein": 45, "carbs": 10, "fats": 42},\n'
        '        "Snacks": {"name": "Title", "ingredients": "list", "portion": "100g", "calories": 200, "protein": 10, "carbs": 5, "fats": 16}\n'
        '      }\n'
        '    }\n'
        '  ],\n'
        '  "grocery_list": {\n'
        '    "🥦 Fresh Produce": [{"item": "Spinach", "quantity": "500g"}],\n'
        '    "🥩 Proteins": [{"item": "Salmon", "quantity": "800g"}],\n'
        '    "🧀 Dairy & Healthy Fats": [{"item": "Olive oil", "quantity": "500ml"}]\n'
        '  }\n'
        "}\n"
        "Do not include conversational text outside the JSON."
    )

    try:
        if provider == PROVIDER_GEMINI:
            raw_text = call_gemini_multimodal(api_key, model_name, [prompt])
            data = _clean_json_response(raw_text)
            data["is_demo"] = False
            return data

        elif provider == PROVIDER_GROQ:
            from groq import Groq
            client = Groq(api_key=api_key)
            model_id = model_name or "llama-3.3-70b-versatile"
            completion = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            raw = completion.choices[0].message.content
            data = _clean_json_response(raw)
            data["is_demo"] = False
            return data

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    except Exception as exc:
        demo = get_demo_meal_plan(target_cals, constraint, goal)
        demo["is_demo"] = True
        demo["demo_notice"] = f"AI Provider encountered an error ({str(exc)}). Displaying simulated demonstration meal plan."
        return demo
