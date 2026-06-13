import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

# ================== SETUP ==================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SQUARE SURVIVOR")
clock = pygame.time.Clock()

# ================== LOAD ==================
background = pygame.transform.scale(pygame.image.load("latar.png"), (WIDTH, HEIGHT))
heal_image = pygame.transform.scale(pygame.image.load("heal.png").convert_alpha(), (25, 25))

player_left = pygame.image.load("playerleft.png").convert_alpha()
player_right = pygame.image.load("playerright.png").convert_alpha()

enemy_img = pygame.transform.scale(pygame.image.load("enemy.png").convert_alpha(), (50, 50))

pedang_image = pygame.transform.scale(pygame.image.load("pedang2.png").convert_alpha(), (70, 40))

# ================== CLASS ==================
class GameNode:
    def __init__(self, x, y, width, height, image, health=100):
        self.position = pygame.Vector2(x, y)
        self.size = (width, height)
        self.image = image
        self.health = health
        self.max_health = health

    def draw(self, surface):
        img = pygame.transform.scale(self.image, self.size)
        surface.blit(img, self.position)

    def get_rect(self):
        return pygame.Rect(self.position.x, self.position.y, self.size[0], self.size[1])


class HealItem:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)

    def draw(self, surface):
        surface.blit(heal_image, self.position)

    def get_rect(self):
        return pygame.Rect(self.position.x, self.position.y, 25, 25)

# ================== PLAYER ==================
player = GameNode(400, HEIGHT // 1.3, 60, 60, player_right, 50)

pedang = GameNode(0, 0, 70, 40, pedang_image, 0)

# ================== DATA ==================
enemies = []
heal_items = []

def spawn_enemy():
    side = random.choice(["left", "right"])
    x = -50 if side == "left" else WIDTH + 50
    y = HEIGHT // 1.3
    enemies.append(GameNode(x, y, 50, 50, enemy_img, random.choice([50, 75])))

def spawn_heal(x, y):
    heal_items.append(HealItem(x, y))

# ================== INIT ==================
for _ in range(3):
    spawn_enemy()

score = 0
running = True

# ================== LOOP ==================
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ===== CONTROL =====
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.position.x -= 5
        player.image = player_left

    elif keys[pygame.K_RIGHT]:
        player.position.x += 5
        player.image = player_right

    # ===== PEDANG (HORIZONTAL) =====
    if player.image == player_right:
        pedang.image = pedang_image
        pedang.position = pygame.Vector2(player.position.x + 50, player.position.y + 10)

    else:
        pedang.image = pygame.transform.flip(pedang_image, True, False)
        pedang.position = pygame.Vector2(player.position.x - 60, player.position.y + 10)

    player_rect = player.get_rect()
    sword_rect = pedang.get_rect()

    # ===== ENEMY =====
    for enemy in enemies[:]:
        if enemy.position.x < player.position.x:
            enemy.position.x += 2
        else:
            enemy.position.x -= 2

        if sword_rect.colliderect(enemy.get_rect()):
            enemy.health -= 25

        if enemy.health <= 0:
            spawn_heal(enemy.position.x, enemy.position.y)
            enemies.remove(enemy)
            score += 10

        if player_rect.colliderect(enemy.get_rect()):
            player.health -= 1

    # ===== HEAL =====
    for item in heal_items[:]:
        if player_rect.colliderect(item.get_rect()):
            player.health = min(100, player.health + 20)
            heal_items.remove(item)

    # ===== DRAW =====
    player.draw(screen)
    pedang.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    for item in heal_items:
        item.draw(screen)

    # ===== UI =====
    pygame.draw.rect(screen, (255,0,0), (10,10,200,20))
    pygame.draw.rect(screen, (0,255,0), (10,10,200*(player.health/100),20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()