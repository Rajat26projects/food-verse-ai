# Food Verse AI – Multimodal Food Intelligence Agent

**Category:** Generative AI | Nutrition, Freshness & Kitchen Safety  
**Platform ID:** `6ac4ca021dcde6d7857c169a`  
**Capstone Project:** Skill Wallet Capstone Project 3  
**Application Framework:** Streamlit (Python 3.9+)  

---

## 📖 Executive Summary & Architecture

**Food Verse AI** is a production-grade, multimodal food intelligence ecosystem capable of analyzing dish photographs, perishable food conditions, commercial kitchen videos, and individualized metabolic profiles.

The application combines **Computer Vision (OpenCV, Pillow)** with **Multimodal Large Language & Vision Models (Google Gemini 1.5/2.0 and Groq LLaMA 3.2 Vision)** to deliver real-time food diagnostics, HACCP kitchen safety auditing, and adaptive metabolic meal planning without requiring any external database.

```
                              ┌────────────────────────────────────────┐
                              │               User Input               │
                              │ (Dish / Perishable / Video / Profile)  │
                              └──────────────────┬─────────────────────┘
                                                 │
                                                 ▼
                              ┌────────────────────────────────────────┐
                              │        Streamlit Frontend (app.py)     │
                              │   Modern Glassmorphic UI & Navigation  │
                              └──────────────────┬─────────────────────┘
                                                 │
                   ┌─────────────────────────────┼─────────────────────────────┐
                   │                             │                             │
                   ▼                             ▼                             ▼
    ┌──────────────────────────────┐ ┌──────────────────────────┐ ┌──────────────────────────┐
    │     Computer Vision (CV)     │ │   Multimodal AI Engine   │ │  Metabolic Calculations  │
    │   - OpenCV Frame Extractor   │ │   - Google Gemini 1.5    │ │  - Mifflin-St Jeor BMR   │
    │   - Image Quality Diagnostics│ │   - Groq LLaMA 3.2 Vision│ │  - Activity-Based TDEE   │
    │   - PIL Image Preprocessing  │ │   - Structured JSON API  │ │  - Macro Split Partition │
    └──────────────┬───────────────┘ └───────────┬──────────────┘ └────────────┬─────────────┘
                   │                             │                             │
                   └─────────────────────────────┼─────────────────────────────┘
                                                 │
                                                 ▼
                              ┌────────────────────────────────────────┐
                              │          Demonstration Engine          │
                              │ (Graceful Offline & Sample Fallback)   │
                              └──────────────────┬─────────────────────┘
                                                 │
                                                 ▼
                              ┌────────────────────────────────────────┐
                              │            Output Modules              │
                              │ 1. Food Recognition & Nutrition Audit  │
                              │ 2. Freshness & Spoilage Diagnostic    │
                              │ 3. Kitchen Hygiene & HACCP Compliance  │
                              │ 4. Smart Recipe Assistant (Pantry)     │
                              │ 5. Personalized 7-Day Meal Planner     │
                              └────────────────────────────────────────┘
```

---

## 🌟 Core Modules

### 1. 🥗 Food Recognition & Nutrition Audit (Epic 2)
- **Dish & Cuisine Identification:** Detects dish name, regional cuisine type, and visible ingredients.
- **Portion & Macronutrient Breakdown:** Visual estimation of portion weight (grams), calories (kcal), protein (g), carbohydrates (g), total fats (g), and dietary fiber (g).
- **Interactive Visualizations:** Plotly caloric distribution donut charts with interactive tooltips.
- **Health Score & Allergen Alerts:** Composite 1–100 health badge with alerts for major allergens (dairy, nuts, gluten, soy).
- **Scientific Labeling:** Explicitly informs users that portion weights and nutritional values are approximations; hidden ingredients (added sodium, refined oils) cannot be verified from an image alone.

### 2. 🍎 Food Freshness & Spoilage Diagnostic (Epic 3)
- **Multi-Category Support:** Evaluates perishable fruits, vegetables, dairy, poultry, and meat.
- **Superficial Feature Analysis:** Inspects surface texture, senescent browning, dehydration wrinkling, and mycelial mold formation.
- **Freshness Classification:** Tri-state categorization: `Fresh`, `Moderately Fresh`, or `Spoiled`.
- **Actionable Guidance:** Directly assigns actionable safety instructions: `Safe to consume`, `Consume within 24 hours`, or `Discard immediately`.
- **Microbiological Notice:** Explains uncertainty and clarifies that visual inspection cannot detect odorless foodborne pathogens (e.g. *Salmonella*, *Listeria*, *E. coli*).

### 3. 🧑‍🍳 Kitchen Hygiene & Food Safety Compliance (Epic 4)
- **Multi-Format Ingestion:** Supports high-resolution kitchen photographs and commercial kitchen video clips (`.mp4`, `.mov`, `.avi`).
- **OpenCV Keyframe Extraction:** Video uploads are processed by sampling evenly spaced representative operational frames, preventing API payload bloat and latency.
- **HACCP & OSHA Visual Audit:**
  - Chef hat & hairnet compliance
  - Personal protective equipment (nitrile glove usage)
  - Surface sanitization and station cleanliness
  - Cross-contamination hazards (e.g., raw poultry placed adjacent to ready-to-eat produce)
- **Itemized Violations Table:** Structured records including violation title, visual observation evidence, severity (`High`, `Medium`, `Low`), and required corrective action.

### 4. 🍳 Smart Kitchen Recipe Assistant (Epic 4)
- **Zero-Waste Pantry Input:** Flexible input allowing users to enter whatever ingredients they have in their kitchen.
- **One-Click Presets:** Quick-fill presets for Desi Veg, Mediterranean High-Protein, Plant-Based Superfood, and Low-Carb Keto.
- **Chef-Crafted Output:** Formulates 2–3 creative recipes complete with preparation time, cooking time, difficulty level, caloric breakdown, step-by-step numbered instructions, ingredient substitutions, and healthy cooking tips.

### 5. 📅 Personalized Meal Planner (Epic 5)
- **Metabolic Profile:** Captures age, gender, weight (kg), height (cm), activity level (1.2 to 1.9 multiplier), dietary constraints (`Vegan`, `Keto`, `Diabetic-friendly`, `Standard`), and fitness goals (`Fat loss`, `Muscle gain`, `Maintenance`).
- **Clinical Formulations:**
  - **Mifflin-St Jeor Equation** for Basal Metabolic Rate (BMR).
  - Activity-factored Total Daily Energy Expenditure (TDEE).
  - Caloric target calculation with physiological safety minimums.
- **Adaptive 7-Day Meal Schedule:** Complete Monday through Sunday schedules divided into Breakfast, Lunch, Dinner, and Snacks with macro partitioning.
- **Consolidated Grocery List:** Synthesizes ingredients across all 28 planned meals into aisle categories (`Produce`, `Proteins`, `Dairy/Alternatives`, `Whole Grains`, `Healthy Fats`), combining duplicates with estimated quantities and downloadable `.txt` export.

---

## ⚡ Demonstration Mode

Food Verse AI provides a **100% functional Demonstration Mode** when no API key is provided:
- All five modules are immediately interactive.
- Pre-built high-contrast curated sample dishes, perishable food items, and commercial kitchen scenes are available with a single click.
- Output banners clearly distinguish **Demonstration / Simulated Data** from **Live AI Generation**.
- No application crashes or blocking modal screens occur if API keys are absent.

---

## 🛠️ Technology Stack

| Component | Technology | Rationale |
|---|---|---|
| **Programming Language** | Python 3.9+ | Standard cross-platform AI development language |
| **Frontend Framework** | Streamlit | Modern, dynamic, self-contained UI without external backend complexity |
| **Vision & Image Processing** | OpenCV (`opencv-python-headless`), Pillow | Fast video frame extraction and image quality metrics |
| **Multimodal AI Providers** | Google Gemini (1.5 Flash / Pro) & Groq (LLaMA 3.2 Vision) | Cutting-edge multimodal understanding and speed |
| **Data Contracts** | Pydantic & Structured JSON | Validates AI outputs before UI rendering |
| **Data Visualization** | Plotly & Pandas | High-interactivity caloric charts and clean tables |
| **Styling** | Vanilla CSS (`assets/style.css`) | Glassmorphic cards, responsive grids, and vibrant status badges |

---

## 🚀 Installation & Local Execution

### 1. Prerequisites
- Python 3.9 or higher
- Git

### 2. Clone Repository & Create Environment
```bash
git clone <repository-url>
cd smart_bridge

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS / Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## 🔑 Secure API Configuration

You can configure API credentials using either of the following secure methods:

### Method A: Streamlit In-App UI (Session State)
1. Launch the application.
2. In the left sidebar under **⚙️ AI Engine Configuration**, select your provider (**Google Gemini** or **Groq**).
3. Enter your API key in the password-masked field.
4. *Security Guarantee:* The key is saved strictly in `st.session_state` for the lifetime of your session. It is never logged, printed, or saved to disk.

### Method B: Environment Variables
Create a `.env` file or export the variable in your terminal:
```bash
export GEMINI_API_KEY="your-google-gemini-api-key"
# or
export GROQ_API_KEY="your-groq-api-key"
```

---

## ☁️ Streamlit Community Cloud Deployment

This repository is optimized for seamless deployment to **Streamlit Community Cloud**:
1. Push the repository to your GitHub account.
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **"New app"** and select your repository, branch (`main`), and set the main file path to:
   ```
   app.py
   ```
4. (Optional) In the **Advanced settings -> Secrets** tab, enter your API key:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
5. Click **"Deploy"**. The app will automatically build and launch.

---

## 📂 Project Structure

```
smart_bridge/
├── app.py                      # Main Streamlit application and module router
├── config.py                   # Global constants, models, formulas, and disclaimers
├── requirements.txt            # Python package dependencies
├── README.md                   # Comprehensive documentation and deployment guide
├── assets/
│   ├── style.css               # Modern CSS design system (glassmorphism, badges)
│   └── sample_images.py        # Visual test sample generators for dishes and kitchen scenes
├── modules/
│   ├── __init__.py
│   ├── food_recognition.py     # Module 1: Food Recognition & Nutrition Breakdown
│   ├── food_freshness.py       # Module 2: Freshness & Spoilage Diagnostic
│   ├── kitchen_hygiene.py      # Module 3: Kitchen Hygiene & Video Frame Audit
│   ├── recipe_assistant.py     # Module 4: Smart Kitchen Recipe Assistant
│   └── meal_planner.py         # Module 5: BMR/TDEE & 7-Day Meal Planner
├── services/
│   ├── __init__.py
│   ├── ai_service.py           # Unified multimodal client (Gemini & Groq) with JSON contracts
│   ├── cv_service.py           # OpenCV video frame extraction and image quality metrics
│   ├── demo_data.py            # High-fidelity domain simulation datasets
│   └── nutrition_calc.py       # Mifflin-St Jeor equations and macro partitioning
└── tests/
    └── test_core.py            # Unit test suite verifying formulas and contracts
```

---

## ⚖️ Safety & Regulatory Disclaimers

- **Nutritional Estimates:** Nutrient quantities and portion weights are approximations derived from visible features and standard dietary databases. Hidden ingredients (added oils, sugars, sodium) cannot be determined reliably from an image alone.
- **Microbiological Risk:** Visual freshness diagnostics evaluate external physical morphology only. Visual analysis cannot detect odorless foodborne bacteria (e.g. *Salmonella*, *Listeria*, *Campylobacter*) or heat-stable microbial enterotoxins. When in doubt, discard perishable food items.
- **Kitchen Hygiene:** Computer vision compliance auditing verifies observable protective equipment and physical segregation. It does not replace ATP bioluminescence swab testing or certified health inspections.
- **Medical Advisory:** Caloric targets and meal plans are provided for nutritional planning purposes and do not constitute individualized clinical medical advice. Individuals with diabetes or metabolic conditions must consult a licensed physician or registered dietitian.
