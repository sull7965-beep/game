import numpy as np
from scipy.stats import norm

# =========================
# DATA
# =========================
mean_pretest = 55.0
mean_posttest = 70.0

n = 40
sigma = 8
alpha = 0.05

# =========================
# RATA-RATA KENAIKAN
# =========================
mean_diff = mean_posttest - mean_pretest
print("Rata-rata kenaikan:", mean_diff)

# =========================
# Z-TEST
# =========================
z = (mean_diff - 0) / (sigma / np.sqrt(n))
print("Z hitung:", round(z, 2))

# =========================
# P-VALUE
# =========================
p_value = 2 * (1 - norm.cdf(abs(z)))
print("P-value:", p_value)

# =========================
# KEPUTUSAN
# =========================
if p_value < alpha:
    print("Keputusan: TOLAK H0")
else:
    print("Keputusan: GAGAL TOLAK H0")