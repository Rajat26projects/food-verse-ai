"""
Module 4: Smart Kitchen Recipe Assistant
Generates chef-crafted, nutritionally balanced recipes based on ingredients
available in the user's pantry, with healthy alternatives and substitution guides.
"""

import streamlit as st
from services.ai_service import generate_smart_recipes


def render_recipe_assistant_module(api_key: str, provider: str, model_name: str):
    """Renders the Smart Kitchen Recipe Assistant interface."""
    st.markdown("### 🍳 Module 4: Smart Kitchen Recipe Assistant")
    st.markdown(
        "Prevent food waste and eat nutritionally optimized meals. Enter whatever ingredients you have "
        "in your kitchen, and our AI culinary chef designs custom recipes with step-by-step cooking instructions "
        "and healthy substitutions."
    )

    # Preset pantry quick-fills
    st.markdown("##### ⚡ Quick Pantry Presets")
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        if st.button("🥦 Desi Veg Bowl", use_container_width=True):
            st.session_state["recipe_ingredients_input"] = "Paneer, Spinach, Potatoes, Tomatoes, Onions, Brown Rice"
    with col_p2:
        if st.button("🍗 Mediterranean High-Protein", use_container_width=True):
            st.session_state["recipe_ingredients_input"] = "Chicken Breast, Quinoa, Cucumber, Tomatoes, Olive Oil, Lemon, Feta"
    with col_p3:
        if st.button("🌱 Plant-Based Superfood", use_container_width=True):
            st.session_state["recipe_ingredients_input"] = "Tofu, Sweet Potatoes, Kale, Chickpeas, Tahini, Garlic"
    with col_p4:
        if st.button("🥑 Low-Carb Keto", use_container_width=True):
            st.session_state["recipe_ingredients_input"] = "Eggs, Avocado, Mushrooms, Baby Spinach, Butter, Cheddar Cheese"

    default_ingredients = st.session_state.get(
        "recipe_ingredients_input",
        "Rice, Potatoes, Tomatoes, Onions, Paneer, Spinach"
    )

    col_input, col_pref = st.columns([2, 1])
    with col_input:
        ingredients_str = st.text_area(
            "Enter available ingredients (comma or newline separated):",
            value=default_ingredients,
            height=100,
            help="E.g., Rice, Potatoes, Tomatoes, Onions, Paneer, Spinach, Garlic, Spices"
        )
    with col_pref:
        diet_pref = st.selectbox(
            "Dietary / Culinary Preference",
            ["Balanced & Wholesome", "High Protein", "Vegetarian", "Vegan / Plant-Based", "Keto / Low-Carb", "Under 25 Minutes (Quick & Easy)"]
        )

    generate_btn = st.button("👨‍🍳 Generate Tailored Recipes", type="primary", use_container_width=True)

    if generate_btn or "recipe_results" in st.session_state:
        if generate_btn:
            raw_ings = [i.strip() for i in ingredients_str.replace("\n", ",").split(",") if i.strip()]
            if not raw_ings:
                st.warning("Please provide at least one ingredient to generate recipes.")
                return

            with st.spinner("🍳 Chef AI formulating recipes, optimizing cooking times, and mapping substitutions..."):
                recipes = generate_smart_recipes(
                    ingredients=raw_ings,
                    dietary_pref=diet_pref,
                    provider=provider,
                    api_key=api_key,
                    model_name=model_name
                )
                st.session_state["recipe_results"] = recipes
        else:
            recipes = st.session_state["recipe_results"]

        _display_recipe_results(recipes)


def _display_recipe_results(recipes: list):
    st.markdown("---")

    if not recipes:
        st.warning("No recipes could be formulated. Try adjusting the entered ingredients.")
        return

    # Check demo state
    is_demo = any(r.get("is_demo", False) for r in recipes)
    if is_demo:
        st.markdown(
            f"""
            <div class="demo-banner">
                <strong>⚡ Demonstration Mode Notice:</strong> {recipes[0].get("demo_notice", "Displaying chef demonstration recipes.")}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="live-banner">
                <strong>✨ Live AI Culinary Generation:</strong> Creative recipes formulated in real-time by active model.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(f"#### 🍽️ Formulated Recipes ({len(recipes)} Options)")

    # Display recipes as tabs or expandable cards
    tab_titles = [f"🍲 {r.get('recipe_name', f'Recipe {i+1}')[:28]}..." if len(r.get('recipe_name', '')) > 28 else f"🍲 {r.get('recipe_name', f'Recipe {i+1}')}" for i, r in enumerate(recipes)]
    tabs = st.tabs(tab_titles)

    for i, tab in enumerate(tabs):
        r = recipes[i]
        with tab:
            st.markdown(f"### {r.get('recipe_name', 'Custom Dish')}")
            st.markdown(f"*{r.get('description', '')}*")

            # Quick stats row
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.metric("Prep Time", f"{r.get('prep_time_minutes', 10)} min")
            with c2:
                st.metric("Cook Time", f"{r.get('cook_time_minutes', 15)} min")
            with c3:
                st.metric("Total Time", f"{r.get('total_time_minutes', 25)} min")
            with c4:
                st.metric("Difficulty", r.get("difficulty", "Easy"))
            with c5:
                st.metric("Calories", f"{r.get('calories_per_serving', 350)} kcal")

            # Macros badge bar
            macros = r.get("macros", {})
            if macros:
                st.markdown(
                    f"""
                    <div style="background: #F1F5F9; border-radius: 8px; padding: 0.5rem 1rem; margin-bottom: 1rem; display: flex; gap: 15px; font-size: 0.88rem;">
                        <span><strong>Protein:</strong> {macros.get('protein_g', 0)}g</span>
                        <span><strong>Carbohydrates:</strong> {macros.get('carbs_g', 0)}g</span>
                        <span><strong>Fats:</strong> {macros.get('fats_g', 0)}g</span>
                        <span><strong>Fiber:</strong> {macros.get('fiber_g', 0)}g</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Two-column layout: Ingredients vs Step-by-Step Instructions
            col_ing, col_steps = st.columns([1, 1])

            with col_ing:
                st.markdown("##### 🛒 Ingredients & Quantities")
                used_ings = r.get("ingredients_used", r.get("ingredient_quantities", []))
                for item in used_ings:
                    st.markdown(f"- {item}")

                pantry_items = r.get("pantry_staples_needed", r.get("pantry_staples_assumed", []))
                if pantry_items:
                    st.markdown("**Pantry Essentials:**")
                    for p in pantry_items:
                        st.markdown(f"- *{p}*")

            with col_steps:
                st.markdown("##### 👩‍🍳 Step-by-Step Cooking Instructions")
                instructions = r.get("step_by_step_instructions", r.get("instructions", []))
                for s_num, step in enumerate(instructions, 1):
                    st.markdown(f"**{s_num}.** {step}")

            # Substitutions & Healthy tips
            st.markdown("<br>", unsafe_allow_html=True)
            col_sub, col_tip = st.columns([1, 1])

            with col_sub:
                st.markdown("##### 🔄 Ingredient Substitutions")
                subs = r.get("ingredient_substitutions", [])
                if subs:
                    for s in subs:
                        st.markdown(f"- **{s.get('original')}:** Swap with *{s.get('substitute')}* ({s.get('reason', s.get('note', ''))})")
                else:
                    st.write("No modifications necessary.")

            with col_tip:
                st.markdown("##### 💡 Chef's Health & Technique Tip")
                tip = r.get("healthy_cooking_tips", "Gentle cooking preserves vitamins.")
                st.info(tip)
