def generate_rhombic_dot_grid(n, spacing=1.0):
    dots = []
    y = 0
    for i in range(1, n + 1):
        x_start = -(i - 1)
        for j in range(i):
            dots.append((x_start + 2*j, y))
        y += spacing

    for i in range(n - 1, 0, -1):
        x_start = -(i - 1)
        for j in range(i):
            dots.append((x_start + 2*j, y))
        y += spacing

    return dots
