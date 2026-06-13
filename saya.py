import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
APPLE_SPEED = 3

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Apple")

# Clock
clock = pygame.time.Clock()

# Player
player_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT - 50, 100, 20)

# Apple
apple_rect = pygame.Rect(random.randint(0, WIDTH-20), -20, 20, 20)

# Score
score = 0
font = pygame.font.SysFont(None, 36)

def show_message(msg):
    text = font.render(msg, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += PLAYER_SPEED
        
    # Move apple
    apple_rect.y += APPLE_SPEED
    
    # Check collision
    if player_rect.colliderect(apple_rect):
        score += 1
        # Reset apple
        apple_rect.x = random.randint(0, WIDTH-20)
        apple_rect.y = -20
        APPLE_SPEED += 0.2 # Increase speed
        
    if apple_rect.top > HEIGHT:
        show_message("Game Over!")
        running = False
        
    # Drawing
    screen.fill(BLUE)
    pygame.draw.rect(screen, WHITE, player_rect)
    pygame.draw.rect(screen, RED, apple_rect)
    
    # Score text
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
