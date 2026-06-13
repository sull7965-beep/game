import numpy as np
import matplotlib.pyplot as plt

# =========================
# DATA SIMULASI (konsisten dengan mean)
# =========================
pretest = np.array([
    52, 54, 55, 56, 57, 58, 55, 54, 56, 57,
    55, 53, 54, 56, 58, 59, 55, 54, 56, 57,
    55, 53, 54, 56, 58, 59, 55, 54, 56, 57
])

posttest = np.array([
    68, 69, 70, 71, 72, 73, 70, 69, 71, 72,
    70, 68, 69, 71, 73, 74, 70, 69, 71, 72,
    70, 68, 69, 71, 73, 74, 70, 69, 71, 72
])

# =========================
# BOXPLOT
# =========================
plt.figure(figsize=(8,5))

plt.boxplot([pretest, posttest],
            labels=["Pre-Test", "Post-Test"],
            patch_artist=True,
            boxprops=dict(facecolor="lightgreen"),
            medianprops=dict(color="red"))

plt.title("Boxplot Pre-Test vs Post-Test")
plt.ylabel("Nilai")
plt.grid(True, linestyle="--", alpha=0.5)

plt.show()  