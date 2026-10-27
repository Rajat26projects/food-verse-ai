"""
Configuration and Global State Management for Food Verse AI
Platform ID: 6ac4ca021dcde6d7857c169a
Skill Wallet Capstone Project 3
"""

import os
from typing import Optional

# Application Metadata
APP_TITLE = "Food Verse AI – Multimodal Food Intelligence Agent"
APP_SUBTITLE = "Multimodal Food Intelligence Ecosystem • Generative AI & Computer Vision"
APP_VERSION = "1.0.0"
APP_ICON = "🥗"
AUTHOR = "Skill Wallet Capstone Project 3"

# Supported AI Providers
PROVIDER_GEMINI = "Google Gemini"
PROVIDER_GROQ = "Groq"
DEMO_MODE_LABEL = "⚡ Demonstration Mode (Simulated AI)"

# Supported Models (Multimodal Vision Capable)
GEMINI_MODELS = [
    "gemini-2.0-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash-002",
    "gemini-1.5-flash",
    "gemini-1.5-pro-latest",
    "gemini-1.5-pro",
    "gemini-2.5-flash"
]

GROQ_MODELS = [
    "llama-3.2-11b-vision-preview",
    "llama-3.2-90b-vision-preview",
    "llama-3.3-70b-versatile"
]

# Dietary Constraints
DIETARY_CONSTRAINTS = [
    "Standard / Balanced",
    "Vegan",
    "Keto",
    "Diabetic-friendly"
]

# Fitness Goals
FITNESS_GOALS = [
    "Fat loss",
    "Muscle gain",
    "Maintenance"
]

# Activity Levels & Multipliers
ACTIVITY_LEVELS = {
    "Sedentary (Little or no exercise, desk job)": 1.2,
    "Lightly Active (Light exercise/sports 1-3 days/week)": 1.375,
    "Moderately Active (Moderate exercise 3-5 days/week)": 1.55,
    "Very Active (Hard exercise/sports 6-7 days/week)": 1.725,
    "Extra Active (Very hard exercise & physical job or 2x training)": 1.9,
}

# Freshness Categories and Badges
FRESHNESS_CATEGORIES = {
    "Fresh": {"badge": "🟢 Fresh", "color": "#10B981"},
    "Moderately Fresh": {"badge": "🟡 Moderately Fresh", "color": "#F59E0B"},
    "Spoiled": {"badge": "🔴 Spoiled", "color": "#EF4444"},
}

FOOD_SAFETY_ACTIONS = {
    "Safe to consume": {"color": "#10B981", "icon": "✅"},
    "Consume within 24 hours": {"color": "#F59E0B", "icon": "⚠️"},
    "Discard immediately": {"color": "#EF4444", "icon": "🚫"},
}

# Disclaimers
NUTRITION_DISCLAIMER = (
    "⚠️ **Disclaimer:** All nutritional values, macronutrients, and portion estimates are calculated "
    "using visual features and AI statistical estimation. Hidden preparation elements (such as added oils, sodium, "
    "and hidden sugars) cannot be determined reliably from an image alone. Portion weights are estimated approximations."
)

FRESHNESS_DISCLAIMER = (
    "⚠️ **Food Safety Notice:** Visual inspection evaluates superficial condition, texture, and discoloration. "
    "It cannot detect odorless foodborne pathogens (e.g., Salmonella, Listeria, E. coli) or internal bacterial toxin accumulation. "
    "Always rely on standard hygiene protocols, temperature checks, and smell tests. When in doubt, discard the food."
)

KITCHEN_SAFETY_DISCLAIMER = (
    "⚠️ **Compliance Notice:** Computer vision auditing identifies observable physical hazards and protective equipment compliance. "
    "It is not a substitute for microbiological swab testing, ATP surface verification, or certified regulatory public health inspections."
)

MEDICAL_DISCLAIMER = (
    "⚠️ **Health Advisory:** Caloric targets, macronutrient distributions, and meal plans are generated for nutritional education and planning. "
    "They do not constitute individualized clinical or medical dietary advice. Individuals diagnosed with diabetes, renal conditions, "
    "or metabolic disorders should consult a registered dietitian or licensed physician."
)
