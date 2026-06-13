class Kopi:
    # __init__ bertugas mencatat pesanan Anda di awal
    def __init__(self, ukuran, rasa):
        self.ukuran = ukuran  # Mencatat ukuran kopi milik Anda
        self.rasa = rasa      # Mencatat rasa kopi milik Anda

# Saat Anda mengetik ini, __init__ langsung bekerja di belakang layar
kopi_saya = Kopi("Besar", "Hazelnut")

# Sekarang kopi Anda sudah punya identitas
print(kopi_saya.ukuran)  # Output: Hazelnut
