"""
Nutritional and Metabolic Calculations Service
Implements clinical Mifflin-St Jeor equations, TDEE calculations,
adaptive caloric goals, and macronutrient distribution models.
"""

from typing import Dict, Any, Tuple


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Calculates Basal Metabolic Rate (BMR) using the clinically validated
    Mifflin-St Jeor equation.

    Formula:
      - Men:   BMR = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
      - Women: BMR = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    """
    base = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age)
    if gender.strip().lower() in ["male", "man", "m"]:
        bmr = base + 5.0
    else:
        bmr = base - 161.0
    return round(bmr, 1)


def calculate_tdee(bmr: float, activity_multiplier: float) -> float:
    """
    Calculates Total Daily Energy Expenditure (TDEE).
    Formula: TDEE = BMR * Activity Factor
    """
    return round(bmr * activity_multiplier, 1)


def calculate_target_calories(tdee: float, bmr: float, goal: str, gender: str) -> Tuple[int, str]:
    """
    Calculates the suggested target calories based on fitness goals with safe physiological boundaries.
    
    - Fat loss: Deficit of ~500 kcal/day (safe 0.5kg/week fat loss), capped above safe floor.
    - Muscle gain: Moderate surplus of +350 kcal/day to support protein synthesis without excessive adiposity.
    - Maintenance: TDEE.
    """
    goal_norm = goal.strip().lower()
    min_floor = 1500 if gender.lower().startswith("m") else 1200

    if "fat loss" in goal_norm or "weight loss" in goal_norm:
        target = round(tdee - 500)
        if target < min_floor:
            target = min_floor
            note = f"Calorie deficit applied (-500 kcal), protected by safe physiological minimum ({min_floor} kcal)."
        else:
            note = "Caloric deficit of 500 kcal/day applied for sustainable fat reduction."
    elif "muscle" in goal_norm or "gain" in goal_norm:
        target = round(tdee + 350)
        note = "Lean surplus of +350 kcal/day applied to facilitate muscular hypertrophy."
    else:
        target = round(tdee)
        note = "Maintenance intake calculated to balance energy expenditure."

    return int(target), note


def calculate_macro_split(target_calories: int, dietary_constraint: str, fitness_goal: str, weight_kg: float) -> Dict[str, Any]:
    """
    Computes macronutrient gram and percentage targets tailored to dietary constraints and fitness goals.
    
    1g Protein = 4 kcal
    1g Carbohydrate = 4 kcal
    1g Fat = 9 kcal
    """
    constraint_norm = dietary_constraint.lower()
    goal_norm = fitness_goal.lower()

    if "keto" in constraint_norm:
        # Keto: 70% Fat, 25% Protein, 5% Net Carbs
        fat_pct, protein_pct, carb_pct = 0.70, 0.25, 0.05
    elif "diabetic" in constraint_norm:
        # Diabetic-friendly: Controlled Low-GI carbs (35%), 35% Protein, 30% Healthy Fats
        fat_pct, protein_pct, carb_pct = 0.30, 0.35, 0.35
    elif "vegan" in constraint_norm:
        # Vegan: Plant-rich complex carbs 45%, 30% Protein, 25% Fat
        fat_pct, protein_pct, carb_pct = 0.25, 0.30, 0.45
    else:
        # Standard / Balanced:
        if "muscle" in goal_norm:
            # Higher protein: 35% Protein, 45% Carb, 20% Fat
            fat_pct, protein_pct, carb_pct = 0.20, 0.35, 0.45
        elif "fat loss" in goal_norm:
            # Satiating protein: 35% Protein, 35% Carb, 30% Fat
            fat_pct, protein_pct, carb_pct = 0.30, 0.35, 0.35
        else:
            # Balanced: 30% Protein, 45% Carb, 25% Fat
            fat_pct, protein_pct, carb_pct = 0.25, 0.30, 0.45

    protein_cals = target_calories * protein_pct
    carb_cals = target_calories * carb_pct
    fat_cals = target_calories * fat_pct

    protein_g = round(protein_cals / 4.0)
    carb_g = round(carb_cals / 4.0)
    fat_g = round(fat_cals / 9.0)

    protein_per_kg = round(protein_g / max(weight_kg, 1.0), 2)

    return {
        "calories": target_calories,
        "protein_g": protein_g,
        "carbs_g": carb_g,
        "fats_g": fat_g,
        "percentages": {
            "protein": int(protein_pct * 100),
            "carbs": int(carb_pct * 100),
            "fats": int(fat_pct * 100)
        },
        "protein_per_kg": protein_per_kg
    }
