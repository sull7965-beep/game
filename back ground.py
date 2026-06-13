import pygame
import sys
import random

# 1. STRUKTUR DATA: DOUBLY LINKED LIST
class Node:
    def __init__(self, x_pos):
        self.x = x_pos
        self.next = None
        self.prev = None

class PosisiDLL:
    def __init__(self):
        n1 = Node(150)
        n2 = Node(400)
        n3 = Node(650)
        
        n1.next = n2
        n2.prev = n1
        n2.next = n3
        n3.prev = n2
        
        self.head = n1

# Inisialisasi Pygame
pygame.init()
pygame.mixer.init()

# Konstanta
LEBAR, TINGGI = 800, 600
KECEPATAN_PEMAIN = 7
KECEPATAN_APEL = 3

PUTIH = (255, 255, 255)
MERAH = (255, 0, 0)
BIRU = (0, 0, 255)

layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Game Tangkap Apel DLL")

# --- TAMBAHAN UNTUK BACKGROUND ---
try:
    bg_img = pygame.image.load("background.jpg") # Pastikan file ada di folder
    bg_img = pygame.transform.scale(bg_img, (LEBAR, TINGGI))
except:
    bg_img = None # Jika gambar tidak ada, tidak error
# ---------------------------------

# Inisialisasi DLL dan Posisi Awal
daftar_posisi = PosisiDLL()
node_sekarang = daftar_posisi.head.next

# Load Suara
try:
    suara_skor = pygame.mixer.Sound("suara.wav")
    suara_skor.set_volume(1.0)
except:
    suara_skor = None

jam = pygame.time.Clock()
huruf = pygame.font.SysFont(None, 36)

# Objek Game
pemain_rect = pygame.Rect(LEBAR//2 - 50, TINGGI - 50, 100, 20)
apel_rect = pygame.Rect(node_sekarang.x, -20, 20, 20)
skor = 0

def tampilkan_pesan(teks_pesan):
    gambar_teks = huruf.render(teks_pesan, True, PUTIH)
    kotak_teks = gambar_teks.get_rect(center=(LEBAR//2, TINGGI//2))
    layar.blit(gambar_teks, kotak_teks)
    pygame.display.flip()
    pygame.time.wait(2000)

berjalan = True
while berjalan:
    for kejadian in pygame.event.get():
        if kejadian.type == pygame.QUIT:
            berjalan = False
    
    tombol = pygame.key.get_pressed()
    if (tombol[pygame.K_LEFT] or tombol[pygame.K_a]) and pemain_rect.left > 0:
        pemain_rect.x -= KECEPATAN_PEMAIN
    if (tombol[pygame.K_RIGHT] or tombol[pygame.K_d]) and pemain_rect.right < LEBAR:
        pemain_rect.x += KECEPATAN_PEMAIN
        
    apel_rect.y += KECEPATAN_APEL
    
    if pemain_rect.colliderect(apel_rect):
        skor += 1
        if suara_skor: suara_skor.play()
        
        if random.choice([True, False]):
            if node_sekarang.next: node_sekarang = node_sekarang.next
            else: node_sekarang = node_sekarang.prev
        else:
            if node_sekarang.prev: node_sekarang = node_sekarang.prev
            else: node_sekarang = node_sekarang.next
            
        apel_rect.x = node_sekarang.x
        apel_rect.y = -20
        KECEPATAN_APEL += 0.2
        
    if apel_rect.top > TINGGI:
        tampilkan_pesan("GAME OVER!")
        berjalan = False
        
    # --- BAGIAN MENGGAMBAR ---
    if bg_img:
        layar.blit(bg_img, (0, 0)) # Gambar Background
    else:
        layar.fill(BIRU) # Warna cadangan jika gambar gagal load
        
    pygame.draw.rect(layar, PUTIH, pemain_rect)
    pygame.draw.rect(layar, MERAH, apel_rect)
    
    teks_skor = huruf.render(f"SKOR: {skor}", True, PUTIH)
    layar.blit(teks_skor, (10, 10))
    
    pygame.display.flip()
    jam.tick(60)

pygame.quit()
sys.exit()
