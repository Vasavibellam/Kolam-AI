import os
import csv
import matplotlib.pyplot as plt

from backend.kolam_generator import generate_advanced_pulli_kolam
from backend.kolam_visualization import draw_kolam
from backend.kolam_symmetry import classify_kolam_symmetry


def generate_kolam_dataset(
    output_dir="ml_dataset",
    samples=1000
):
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, "labels.csv")

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "filename",
            "n",
            "curvature",
            "symmetry_label"
        ])

        for i in range(samples):
            n = int(3 + i % 6)       # 3–8
            curvature = 0.2 + (i % 6) * 0.1

            dots, curves = generate_advanced_pulli_kolam(n, curvature)

            fig = draw_kolam(dots, curves)
            filename = f"kolam_{i}.png"
            fig.savefig(os.path.join(output_dir, filename))
            plt.close(fig)

            symmetry = classify_kolam_symmetry(dots)

            writer.writerow([
                filename,
                n,
                curvature,
                symmetry["ml_label"]
            ])
