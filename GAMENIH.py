import pygame
import sys
import random
import math

# PLAYER DAN MUSUH TIDAK NGAMBANG LAGI
def draw_shadow(surface, pos, size):
    height_factor = max(0.5, 1 - abs(ground_y_offset) / 100)
    shadow = pygame.Surface(
    (int(size[0]*0.8 * height_factor), int(size[1]*0.25 * height_factor)),
    pygame.SRCALPHA
    )
    pygame.draw.ellipse(shadow, (0, 0, 0, 80), shadow.get_rect())
    
    shadow_pos = (
        pos.x + size[0]*0.1,
        pos.y + size[1] - (size[1] * 0.2)
    )
    
    surface.blit(shadow, shadow_pos)

# --- HEAL ITEM ------
class HealItem:
    def __init__(self, x, y, image):
        self.position = pygame.Vector2(x, y)
        self.size = (25, 25)
        self.image = image

    def get_rect(self):
        return pygame.Rect(self.position.x, self.position.y, self.size[0], self.size[1])

    def draw(self, surface):
        surface.blit(self.image, self.position)
        alpha = 128 + int(127 * math.sin(pygame.time.get_ticks() * 0.005))
        self.image.set_alpha(alpha)
    
# --- 1. Struktur Tree (Node) ---
class GameNode:
    def __init__(self, x, y, color, width, height, health=100, show_health=True, image=None):
        self.position = pygame.Vector2(x, y)
        self.color = color
        self.size = (width, height)
        self.image = image
        self.angle = 0
        self.children = []
        self.max_health = health
        self.health = health
        self.hit_timer = 0
        self.show_health = show_health
        self.stun_timer = 0

    def draw_health_bar(self, surface, parent_pos):
        abs_pos = parent_pos + self.position
        # 🔥 TAMBAHKAN INI
        draw_shadow(surface, abs_pos, self.size)
        
        bar_width = self.size[0]
        bar_height = 5

        health_ratio = 0 if self.max_health == 0 else max(0, self.health / self.max_health)
        
        # background merah
        pygame.draw.rect(surface, (255, 0, 0),
             (abs_pos.x, abs_pos.y - 10, bar_width, bar_height))
    
        # Health (hijau)
        pygame.draw.rect(surface, (0, 255, 0),
             (abs_pos.x, abs_pos.y - 10, bar_width * health_ratio, bar_height))

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_rect(self, parent_pos):
        abs_pos = parent_pos + self.position
        # Perbaikan bug ukuran Rect dari kode sebelumnya
        return pygame.Rect(abs_pos.x, abs_pos.y, self.size[0], self.size[1])

    def draw(self, surface, parent_pos):
        abs_pos = parent_pos + self.position

        if self.image:
            obj_surface = pygame.transform.scale(self.image, self.size)
        else:
            obj_surface = pygame.Surface(self.size, pygame.SRCALPHA)
            
            if self.stun_timer > 0:
                obj_surface.fill((100, 100, 255))  # biru saat stun
            else:
                obj_surface.fill(self.color)
        
        rotated_surface = pygame.transform.rotate(obj_surface, self.angle)
        new_rect = rotated_surface.get_rect(center=(abs_pos.x + self.size[0]/2, abs_pos.y + self.size[1]/2))
        
        surface.blit(rotated_surface, new_rect.topleft)

        # TAMBAHAN: gambar health bar
        if self.show_health:
            self.draw_health_bar(surface, parent_pos)
        
        for child in self.children:
            child.draw(surface, abs_pos)

# --- 2. Inisialisasi Game ---
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("sound.ogg")
pygame.mixer.music.set_volume(0.2)   # volume 0.0 - 1.0


levelup_sound = pygame.mixer.Sound("levelup.ogg")
gameover_sound = pygame.mixer.Sound("gameover.ogg")

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("SQUARE SURVIVOR")
clock = pygame.time.Clock()

font_title = pygame.font.SysFont("Arial", 60, bold=True)
font_menu = pygame.font.SysFont("Arial", 36, bold=True)
font_text = pygame.font.SysFont("Arial", 24)
font_gameover = pygame.font.SysFont("Arial", 72, bold=True)
font_name = pygame.font.SysFont("Arial", 17, bold=True)


game_state = "MENU"

# --- 3. Pengaturan ObjeK LATAR ---
background = pygame.image.load("latar.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

#---- MEMOTONG GAMBAR LASER -----
def cut_sprite(sheet, width, height):
    frames = []
    for i in range(sheet.get_width() // width):
        frame = sheet.subsurface((i * width, 0, width, height))
        frames.append(frame)
    return frames

laser_sheet = pygame.image.load("laser4.png").convert_alpha()
laser_frames = cut_sprite(laser_sheet, 400, 40)


#----- OBJEK UTAMA PLAYER DLL------
heal_image = pygame.image.load("heal.png").convert_alpha()
heal_image = pygame.transform.scale(heal_image, (25, 25))
player_down = pygame.image.load("player.png").convert_alpha()
player_up = pygame.image.load("hero_up.png").convert_alpha()
player_left = pygame.image.load("playerleft.png").convert_alpha()
player_right = pygame.image.load("playerright.png").convert_alpha()
player = pygame.transform.scale(player_down, (60, 60))
player = GameNode(400, 300, None, 60, 60, health=50, image=player_down)
enemy_img = pygame.image.load("enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (50, 50))



# Default awal pedang berada di sebelah kanan
pedang_image = pygame.image.load("pedang2.png").convert_alpha()
pedang_image.set_colorkey((0, 0, 0))
pedang_image = pygame.transform.scale(pedang_image, (70, 40))
pedang = GameNode(50, 20, None, 70, 40, show_health=False, image = pedang_image)
player.add_child(pedang)

# --- LASER SYSTEM ---
laser_ready = True
laser_cooldown = 0
laser_max_cooldown = 600

laser_active = False
laser_duration = 60

laser_frames = [
    pygame.image.load("laser1.png").convert_alpha(),
    pygame.image.load("laser2.png").convert_alpha(),
    pygame.image.load("laser3.png").convert_alpha(),
    pygame.image.load("laser4.png").convert_alpha()
]

# resize semua
laser_frames = [pygame.transform.scale(img, (500, 40)) for img in laser_frames]

laser_frame_index = 0
laser_anim_speed = 0.5

MAX_ENEMIES = 10
enemies = [] 
heal_items = []   
def spawn_enemy():

    side = random.choice(['left', 'right'])

    y = HEIGHT // 2

    if side == 'left':
        x = -50
    else:
        x = WIDTH + 50

    enemy_img = pygame.image.load("enemy.png").convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (50, 50))
    health = random.choice([50, 75])

    enemies.append(GameNode(x, y, None, 50, 50, health=health, image=enemy_img))

for _ in range(3):
    if len(enemies) < MAX_ENEMIES:
     spawn_enemy()

MAX_HEAL_ITEMS = 3 #heal item munculmax 3

def spawn_heal():   #memunculkan heal item
    if len(heal_items) >= MAX_HEAL_ITEMS:
       return

    side = random.choice(['left', 'right'])

    y = HEIGHT // 1.2

    if side == 'left':
        x = -30
    else:
        x = WIDTH + 30
  
    heal_items.append(HealItem(x, y, heal_image))

running = True
is_game_over = False
score = 0
display_score = 0  # TAMBAHAN
level = 1
prev_level = 1
level_up_timer = 0
is_level_up = False
level_up_delay = 0
level_up_text_scale = 1.0
level_up_alpha = 255
enemy_spawn_timer = 0
enemy_spawn_delay = 120  + level * 10 # makin besar = makin lama
gameover_played = False


# --- JUMP SYSTEM ---
is_jumping = False
jump_velocity = 0
gravity = 0.7
jump_power = -18
ground_y_offset = 0  # untuk efek naik turun



while running: 
    screen.blit(background, (0, 0))

        # 🔥 OVERLAY GELAP
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(80)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

            # 🔥 TAMBAHKAN DI SINI
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               running = False

    # ==================== STATUS 1: HALAMAN MENU UTAMA ====================
    if game_state == "MENU":
        title_text = font_title.render("SQUARE SURVIVOR", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        
        btn_start_rect = pygame.Rect(WIDTH // 2 - 150, 250, 300, 50)
        start_color = (0, 200, 0) if btn_start_rect.collidepoint(mouse_pos) else (0, 150, 0)
        pygame.draw.rect(screen, start_color, btn_start_rect, border_radius=10)
        
        start_text = font_menu.render("START GAME", True, (255, 255, 255))
        screen.blit(start_text, (btn_start_rect.centerx - start_text.get_width() // 2, btn_start_rect.centery - start_text.get_height() // 2))

        btn_tuto_rect = pygame.Rect(WIDTH // 2 - 150, 330, 300, 50)
        tuto_color = (200, 150, 0) if btn_tuto_rect.collidepoint(mouse_pos) else (150, 100, 0)
        pygame.draw.rect(screen, tuto_color, btn_tuto_rect, border_radius=10)
        
        tuto_text = font_menu.render("TUTORIAL", True, (255, 255, 255))
        screen.blit(tuto_text, (btn_tuto_rect.centerx - tuto_text.get_width() // 2, btn_tuto_rect.centery - tuto_text.get_height() // 2))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_start_rect.collidepoint(mouse_pos):
                   
                   game_state = "GAMEPLAY"
                   pygame.mixer.music.play(-1)
                elif btn_tuto_rect.collidepoint(mouse_pos):
                    game_state = "TUTORIAL"

    # ==================== STATUS 2: HALAMAN TUTORIAL ====================
    elif game_state == "TUTORIAL":
        tuto_title = font_title.render("CARA BERMAIN", True, (255, 255, 255))
        screen.blit(tuto_title, (WIDTH // 2 - tuto_title.get_width() // 2, 80))
        
        lines = [
            "1. Gunakan TOMBOL PANAH untuk bergerak (Kotak Hijau).",
            "2. Objek biru ialah pedang.",
            "3. Objek orange adalah musuh"
        ]
        
        for i, line in enumerate(lines):
            line_surface = font_text.render(line, True, (200, 200, 200))
            screen.blit(line_surface, (100, 220 + (i * 40)))
            
        btn_back_rect = pygame.Rect(WIDTH // 2 - 150, 450, 300, 50)
        back_color = (200, 50, 50) if btn_back_rect.collidepoint(mouse_pos) else (150, 30, 30)
        pygame.draw.rect(screen, back_color, btn_back_rect, border_radius=10)
        
        back_text = font_menu.render("KEMBALI", True, (255, 255, 255))
        screen.blit(back_text, (btn_back_rect.centerx - back_text.get_width() // 2, btn_back_rect.centery - back_text.get_height() // 2))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_back_rect.collidepoint(mouse_pos):
                    game_state = "MENU"

#===========GAMEPLAY================
    elif game_state == "GAMEPLAY":

     if not is_game_over:

        # --- LEVEL SYSTEM ---
        prev_level = level
        level = score // 120 + 1

        if level > prev_level:
            is_level_up = True
            level_up_timer = 120 
            level_up_delay = 240
            level_up_text_scale = 3.0   # mulai besar
            level_up_alpha = 255        # full terang
            enemies.clear()
            levelup_sound.play()

        # --- LEVEL PAUSE ---
        if is_level_up:
            level_up_delay -= 1
                # --- ANIMASI TEXT ---
            level_up_timer -= 1

            if level_up_text_scale > 1.0:
               level_up_text_scale -= 0.012  # mengecil perlahan

               level_up_alpha -= 1.5  # fade out

            if level_up_timer <= 0:
               level_up_alpha = 0

            if level_up_delay <= 0:
                is_level_up = False
                for _ in range(3 + level):
                    if len(enemies) < MAX_ENEMIES:
                        spawn_enemy()
        #---- MOVE ------
        # --- CONTROL ---
        keys = pygame.key.get_pressed()
        move_speed = 5


        # TEKAN F UNTUK LASER
        if keys[pygame.K_f] and laser_ready:
           laser_active = True
           laser_ready = False
           laser_cooldown = laser_max_cooldown
           laser_duration = 60

        # COOLDOWN LASER
        if not laser_ready:
           laser_cooldown -= 1
           if laser_cooldown <= 0:
              laser_ready = True 

        # --- JUMP CONTROL ---
        if keys[pygame.K_SPACE] and not is_jumping:
           is_jumping = True
           jump_velocity = jump_power

       # ===== PEDANG FIX HORIZONTAL =====
        if keys[pygame.K_RIGHT]:
            player.position.x += move_speed
            pedang.position = pygame.Vector2(50, 15)
            pedang.angle = 0   # lurus ke kanan

        if keys[pygame.K_LEFT]:
            player.position.x -= move_speed
            pedang.position = pygame.Vector2(-60, 15)
            pedang.angle = 180  # lurus ke kiri

        
        # --- JUMP PHYSICS ---
        if is_jumping:
           ground_y_offset += jump_velocity
           jump_velocity += gravity

           if ground_y_offset >= 0:
              ground_y_offset = 0
              is_jumping = False


         # --- BATAS MAP ---
        player.position.x = max(0, min(player.position.x, WIDTH - player.size[0]))

        # 🔥 KUNCI Y (WAJIB DI BAWAH)
        player.position.y = HEIGHT // 1.2 + ground_y_offset

        player_rect = player.get_rect(pygame.Vector2(0, 0))
        sword_rect = pedang.get_rect(player.position)

        # --- HIT TIMER ---
        if player.hit_timer > 0:
            player.hit_timer -= 1
        
        # --- SPAWN TIMER ---
        enemy_spawn_timer -= 1

        if enemy_spawn_timer <= 0:
            if len(enemies) < MAX_ENEMIES:
              spawn_enemy()
 
            enemy_spawn_timer = enemy_spawn_delay
  
        # --- HEAL ---
        for item in heal_items[:]:
            if player_rect.colliderect(item.get_rect()):
               player.health = min(player.max_health, player.health + 20)
               heal_items.remove(item)
        #------ LOGIKA LASER BUNUH MUSUH----

        if laser_active:
           laser_duration -= 1

               # ✅ ANIMASI DI SINI
           laser_frame_index += laser_anim_speed
           if laser_frame_index >= len(laser_frames):
              laser_frame_index = 0

           if pedang.angle == 0:  # kanan
                laser_rect = pygame.Rect(
                   player.position.x + 60,
                   player.position.y + 10,
                    400,
                    30
                )
           else:  # kiri
                laser_rect = pygame.Rect(
                   player.position.x - 400,
                   player.position.y + 10,
                    400,
                    30
                )

           for enemy in enemies[:]:
               if laser_rect.colliderect(enemy.get_rect(pygame.Vector2(0,0))):
                  enemies.remove(enemy)
                  score += 10

           if laser_duration <= 0:
              laser_active = False


        # --- ENEMY ---
        for enemy in enemies[:]:
            if enemy.stun_timer > 0:
                enemy.stun_timer -= 1
            else:
                 # 🔥 KUNCI DI SINI (horizontal saja)
              enemy.position.y = HEIGHT // 1.2

              if enemy.position.x < player.position.x:
                 enemy.position.x += 2
              elif enemy.position.x > player.position.x:
                 enemy.position.x -= 2
            enemy_rect = enemy.get_rect(pygame.Vector2(0, 0))

            # kena pedang
            if sword_rect.colliderect(enemy_rect):
                enemy.health -= 25

                knock = (enemy.position - player.position)
                if knock.length() > 0:
                    enemy.position += knock.normalize() * 50

                enemy.stun_timer = 30

            # mati
            if enemy.health <= 0:
                enemies.remove(enemy)
                score += 10

                 # 🔥 TAMBAHKAN INI
                if random.random() < 0.1:  # 10% chance
                 spawn_heal()

            # kena player
            elif player_rect.colliderect(enemy_rect):
                if player.hit_timer <= 0:
                    player.health -= 10
                    player.hit_timer = 30

                    if player.health <= 0 and not gameover_played:
                     is_game_over = True
                     gameover_sound.play()
                     gameover_played = True

        # --- SCORE ANIMATION ---
        if display_score < score:
            display_score += 1

        # --- RENDER ---
        player.draw(screen, pygame.Vector2(0, 0))

        # GAMBAR LASER
        if laser_active:
           current_laser = laser_frames[int(laser_frame_index)]

           if pedang.angle == 0:
              screen.blit(current_laser, (player.position.x + 60, player.position.y + 10))
           else:
              flipped = pygame.transform.flip(current_laser, True, False)
              screen.blit(flipped, (player.position.x - 400, player.position.y + 10))


        # --- NAMA PLAYER ---
        player_name = font_name.render("SULE", True, (255, 255, 255))
        screen.blit(player_name, (
            player.position.x + player.size[0]//2 - player_name.get_width()//2,
            player.position.y - 30
        ))

        for enemy in enemies:
            enemy.draw(screen, pygame.Vector2(0, 0))

             # --- NAMA MUSUH ---
            enemy_name = font_name.render("HUGO", True, (255, 100, 100))
            screen.blit(enemy_name, (
                enemy.position.x + enemy.size[0]//2 - enemy_name.get_width()//2,
                enemy.position.y - 30
            ))

        for item in heal_items:
      # 🔥 gerak ke arah player (horizontal saja)
           if item.position.x < player.position.x:
              item.position.x += 1
           elif item.position.x > player.position.x:
               item.position.x -= 1

           item.draw(screen)

        # UI
        hp_ratio = player.health / player.max_health
        pygame.draw.rect(screen, (255, 0, 0), (10, 40, 200, 20))
        pygame.draw.rect(screen, (0, 255, 0), (10, 40, 200 * hp_ratio, 20))

        screen.blit(font_text.render(f"HP: {player.health}", True, (255,255,255)), (10, 65))
        screen.blit(font_text.render(f"POINT: {display_score}", True, (255,255,255)), (10, 90))
        screen.blit(font_text.render(f"LEVEL: {level}", True, (255,255,0)), (10, 120))

        # --- LASER BAR ---
        bar_x, bar_y = 10, 150
        bar_width, bar_height = 200, 15

        pygame.draw.rect(screen, (100,100,100), (bar_x, bar_y, bar_width, bar_height))

        if laser_ready:
           charge_ratio = 1
        else:
           charge_ratio = 1 - (laser_cooldown / laser_max_cooldown)

        pygame.draw.rect(screen, (0, 200, 255),
                        (bar_x, bar_y, bar_width * charge_ratio, bar_height))

        screen.blit(font_text.render("LASER", True, (255,255,255)), (10, 170))


        # --- DRAW LEVEL UP TEXT ---
        if is_level_up and level_up_alpha > 0:
           text = font_title.render("LEVEL UP!", True, (255, 255, 0))
    
          # scale
           scaled_size = (
               int(text.get_width() * level_up_text_scale),
               int(text.get_height() * level_up_text_scale)
           )
           text = pygame.transform.scale(text, scaled_size)

          # transparency
           text.set_alpha(level_up_alpha)

           screen.blit(
               text,
               (WIDTH//2 - text.get_width()//2,
               HEIGHT//2 - text.get_height()//2)
           )
     else:
              # --- GAME OVER SCREEN ---
         pygame.mixer.music.stop()

         msg = font_gameover.render("GAME OVER!", True, (255, 0, 0))
         screen.blit(msg, (WIDTH//2 - 180, HEIGHT//2 - 100))

         final_score = font_menu.render(f"POINT: {score}", True, (255, 255, 255))
         screen.blit(final_score, (WIDTH//2 - 80, HEIGHT//2 - 20))

         # --- BUTTON RESTART ---
         btn_restart = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 50, 300, 50)
         color_restart = (0, 200, 0) if btn_restart.collidepoint(mouse_pos) else (0, 150, 0)
         pygame.draw.rect(screen, color_restart, btn_restart, border_radius=10)

         text_restart = font_menu.render("RESTART", True, (255,255,255))
         screen.blit(text_restart, (
             btn_restart.centerx - text_restart.get_width()//2,
             btn_restart.centery - text_restart.get_height()//2
         ))

         # --- BUTTON MENU ---
         btn_menu = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 120, 300, 50)
         color_menu = (200, 50, 50) if btn_menu.collidepoint(mouse_pos) else (150, 30, 30)
         pygame.draw.rect(screen, color_menu, btn_menu, border_radius=10)

         text_menu = font_menu.render("MENU", True, (255,255,255))
         screen.blit(text_menu, (
             btn_menu.centerx - text_menu.get_width()//2,
             btn_menu.centery - text_menu.get_height()//2
         ))

         # --- CLICK EVENT ---
         for event in events:
              if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
                  if btn_restart.collidepoint(mouse_pos):
                     is_game_over = False
                     player.health = player.max_health
                     player.position = pygame.Vector2(400, 300)

                     enemies.clear()
                     heal_items.clear()

                     score = 0
                     display_score = 0
                     level = 1
                     gameover_played = False

                     for _ in range(5):
                        spawn_enemy()

                     pygame.mixer.music.play(-1)

                  elif btn_menu.collidepoint(mouse_pos):
                     is_game_over = False
                     game_state = "MENU"

                     enemies.clear()
                     heal_items.clear()

                     score = 0
                     display_score = 0
                     level = 1
                     gameover_played = False
         
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()

