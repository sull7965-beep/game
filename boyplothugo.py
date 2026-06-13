import matplotlib.pyplot as plt
import numpy as np

# 1. Menentukan parameter agar data simulasi sesuai dengan soal Anda
np.random.seed(42)  # Mengunci pola acak agar hasil selalu sama saat dijalankan
n_sampel = 30

# Simulasikan data Pre-test dengan rata-rata 35.5
pre_test = np.random.normal(loc=35.5, scale=8, size=n_sampel)
pre_test = pre_test - np.mean(pre_test) + 35.5  # Koreksi agar rata-rata eksak 35.5

# Simulasikan data selisih dengan rata-rata peningkatan 6.7 (42.2 - 35.5)
selisih = np.random.normal(loc=6.7, scale=5, size=n_sampel)
selisih = selisih - np.mean(selisih) + 6.7  # Koreksi rata-rata peningkatan

# Menghitung nilai Post-test (Pre-test + Peningkatan)
post_test = pre_test + selisih

# 2. Membuat Visualisasi Boxplot
plt.figure(figsize=(8, 6))

# Membuat grafik kotak (boxplot)
# Menggunakan tick_labels (versi matplotlib terbaru) untuk memberi nama kategori
data_grafik = [pre_test, post_test]
plt.boxplot(data_grafik, tick_labels=['Pre-test', 'Post-test'], patch_artist=True,
            boxprops=dict(facecolor='#D9E2EC', color='#102A43', linewidth=1.5),
            medianprops=dict(color='#BA2525', linewidth=2.5),
            whiskerprops=dict(color='#102A43', linewidth=1.5),
            capprops=dict(color='#102A43', linewidth=1.5))

# 3. Menambahkan Atribut Grafik (Judul dan Label)
plt.title('Perbandingan Distribusi Nilai Pre-test vs Post-test\n(Statistika Inferensial Data Berpasangan)', 
          fontsize=12, fontweight='bold', pad=15)
plt.ylabel('Skor / Nilai', fontsize=11, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.5)  # Menambahkan garis bantu horizontal

# 4. Menampilkan Hasil Grafik ke Layar
plt.tight_layout()
plt.show()
