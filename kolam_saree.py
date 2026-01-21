import matplotlib.pyplot as plt

def generate_saree_print(curves, rows=5, cols=8, spacing=12):
    tiled_curves = []

    for r in range(rows):
        for c in range(cols):
            dx = c * spacing
            dy = r * spacing

            for curve in curves:
                shifted = [(x + dx, y + dy) for x, y in curve]
                tiled_curves.append(shifted)

    return tiled_curves


def draw_saree_print(tiled_curves, color="#1A237E"):
    fig, ax = plt.subplots(figsize=(8, 12))

    for curve in tiled_curves:
        xs, ys = zip(*curve)
        ax.plot(xs, ys, color=color, linewidth=1)

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Kolam-Based Saree Print")

    return fig
