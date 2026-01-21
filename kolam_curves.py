def bezier_curve(p1, p2, curvature=0.5):
    cx = (p1[0] + p2[0]) / 2
    cy = (p1[1] + p2[1]) / 2 + curvature
    return (p1, (cx, cy), p2)
