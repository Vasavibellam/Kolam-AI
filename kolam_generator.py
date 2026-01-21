from backend.kolam_dots import generate_rhombic_dot_grid
from backend.kolam_rules import valid_move
from backend.kolam_curves import bezier_curve

def generate_advanced_pulli_kolam(n, curvature=0.4):
    dots = generate_rhombic_dot_grid(n)
    visited = set()
    curves = []

    for i in range(len(dots) - 1):
        p1 = dots[i]
        p2 = dots[i + 1]

        if valid_move(p1, p2, visited):
            curve = bezier_curve(p1, p2, curvature)
            curves.append(curve)
            visited.add((p1, p2))

    return dots, curves
