import matplotlib.pyplot as plt
from kolam_rules import generate_dot_grid, diagonal_connections
from kolam_symmetry import apply_symmetry

def dot_kolam(n, symmetry):
    points = generate_dot_grid(n)
    points = apply_symmetry(points, symmetry)

    fig, ax = plt.subplots()
    for x, y in points:
        ax.plot(x, y, 'ko')

    ax.set_aspect('equal')
    ax.axis('off')
    return fig


def line_kolam(n, symmetry):
    points = generate_dot_grid(n)
    lines = diagonal_connections(points)

    fig, ax = plt.subplots()
    for (x1, y1), (x2, y2) in lines:
        ax.plot([x1, x2], [y1, y2], 'k')

    ax.set_aspect('equal')
    ax.axis('off')
    return fig


def loop_kolam(n, symmetry):
    points = generate_dot_grid(n)
    points = apply_symmetry(points, symmetry)

    fig, ax = plt.subplots()
    for x, y in points:
        circle = plt.Circle((x, y), 0.4, fill=False)
        ax.add_patch(circle)

    ax.set_aspect('equal')
    ax.axis('off')
    return fig
