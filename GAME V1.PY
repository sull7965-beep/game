import pygame
import sys
import random
import numpy as np

# MEMBUAT MUSIC BACKGROUND
def create_background_track():
    sample_rate = 44100
    # Pola nada (frekuensi: C4, E4, G4, A4)
    notes = [261.63, 329.63, 392.00, 440.00]
    full_wave = np.array([], dtype=np.int16)
    
    for freq in notes:
        duration = 0.5  # tiap nada setengah detik
        n_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        # Membuat gelombang dengan volume lebih pelan (0.3) agar tidak berisik
        wave = (np.sin(2 * np.pi * freq * t) * 10000).astype(np.int16)
        full_wave = np.concatenate((full_wave, wave))
    
    wave_stereo = np.column_stack((full_wave, full_wave))
    return pygame.sndarray.make_sound(wave_stereo)

# --- 1. Struktur Tree (Node) ---
class GameNode:
    def __init__(self, x, y, color, width, height):
        self.position = pygame.Vector2(x, y)
        self.color = color
        self.size = (width, height)
        self.angle = 0
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    # Mendapatkan Rect untuk deteksi tabrakan
    def get_rect(self, parent_pos):
        abs_pos = parent_pos + self.position
        return pygame.Rect(abs_pos.x, abs_pos.y, self.size[0], self.size[1])

    def draw(self, surface, parent_pos):
        abs_pos = parent_pos + self.position
        
        # Membuat surface untuk objek agar bisa dirotasi
        obj_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        obj_surface.fill(self.color)
        
        # Proses rotasi
        rotated_surface = pygame.transform.rotate(obj_surface, self.angle)
        new_rect = rotated_surface.get_rect(center=(abs_pos.x + self.size[0]/2, abs_pos.y + self.size[1]/2))
        
        surface.blit(rotated_surface, new_rect.topleft)
        
        # Gambar semua anak (posisi relatif)
        for child in self.children:
            child.draw(surface, abs_pos)

# --- 2. Inisialisasi Game ---
pygame.init()
pygame.mixer.init() # PENTING: Harus ada agar suara aktif

# --- TARUH DI SINI (Membuat Objek) ---
bg_music = create_background_track()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("game dengan strukture tree")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 72, bold=True)

# --- 3. Pengaturan Objek ---
player = GameNode(400, 300, (0, 255, 0), 50, 50)
pedang = GameNode(50, 15, (0, 0, 255), 60, 15)
player.add_child(pedang)


enemies = []
def spawn_enemy():
    # Munculkan musuh di pinggir layar secara acak
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':    pos = (random.randint(0, WIDTH), -50)
    elif side == 'bottom': pos = (random.randint(0, WIDTH), HEIGHT + 50)
    elif side == 'left':   pos = (-50, random.randint(0, HEIGHT))
    else:                pos = (WIDTH + 50, random.randint(0, HEIGHT))
    
    enemies.append(GameNode(pos[0], pos[1], (255, 165, 0), 40, 40))

# Spawn awal 3 musuh
for _ in range(3):
    spawn_enemy()

# --- 4. Game Loop Utama ---
running = True
is_game_over = False

bg_music.play(loops=-1) # loops=-1 artinya musik akan mengulang terus

while running:
    screen.fill((30, 30, 30))
    
    # Input Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not is_game_over:

        
        # Kontrol Player
        keys = pygame.key.get_pressed()
        move_speed = 5
        if keys[pygame.K_LEFT]:  player.position.x -= move_speed
        if keys[pygame.K_RIGHT]: player.position.x += move_speed
        if keys[pygame.K_UP]:    player.position.y -= move_speed
        if keys[pygame.K_DOWN]:  player.position.y += move_speed


        # Batas Kiri: Player mentok di koordinat 0
        # Batas Kanan: Dikurangi lebar player (50) DAN panjang pedang (60) agar pedang tidak tembus
        player.position.x = max(0, min(player.position.x, WIDTH - player.size[0] - pedang.size[0]))
        
        # Batas Atas & Bawah: Mengikuti tinggi player karena pedang sejajar horizontal
        player.position.y = max(0, min(player.position.y, HEIGHT - player.size[1]))


        # Animasi Pedang (Rotasi)
        pedang.angle = 0
        
        # Ambil Rect untuk tabrakan
        player_rect = player.get_rect(pygame.Vector2(0,0))
        sword_rect = pedang.get_rect(player.position)

        # Logika Musuh
        for enemy in enemies[:]:
            # Musuh mengejar player
            direction = (player.position - enemy.position)
            if direction.length() > 0:
                enemy.position += direction.normalize() * 2


            # Batasi Musuh agar tidak keluar layar setelah masuk ke area permainan
            enemy.position.x = max(0, min(enemy.position.x, WIDTH - enemy.size[0]))
            enemy.position.y = max(0, min(enemy.position.y, HEIGHT - enemy.size[1]))

            
            enemy_rect = enemy.get_rect(pygame.Vector2(0,0))

            # Cek Tabrakan: Pedang vs Musuh
            if sword_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                spawn_enemy() # Spawn musuh baru saat satu mati

            # Cek Tabrakan: Musuh vs Player
            elif player_rect.colliderect(enemy_rect):
                is_game_over = True

        # Render Objek
        player.draw(screen, pygame.Vector2(0, 0))
        for enemy in enemies:
            enemy.draw(screen, pygame.Vector2(0, 0))
    
    else:
        # Tampilan jika Game Over
        msg = font.render("MAMPUSS", True, (255, 0, 0))
        screen.blit(msg, (WIDTH//2 - 180, HEIGHT//2 - 40))
        pygame.display.flip()
        
        # Jeda 3 detik sebelum menutup jendela
        pygame.time.delay(3000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()