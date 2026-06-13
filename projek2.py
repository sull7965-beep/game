import pygame
import sys
import random
import math

pygame.init()

# --- SETUP ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# --- WARNA ---
WHITE = (255,255,255)
RED = (200,50,50)
GREEN = (50,200,50)
BLUE = (50,100,255)
BLACK = (20,20,20)
YELLOW = (255,255,0)

# --- PLAYER ---
class Player:
    def __init__(self):
        self.rect = pygame.Rect(400, 300, 40, 40)
        self.speed = 5
        self.hp = 100

    def move(self, keys):
        if keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_s]: self.rect.y += self.speed
        if keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_d]: self.rect.x += self.speed

        self.rect.clamp_ip(screen.get_rect())

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

# --- BULLET ---
class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.pos = pygame.Vector2(x, y)
        direction = pygame.Vector2(target_x - x, target_y - y)
        if direction.length() != 0:
            direction = direction.normalize()
        self.velocity = direction * 10
        self.radius = 5

    def update(self):
        self.pos += self.velocity

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.pos.x), int(self.pos.y)), self.radius)

    def offscreen(self):
        return not (0 <= self.pos.x <= WIDTH and 0 <= self.pos.y <= HEIGHT)

# --- ENEMY ---
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH), random.randint(0, HEIGHT), 30, 30)
        self.speed = random.uniform(1.5, 2.5)

    def move_towards(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, math.hypot(dx, dy))
        self.rect.x += dx/dist * self.speed
        self.rect.y += dy/dist * self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

# --- GAME OBJECTS ---
player = Player()
bullets = []
enemies = []

score = 0
spawn_timer = 0

# --- MAIN LOOP ---
running = True
while running:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    # --- EVENT ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # klik kiri
                bullets.append(Bullet(player.rect.centerx, player.rect.centery, mouse_pos[0], mouse_pos[1]))

    # --- UPDATE ---
    player.move(keys)

    # Spawn enemy
    spawn_timer += 1
    if spawn_timer > 60:
        enemies.append(Enemy())
        spawn_timer = 0

    # Update bullets
    for bullet in bullets[:]:
        bullet.update()

        if bullet.offscreen():
            bullets.remove(bullet)

    # Update enemies
    for enemy in enemies[:]:
        enemy.move_towards(player)

        if enemy.rect.colliderect(player.rect):
            player.hp -= 1

    # Collision bullet vs enemy
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if enemy.rect.collidepoint(bullet.pos):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break

    # --- DRAW ---
    player.draw()

    for bullet in bullets:
        bullet.draw()

    for enemy in enemies:
        enemy.draw()

    # UI
    hp_text = font.render(f"HP: {player.hp}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)

    screen.blit(hp_text, (10,10))
    screen.blit(score_text, (10,40))

    # Game Over
    if player.hp <= 0:
        game_over = font.render("GAME OVER", True, RED)
        screen.blit(game_over, (WIDTH//2 - 80, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()