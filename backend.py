import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File

# ✅ ABSOLUTE IMPORTS (ONLY THESE)
from backend.kolam_generator import generate_sikku_kolam
from backend.kolam_analysis import analyze_kolam
from backend.kolam_image_analysis import (
    preprocess_image,
    detect_dots,
    extract_loops
)

app = FastAPI()

# -------------------------------------------------
# ROOT
# -------------------------------------------------
@app.get("/")
def home():
    return {"status": "Kolam backend running"}

# -------------------------------------------------
# RULE-BASED KOLAM API
# -------------------------------------------------
@app.get("/generate")
def generate(grid: int = 5):
    dots, junctions = generate_sikku_kolam(grid)
    analysis = analyze_kolam(dots, junctions)

    return {
        "grid": grid,
        "dots": dots,
        "junctions": junctions,
        "analysis": analysis
    }

# -------------------------------------------------
# IMAGE-BASED KOLAM API
# -------------------------------------------------
@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    data = await file.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

    thresh = preprocess_image(img)
    dots = detect_dots(thresh)
    loops = extract_loops(thresh)

    return {
        "dot_count": len(dots),
        "loop_count": len(loops),
        "kolam_type": "Sikku" if len(loops) == 1 else "Pulli"
    }
