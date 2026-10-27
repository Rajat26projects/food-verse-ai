"""
Module 3: Kitchen Hygiene and Food Safety Compliance
Performs visual audit of commercial kitchen photographs and video frames using OpenCV
to inspect PPE compliance (hairnets, gloves), cleanliness, and cross-contamination hazards.
"""

import streamlit as st
from PIL import Image
import pandas as pd

from config import KITCHEN_SAFETY_DISCLAIMER
from services.cv_service import extract_video_frames, assess_image_quality
from services.ai_service import analyze_kitchen_hygiene
from assets.sample_images import get_sample_kitchen_image


def render_kitchen_hygiene_module(api_key: str, provider: str, model_name: str):
    """Renders the Commercial Kitchen Hygiene Compliance Audit interface."""
    st.markdown("### 🧑‍🍳 Module 3: Kitchen Hygiene & Safety Compliance")
    st.markdown(
        "Audit commercial kitchen workspaces, prep lines, and personnel hygiene. "
        "Upload a kitchen photograph or video clip. OpenCV samples key operational frames "
        "for cross-contamination hazards, PPE (hairnet/glove) compliance, and sanitization standards."
    )

    media_type = st.radio(
        "Media Audit Type",
        ["Kitchen Photograph", "Kitchen Video (Keyframe Extraction)", "Try Sample Commercial Kitchen Scene"],
        horizontal=True
    )

    frames_to_audit = []
    video_meta = {}

    if media_type == "Try Sample Commercial Kitchen Scene":
        sample_img = get_sample_kitchen_image()
        frames_to_audit = [sample_img]
        st.image(sample_img, caption="Simulated Commercial Kitchen Prep Station (Raw Poultry Hazard)", use_container_width=True)

    elif media_type == "Kitchen Photograph":
        uploaded_img = st.file_uploader(
            "Upload Kitchen Photograph (JPG, JPEG, PNG)",
            type=["jpg", "jpeg", "png"],
            help="High-resolution views of food preparation stations, counters, and staff provide optimal audit accuracy."
        )
        if uploaded_img is not None:
            try:
                img = Image.open(uploaded_img)
                frames_to_audit = [img]
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.image(img, caption="Uploaded Kitchen Workspace Photo", use_container_width=True)
                with col2:
                    quality = assess_image_quality(img)
                    st.markdown("**Image Diagnostic:**")
                    st.write(f"- Resolution: `{quality['width']} x {quality['height']}`")
                    st.write(f"- Sharpness: `{quality['sharpness_score']}` ({quality['quality_status']})")
                    st.write(f"- Mean Luminance: `{quality['brightness']}`")
            except Exception as e:
                st.error(f"Error opening image: {e}")

    else: # Video
        uploaded_video = st.file_uploader(
            "Upload Kitchen Video (MP4, MOV, AVI)",
            type=["mp4", "mov", "avi"],
            help="OpenCV extracts representative operational keyframes across the footage."
        )
        if uploaded_video is not None:
            video_bytes = uploaded_video.read()
            with st.spinner("🎞️ OpenCV extracting and normalizing representative operational keyframes..."):
                extracted, video_meta = extract_video_frames(video_bytes, max_frames=4)
                frames_to_audit = extracted

            if frames_to_audit:
                st.success(f"Extracted {len(frames_to_audit)} representative keyframes ({video_meta.get('duration_sec', 0)}s duration, {video_meta.get('fps', 0)} FPS).")
                cols = st.columns(len(frames_to_audit))
                for i, col in enumerate(cols):
                    with col:
                        st.image(frames_to_audit[i], caption=f"Keyframe #{i+1}", use_container_width=True)

    if frames_to_audit:
        st.markdown("<br>", unsafe_allow_html=True)
        audit_btn = st.button("🛡️ Audit Kitchen Hygiene & Safety Compliance", type="primary", use_container_width=True)

        if audit_btn or "hygiene_results" in st.session_state:
            if audit_btn:
                with st.spinner("🤖 Auditing hairnets, glove usage, surface sanitization, and cross-contamination hazards..."):
                    results = analyze_kitchen_hygiene(
                        images=frames_to_audit,
                        provider=provider,
                        api_key=api_key,
                        model_name=model_name
                    )
                    st.session_state["hygiene_results"] = results
            else:
                results = st.session_state["hygiene_results"]

            _display_hygiene_results(results)
    else:
        st.markdown(
            """
            <div style="background-color: #F8FAFC; border: 2px dashed #CBD5E1; border-radius: 12px; padding: 2.5rem; text-align: center; margin: 1.5rem 0;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">👨‍🍳</div>
                <h4 style="color: #475569; margin-bottom: 0.2rem;">No Kitchen Media Loaded</h4>
                <p style="color: #64748B; font-size: 0.9rem;">Select 'Try Sample Commercial Kitchen Scene' or upload an image/video to begin compliance verification.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def _display_hygiene_results(data: dict):
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
                <strong>✨ Live AI Audit:</strong> Commercial kitchen compliance verified via multimodal visual evaluation.
            </div>
            """,
            unsafe_allow_html=True
        )

    # 2. Overall Score & Rating Banner
    score = int(data.get("overall_compliance_score", 80))
    score_color = "#10B981" if score >= 85 else ("#F59E0B" if score >= 70 else "#EF4444")
    rating_text = data.get("compliance_rating", "Acceptable")

    col_score, col_obs = st.columns([1, 2])
    with col_score:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 2px solid {score_color}; border-radius: 12px; padding: 1.2rem; text-align: center;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Hygiene Compliance Score</div>
                <div style="font-size: 2.8rem; font-weight: 800; color: {score_color}; line-height: 1.1;">{score}%</div>
                <div style="font-size: 0.85rem; font-weight: 700; color: {score_color}; margin-top: 0.3rem;">{rating_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_obs:
        st.markdown("##### 📋 Inspector Observations")
        st.write(data.get("key_observations", "Visual audit completed."))
        
        # Sub-metrics if present
        metrics = data.get("metrics", {})
        if metrics:
            m_cols = st.columns(len(metrics))
            for i, (k, v) in enumerate(metrics.items()):
                with m_cols[i]:
                    label = k.replace("_", " ").title()
                    st.metric(label, v)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Itemized Violations
    st.markdown("##### 🚨 Itemized Compliance Violations & Corrective Actions")
    violations = data.get("violations", [])
    if violations:
        for v in violations:
            sev = v.get("severity", "Medium").lower()
            sev_badge = v.get("severity_badge", f"Priority: {v.get('severity')}")
            css_class = "violation-card"
            if sev == "medium":
                css_class += " medium"
            elif sev == "low":
                css_class += " low"

            st.markdown(
                f"""
                <div class="{css_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <strong style="font-size: 1.05rem; color: #0F172A;">[{v.get('id', 'VIOL')}] {v.get('title', v.get('description', 'Violation'))}</strong>
                        <span style="font-size: 0.8rem; font-weight: 700;">{sev_badge}</span>
                    </div>
                    <p style="margin: 0.2rem 0; color: #334155;"><strong>Visual Observation:</strong> {v.get('visual_observation', 'Observed in audit.')}</p>
                    <p style="margin: 0.2rem 0; color: #0369A1;"><strong>Required Corrective Action:</strong> {v.get('corrective_action', 'Address in accordance with health code.')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.success("✅ No critical food safety or hygiene non-compliances detected in the evaluated scenes.")

    # 4. Good Practices & Action Checklist
    c_good, c_check = st.columns(2)
    with c_good:
        st.markdown("##### ✅ Good Practices Observed")
        goods = data.get("good_practices_observed", [])
        if goods:
            for g in goods:
                st.markdown(f"- {g}")
        else:
            st.write("Standard procedures followed.")

    with c_check:
        st.markdown("##### 📌 Safety Action Checklist")
        actions = data.get("action_checklist", [])
        if actions:
            for a in actions:
                st.checkbox(a, key=f"hygiene_act_{a[:20]}")
        else:
            st.write("Maintain current hygiene protocols.")

    # 5. Regulatory Disclaimer
    st.markdown(f"<div class='disclaimer-box'>{KITCHEN_SAFETY_DISCLAIMER}</div>", unsafe_allow_html=True)
