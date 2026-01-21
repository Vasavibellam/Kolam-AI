import cv2
import numpy as np

# ==================================================
# 1️⃣ PREPROCESS IMAGE
# ==================================================
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        15, 4
    )

    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

    return thresh


# ==================================================
# 2️⃣ DOT DETECTION
# ==================================================
def detect_dots(thresh):
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    dots = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 25 < area < 120:
            (x, y), r = cv2.minEnclosingCircle(cnt)
            if 3 < r < 7:
                dots.append((int(x), int(y)))

    return remove_duplicates(dots)


def remove_duplicates(points, min_dist=14):
    unique = []
    for p in points:
        if not any(np.linalg.norm(np.array(p) - np.array(q)) < min_dist for q in unique):
            unique.append(p)
    return unique


# ==================================================
# 3️⃣ LOOP EXTRACTION (FULL KOLAM)
# ==================================================
def extract_loops(thresh):
    contours, hierarchy = cv2.findContours(
        thresh,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_NONE
    )

    loops = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        length = len(cnt)

        if area < 300 or length < 150:
            continue

        contour = cnt.squeeze()
        if contour.ndim != 2:
            continue

        simplified = simplify_contour(contour)
        smoothed = adaptive_smooth(simplified)
        dense = densify_curve(smoothed)

        loops.append(dense)

    return loops


# ==================================================
# 4️⃣ CONTOUR SIMPLIFICATION
# ==================================================
def simplify_contour(contour, step=3):
    reduced = contour[::step]
    simplified = [reduced[0]]

    for i in range(1, len(reduced) - 1):
        p0, p1, p2 = reduced[i - 1], reduced[i], reduced[i + 1]
        v1, v2 = p1 - p0, p2 - p1
        angle = angle_between(v1, v2)

        if angle > 8:   # slightly relaxed
            simplified.append(p1)

    simplified.append(reduced[-1])
    return np.array(simplified)


# ==================================================
# 5️⃣ ANGLE COMPUTATION
# ==================================================
def angle_between(v1, v2):
    v1, v2 = v1.astype(float), v2.astype(float)
    n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
    if n1 == 0 or n2 == 0:
        return 0

    cos = np.dot(v1, v2) / (n1 * n2)
    cos = np.clip(cos, -1.0, 1.0)
    return np.degrees(np.arccos(cos))


# ==================================================
# 6️⃣ ADAPTIVE SMOOTHING (KOLAM-LIKE FLOW)
# ==================================================
def adaptive_smooth(points):
    points = points.astype(float)
    smoothed = points.copy()

    for i in range(1, len(points) - 1):
        curvature = angle_between(points[i] - points[i - 1],
                                  points[i + 1] - points[i])

        alpha = 0.15 if curvature < 20 else 0.25

        smoothed[i] = (
            alpha * points[i - 1]
            + (1 - 2 * alpha) * points[i]
            + alpha * points[i + 1]
        )

    return smoothed.astype(int)


# ==================================================
# 7️⃣ CURVE DENSIFICATION (SMOOTHER LOOK)
# ==================================================
def densify_curve(points):
    dense = []

    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        dense.append(p1)

        dist = np.linalg.norm(p2 - p1)
        if dist > 10:
            mid = ((p1 + p2) / 2).astype(int)
            dense.append(mid)

    dense.append(points[-1])

    return np.array(dense)
