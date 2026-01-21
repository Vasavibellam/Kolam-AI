import matplotlib.pyplot as plt


def draw_kolam(dots, curves):
    fig, ax = plt.subplots(figsize=(6, 6))

    x, y = zip(*dots)
    ax.scatter(x, y, color="black")

    for curve in curves:
        xs, ys = zip(*curve)
        ax.plot(xs, ys, color="blue")

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Generated Pulli Kolam")

    return fig


def draw_reconstructed_kolam(loops):
    fig, ax = plt.subplots(figsize=(6, 6))

    for loop in loops:
        xs, ys = zip(*loop)
        ax.plot(xs, ys, color="blue")

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Reconstructed Kolam")

    return fig
