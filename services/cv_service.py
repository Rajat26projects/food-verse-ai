"""
Computer Vision and Frame Extraction Service
Leverages OpenCV and Pillow for video frame sampling, image validation,
and visual quality diagnostics.
"""

import io
import os
import tempfile
from typing import List, Tuple, Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Safely import cv2
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    cv2 = None
    OPENCV_AVAILABLE = False


def extract_video_frames(video_bytes: bytes, max_frames: int = 4) -> Tuple[List[Image.Image], Dict[str, Any]]:
    """
    Extracts representative keyframes from a video file using OpenCV.
    
    Args:
        video_bytes: Raw bytes of the uploaded video.
        max_frames: Number of evenly spaced keyframes to extract (default 4).
        
    Returns:
        Tuple of (List of PIL Images, metadata dictionary).
    """
    if not OPENCV_AVAILABLE:
        # Fallback if cv2 isn't ready: generate synthetic frames
        return [create_sample_kitchen_frame(f"Frame #{i+1} (Simulation)") for i in range(max_frames)], {
            "fps": 30.0,
            "total_frames": 120,
            "duration_sec": 4.0,
            "extracted_count": max_frames,
            "source": "simulated"
        }

    # Write video bytes to a safe temporary file for OpenCV VideoCapture
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_bytes)
        tmp_path = tmp.name

    frames: List[Image.Image] = []
    metadata: Dict[str, Any] = {}

    try:
        cap = cv2.VideoCapture(tmp_path)
        if not cap.isOpened():
            raise ValueError("Failed to open video stream. The format or codec may be unsupported.")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = float(cap.get(cv2.CAP_PROP_FPS)) or 30.0
        duration_sec = total_frames / fps if fps > 0 else 0.0

        metadata = {
            "fps": round(fps, 1),
            "total_frames": total_frames,
            "duration_sec": round(duration_sec, 2),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        }

        if total_frames <= 0:
            # If frame count is unavailable, sequential sampling
            count = 0
            while len(frames) < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                if count % 25 == 0:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(Image.fromarray(frame_rgb))
                count += 1
        else:
            # Evenly space frame indices across duration
            indices = np.linspace(0, max(0, total_frames - 1), num=max_frames, dtype=int)
            for idx in indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
                ret, frame = cap.read()
                if ret and frame is not None:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # Resize large frames for optimal memory and API speed
                    h, w = frame_rgb.shape[:2]
                    if w > 1280:
                        scale = 1280 / w
                        frame_rgb = cv2.resize(frame_rgb, (1280, int(h * scale)))
                    frames.append(Image.fromarray(frame_rgb))

        cap.release()
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    metadata["extracted_count"] = len(frames)
    metadata["source"] = "opencv"
    return frames, metadata


def assess_image_quality(image: Image.Image) -> Dict[str, Any]:
    """
    Computes visual metrics (sharpness, brightness, contrast) using OpenCV/NumPy.
    """
    img_arr = np.array(image.convert("RGB"))
    brightness = float(np.mean(img_arr))
    contrast = float(np.std(img_arr))

    sharpness = 100.0
    if OPENCV_AVAILABLE:
        gray = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)
        laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        sharpness = round(min(laplacian_var, 500.0) / 5.0, 1)

    is_blurry = sharpness < 15.0
    is_too_dark = brightness < 40.0
    is_too_bright = brightness > 230.0

    return {
        "width": image.width,
        "height": image.height,
        "brightness": round(brightness, 1),
        "contrast": round(contrast, 1),
        "sharpness_score": sharpness,
        "is_blurry": is_blurry,
        "is_suboptimal_lighting": is_too_dark or is_too_bright,
        "quality_status": "Suboptimal" if (is_blurry or is_too_dark or is_too_bright) else "Good"
    }


def create_sample_kitchen_frame(label: str = "Kitchen Hygiene Station") -> Image.Image:
    """Creates a high-contrast synthetic kitchen workspace image for testing."""
    img = Image.new("RGB", (640, 480), color=(240, 244, 248))
    draw = ImageDraw.Draw(img)

    # Stainless steel table
    draw.rectangle([40, 220, 600, 420], fill=(210, 215, 220), outline=(160, 170, 180), width=3)
    # Cutting board
    draw.rectangle([100, 260, 320, 380], fill=(245, 235, 210), outline=(180, 150, 110), width=2)
    # Produce
    draw.ellipse([140, 290, 200, 350], fill=(76, 175, 80)) # Green vegetables
    draw.ellipse([220, 300, 270, 350], fill=(244, 67, 54)) # Tomatoes
    # Prep bowl
    draw.ellipse([380, 270, 520, 370], fill=(189, 195, 199), outline=(127, 140, 141), width=2)

    # Header label
    draw.rectangle([0, 0, 640, 60], fill=(44, 62, 80))
    draw.text((20, 18), f"Food Verse AI Visual Capture: {label}", fill=(255, 255, 255))
    draw.text((20, 440), "Simulated Kitchen Observation Frame • Commercial Grade", fill=(100, 110, 120))
    return img
