"""
Demonstration Data Service for Food Verse AI
Provides realistic, medically sound, and domain-accurate simulated outputs
for all five core modules when operating without API keys.
"""

from typing import Dict, Any, List, Optional
import random


def get_demo_food_recognition(sample_name: Optional[str] = None) -> Dict[str, Any]:
    """Returns realistic food recognition and nutritional audit data."""
    catalog = {
        "paneer_tikka": {
            "dish_name": "Paneer Tikka Masala with Fragrant Brown Rice",
            "cuisine_type": "North Indian / Mughlai",
            "visible_ingredients": [
                "Charred Paneer cubes (cottage cheese)",
                "Rich spiced tomato-onion reduction",
                "Roasted green bell peppers",
                "Steamed whole grain brown rice",
                "Fresh cilantro (coriander) garnish",
                "Low-fat cream drizzle"
            ],
            "portion_size": "Estimated 380g (1 cup curry + 1 cup rice)",
            "calories_kcal": 495,
            "protein_g": 24.0,
            "carbs_g": 56.0,
            "fats_g": 19.0,
            "fiber_g": 6.8,
            "micronutrients": {
                "Calcium": "340 mg (34% DV)",
                "Iron": "3.2 mg (18% DV)",
                "Vitamin C": "35 mg (39% DV)",
                "Vitamin A": "450 mcg (50% DV)",
                "Potassium": "420 mg (9% DV)",
                "Sodium": "580 mg (25% DV)"
            },
            "allergen_alerts": [
                "Dairy (Paneer & dairy cream base)",
                "Trace Gluten (May be present in commercial curry bases)"
            ],
            "health_score": 84,
            "health_badge": "High Protein & Fiber • Moderately Rich",
            "health_analysis": (
                "Excellent balance of bioavailable vegetarian protein from paneer and slow-digesting complex "
                "carbohydrates from brown rice. Tomato and bell pepper lycopene/capsaicin provide powerful antioxidants. "
                "Moderation advised regarding sodium and dairy fat content."
            ),
            "is_demo": True
        },
        "mediterranean_chicken": {
            "dish_name": "Mediterranean Herb Grilled Chicken & Quinoa Harvest Bowl",
            "cuisine_type": "Mediterranean / Clean Eating",
            "visible_ingredients": [
                "Marinated grilled chicken breast strips",
                "Fluffy tri-color quinoa",
                "Persian cucumber ribbons",
                "Kalamata olives",
                "Cherry tomatoes halved",
                "Crumble sheep's milk feta",
                "Cold-pressed extra virgin olive oil vinaigrette"
            ],
            "portion_size": "Estimated 420g (Single harvest bowl)",
            "calories_kcal": 530,
            "protein_g": 42.0,
            "carbs_g": 44.0,
            "fats_g": 20.0,
            "fiber_g": 7.5,
            "micronutrients": {
                "Calcium": "190 mg (19% DV)",
                "Iron": "4.1 mg (23% DV)",
                "Vitamin C": "26 mg (29% DV)",
                "Magnesium": "95 mg (23% DV)",
                "Potassium": "680 mg (14% DV)",
                "Sodium": "510 mg (22% DV)"
            },
            "allergen_alerts": [
                "Dairy (Feta cheese)"
            ],
            "health_score": 93,
            "health_badge": "Superfood Tier • Cardiometabolic Friendly",
            "health_analysis": (
                "Superior macronutrient partition with high lean protein (42g) promoting satiety and muscle retention. "
                "Monounsaturated fatty acids from olive oil and complete amino-acid profile from quinoa enhance cardiovascular health."
            ),
            "is_demo": True
        },
        "vegan_avocado_salad": {
            "dish_name": "Zesty Avocado & Edamame Green Goddess Salad",
            "cuisine_type": "Plant-based / Modern Fusion",
            "visible_ingredients": [
                "Hass avocado slices",
                "Steamed green edamame beans",
                "Baby spinach & massaged kale mix",
                "Sprouted hemp seeds",
                "Pomegranate arils",
                "Tahini lemon dressing"
            ],
            "portion_size": "Estimated 320g (Entrée salad)",
            "calories_kcal": 410,
            "protein_g": 16.5,
            "carbs_g": 28.0,
            "fats_g": 27.0,
            "fiber_g": 12.0,
            "micronutrients": {
                "Folate": "210 mcg (53% DV)",
                "Iron": "3.8 mg (21% DV)",
                "Potassium": "790 mg (17% DV)",
                "Vitamin K": "380 mcg (317% DV)",
                "Vitamin E": "4.2 mg (28% DV)",
                "Sodium": "240 mg (10% DV)"
            },
            "allergen_alerts": [
                "Soy (Edamame beans)",
                "Sesame (Tahini paste)"
            ],
            "health_score": 96,
            "health_badge": "Nutrient Dense • Exceptional Fiber",
            "health_analysis": (
                "Outstanding dietary fiber content (12g, nearly 50% RDA) and heart-healthy oleic acid from avocado. "
                "Exceptionally low sodium footprint with abundant micronutrients."
            ),
            "is_demo": True
        }
    }

    if sample_name and sample_name in catalog:
        return catalog[sample_name]
    return list(catalog.values())[0]


def get_demo_food_freshness(food_type: Optional[str] = None) -> Dict[str, Any]:
    """Returns realistic food freshness and spoilage diagnostic data."""
    catalog = {
        "banana_speckled": {
            "food_item": "Cavendish Banana Cluster",
            "food_category": "Fresh Fruit / Tropical",
            "freshness_category": "Moderately Fresh",
            "actionable_guidance": "Consume within 24 hours",
            "confidence_score": 92,
            "visual_indicators": [
                {
                    "feature": "Surface Texture",
                    "observation": "Localized epidermal softening, skin retains structure with slight sponginess upon gentle pressure.",
                    "status": "Acceptable / Ripe"
                },
                {
                    "feature": "Discoloration & Pigmentation",
                    "observation": "Prominent senescent sugar spotting (melanin speckles) covering approximately 30-40% of yellow peel.",
                    "status": "Advanced Ripening"
                },
                {
                    "feature": "Wrinkling & Turgidity",
                    "observation": "Minor dehydration along the peduncle (stem); pulp integrity remains intact without collapse.",
                    "status": "Moderate Dehydration"
                },
                {
                    "feature": "Visible Mold / Microbial Mycelium",
                    "observation": "Zero fungal hyphae, white mycelial growth, or mucor contamination observed on peel or crown.",
                    "status": "Clear / Negative"
                }
            ],
            "storage_preservation_tips": [
                "Refrigerate immediately: Chilling will darken peel pigments but dramatically retards internal sugar fermentation.",
                "Peel, slice, and freeze in sealed airtight pouches for smoothies, protein oatmeal, or zero-waste banana bread.",
                "Keep isolated from ethylene-sensitive produce such as leafy greens, cucumbers, and carrots."
            ],
            "microbial_risk_level": "Low (Surface enzymatic browning; no pathogenic mold colonization)",
            "is_demo": True
        },
        "fresh_strawberries": {
            "food_item": "Garden Fresh Strawberries",
            "food_category": "Berries / Perishable Fruit",
            "freshness_category": "Fresh",
            "actionable_guidance": "Safe to consume",
            "confidence_score": 97,
            "visual_indicators": [
                {
                    "feature": "Surface Texture",
                    "observation": "Turgid, glossy drupelet achenes with firm, taut epidermis and zero fluid weeping.",
                    "status": "Peak Crispness"
                },
                {
                    "feature": "Discoloration",
                    "observation": "Uniform deep crimson anthocyanin pigmentation across 95%+ of exterior.",
                    "status": "Optimal Pigment"
                },
                {
                    "feature": "Wrinkling & Softening",
                    "observation": "No shriveling or epidermal collapse visible.",
                    "status": "Full Hydration"
                },
                {
                    "feature": "Visible Mold (Botrytis cinerea)",
                    "observation": "No fuzzy gray mold or fungal spores detectable under high-contrast inspection.",
                    "status": "Pristine"
                }
            ],
            "storage_preservation_tips": [
                "Store unwashed in a ventilated container lined with clean paper towels at 2°C - 4°C.",
                "Wash immediately prior to consumption; residual surface moisture accelerates mold germination.",
                "Consume within 3 to 5 days for optimal vitamin C and flavonoid preservation."
            ],
            "microbial_risk_level": "Negligible",
            "is_demo": True
        },
        "spoiled_poultry": {
            "food_item": "Raw Chicken Breast Fillet",
            "food_category": "Fresh Poultry / Animal Protein",
            "freshness_category": "Spoiled",
            "actionable_guidance": "Discard immediately",
            "confidence_score": 95,
            "visual_indicators": [
                {
                    "feature": "Surface Texture",
                    "observation": "Viscous pseudomonas biofilm sheen; slimy translucent surface exudate visibly pooled.",
                    "status": "Severe Slime Formation"
                },
                {
                    "feature": "Discoloration",
                    "observation": "Grayish-green tint and dull patchy discoloration replacing natural healthy translucent pink hue.",
                    "status": "Putrefactive Discoloration"
                },
                {
                    "feature": "Wrinkling / Structural Breakdown",
                    "observation": "Loss of cellular elasticity, myofibrillar degradation with ragged flaccid edges.",
                    "status": "Tissue Breakdown"
                },
                {
                    "feature": "Microbial Proliferation",
                    "observation": "Clear signs of aerobic bacterial spoilage (Pseudomonas / Brochothrix growth indicators).",
                    "status": "High Pathogen Threat"
                }
            ],
            "storage_preservation_tips": [
                "DO NOT CONSUME OR COOK. Cooking does not neutralize heat-stable bacterial enterotoxins.",
                "Double-bag securely and dispose of in an exterior waste receptacle immediately.",
                "Sanitize cutting surfaces, utensils, and hands using bleach/quat sanitizer (minimum 200 ppm)."
            ],
            "microbial_risk_level": "Extremely High (Dangerous risk of Salmonella, Campylobacter, and Staphylococcus aureus intoxication)",
            "is_demo": True
        }
    }

    if food_type and food_type in catalog:
        return catalog[food_type]
    return list(catalog.values())[0]


def get_demo_kitchen_hygiene() -> Dict[str, Any]:
    """Returns realistic commercial kitchen hygiene and safety audit findings."""
    return {
        "overall_compliance_score": 82,
        "compliance_rating": "Acceptable (Corrective Action Required)",
        "rating_color": "#F59E0B",
        "key_observations": (
            "Audited across 4 extracted representative frames. Kitchen operations show strong personal glove usage "
            "and clean stainless prep surfaces. However, critical segregation lapses between raw animal proteins "
            "and ready-to-eat salad produce were detected, along with incomplete hair restraint usage."
        ),
        "metrics": {
            "ppe_compliance": "85%",
            "surface_sanitization": "90%",
            "cross_contamination_control": "65%",
            "waste_management": "95%"
        },
        "violations": [
            {
                "id": "VIOL-01",
                "title": "Cross-Contamination: Raw Poultry Adjacent to Ready-to-Eat Produce",
                "description": "Raw chicken handling board positioned within 18cm of uncovered pre-chopped salad greens.",
                "visual_observation": "Frame #2: Yellow poultry board placed directly flush against green vegetable station without physical splash barrier or 1-meter clear zone.",
                "severity": "High",
                "severity_badge": "🔴 High Priority",
                "corrective_action": "Relocate raw meat processing to designated cold prep line. Mandate use of color-coded cutting boards (FDA Food Code §3-302.11)."
            },
            {
                "id": "VIOL-02",
                "title": "Incomplete Hair Restraint Compliance",
                "description": "Assistant cook observed without mandatory full hairnet / beard restraint.",
                "visual_observation": "Frame #1: Station 3 operator has hair extending past collar without containment snood or chef hat.",
                "severity": "Medium",
                "severity_badge": "🟡 Medium Priority",
                "corrective_action": "Require all personnel in active preparation zones to wear certified hairnets and beard restraints before line entry."
            },
            {
                "id": "VIOL-03",
                "title": "Stationary Sanitizer Bucket Unlabeled",
                "description": "Chemical wiping bucket lacks clear hazard labeling and test strip verification date.",
                "visual_observation": "Frame #3: Red sanitation bucket on lower shelf without chemical label or test strip log.",
                "severity": "Low",
                "severity_badge": "🔵 Low Priority",
                "corrective_action": "Apply GHS chemical label and verify active chlorine concentration (50-100 ppm) or quat (200 ppm) every 2 hours."
            }
        ],
        "good_practices_observed": [
            "Consistent use of clean blue nitrile gloves during final plating and cold assembly.",
            "Stainless steel table finishes are mirror-grade and free of organic crust or deep knife grooving.",
            "Footwear compliance: Closed-toe slip-resistant kitchen clogs observed on all team members.",
            "Covered foot-pedal waste receptacles positioned away from active food prep surfaces."
        ],
        "action_checklist": [
            "Establish physical barrier or dedicated table for raw poultry processing.",
            "Re-issue PPE kits and conduct morning pre-shift hairnet inspection.",
            "Update chemical sanitizer test log with 2-hour interval stamps."
        ],
        "is_demo": True
    }


def get_demo_recipes(user_ingredients: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Generates 3 creative, nutritious recipes using available kitchen ingredients."""
    user_ings_str = ", ".join(user_ingredients) if user_ingredients else "Rice, Potatoes, Tomatoes, Onions, Paneer, Spinach"

    return [
        {
            "recipe_name": "Golden Turmeric Paneer & Crisp Potato Skillet with Wilted Spinach",
            "description": "A fragrant, one-pan culinary triumph featuring seared protein-rich paneer cubes tossed with cumin-spiced potatoes and baby spinach in an aromatic tomato-onion reduction.",
            "cuisine": "Indian Fusion",
            "difficulty": "Easy",
            "prep_time_minutes": 10,
            "cook_time_minutes": 15,
            "total_time_minutes": 25,
            "servings": 2,
            "calories_per_serving": 385,
            "macros": {"protein_g": 22, "carbs_g": 32, "fats_g": 18, "fiber_g": 5.4},
            "ingredients_used": [
                "200g Fresh Paneer, cut into 2cm cubes",
                "1 medium Potato, boiled and diced",
                "2 cups Fresh Spinach, thoroughly rinsed",
                "1 large Onion, finely sliced",
                "2 ripe Tomatoes, pureed or finely diced"
            ],
            "pantry_staples_needed": [
                "1 tbsp Cold-pressed Mustard or Olive oil",
                "1 tsp Cumin seeds",
                "1/2 tsp Turmeric powder",
                "1/2 tsp Kashmiri chili powder",
                "1/2 tsp Sea salt",
                "Fresh lemon juice to finish"
            ],
            "step_by_step_instructions": [
                "Heat oil in a heavy-bottomed cast iron skillet over medium flame. Add cumin seeds and let them sizzle for 20 seconds until aromatic.",
                "Add sliced onions and sauté for 4-5 minutes until caramelized and golden brown.",
                "Stir in diced tomatoes, turmeric, chili powder, and sea salt. Cook down for 3 minutes until oil lightly separates from the masala base.",
                "Gently add the diced boiled potatoes and paneer cubes. Toss carefully to coat each morsel without crumbling the paneer.",
                "Fold in fresh spinach leaves in two batches. Cover with a lid for 90 seconds until leaves just wilt into a vibrant emerald green.",
                "Remove from heat, drizzle fresh lemon juice over the top, and serve warm."
            ],
            "ingredient_substitutions": [
                {"original": "Paneer", "substitute": "Extra-Firm Organic Tofu", "reason": "Transforms this recipe into a 100% plant-based / vegan meal with identical protein density."},
                {"original": "Potato", "substitute": "Steamed Cauliflower florets", "reason": "Cuts carbohydrates by 65% for a strict ketogenic or diabetic-friendly profile."}
            ],
            "healthy_cooking_tips": "Do not overcook the spinach leaves; quick flash-cooking preserves heat-sensitive folate and vitamin C.",
            "is_demo": True
        },
        {
            "recipe_name": "Rustic Tuscan-Style Tomato, Spinach & Brown Rice Risotto-Bowl",
            "description": "Creamy, wholesome brown rice simmered in a savory tomato-garlic broth, topped with sautéed iron-rich greens and golden paneer croutons.",
            "cuisine": "Mediterranean-Italian",
            "difficulty": "Intermediate",
            "prep_time_minutes": 12,
            "cook_time_minutes": 20,
            "total_time_minutes": 32,
            "servings": 3,
            "calories_per_serving": 410,
            "macros": {"protein_g": 19, "carbs_g": 52, "fats_g": 14, "fiber_g": 7.2},
            "ingredients_used": [
                "1.5 cups Cooked Brown Rice (or uncooked simmered)",
                "3 ripe Tomatoes, diced",
                "1 medium Onion, diced",
                "3 cups Fresh Spinach leaves",
                "150g Paneer, pan-seared lightly"
            ],
            "pantry_staples_needed": [
                "1 tbsp Extra virgin olive oil",
                "3 cloves Garlic, minced",
                "1 tsp Dried Italian herbs (oregano, basil)",
                "Black pepper and pink Himalayan salt"
            ],
            "step_by_step_instructions": [
                "Warm olive oil in a deep sauté pan over medium-low heat. Sauté minced garlic and onions until translucent (3 minutes).",
                "Add diced tomatoes, Italian herbs, and salt. Cook down for 6 minutes until rich and saucy.",
                "Add the cooked brown rice and 1/4 cup vegetable stock or warm water. Simmer gently while stirring until rice absorbs the tomato essence.",
                "Fold in spinach until tender and glossy.",
                "Top with lightly seared paneer cubes and cracked black pepper before serving."
            ],
            "ingredient_substitutions": [
                {"original": "Brown Rice", "substitute": "Quinoa or Riced Cauliflower", "reason": "Quinoa boosts complete plant protein; cauliflower creates an ultra-low-carb dish."}
            ],
            "healthy_cooking_tips": "Using pre-cooked chilled brown rice increases resistant starch, lowering glycemic spike and feeding beneficial gut flora.",
            "is_demo": True
        },
        {
            "recipe_name": "Crispy Spiced Potato & Vegetable Hash with Protein Topping",
            "description": "A quick, satisfying breakfast or brunch hash combining golden crisped potatoes, sweet caramelized onions, juicy charred tomatoes, and warm spices.",
            "cuisine": "Modern Brunch",
            "difficulty": "Easy",
            "prep_time_minutes": 8,
            "cook_time_minutes": 12,
            "total_time_minutes": 20,
            "servings": 2,
            "calories_per_serving": 330,
            "macros": {"protein_g": 15, "carbs_g": 38, "fats_g": 13, "fiber_g": 4.8},
            "ingredients_used": [
                "2 medium Potatoes, cut into small 1cm hash cubes",
                "1 medium Onion, diced",
                "1 Tomato, deseeded and diced",
                "1 cup Spinach, shredded",
                "100g Paneer or Tofu, grated or cubed"
            ],
            "pantry_staples_needed": [
                "1 tbsp Avocado or Olive oil",
                "1/2 tsp Smoked paprika",
                "1/2 tsp Garlic powder",
                "Salt & cracked black pepper"
            ],
            "step_by_step_instructions": [
                "Toss cubed potatoes with paprika, garlic powder, salt, and 1 tsp oil.",
                "In a wide skillet, sear potatoes in a single layer for 7 minutes, flipping occasionally until golden crisp on all sides.",
                "Push potatoes to the side; add remaining oil and sauté onions and tomatoes for 3 minutes.",
                "Mix everything together, stir in shredded spinach and paneer, and toss for 2 minutes until spinach is wilted and cheese is hot.",
                "Serve immediately with a pinch of fresh herbs."
            ],
            "ingredient_substitutions": [
                {"original": "Potatoes", "substitute": "Sweet Potatoes or Zucchini", "reason": "Sweet potato provides beta-carotene; zucchini creates a light summer hash."}
            ],
            "healthy_cooking_tips": "Parboiling or microwaving cubed potatoes for 2 minutes before searing reduces required oil and slashes cook time in half.",
            "is_demo": True
        }
    ]


def get_demo_meal_plan(target_calories: int, dietary_constraint: str, fitness_goal: str) -> Dict[str, Any]:
    """Generates an adaptive, realistic 7-day meal plan with exact grocery consolidation."""
    is_vegan = "vegan" in dietary_constraint.lower()
    is_keto = "keto" in dietary_constraint.lower()
    is_diabetic = "diabetic" in dietary_constraint.lower()

    # Pre-calculated 7-day adaptive schedules
    if is_keto:
        day_schedule = _generate_keto_schedule(target_calories)
    elif is_vegan:
        day_schedule = _generate_vegan_schedule(target_calories)
    elif is_diabetic:
        day_schedule = _generate_diabetic_schedule(target_calories)
    else:
        day_schedule = _generate_balanced_schedule(target_calories)

    grocery_list = _generate_grocery_list(day_schedule, dietary_constraint)

    return {
        "target_calories": target_calories,
        "dietary_constraint": dietary_constraint,
        "fitness_goal": fitness_goal,
        "days": day_schedule,
        "grocery_list": grocery_list,
        "is_demo": True
    }


def _generate_balanced_schedule(cal: int) -> List[Dict[str, Any]]:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    schedule = []
    
    # Scale meals proportionally
    b_cal = round(cal * 0.25)
    l_cal = round(cal * 0.35)
    d_cal = round(cal * 0.28)
    s_cal = round(cal * 0.12)

    meals_pool = [
        {
            "breakfast": ("Greek Yogurt Power Parfait with Berries & Walnuts", "Greek yogurt, wild blueberries, rolled oats, crushed walnuts, cinnamon", "320g", b_cal, 24, 38, 9),
            "lunch": ("Grilled Lemon Herb Chicken Bowl with Quinoa & Steamed Greens", "Free-range chicken breast, cooked quinoa, broccoli florets, olive oil dressing", "420g", l_cal, 44, 46, 14),
            "dinner": ("Atlantic Salmon Fillet with Roasted Asparagus & Sweet Potato Mash", "Wild salmon, baked sweet potato, asparagus spears, fresh herbs", "380g", d_cal, 36, 42, 16),
            "snack": ("Apple Wedges with Natural Almond Butter", "Crisp Gala apple, pure almond butter", "180g", s_cal, 6, 24, 11)
        },
        {
            "breakfast": ("Vegetable Omelet with Sprouted Grain Toast & Avocado", "Pasture-raised eggs, baby spinach, bell peppers, sprouted toast, avocado", "300g", b_cal, 26, 32, 15),
            "lunch": ("Mediterranean Turkey & Chickpea Harvest Salad", "Lean turkey slices, chickpeas, cucumber, cherry tomatoes, kalamata olives, feta", "440g", l_cal, 42, 48, 15),
            "dinner": ("Tofu & Edamame Brown Rice Stir-Fry with Sesame Ginger Dressing", "Firm organic tofu, shelled edamame, brown rice, bell peppers, snap peas", "400g", d_cal, 30, 52, 13),
            "snack": ("Mixed Raw Walnuts & Dark Chocolate Square (85%)", "Raw walnut halves, 85% dark chocolate", "45g", s_cal, 5, 12, 16)
        }
    ]

    for i, day_name in enumerate(days):
        pool_idx = i % len(meals_pool)
        item = meals_pool[pool_idx]
        b_name, b_ing, b_port, b_c, b_p, b_cb, b_f = item["breakfast"]
        l_name, l_ing, l_port, l_c, l_p, l_cb, l_f = item["lunch"]
        d_name, d_ing, d_port, d_c, d_p, d_cb, d_f = item["dinner"]
        s_name, s_ing, s_port, s_c, s_p, s_cb, s_f = item["snack"]

        schedule.append({
            "day": day_name,
            "day_number": i + 1,
            "total_calories": b_c + l_c + d_c + s_c,
            "total_protein_g": b_p + l_p + d_p + s_p,
            "total_carbs_g": b_cb + l_cb + d_cb + s_cb,
            "total_fats_g": b_f + l_f + d_f + s_f,
            "meals": {
                "Breakfast": {"name": b_name, "ingredients": b_ing, "portion": b_port, "calories": b_c, "protein": b_p, "carbs": b_cb, "fats": b_f},
                "Lunch": {"name": l_name, "ingredients": l_ing, "portion": l_port, "calories": l_c, "protein": l_p, "carbs": l_cb, "fats": l_f},
                "Dinner": {"name": d_name, "ingredients": d_ing, "portion": d_port, "calories": d_c, "protein": d_p, "carbs": d_cb, "fats": d_f},
                "Snacks": {"name": s_name, "ingredients": s_ing, "portion": s_port, "calories": s_c, "protein": s_p, "carbs": s_cb, "fats": s_f}
            }
        })
    return schedule


def _generate_vegan_schedule(cal: int) -> List[Dict[str, Any]]:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    schedule = []
    b_cal = round(cal * 0.25)
    l_cal = round(cal * 0.35)
    d_cal = round(cal * 0.28)
    s_cal = round(cal * 0.12)

    for i, day_name in enumerate(days):
        schedule.append({
            "day": day_name,
            "day_number": i + 1,
            "total_calories": cal,
            "total_protein_g": round(cal * 0.25 / 4),
            "total_carbs_g": round(cal * 0.50 / 4),
            "total_fats_g": round(cal * 0.25 / 9),
            "meals": {
                "Breakfast": {
                    "name": "Superfood Chia & Hemp Seed Protein Porridge with Blueberries",
                    "ingredients": "Rolled oats, chia seeds, hemp protein, almond milk, fresh blueberries",
                    "portion": "350g", "calories": b_cal, "protein": 22, "carbs": 48, "fats": 12
                },
                "Lunch": {
                    "name": "Warm Spiced Chickpea & Roasted Sweet Potato Buddha Bowl",
                    "ingredients": "Braised chickpeas, baked sweet potato cubes, massaged kale, tahini lemon dressing",
                    "portion": "440g", "calories": l_cal, "protein": 26, "carbs": 68, "fats": 16
                },
                "Dinner": {
                    "name": "Pan-Seared Organic Tempeh with Steamed Broccolini & Quinoa",
                    "ingredients": "Marinated tempeh, quinoa pilaf, steamed broccolini, toasted sesame seeds",
                    "portion": "400g", "calories": d_cal, "protein": 32, "carbs": 50, "fats": 18
                },
                "Snacks": {
                    "name": "Spiced Roasted Edamame & Fresh Orange Slices",
                    "ingredients": "Dry-roasted edamame beans, Valencia orange",
                    "portion": "160g", "calories": s_cal, "protein": 14, "carbs": 20, "fats": 4
                }
            }
        })
    return schedule


def _generate_keto_schedule(cal: int) -> List[Dict[str, Any]]:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    schedule = []
    b_cal = round(cal * 0.25)
    l_cal = round(cal * 0.35)
    d_cal = round(cal * 0.28)
    s_cal = round(cal * 0.12)

    for i, day_name in enumerate(days):
        schedule.append({
            "day": day_name,
            "day_number": i + 1,
            "total_calories": cal,
            "total_protein_g": round(cal * 0.25 / 4),
            "total_carbs_g": 25, # Strict net carbs
            "total_fats_g": round(cal * 0.70 / 9),
            "meals": {
                "Breakfast": {
                    "name": "Keto Avocado & Pasture Egg Scramble with Spinach & Goat Cheese",
                    "ingredients": "3 whole eggs, half avocado, baby spinach, grass-fed butter, goat cheese",
                    "portion": "300g", "calories": b_cal, "protein": 24, "carbs": 4, "fats": 38
                },
                "Lunch": {
                    "name": "Pan-Seared Wild Salmon Salad with Extra Virgin Olive Oil & Walnuts",
                    "ingredients": "Salmon fillet, mixed butterhead greens, cucumber, walnuts, olive oil vinaigrette",
                    "portion": "380g", "calories": l_cal, "protein": 38, "carbs": 6, "fats": 46
                },
                "Dinner": {
                    "name": "Herb Butter Grilled Ribeye Steak with Garlic Butter Cauliflower Mash",
                    "ingredients": "Grass-fed beef steak, riced cauliflower, heavy cream, garlic herb butter",
                    "portion": "360g", "calories": d_cal, "protein": 42, "carbs": 7, "fats": 44
                },
                "Snacks": {
                    "name": "Macadamia Nut Handful & Celery Sticks with Cream Cheese",
                    "ingredients": "Raw macadamia nuts, celery stalks, organic cream cheese",
                    "portion": "80g", "calories": s_cal, "protein": 5, "carbs": 3, "fats": 22
                }
            }
        })
    return schedule


def _generate_diabetic_schedule(cal: int) -> List[Dict[str, Any]]:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    schedule = []
    b_cal = round(cal * 0.25)
    l_cal = round(cal * 0.35)
    d_cal = round(cal * 0.28)
    s_cal = round(cal * 0.12)

    for i, day_name in enumerate(days):
        schedule.append({
            "day": day_name,
            "day_number": i + 1,
            "total_calories": cal,
            "total_protein_g": round(cal * 0.35 / 4),
            "total_carbs_g": round(cal * 0.35 / 4),
            "total_fats_g": round(cal * 0.30 / 9),
            "meals": {
                "Breakfast": {
                    "name": "Steel-Cut Cinnamon Oats with Chia Seeds & Crushed Pecans",
                    "ingredients": "Steel-cut oats (high beta-glucan), cinnamon, chia seeds, pecans, unsweetened almond milk",
                    "portion": "320g", "calories": b_cal, "protein": 18, "carbs": 35, "fats": 14
                },
                "Lunch": {
                    "name": "Grilled Lemon-Oregano Chicken with Lentil Tabbouleh",
                    "ingredients": "Chicken breast, brown lentils, flat-leaf parsley, cucumber, tomato, olive oil",
                    "portion": "420g", "calories": l_cal, "protein": 44, "carbs": 38, "fats": 12
                },
                "Dinner": {
                    "name": "Baked Cod Fillet with Roasted Zucchini Ribbons & Steamed Quinoa",
                    "ingredients": "Atlantic cod, yellow zucchini, quinoa, garlic, extra virgin olive oil",
                    "portion": "380g", "calories": d_cal, "protein": 38, "carbs": 34, "fats": 11
                },
                "Snacks": {
                    "name": "Crisp Celery Sticks & Carrot Matchsticks with Roasted Red Pepper Hummus",
                    "ingredients": "Celery, carrots, chickpea hummus",
                    "portion": "150g", "calories": s_cal, "protein": 6, "carbs": 18, "fats": 6
                }
            }
        })
    return schedule


def _generate_grocery_list(schedule: List[Dict[str, Any]], dietary_constraint: str) -> Dict[str, List[Dict[str, str]]]:
    """Consolidates required 7-day ingredients into structured, non-duplicate shopping aisles."""
    is_vegan = "vegan" in dietary_constraint.lower()
    is_keto = "keto" in dietary_constraint.lower()

    if is_keto:
        return {
            "🥦 Fresh Produce": [
                {"item": "Avocados (Hass)", "quantity": "4 large fruits"},
                {"item": "Baby Spinach & Mixed Butterhead Greens", "quantity": "500g (2 large tubs)"},
                {"item": "Cauliflower (for ricing)", "quantity": "2 large heads (~1.5kg)"},
                {"item": "English Cucumbers & Celery Stalks", "quantity": "3 cucumbers, 1 bunch celery"},
                {"item": "Garlic Bulbs & Fresh Herbs", "quantity": "2 bulbs garlic, rosemary, thyme"}
            ],
            "🥩 Proteins & Animal Products": [
                {"item": "Pasture-Raised Whole Eggs", "quantity": "2 dozen (24 eggs)"},
                {"item": "Wild Atlantic Salmon Fillets", "quantity": "800g (4 portions)"},
                {"item": "Grass-Fed Beef Ribeye / Sirloin", "quantity": "700g (3 steaks)"},
                {"item": "Free-Range Chicken Thighs (Skin-on)", "quantity": "600g (3 portions)"}
            ],
            "🧀 Dairy & Healthy Fats": [
                {"item": "Grass-Fed Butter / Ghee", "quantity": "250g block"},
                {"item": "Extra Virgin Olive Oil (Cold-Pressed)", "quantity": "500ml bottle"},
                {"item": "Goat Cheese & Organic Cream Cheese", "quantity": "200g each"},
                {"item": "Heavy Whipping Cream", "quantity": "250ml carton"}
            ],
            "🌰 Nuts, Seeds & Pantry": [
                {"item": "Raw Macadamia Nuts & Walnuts", "quantity": "300g resealable bag"},
                {"item": "Pink Himalayan Salt & Black Peppercorns", "quantity": "1 grinder each"}
            ]
        }
    elif is_vegan:
        return {
            "🥦 Fresh Produce": [
                {"item": "Baby Spinach & Lacinato Kale", "quantity": "600g (3 tubs)"},
                {"item": "Sweet Potatoes (Jewel or Beauregard)", "quantity": "1.8kg (4-5 medium)"},
                {"item": "Broccolini & Snap Peas", "quantity": "500g"},
                {"item": "Fresh Wild Blueberries & Valencia Oranges", "quantity": "3 pints berries, 6 oranges"},
                {"item": "Lemons & Fresh Ginger Root", "quantity": "6 lemons, 100g ginger"}
            ],
            "🌱 Plant Proteins & Legumes": [
                {"item": "Organic Firm Tofu & Tempeh", "quantity": "4 blocks (800g total)"},
                {"item": "Dry or Canned Chickpeas (Organic)", "quantity": "4 cans (400g each)"},
                {"item": "Frozen Edamame Beans (Shelled)", "quantity": "500g bag"},
                {"item": "Organic Hemp Seed Protein Powder", "quantity": "250g pouch"}
            ],
            "🌾 Whole Grains & Pantry": [
                {"item": "Rolled Old-Fashioned Oats", "quantity": "600g bag"},
                {"item": "Tri-Color Quinoa & Brown Basmati Rice", "quantity": "500g each"},
                {"item": "Whole Chia Seeds & Hemp Hearts", "quantity": "250g bag each"},
                {"item": "Pure Sesame Tahini Paste", "quantity": "350g jar"},
                {"item": "Unsweetened Almond or Oat Milk", "quantity": "2 cartons (1L each)"}
            ]
        }
    else:
        return {
            "🥦 Fresh Produce": [
                {"item": "Baby Spinach & Broccoli Florets", "quantity": "500g spinach, 2 heads broccoli"},
                {"item": "Asparagus Spears & Sweet Potatoes", "quantity": "1 bunch asparagus, 1.2kg sweet potatoes"},
                {"item": "Gala Apples & Fresh Blueberries", "quantity": "6 apples, 2 pints berries"},
                {"item": "Cherry Tomatoes & Persian Cucumbers", "quantity": "2 pints tomatoes, 4 cucumbers"},
                {"item": "Avocados (Hass)", "quantity": "3 medium fruits"}
            ],
            "🍗 Proteins & Seafood": [
                {"item": "Free-Range Chicken Breast Fillets", "quantity": "1.2kg (skinless, boneless)"},
                {"item": "Wild-Caught Salmon Fillets", "quantity": "700g (3-4 fillets)"},
                {"item": "Pasture-Raised Eggs", "quantity": "1 dozen (12 eggs)"},
                {"item": "Extra-Firm Organic Tofu", "quantity": "1 block (350g)"}
            ],
            "🥛 Dairy & Healthy Fats": [
                {"item": "Plain Greek Yogurt (0-2% fat)", "quantity": "1kg tub"},
                {"item": "Sheep's Milk Feta Cheese", "quantity": "200g pack"},
                {"item": "Cold-Pressed Extra Virgin Olive Oil", "quantity": "500ml bottle"},
                {"item": "Pure Roasted Almond Butter", "quantity": "350g jar"}
            ],
            "🌾 Whole Grains & Pantry": [
                {"item": "Tri-Color Quinoa & Sprouted Grain Bread", "quantity": "500g quinoa, 1 loaf bread"},
                {"item": "Old Fashioned Rolled Oats", "quantity": "500g bag"},
                {"item": "Cooked Chickpeas (Canned, Low Sodium)", "quantity": "2 cans (400g each)"},
                {"item": "Raw Walnuts & 85% Dark Chocolate", "quantity": "200g walnuts, 1 bar dark chocolate"}
            ]
        }
