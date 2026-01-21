import numpy as np

def classify_kolam_symmetry(dots):
    """
    Robust symmetry classifier
    Handles malformed / 1D dot inputs safely
    """

    # ----------------------------
    # SAFETY CHECK
    # ----------------------------
    if len(dots) == 0:
        return {"symmetry_type": "Unknown", "reason": "No dots detected"}

    # Ensure (N,2) format
    try:
        dots = np.array(dots, dtype=float)
        if dots.ndim != 2 or dots.shape[1] != 2:
            raise ValueError
    except Exception:
        return {
            "symmetry_type": "Invalid Input",
            "reason": "Dots must be (x, y) coordinates",
            "raw_dots": str(dots)
        }

    # ----------------------------
    # CENTERING
    # ----------------------------
    centroid = np.mean(dots, axis=0)
    centered = dots - centroid

    # ----------------------------
    # SYMMETRY TESTS
    # ----------------------------
    reflected = centered.copy()
    reflected[:, 0] *= -1     # Vertical reflection

    rotated = -centered       # 180° rotation

    reflection_match = _match_points(centered, reflected)
    rotation_match = _match_points(centered, rotated)

    if reflection_match and rotation_match:
        symmetry = "Rotational + Reflection Symmetry"
    elif reflection_match:
        symmetry = "Reflection Symmetry"
    elif rotation_match:
        symmetry = "Rotational Symmetry"
    else:
        symmetry = "Asymmetric"

    return {
        "symmetry_type": symmetry,
        "num_dots": len(dots),
        "centroid": centroid.tolist(),
        "ml_label": symmetry.replace(" ", "_").lower()
    }


def _match_points(a, b, tol=0.25):
    for p in a:
        if not np.any(np.linalg.norm(b - p, axis=1) < tol):
            return False
    return True
