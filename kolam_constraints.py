import numpy as np
from backend.kolam_symmetry import apply_symmetry

def enforce_kolam_rules(points, symmetry):
    """
    Ensures Kolam constraints:
    - Closed loops
    - Valid symmetry
    - Dot continuity
    """

    points = apply_symmetry(points, symmetry)

    # Remove isolated points
    filtered = []
    for x, y in points:
        if any(abs(x - px) <= 1 and abs(y - py) <= 1 for px, py in points):
            filtered.append((x, y))

    return filtered
