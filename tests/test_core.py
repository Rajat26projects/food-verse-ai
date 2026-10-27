"""
Automated Test Suite for Food Verse AI
Validates mathematical models, clinical formulas, data contracts,
computer vision helpers, and demonstration mode fallbacks.
"""

import unittest
from PIL import Image

from services.nutrition_calc import (
    calculate_bmr,
    calculate_tdee,
    calculate_target_calories,
    calculate_macro_split
)
from services.cv_service import assess_image_quality, create_sample_kitchen_frame
from services.demo_data import (
    get_demo_food_recognition,
    get_demo_food_freshness,
    get_demo_kitchen_hygiene,
    get_demo_recipes,
    get_demo_meal_plan
)
from services.ai_service import _clean_json_response, analyze_food_image


class TestNutritionCalculations(unittest.TestCase):
    """Verifies Mifflin-St Jeor and TDEE formulas against clinical benchmarks."""

    def test_bmr_male(self):
        # 70kg, 175cm, 25 years old Male
        # BMR = (10 * 70) + (6.25 * 175) - (5 * 25) + 5
        #     = 700 + 1093.75 - 125 + 5 = 1673.75 -> 1673.8
        bmr = calculate_bmr(weight_kg=70.0, height_cm=175.0, age=25, gender="Male")
        self.assertAlmostEqual(bmr, 1673.8, places=1)

    def test_bmr_female(self):
        # 60kg, 165cm, 30 years old Female
        # BMR = (10 * 60) + (6.25 * 165) - (5 * 30) - 161
        #     = 600 + 1031.25 - 150 - 161 = 1320.25 -> 1320.2
        bmr = calculate_bmr(weight_kg=60.0, height_cm=165.0, age=30, gender="Female")
        self.assertAlmostEqual(bmr, 1320.2, places=1)

    def test_tdee_calculation(self):
        bmr = 1600.0
        # Moderately active (1.55) -> 2480.0
        tdee = calculate_tdee(bmr, 1.55)
        self.assertEqual(tdee, 2480.0)

    def test_target_calories_fat_loss_and_floors(self):
        tdee = 2200.0
        bmr = 1500.0
        target, note = calculate_target_calories(tdee, bmr, goal="Fat loss", gender="Male")
        self.assertEqual(target, 1700)
        self.assertIn("deficit", note.lower())

        # Check safety floor for female (minimum 1200 kcal)
        low_tdee = 1300.0
        target_f, _ = calculate_target_calories(low_tdee, 1000.0, goal="Fat loss", gender="Female")
        self.assertGreaterEqual(target_f, 1200)

    def test_macro_split_keto(self):
        split = calculate_macro_split(
            target_calories=2000,
            dietary_constraint="Keto",
            fitness_goal="Fat loss",
            weight_kg=70.0
        )
        self.assertEqual(split["percentages"]["fats"], 70)
        self.assertEqual(split["percentages"]["protein"], 25)
        self.assertEqual(split["percentages"]["carbs"], 5)
        # 70% of 2000 = 1400 kcal / 9 = ~156g fat
        self.assertAlmostEqual(split["fats_g"], 156, delta=2)


class TestDemoDataContracts(unittest.TestCase):
    """Verifies that all demonstration data conform strictly to structured contracts."""

    def test_food_recognition_contract(self):
        data = get_demo_food_recognition("paneer_tikka")
        self.assertIn("dish_name", data)
        self.assertIn("calories_kcal", data)
        self.assertIn("protein_g", data)
        self.assertIn("carbs_g", data)
        self.assertIn("fats_g", data)
        self.assertIn("visible_ingredients", data)
        self.assertIn("allergen_alerts", data)
        self.assertIn("health_score", data)
        self.assertGreater(data["health_score"], 0)

    def test_freshness_contract(self):
        data = get_demo_food_freshness("banana_speckled")
        self.assertIn("freshness_category", data)
        self.assertIn(data["freshness_category"], ["Fresh", "Moderately Fresh", "Spoiled"])
        self.assertIn("actionable_guidance", data)
        self.assertIn(data["actionable_guidance"], ["Safe to consume", "Consume within 24 hours", "Discard immediately"])
        self.assertIn("visual_indicators", data)
        self.assertTrue(len(data["visual_indicators"]) >= 3)

    def test_kitchen_hygiene_contract(self):
        data = get_demo_kitchen_hygiene()
        self.assertIn("overall_compliance_score", data)
        self.assertTrue(0 <= data["overall_compliance_score"] <= 100)
        self.assertIn("violations", data)
        self.assertTrue(len(data["violations"]) > 0)
        for v in data["violations"]:
            self.assertIn("description", v)
            self.assertIn("visual_observation", v)
            self.assertIn("severity", v)
            self.assertIn("corrective_action", v)

    def test_recipe_assistant_contract(self):
        recipes = get_demo_recipes(["Paneer", "Spinach"])
        self.assertTrue(len(recipes) >= 2)
        r = recipes[0]
        self.assertIn("recipe_name", r)
        self.assertIn("prep_time_minutes", r)
        self.assertIn("cook_time_minutes", r)
        self.assertIn("step_by_step_instructions", r)
        self.assertIn("ingredient_substitutions", r)

    def test_meal_planner_contract(self):
        plan = get_demo_meal_plan(target_calories=2100, dietary_constraint="Vegan", fitness_goal="Muscle gain")
        self.assertIn("days", plan)
        self.assertEqual(len(plan["days"]), 7)
        self.assertIn("grocery_list", plan)
        self.assertTrue(len(plan["grocery_list"]) >= 3)


class TestComputerVisionService(unittest.TestCase):
    """Verifies synthetic frame generation and image diagnostics."""

    def test_image_quality_assessment(self):
        frame = create_sample_kitchen_frame("Test Station")
        diag = assess_image_quality(frame)
        self.assertEqual(diag["width"], 640)
        self.assertEqual(diag["height"], 480)
        self.assertIn("sharpness_score", diag)
        self.assertIn("quality_status", diag)


class TestAIServiceJSONCleaner(unittest.TestCase):
    """Verifies regex extraction of JSON objects from markdown wrappers."""

    def test_clean_json_codeblock(self):
        raw = "```json\n{\"dish_name\": \"Salad\", \"calories_kcal\": 250}\n```"
        parsed = _clean_json_response(raw)
        self.assertEqual(parsed["dish_name"], "Salad")
        self.assertEqual(parsed["calories_kcal"], 250)

    def test_clean_json_array(self):
        raw = "Here is the list: ```json\n[{\"recipe\": \"Soup\"}]\n```"
        parsed = _clean_json_response(raw)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["recipe"], "Soup")


if __name__ == "__main__":
    unittest.main()
