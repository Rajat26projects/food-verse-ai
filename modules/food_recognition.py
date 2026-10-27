"""
Module 1: Food Recognition and Nutrition Audit
Analyzes meal photographs to detect dishes, ingredients, portion sizes,
and computes comprehensive macronutrient & micronutrient breakdowns.
"""

import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import pandas as pd

from config import NUTRITION_DISCLAIMER
from services.ai_service import analyze_food_image
from assets.sample_images import get_sample_dish_image


def render_food_recognition_module(api_key: str, provider: str, model_name: str):
    """Renders the Food Recognition and Nutrition Audit interactive interface."""
    st.markdown("### 🥗 Module 1: Food Recognition & Nutrition Audit")
    st.markdown(
        "Upload a photograph of any dish or meal. Our multimodal intelligence agent identifies the dish, "
        "recognizes visible ingredients, estimates portion dimensions, and computes complete nutritional diagnostics."
    )

    # Input method selection: Upload file vs Sample preset
    col_input_mode, col_preset = st.columns([1, 2])
    with col_input_mode:
        input_choice = st.radio(
            "Image Source",
            ["Upload Image", "Try Sample Dish"],
            horizontal=True
        )

    active_image = None
    preset_key = "paneer_tikka"

    if input_choice == "Try Sample Dish":
        with col_preset:
            preset_option = st.selectbox(
                "Select a Curated Sample Meal",
                [
                    "Paneer Tikka Masala with Brown Rice (Vegetarian)",
                    "Mediterranean Grilled Chicken Quinoa Bowl (High Protein)"
                ]
            )
            if "Paneer" in preset_option:
                preset_key = "paneer_tikka"
            else:
                preset_key = "mediterranean_chicken"
            active_image = get_sample_dish_image(preset_key)
    else:
        uploaded_file = st.file_uploader(
            "Upload a meal photograph (JPG, JPEG, PNG)",
            type=["jpg", "jpeg", "png"],
            help="High-contrast, well-lit overhead or 45-degree angle food photos deliver the highest recognition fidelity."
        )
        if uploaded_file is not None:
            try:
                active_image = Image.open(uploaded_file)
            except Exception as e:
                st.error(f"Unable to read image file: {e}")

    # Display image preview and execution button
    if active_image:
        col_img, col_cta = st.columns([1, 1])
        with col_img:
            st.image(active_image, caption="Target Food Photograph", use_container_width=True)
        with col_cta:
            st.info("Ready for Multimodal Audit. The visual model will extract visible ingredients, portion estimates, and nutrient partitions.")
            analyze_btn = st.button("🚀 Analyze Food & Nutrition", type="primary", use_container_width=True)

        if analyze_btn or "food_recognition_results" in st.session_state:
            if analyze_btn:
                with st.spinner("🤖 Multimodal AI auditing dish geometry, ingredients, and nutrition..."):
                    results = analyze_food_image(
                        image=active_image,
                        provider=provider,
                        api_key=api_key,
                        model_name=model_name
                    )
                    st.session_state["food_recognition_results"] = results
            else:
                results = st.session_state["food_recognition_results"]

            _display_results(results)
    else:
        st.markdown(
            """
            <div style="background-color: #F8FAFC; border: 2px dashed #CBD5E1; border-radius: 12px; padding: 2.5rem; text-align: center; margin: 1.5rem 0;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📸</div>
                <h4 style="color: #475569; margin-bottom: 0.2rem;">No Food Image Selected</h4>
                <p style="color: #64748B; font-size: 0.9rem;">Upload a meal photograph above or switch to 'Try Sample Dish' for immediate demonstration.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def _display_results(data: dict):
    st.markdown("---")
    
    # 1. Mode Banner
    if data.get("is_demo", False):
        st.markdown(
            f"""
            <div class="demo-banner">
                <strong>⚡ Demonstration Mode Notice:</strong> {data.get("demo_notice", "Simulated results displayed.")}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="live-banner">
                <strong>✨ Live AI Analysis:</strong> Multimodal inference successfully generated from active vision model.
            </div>
            """,
            unsafe_allow_html=True
        )

    # 2. Dish Identity & Health Score Banner
    health_score = int(data.get("health_score", 80))
    health_color = "#10B981" if health_score >= 80 else ("#F59E0B" if health_score >= 60 else "#EF4444")

    col_title, col_score = st.columns([3, 1])
    with col_title:
        st.markdown(f"## {data.get('dish_name', 'Identified Dish')}")
        st.markdown(
            f"**Cuisine:** `{data.get('cuisine_type', 'General')}` &nbsp;|&nbsp; "
            f"**Portion:** `{data.get('portion_size', 'Standard Serving')}`"
        )
    with col_score:
        st.markdown(
            f"""
            <div style="background-color: #F8FAFC; border: 2px solid {health_color}; border-radius: 12px; padding: 0.75rem; text-align: center;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Health Score</div>
                <div style="font-size: 2rem; font-weight: 800; color: {health_color}; line-height: 1.1;">{health_score}<span style="font-size: 1rem; color: #94A3B8;">/100</span></div>
                <div style="font-size: 0.72rem; color: #475569; font-weight: 600;">{data.get('health_badge', 'Nutritional Rating')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 3. Macronutrient Metric Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Calories", f"{data.get('calories_kcal', 0)} kcal")
    with c2:
        st.metric("Protein", f"{data.get('protein_g', 0)} g")
    with c3:
        st.metric("Carbohydrates", f"{data.get('carbs_g', 0)} g")
    with c4:
        st.metric("Total Fats", f"{data.get('fats_g', 0)} g")
    with c5:
        st.metric("Dietary Fiber", f"{data.get('fiber_g', 0)} g")

    # 4. Interactive Charts & Ingredients
    col_chart, col_details = st.columns([1, 1])

    with col_chart:
        st.markdown("##### 📊 Macronutrient Caloric Contribution")
        prot_g = float(data.get("protein_g", 0))
        carb_g = float(data.get("carbs_g", 0))
        fat_g = float(data.get("fats_g", 0))
        
        prot_cals = prot_g * 4
        carb_cals = carb_g * 4
        fat_cals = fat_g * 9
        total_calc_cals = max(prot_cals + carb_cals + fat_cals, 1)

        labels = ['Protein', 'Carbohydrates', 'Fats']
        values = [prot_cals, carb_cals, fat_cals]
        colors = ['#10B981', '#3B82F6', '#F59E0B']

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.55,
            marker_colors=colors,
            textinfo='label+percent',
            hoverinfo='label+value',
            insidetextorientation='horizontal'
        )])
        fig.update_layout(
            showlegend=True,
            margin=dict(t=10, b=10, l=10, r=10),
            height=260,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_details:
        st.markdown("##### 🥗 Identified Visible Ingredients")
        ingredients = data.get("visible_ingredients", [])
        if ingredients:
            ing_html = " ".join([f"<span class='badge-pill badge-green' style='margin: 3px;'>{ing}</span>" for ing in ingredients])
            st.markdown(ing_html, unsafe_allow_html=True)
        else:
            st.write("No distinct ingredients parsed.")

        st.markdown("<br>", unsafe_allow_html=True)
        # Allergen alerts
        allergens = data.get("allergen_alerts", [])
        if allergens:
            st.markdown(
                f"""
                <div style="background-color: #FEF2F2; border-left: 4px solid #EF4444; padding: 0.8rem; border-radius: 6px;">
                    <strong style="color: #991B1B;">⚠️ Potential Allergen Alerts:</strong>
                    <ul style="margin: 0.3rem 0 0 1.2rem; color: #7F1D1D;">
                        {''.join([f"<li>{a}</li>" for a in allergens])}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.success("✅ No common major allergen risks flagged.")

    # 5. Micronutrients and Health Analysis
    st.markdown("##### 🔬 Micronutrients & Nutritional Analysis")
    micros = data.get("micronutrients", {})
    if micros:
        df_micros = pd.DataFrame(list(micros.items()), columns=["Micronutrient", "Estimated Quantity / Daily Value"])
        st.dataframe(df_micros, hide_index=True, use_container_width=True)

    if data.get("health_analysis"):
        st.info(f"**Nutritional Assessment:** {data.get('health_analysis')}")

    # 6. Scientific Disclaimer
    st.markdown(f"<div class='disclaimer-box'>{NUTRITION_DISCLAIMER}</div>", unsafe_allow_html=True)
