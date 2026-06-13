import math
from scipy import stats

# 1. Input data yang diketahui
mean_pre = 35.5
mean_post = 42.2
n = 30         # Ukuran sampel (asumsi)
s_d = 10.0     # Standar deviasi selisih (asumsi)
alpha = 0.05   # Tingkat signifikansi

# 2. Hitung rata-rata selisih (D_bar) dan Standar Error (SE)
mean_diff = mean_post - mean_pre
standard_error = s_d / math.sqrt(n)

# 3. Hitung Z-hitung
z_score = mean_diff / standard_error

# 4. Hitung P-value (Uji dua arah)
# stats.norm.sf menghitung area di sebelah kanan nilai Z (survival function)
p_value = 2 * stats.norm.sf(abs(z_score))

# 5. Menentukan keputusan H0
keputusan = "DITOLAK" if p_value < alpha else "GAGAL DITOLAK"

# 6. Menampilkan Hasil Perhitungan
print("="*45)
print(" HASIL PERHITUNGAN Z-TEST DATA BERPASANGAN")
print("="*45)
print(f"Rata-rata Pre-test       : {mean_pre}")
print(f"Rata-rata Post-test      : {mean_post}")
print(f"Rata-rata Selisih (D)    : {mean_diff:.2f}")
print(f"Standar Error (SE)       : {standard_error:.4f}")
print(f"Nilai Z-hitung           : {z_score:.4f}")
print(f"Nilai P-value            : {p_value:.5f}")
print(f"Tingkat Signifikansi (α) : {alpha}")
print("-"*45)
print(f"Keputusan Statistik     : H0 {keputusan}")
print("="*45)
