"""
Food Verse AI – Multimodal Food Intelligence Agent
Skill Wallet Capstone Project 3
Platform ID: 6ac4ca021dcde6d7857c169a
Main Streamlit Application Entrypoint
"""

import os
import streamlit as st
from PIL import Image

# Import configuration and modules
from config import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_ICON,
    PROVIDER_GEMINI,
    PROVIDER_GROQ,
    GEMINI_MODELS,
    GROQ_MODELS,
    DEMO_MODE_LABEL
)
from modules.food_recognition import render_food_recognition_module
from modules.food_freshness import render_food_freshness_module
from modules.kitchen_hygiene import render_kitchen_hygiene_module
from modules.recipe_assistant import render_recipe_assistant_module
from modules.meal_planner import render_meal_planner_module

# 1. Page Configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Custom Modern CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def init_session_state():
    """Initializes persistent application session variables."""
    if "api_provider" not in st.session_state:
        st.session_state["api_provider"] = PROVIDER_GEMINI
    if "api_key" not in st.session_state:
        # Check environment variable fallback safely
        st.session_state["api_key"] = os.getenv("GEMINI_API_KEY", os.getenv("GROQ_API_KEY", ""))
    if "current_module" not in st.session_state:
        st.session_state["current_module"] = "🥗 1. Food Recognition & Nutrition"


init_session_state()

# 3. Sidebar Configuration & Interactive Navigation
with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
            <div style="font-size: 2.8rem;">{APP_ICON}</div>
            <h2 style="margin: 0; font-size: 1.25rem; color: #0F172A;">Food Verse AI</h2>
            <p style="margin: 0; font-size: 0.78rem; color: #64748B;">Multimodal Food Intelligence Agent</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ⚙️ AI Engine Configuration")

    provider = st.selectbox(
        "Multimodal Provider",
        [PROVIDER_GEMINI, PROVIDER_GROQ],
        index=0 if st.session_state["api_provider"] == PROVIDER_GEMINI else 1,
        help="Select between Google Gemini 1.5/2.0 or Groq LLaMA-Vision models."
    )
    st.session_state["api_provider"] = provider

    # Secure API Key Input
    api_key_env = os.getenv("GEMINI_API_KEY" if provider == PROVIDER_GEMINI else "GROQ_API_KEY", "")
    user_api_key = st.text_input(
        f"{provider} API Key",
        value=st.session_state["api_key"] if st.session_state["api_key"] else api_key_env,
        type="password",
        placeholder="Enter key or leave blank for Demo Mode",
        help="Keys are stored exclusively in temporary session memory and are never written to disk or printed."
    )
    st.session_state["api_key"] = user_api_key.strip()

    # Model selector based on provider
    if provider == PROVIDER_GEMINI:
        from services.ai_service import get_available_gemini_models
        active_models = get_available_gemini_models(st.session_state["api_key"])
        model_name = st.selectbox("Gemini Model", active_models, index=0)
    else:
        model_name = st.selectbox("Groq Model", GROQ_MODELS, index=0)

    # Engine Status Indicator
    if st.session_state["api_key"]:
        st.success(f"🔑 Live AI Connected: `{model_name}`")
    else:
        st.info(f"⚡ Running in Demonstration Mode (No API key provided). Full simulation active.")

    st.markdown("---")
    st.markdown("### 🧭 Core Intelligence Modules")

    modules_list = [
        "🥗 1. Food Recognition & Nutrition",
        "🍎 2. Food Freshness & Spoilage",
        "🧑‍🍳 3. Kitchen Hygiene Compliance",
        "🍳 4. Smart Recipe Assistant",
        "📅 5. Personalized Meal Planner"
    ]

    selected_module = st.radio(
        "Select Active Module",
        modules_list,
        index=modules_list.index(st.session_state["current_module"]) if st.session_state["current_module"] in modules_list else 0
    )
    st.session_state["current_module"] = selected_module

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.75rem; color: #94A3B8; line-height: 1.4;">
            <strong>Platform ID:</strong> <code>6ac4ca021dcde6d7857c169a</code><br>
            <strong>Category:</strong> Generative AI | Nutrition, Freshness & Kitchen Safety<br>
            <strong>Version:</strong> 1.0.0 (Production Ready)<br>
            <strong>Deployment:</strong> Streamlit Community Cloud
        </div>
        """,
        unsafe_allow_html=True
    )


# 4. Main View Header / Hero Banner
st.markdown(
    f"""
    <div class="hero-banner">
        <h1 class="hero-title">{APP_TITLE}</h1>
        <div class="hero-subtitle">
            Autonomous Multimodal Vision, Spoilage Diagnostics, HACCP Safety Audits & Personalized Metabolic Planning
        </div>
        <div style="margin-top: 0.8rem; display: flex; gap: 10px; flex-wrap: wrap; font-size: 0.8rem;">
            <span style="background: rgba(255,255,255,0.15); padding: 3px 10px; border-radius: 6px;">Category: Generative AI</span>
            <span style="background: rgba(255,255,255,0.15); padding: 3px 10px; border-radius: 6px;">ID: 6ac4ca021dcde6d7857c169a</span>
            <span style="background: rgba(255,255,255,0.15); padding: 3px 10px; border-radius: 6px;">Provider: {provider}</span>
            <span style="background: rgba(255,255,255,0.15); padding: 3px 10px; border-radius: 6px;">OpenCV + Gemini/Groq</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# 5. Route to Active Module
try:
    if "1. Food Recognition" in selected_module:
        render_food_recognition_module(
            api_key=st.session_state["api_key"],
            provider=provider,
            model_name=model_name
        )
    elif "2. Food Freshness" in selected_module:
        render_food_freshness_module(
            api_key=st.session_state["api_key"],
            provider=provider,
            model_name=model_name
        )
    elif "3. Kitchen Hygiene" in selected_module:
        render_kitchen_hygiene_module(
            api_key=st.session_state["api_key"],
            provider=provider,
            model_name=model_name
        )
    elif "4. Smart Recipe" in selected_module:
        render_recipe_assistant_module(
            api_key=st.session_state["api_key"],
            provider=provider,
            model_name=model_name
        )
    elif "5. Personalized Meal Planner" in selected_module:
        render_meal_planner_module(
            api_key=st.session_state["api_key"],
            provider=provider,
            model_name=model_name
        )
except Exception as err:
    st.error(f"An unexpected error occurred during execution: {err}")
    st.exception(err)


# 6. Global Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #94A3B8; font-size: 0.8rem; padding: 1.5rem 0;">
        <strong>Food Verse AI</strong> • Multimodal Food Intelligence Agent • Skill Wallet Capstone Project 3<br>
        Built with Streamlit, OpenCV, Google Gemini, Groq, Pillow, and Plotly. Fully self-contained without external database dependencies.
    </div>
    """,
    unsafe_allow_html=True
)
