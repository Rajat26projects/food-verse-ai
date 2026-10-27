"""
Module 5: Personalized Meal Planner
Calculates BMR & TDEE using Mifflin-St Jeor clinical equations, generates
adaptive 7-day macro-tailored meal schedules, and builds consolidated grocery lists.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json

from config import (
    DIETARY_CONSTRAINTS,
    FITNESS_GOALS,
    ACTIVITY_LEVELS,
    MEDICAL_DISCLAIMER
)
from services.nutrition_calc import (
    calculate_bmr,
    calculate_tdee,
    calculate_target_calories,
    calculate_macro_split
)
from services.ai_service import generate_personalized_meal_plan


def render_meal_planner_module(api_key: str, provider: str, model_name: str):
    """Renders the Personalized BMR/TDEE Meal Planner interface."""
    st.markdown("### 📅 Module 5: Personalized Meal Planner")
    st.markdown(
        "Scientific metabolic planning. Calculate your Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) "
        "using clinical equations, and generate an adaptive 7-day meal schedule tailored to your dietary constraints and fitness goals."
    )

    with st.expander("ℹ️ Scientific Calculation Methodology (Mifflin-St Jeor & TDEE)", expanded=False):
        st.markdown(
            """
            **Mifflin-St Jeor Clinical Equation (BMR):**
            - **Men:** $\\text{BMR} = (10 \\times \\text{weight}_{\\text{kg}}) + (6.25 \\times \\text{height}_{\\text{cm}}) - (5 \\times \\text{age}) + 5$
            - **Women:** $\\text{BMR} = (10 \\times \\text{weight}_{\\text{kg}}) + (6.25 \\times \\text{height}_{\\text{cm}}) - (5 \\times \\text{age}) - 161$
            
            **Total Daily Energy Expenditure (TDEE):**
            - $\\text{TDEE} = \\text{BMR} \\times \\text{Activity Factor}$ (1.2 to 1.9)
            
            **Goal-Driven Adaptation:**
            - **Fat Loss:** Moderate sustained deficit of 500 kcal/day (capped above physiological floor).
            - **Muscle Gain:** Controlled surplus of +350 kcal/day with elevated protein allocation.
            """
        )

    # 1. Profile Form
    st.markdown("#### 👤 Step 1: Your Metabolic Profile")
    with st.form("metabolic_profile_form"):
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            age = st.number_input("Age (years)", min_value=16, max_value=100, value=28, step=1)
        with col_f2:
            gender = st.selectbox("Biological Gender", ["Male", "Female"])
        with col_f3:
            weight_kg = st.number_input("Weight (kg)", min_value=35.0, max_value=250.0, value=72.0, step=0.5)
        with col_f4:
            height_cm = st.number_input("Height (cm)", min_value=120.0, max_value=240.0, value=175.0, step=0.5)

        col_f5, col_f6, col_f7 = st.columns(3)
        with col_f5:
            activity_label = st.selectbox("Activity Level", list(ACTIVITY_LEVELS.keys()), index=2)
            activity_multiplier = ACTIVITY_LEVELS[activity_label]
        with col_f6:
            dietary_constraint = st.selectbox("Dietary Constraints", DIETARY_CONSTRAINTS, index=0)
        with col_f7:
            fitness_goal = st.selectbox("Fitness Goal", FITNESS_GOALS, index=0)

        calc_submit = st.form_submit_button("⚡ Calculate Targets & Build 7-Day Plan", type="primary", use_container_width=True)

    if calc_submit or "meal_planner_profile" in st.session_state:
        if calc_submit:
            # 2. Compute metabolic metrics
            bmr = calculate_bmr(weight_kg, height_cm, age, gender)
            tdee = calculate_tdee(bmr, activity_multiplier)
            target_cals, goal_note = calculate_target_calories(tdee, bmr, fitness_goal, gender)
            macro_split = calculate_macro_split(target_cals, dietary_constraint, fitness_goal, weight_kg)

            profile = {
                "age": age,
                "gender": gender,
                "weight_kg": weight_kg,
                "height_cm": height_cm,
                "activity_multiplier": activity_multiplier,
                "activity_label": activity_label,
                "dietary_constraint": dietary_constraint,
                "fitness_goal": fitness_goal,
                "bmr": bmr,
                "tdee": tdee,
                "target_calories": target_cals,
                "goal_note": goal_note,
                "macro_split": macro_split
            }
            st.session_state["meal_planner_profile"] = profile

            with st.spinner("🥗 Generating adaptive 7-day meal plan and grocery list..."):
                meal_plan_data = generate_personalized_meal_plan(
                    profile=profile,
                    provider=provider,
                    api_key=api_key,
                    model_name=model_name
                )
                st.session_state["meal_plan_results"] = meal_plan_data
        else:
            profile = st.session_state["meal_planner_profile"]
            meal_plan_data = st.session_state["meal_plan_results"]

        _display_metabolic_summary(profile)
        _display_meal_plan_schedule(meal_plan_data, profile)
        _display_grocery_list(meal_plan_data)


def _display_metabolic_summary(profile: dict):
    st.markdown("---")
    st.markdown("#### ⚡ Step 2: Metabolic Expenditure & Target Partition")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Basal Metabolic Rate (BMR)", f"{profile['bmr']} kcal", help="Minimum daily calories burned in a coma/fasting state.")
    with c2:
        st.metric("Daily Expenditure (TDEE)", f"{profile['tdee']} kcal", help="BMR multiplied by active lifestyle expenditure.")
    with c3:
        delta = profile['target_calories'] - profile['tdee']
        delta_label = f"{delta:+0.0f} kcal" if delta != 0 else "0 kcal (Maintenance)"
        st.metric("Suggested Target Intake", f"{profile['target_calories']} kcal", delta=delta_label)
    with c4:
        st.metric("Target Protein", f"{profile['macro_split']['protein_g']} g", f"{profile['macro_split']['protein_per_kg']} g/kg bodyweight")

    st.caption(f"📌 **Metabolic Goal Note:** {profile['goal_note']}")

    # Macro distribution bar
    macros = profile['macro_split']
    p_pct = macros['percentages']['protein']
    c_pct = macros['percentages']['carbs']
    f_pct = macros['percentages']['fats']

    fig = go.Figure(data=[
        go.Bar(name='Protein', x=['Macros'], y=[macros['protein_g'] * 4], marker_color='#10B981', hovertext=f"Protein: {macros['protein_g']}g ({p_pct}%)"),
        go.Bar(name='Carbs', x=['Macros'], y=[macros['carbs_g'] * 4], marker_color='#3B82F6', hovertext=f"Carbs: {macros['carbs_g']}g ({c_pct}%)"),
        go.Bar(name='Fats', x=['Macros'], y=[macros['fats_g'] * 9], marker_color='#F59E0B', hovertext=f"Fats: {macros['fats_g']}g ({f_pct}%)")
    ])
    fig.update_layout(
        barmode='stack',
        title="Target Daily Calorie Distribution by Macronutrient (kcal)",
        height=140,
        margin=dict(l=20, r=20, t=35, b=20),
        yaxis=dict(showticklabels=False),
        xaxis=dict(showticklabels=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)


def _display_meal_plan_schedule(data: dict, profile: dict):
    st.markdown("#### 📆 Step 3: Adaptive Seven-Day Meal Schedule")

    if data.get("is_demo", False):
        st.markdown(
            f"""
            <div class="demo-banner">
                <strong>⚡ Demonstration Mode Notice:</strong> {data.get("demo_notice", "Displaying clinically calibrated sample meal schedule.")}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="live-banner">
                <strong>✨ Live AI Generation:</strong> Custom 7-day schedule generated by active model.
            </div>
            """,
            unsafe_allow_html=True
        )

    days = data.get("days", [])
    if not days:
        st.warning("Meal schedule details unavailable.")
        return

    day_names = [d.get("day", f"Day {i+1}") for i, d in enumerate(days)]
    day_tabs = st.tabs(day_names)

    meal_icons = {
        "Breakfast": "🍳",
        "Lunch": "🥗",
        "Dinner": "🍲",
        "Snacks": "🍎"
    }

    for i, tab in enumerate(day_tabs):
        day_info = days[i]
        with tab:
            st.markdown(
                f"**Daily Calorie Target:** ~`{day_info.get('total_calories', profile['target_calories'])} kcal` &nbsp;|&nbsp; "
                f"**Protein:** `{day_info.get('total_protein_g', 'Balanced')}g` &nbsp;|&nbsp; "
                f"**Carbs:** `{day_info.get('total_carbs_g', 'Controlled')}g` &nbsp;|&nbsp; "
                f"**Fats:** `{day_info.get('total_fats_g', 'Healthy')}g`"
            )

            meals = day_info.get("meals", {})
            for m_type in ["Breakfast", "Lunch", "Dinner", "Snacks"]:
                if m_type in meals:
                    m = meals[m_type]
                    icon = meal_icons.get(m_type, "🍽️")
                    st.markdown(
                        f"""
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.9rem 1.2rem; margin-bottom: 0.75rem;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <strong style="font-size: 1.02rem; color: #0F172A;">{icon} {m_type}: {m.get('name', 'Wholesome Meal')}</strong>
                                <span class="badge-pill badge-green">{m.get('calories', 0)} kcal</span>
                            </div>
                            <div style="margin-top: 0.4rem; font-size: 0.9rem; color: #475569;">
                                <strong>Ingredients:</strong> {m.get('ingredients', 'Balanced ingredients')}
                            </div>
                            <div style="margin-top: 0.3rem; font-size: 0.82rem; color: #64748B; display: flex; gap: 15px;">
                                <span>Portion: <strong>{m.get('portion', 'Standard')}</strong></span>
                                <span>Protein: <strong>{m.get('protein', 0)}g</strong></span>
                                <span>Carbs: <strong>{m.get('carbs', 0)}g</strong></span>
                                <span>Fats: <strong>{m.get('fats', 0)}g</strong></span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


def _display_grocery_list(data: dict):
    st.markdown("#### 🛒 Step 4: Consolidated Weekly Grocery Shopping List")
    st.markdown(
        "Ingredients from all 28 planned meals are automatically grouped into shopping aisles, "
        "combining duplicates to make weekly provisioning effortless."
    )

    grocery_data = data.get("grocery_list", {})
    if not grocery_data:
        st.write("Grocery list not provided.")
        return

    cols = st.columns(len(grocery_data)) if len(grocery_data) <= 4 else st.columns(2)
    col_idx = 0

    download_lines = ["FOOD VERSE AI - 7-DAY CONSOLIDATED GROCERY LIST", "===============================================\n"]

    for category, items in grocery_data.items():
        with cols[col_idx % len(cols)]:
            st.markdown(f"##### {category}")
            download_lines.append(f"\n{category}")
            download_lines.append("-" * len(category))
            for item_info in items:
                if isinstance(item_info, dict):
                    name = item_info.get("item", "Item")
                    qty = item_info.get("quantity", "")
                    st.checkbox(f"{name} ({qty})", key=f"gro_{category}_{name[:10]}")
                    download_lines.append(f"[ ] {name} ({qty})")
                else:
                    st.checkbox(str(item_info), key=f"gro_{category}_{str(item_info)[:10]}")
                    download_lines.append(f"[ ] {str(item_info)}")
        col_idx += 1

    st.markdown("<br>", unsafe_allow_html=True)
    full_text = "\n".join(download_lines)
    st.download_button(
        label="📥 Download Consolidated Grocery Shopping List (.txt)",
        data=full_text,
        file_name="FoodVerse_Grocery_Shopping_List.txt",
        mime="text/plain",
        use_container_width=True
    )

    # Medical Disclaimer
    st.markdown(f"<div class='disclaimer-box'>{MEDICAL_DISCLAIMER}</div>", unsafe_allow_html=True)
