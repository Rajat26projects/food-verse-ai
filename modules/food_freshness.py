"""
Module 2: Food Freshness and Spoilage Diagnostic
Assesses perishable food items (produce, meat, dairy) using multimodal vision
to classify freshness, detect physical deterioration, and provide actionable storage guidance.
"""

import streamlit as st
from PIL import Image
import pandas as pd

from config import (
    FRESHNESS_CATEGORIES,
    FOOD_SAFETY_ACTIONS,
    FRESHNESS_DISCLAIMER
)
from services.ai_service import analyze_food_freshness
from assets.sample_images import get_sample_freshness_image


def render_food_freshness_module(api_key: str, provider: str, model_name: str):
    """Renders the Food Freshness and Spoilage Diagnostic interface."""
    st.markdown("### 🍎 Module 2: Food Freshness & Spoilage Diagnostic")
    st.markdown(
        "Evaluate perishable foods (fruits, vegetables, meat, poultry, and dairy). "
        "The diagnostic agent analyzes superficial texture, senescent browning, dehydration wrinkling, and fungal signs."
    )

    col_input_mode, col_preset = st.columns([1, 2])
    with col_input_mode:
        input_choice = st.radio(
            "Perishable Source",
            ["Upload Image", "Try Sample Item"],
            horizontal=True
        )

    active_image = None
    preset_key = "banana_speckled"

    if input_choice == "Try Sample Item":
        with col_preset:
            preset_option = st.selectbox(
                "Select a Perishable Item State",
                [
                    "Cavendish Bananas with Melanin Sugar Spots (Moderately Fresh)",
                    "Organic Garden Strawberries (Peak Fresh)",
                    "Raw Poultry with Slime & Discoloration (Spoiled)"
                ]
            )
            if "Bananas" in preset_option:
                preset_key = "banana_speckled"
            elif "Strawberries" in preset_option:
                preset_key = "fresh_strawberries"
            else:
                preset_key = "spoiled_poultry"
            active_image = get_sample_freshness_image(preset_key)
    else:
        uploaded_file = st.file_uploader(
            "Upload image of perishable food (JPG, JPEG, PNG)",
            type=["jpg", "jpeg", "png"],
            help="Close-up photographs of food surfaces, stems, or cross-sections yield optimal inspection accuracy."
        )
        if uploaded_file is not None:
            try:
                active_image = Image.open(uploaded_file)
            except Exception as e:
                st.error(f"Failed to read image file: {e}")

    if active_image:
        col_img, col_cta = st.columns([1, 1])
        with col_img:
            st.image(active_image, caption="Inspected Perishable Item", use_container_width=True)
        with col_cta:
            st.info("Ready for Spoilage Diagnostic. Visual cues will be evaluated against HACCP quality thresholds.")
            diagnose_btn = st.button("🔍 Run Spoilage Diagnostic", type="primary", use_container_width=True)

        if diagnose_btn or "freshness_results" in st.session_state:
            if diagnose_btn:
                with st.spinner("🔬 Auditing surface morphology, enzymatic discoloration, and microbial indicators..."):
                    results = analyze_food_freshness(
                        image=active_image,
                        provider=provider,
                        api_key=api_key,
                        model_name=model_name
                    )
                    st.session_state["freshness_results"] = results
            else:
                results = st.session_state["freshness_results"]

            _display_freshness_results(results)
    else:
        st.markdown(
            """
            <div style="background-color: #F8FAFC; border: 2px dashed #CBD5E1; border-radius: 12px; padding: 2.5rem; text-align: center; margin: 1.5rem 0;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
                <h4 style="color: #475569; margin-bottom: 0.2rem;">No Perishable Item Selected</h4>
                <p style="color: #64748B; font-size: 0.9rem;">Upload a photo of fruit, vegetables, dairy, or meat, or select 'Try Sample Item' to test.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def _display_freshness_results(data: dict):
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
                <strong>✨ Live AI Diagnostic:</strong> Visual deterioration analysis completed using active multimodal model.
            </div>
            """,
            unsafe_allow_html=True
        )

    # 2. Freshness Status & Recommended Action
    category = data.get("freshness_category", "Moderately Fresh")
    action = data.get("actionable_guidance", "Consume within 24 hours")
    confidence = data.get("confidence_score", 90)

    cat_badge = FRESHNESS_CATEGORIES.get(category, {"badge": category, "color": "#64748B"})
    action_info = FOOD_SAFETY_ACTIONS.get(action, {"color": "#64748B", "icon": "ℹ️"})

    col_cat, col_action = st.columns([1, 1])
    with col_cat:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 2px solid {cat_badge['color']}; border-radius: 12px; padding: 1rem; text-align: center;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Predicted Freshness Category</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: {cat_badge['color']}; margin: 0.2rem 0;">
                    {cat_badge['badge']}
                </div>
                <div style="font-size: 0.85rem; color: #475569;">Confidence: <strong>{confidence}%</strong> &nbsp;|&nbsp; Item: <strong>{data.get('food_item', 'Perishable')}</strong></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_action:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 2px solid {action_info['color']}; border-radius: 12px; padding: 1rem; text-align: center;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Recommended Safety Action</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: {action_info['color']}; margin: 0.2rem 0;">
                    {action_info['icon']} {action}
                </div>
                <div style="font-size: 0.85rem; color: #475569;">Classification: <strong>{data.get('food_category', 'General Produce')}</strong></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Itemized Visual Indicators
    st.markdown("##### 🔬 Observable Deterioration Indicators")
    indicators = data.get("visual_indicators", [])
    if indicators:
        df_indicators = pd.DataFrame(indicators)
        df_indicators.columns = ["Visual Characteristic", "Micro-Observation", "Condition Assessment"]
        st.dataframe(df_indicators, hide_index=True, use_container_width=True)

    # 4. Storage & Preservation Tips
    st.markdown("##### ❄️ Food Preservation & Storage Guidelines")
    tips = data.get("storage_preservation_tips", [])
    if tips:
        for idx, tip in enumerate(tips, 1):
            st.markdown(f"**{idx}.** {tip}")

    if data.get("microbial_risk_level"):
        st.warning(f"**Microbiological Risk Assessment:** {data.get('microbial_risk_level')}")

    # 5. Food Safety Disclaimer
    st.markdown(f"<div class='disclaimer-box'>{FRESHNESS_DISCLAIMER}</div>", unsafe_allow_html=True)
