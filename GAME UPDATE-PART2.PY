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

# Membuat Objek Musik
bg_music = create_background_track()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game dengan Struktur Tree & Menu")
clock = pygame.time.Clock()

# Inisialisasi berbagai jenis font dan ukuran
font_title = pygame.font.SysFont("Arial", 60, bold=True)
font_menu = pygame.font.SysFont("Arial", 36, bold=True)
font_text = pygame.font.SysFont("Arial", 24)
font_gameover = pygame.font.SysFont("Arial", 72, bold=True)

# --- STATUS GAME (GAME STATE) ---
# Kondisi awal diset ke halaman MENU utama
game_state = "MENU"

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

# Jalankan musik latar belakang secara looping sejak game dibuka
bg_music.play(loops=-1)

while running:
    screen.fill((30, 30, 30))
    mouse_pos = pygame.mouse.get_pos()
    
    # Kumpulan event input dari user
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # ==================== STATUS 1: HALAMAN MENU UTAMA ====================
    if game_state == "MENU":
        # Judul Game
        title_text = font_title.render("SQUARE SURVIVOR", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        
        # Tombol "START GAME"
        btn_start_rect = pygame.Rect(WIDTH // 2 - 150, 250, 300, 50)
        start_color = (0, 200, 0) if btn_start_rect.collidepoint(mouse_pos) else (0, 150, 0)
        pygame.draw.rect(screen, start_color, btn_start_rect, border_radius=10)
        
        start_text = font_menu.render("START GAME", True, (255, 255, 255))
        screen.blit(start_text, (btn_start_rect.centerx - start_text.get_width() // 2, btn_start_rect.centery - start_text.get_height() // 2))

        # Tombol "TUTORIAL"
        btn_tuto_rect = pygame.Rect(WIDTH // 2 - 150, 330, 300, 50)
        tuto_color = (200, 150, 0) if btn_tuto_rect.collidepoint(mouse_pos) else (150, 100, 0)
        pygame.draw.rect(screen, tuto_color, btn_tuto_rect, border_radius=10)
        
        tuto_text = font_menu.render("TUTORIAL", True, (255, 255, 255))
        screen.blit(tuto_text, (btn_tuto_rect.centerx - tuto_text.get_width() // 2, btn_tuto_rect.centery - tuto_text.get_height() // 2))

        # Logika Deteksi Klik pada Tombol Menu
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_start_rect.collidepoint(mouse_pos):
                    game_state = "GAMEPLAY"
                elif btn_tuto_rect.collidepoint(mouse_pos):
                    game_state = "TUTORIAL"

    # ==================== STATUS 2: HALAMAN TUTORIAL ====================
    elif game_state == "TUTORIAL":
        # Judul Halaman
        tuto_title = font_title.render("CARA BERMAIN", True, (255, 255, 255))
        screen.blit(tuto_title, (WIDTH // 2 - tuto_title.get_width() // 2, 80))
        
        # Teks Panduan Bermain
        lines = [
            "1. Gunakan TOMBOL PANAH untuk menggerakkan Player.",
            "2. Tabrak musuh dengan PEDANG untuk membunuh mereka.",
            "3. Jangan biarkan PLAYER menyentuh musuh, atau Anda kalah!"
        ]
        
        for i, line in enumerate(lines):
            line_surface = font_text.render(line, True, (200, 200, 200))
            screen.blit(line_surface, (100, 220 + (i * 40)))
            
        # Tombol "KEMBALI KE MENU"
        btn_back_rect = pygame.Rect(WIDTH // 2 - 150, 450, 300, 50)
        back_color = (200, 50, 50) if btn_back_rect.collidepoint(mouse_pos) else (150, 30, 30)
        pygame.draw.rect(screen, back_color, btn_back_rect, border_radius=10)
        
        back_text = font_menu.render("KEMBALI", True, (255, 255, 255))
        screen.blit(back_text, (btn_back_rect.centerx - back_text.get_width() // 2, btn_back_rect.centery - back_text.get_height() // 2))

        # Logika Deteksi Klik Kembali
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_back_rect.collidepoint(mouse_pos):
                    game_state = "MENU"

    # ==================== STATUS 3: HALAMAN GAMEPLAY ====================
    elif game_state == "GAMEPLAY":
        if not is_game_over:
            # Kontrol Player
            keys = pygame.key.get_pressed()
            move_speed = 5

            #-- LOGIKA GERAKAN UBAH ARAH PEDANG --
        
            if keys[pygame.K_LEFT]:
                player.position.x -= move_speed
                # UBAH UKURAN DAN POSISI PEDANG RELATIF KE KIRI player
                pedang.size = (60, 15)
                pedang.position = pygame.Vektor2(-60, 15)
            elif keys[pygame.K_RIGHT]:
                player.position.x += move_speed
                #ubah ukuran & posisi pedsng relatif ke kanan player
                pedang.size = (60, 15)
                pedang.position = pygame.Vektor2(50, 15)
            elif keys[pygame.K_UP]:
                player.position.y -= move_speed
                #ubah ukuran & posisi pedang relatif ke atas player (dibalik lebar jadi tinggi)
                pedang.size = (15, 60)
                pedang.position = pygame.Vektor2(15, -60)
            elif keys[pygame.K_DOWN]:
                player.position.y += move_speed
                #ubah ukuran & posisi pedang relatif ke bawah player
                pedang.size = (15, 60)
                pedang.position = pygame.Vektor2(15, 50)
                #--- BARU: PEMBATAN LAYAR DINAMIS (MENGIKUTI UJUNG PEDANG) ---
                #Cari posisi minimal dan maksimal unjung pedang yang valid
                min_x = max(0, -pedang.position.x)
                max_x = WIDTH - player.size[0] - max(0, pedang.position.x + pedang.size[0])
                min_y = max(0, -pedang.position.y)
                max_y = HEIGHT - player.size[1] - max(0, pedang.position.y + pedang.size[1])

               # Mengunci posisi player berdasarkan batasan dinamis di atas
                player.position.x = max(min_x, min(player.position.x, max_x))
                player.position.y = max(min_y, min(player.position.y, max_y))

            # Mengunci sudut pedang agar tidak berputar
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

            # Render Objek Permainan
            player.draw(screen, pygame.Vector2(0, 0))
            for enemy in enemies:
                enemy.draw(screen, pygame.Vector2(0, 0))
        
        else:
            # Menghentikan musik saat kalah
            bg_music.stop()
            
            # Tampilan jika Game Over
            msg = font_gameover.render("MAMPUSS", True, (255, 0, 0))
            screen.blit(msg, (WIDTH//2 - 180, HEIGHT//2 - 40))
            pygame.display.flip()
            
            # Jeda 3 detik sebelum menutup jendela
            pygame.time.delay(3000)
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
