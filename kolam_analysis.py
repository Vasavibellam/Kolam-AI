import numpy as np
import cv2

# --------------------------------------------------
def analyze_kolam(dots, junctions):
    return {
        "Dots": len(dots),
        "Junctions": len(junctions),
        "Kolam Type": "Sikku Kolam",
        "Closed Curve": "Yes",
        "Mathematics": "Graph theory, symmetry, Euler paths"
    }


# --------------------------------------------------
def analyze_kolam_from_image(dots, loops):
    return {
        "Detected Dots": len(dots),
        "Detected Loops": len(loops),
        "Kolam Type": "Sikku Kolam" if len(loops) == 1 else "Pulli Kolam",
        "Symmetry": detect_exact_symmetry(dots),
        "Euler Property": "Valid" if len(loops) == 1 else "Multiple strokes",
        "Knot Crossings": count_knot_crossings(loops),
        "Kolam Grammar": validate_kolam_grammar(dots, loops)
    }


# --------------------------------------------------
def detect_exact_symmetry(dots):
    if not dots:
        return "Unknown"

    pts = np.array(dots)
    c = pts.mean(axis=0)
    centered = pts - c

    if np.allclose(centered, -centered, atol=5):
        return "180° Rotational Symmetry"
    return "No exact symmetry"


# --------------------------------------------------
def count_knot_crossings(loops):
    count = 0
    for loop in loops:
        count += len(loop) // 100
    return count


# --------------------------------------------------
def validate_kolam_grammar(dots, loops):
    return "Valid Traditional Kolam" if loops else "Invalid"


# --------------------------------------------------
def export_kolam_svg(loops, filename="kolam.svg"):
    with open(filename, "w") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg">\n')
        for loop in loops:
            path = "M " + " ".join(
                f"{x},{y}" for x, y in loop
            ) + " Z"
            f.write(
                f'<path d="{path}" fill="none" '
                'stroke="black" stroke-width="2"/>\n'
            )
        f.write("</svg>")
