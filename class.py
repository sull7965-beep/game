import pygame
import sys
import random

# --- 1. Struktur Tree (Node) ---
class GameNode:
    # Mengubah urutan parameter agar mempermudah penggunaan warna/gambar pilihan
    def __init__(self, x, y, width, height, color=(255, 255, 255), image_path=None):
        self.position = pygame.Vector2(x, y)
        self.size = (width, height)
        self.color = color
        self.angle = 0
        self.children = []
        self.image = None
        
        if image_path:
            try:
                raw_image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(raw_image, self.size)
            except pygame.error:
                print(f"Gagal memuat gambar: {image_path}, menggunakan warna fallback.", file=sys.stderr)

    def add_child(self, child_node):
        self.children.append(child_node)

    # Mendapatkan Rect untuk deteksi tabrakan
    def get_rect(self, parent_pos):
        abs_pos = parent_pos + self.position
        return pygame.Rect(abs_pos.x, abs_pos.y, self.size[0], self.size[1])

    def draw(self, surface, parent_pos):
        abs_pos = parent_pos + self.position
        
        # Membuat surface transparan untuk objek agar bisa dirotasi
        obj_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        if self.image:
            # Menggambar asset gambar saja tanpa background warna kotak
            obj_surface.blit(self.image, (0, 0))
        else:
            # Menggunakan warna bawaan jika file gambar tidak ditemukan
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

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("game dengan struktur tree")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 72, bold=True)

STATE_MENU = "MENU"
STATE_GAME = "GAME"
current_state = STATE_MENU

# --- 3. Pengaturan Objek ---
# Pemanggilan objek disesuaikan dengan parameter (x, y, width, height, color, image_path)
player = GameNode(400, 300, 50, 50, image_path="player.png")
pedang = GameNode(50, 15, 60, 15, color=(0, 0, 255))
player.add_child(pedang)

enemies = []
def spawn_enemy():
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':    pos = (random.randint(0, WIDTH), -50)
    elif side == 'bottom': pos = (random.randint(0, WIDTH), HEIGHT + 50)
    elif side == 'left':   pos = (-50, random.randint(0, HEIGHT))
    else:                pos = (WIDTH + 50, random.randint(0, HEIGHT))
    
    enemies.append(GameNode(pos[0], pos[1], 40, 40, color=(255, 165, 0)))

# Spawn awal 3 musuh
for _ in range(3):
    spawn_enemy()

# --- 4. Game Loop Utama ---
running = True
is_game_over = False

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

        # Animasi Pedang (Rotasi dihapus sesuai instruksi sebelumnya)
        # Untuk mengubah arah pedang secara statis, gunakan pedang.angle = nilai_sudut diatur di luar loop
        
        # Ambil Rect untuk tabrakan
        player_rect = player.get_rect(pygame.Vector2(0,0))
        sword_rect = pedang.get_rect(player.position)

        # Logika Musuh
        for enemy in enemies[:]:
            # Musuh mengejar player
            direction = (player.position - enemy.position)
            if direction.length() > 0:
                enemy.position += direction.normalize() * 2
            
            enemy_rect = enemy.get_rect(pygame.Vector2(0,0))

            # Cek Tabrakan: Pedang vs Musuh
            if sword_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                spawn_enemy()

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
        
        pygame.time.delay(3000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
