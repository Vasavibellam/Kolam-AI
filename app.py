import streamlit as st
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# ===================== IMPORTS FROM BACKEND =====================
from backend.kolam_generator import generate_advanced_pulli_kolam
from backend.kolam_visualization import draw_reconstructed_kolam, draw_kolam

from backend.kolam_image_analysis import (
    preprocess_image,
    detect_dots,
    extract_loops
)

from backend.kolam_analysis import (
    analyze_kolam_from_image,
    export_kolam_svg
)

from backend.kolam_saree import generate_saree_print, draw_saree_print
from backend.kolam_palettes import TEXTILE_PALETTES

# ===================== ML / VAE =====================
from ml.generate_kolam import generate_symmetric_kolam

# ===================== DATASET PATH =====================
KAGGLE_DATASET_PATH = "datasets/kaggle_kolams/all"

# ===================== ABSTRACT DOT DATASET =====================
KOLAM_DATASET = {
    "1-7-1 Rhombic Pulli Kolam": {
        "n": 7,
        "description": "Classic symmetric Pulli Kolam with rhombic dot layout"
    },
    "1-5-1 Rhombic Pulli Kolam": {
        "n": 5,
        "description": "Medium complexity symmetric Pulli Kolam"
    }
}

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Kolam Intelligence System",
    layout="centered"
)

st.title("🪔 From Temple Floors 🌸 to Digital Canvas ✨")

# ======================================================
# SAREE BORDER + PALLU FUNCTION
# ======================================================
def draw_saree_border_pallu_streamlit(curves, border_repeat=6):

    fig, ax = plt.subplots(figsize=(14, 4))

    # -------- BORDER --------
    for i in range(border_repeat):
        for curve in curves:
            x, y = zip(*curve)
            ax.plot(
                [xi + i * 6 for xi in x],
                y,
                color="maroon",
                linewidth=1.2
            )

    # -------- PALLU --------
    scale = 2.8
    offset_x = border_repeat * 6 + 3

    for curve in curves:
        x, y = zip(*curve)
        ax.plot(
            [xi * scale + offset_x for xi in x],
            [yi * scale for yi in y],
            color="navy",
            linewidth=2.2
        )

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Kolam-Based Saree Border & Pallu Layout")

    return fig


# ===================== MODE SELECTION =====================
mode = st.radio(
    "Select Mode",
    [
        "Rule-Based Kolam Generation",
        "Single Image Kolam Analysis",
        "Abstract Dataset (Dot-Pattern Kolams)",
        "Kaggle Dataset Image Reconstruction",
        "🧵 Saree / Fabric Print Generator",
        "🧠 AI Kolam Generator (VAE)"
    ]
)

# ==========================================================
# MODE 1: RULE-BASED GENERATION
# ==========================================================
if mode == "Rule-Based Kolam Generation":

    st.subheader("Advanced Rule-Based Pulli Kolam")

    n = st.slider("Dot Grid Size (1–n–1)", 3, 9, 7)
    curvature = st.slider("Bezier Curve Smoothness", 0.1, 0.8, 0.4)

    if st.button("Generate Kolam"):
        dots, curves = generate_advanced_pulli_kolam(n, curvature)
        fig = draw_kolam(dots, curves)
        st.pyplot(fig)

# ==========================================================
# MODE 2: SINGLE IMAGE ANALYSIS
# ==========================================================
elif mode == "Single Image Kolam Analysis":

    st.subheader("Single Image Kolam Reconstruction")

    uploaded = st.file_uploader("Upload Kolam Image", ["png", "jpg", "jpeg"])

    if uploaded:
        image = cv2.imdecode(
            np.frombuffer(uploaded.read(), np.uint8),
            cv2.IMREAD_COLOR
        )

        st.image(image, channels="BGR")

        thresh = preprocess_image(image)
        dots = detect_dots(thresh)
        loops = extract_loops(thresh)

        fig = draw_reconstructed_kolam(loops)
        st.pyplot(fig)

        st.subheader("Kolam Structural Analysis")
        st.json(analyze_kolam_from_image(dots, loops))

# ==========================================================
# MODE 3: ABSTRACT DATASET
# ==========================================================
elif mode == "Abstract Dataset (Dot-Pattern Kolams)":

    st.subheader("Formalized Pulli Kolam Dataset")

    kolam_name = st.selectbox("Select Pattern", list(KOLAM_DATASET.keys()))
    entry = KOLAM_DATASET[kolam_name]

    st.info(entry["description"])

    curvature = st.slider("Bezier Curve Smoothness", 0.1, 0.8, 0.4)

    if st.button("Generate Dataset Kolam"):
        dots, curves = generate_advanced_pulli_kolam(entry["n"], curvature)
        fig = draw_kolam(dots, curves)
        st.pyplot(fig)

# ==========================================================
# MODE 4: KAGGLE DATASET
# ==========================================================
elif mode == "Kaggle Dataset Image Reconstruction":

    st.subheader("📂 Kaggle Kolam Image Dataset")

    if not os.path.exists(KAGGLE_DATASET_PATH):
        st.error("Dataset folder not found")
    else:
        images = [
            f for f in os.listdir(KAGGLE_DATASET_PATH)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        if images:
            selected = st.selectbox("Select Image", images)
            image = cv2.imread(os.path.join(KAGGLE_DATASET_PATH, selected))
            st.image(image, channels="BGR")

            if st.button("Reconstruct Kolam"):
                thresh = preprocess_image(image)
                dots = detect_dots(thresh)
                loops = extract_loops(thresh)

                fig = draw_reconstructed_kolam(loops)
                st.pyplot(fig)

                export_kolam_svg(loops)
        else:
            st.warning("No images found")

# ==========================================================
# MODE 5: SAREE / FABRIC PRINT
# ==========================================================
elif mode == "🧵 Saree / Fabric Print Generator":

    st.subheader("Kolam-Based Saree / Textile Print Generator")

    n = st.slider("Base Kolam Dot Grid Size", 3, 9, 7)
    curvature = st.slider("Curve Smoothness", 0.1, 0.8, 0.4)

    layout_type = st.radio(
        "Select Saree Layout Type",
        ["Fabric Repeat Tile", "Saree Border + Pallu"]
    )

    palette = st.selectbox(
        "Textile Color Palette",
        list(TEXTILE_PALETTES.keys())
    )

    if layout_type == "Fabric Repeat Tile":
        rows = st.slider("Vertical Repeats", 3, 10, 5)
        cols = st.slider("Horizontal Repeats", 4, 12, 8)

    if st.button("Generate Saree Design"):
        dots, curves = generate_advanced_pulli_kolam(n, curvature)

        if layout_type == "Fabric Repeat Tile":
            tiled_curves = generate_saree_print(curves, rows, cols)
            fig = draw_saree_print(
                tiled_curves,
                color=TEXTILE_PALETTES[palette]
            )
            st.pyplot(fig)
        else:
            fig = draw_saree_border_pallu_streamlit(curves)
            st.pyplot(fig)

# ==========================================================
# MODE 6: AI-GENERATED KOLAMS (VAE)
# ==========================================================
elif mode == "🧠 AI Kolam Generator (VAE)":

    st.subheader("🤖 AI-Generated Kolam Designs")

    symmetry = st.selectbox(
        "Select Symmetry",
        ["None", "Horizontal", "Vertical", "Radial"]
    )

    binary = st.checkbox("Binary Kolam (Pulli Style)", value=False)

    if st.button("Generate New Kolam"):
        image = generate_symmetric_kolam(
            symmetry=symmetry.lower(),
            binary=binary
        )

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(image, cmap="gray")
        ax.axis("off")
        ax.set_title("AI-Generated Kolam")

        st.pyplot(fig)
