import pygame
import random
import sys

pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎯 Shooting Burung")

clock = pygame.time.Clock()

# Warna
WHITE = (255, 255, 255)
SKY = (135, 206, 235)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont("arial", 30)

# Burung
class Bird:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(-100, -40)
        self.y = random.randint(50, HEIGHT - 100)
        self.speed = random.randint(4, 8)
        self.size = 60

    def move(self):
        self.x += self.speed
        if self.x > WIDTH:
            self.reset()

    def draw(self):
        pygame.draw.ellipse(screen, (0, 0, 0), (self.x, self.y, self.size, self.size//2))
        pygame.draw.polygon(screen, (255, 200, 0), [
            (self.x + self.size, self.y + self.size//4),
            (self.x + self.size + 10, self.y + self.size//4 + 5),
            (self.x + self.size, self.y + self.size//4 + 10)
        ])

    def hit(self, pos):
        rect = pygame.Rect(self.x, self.y, self.size, self.size//2)
        return rect.collidepoint(pos)


bird = Bird()

score = 0

# Crosshair
def draw_crosshair(pos):
    x, y = pos
    pygame.draw.circle(screen, RED, (x, y), 15, 2)
    pygame.draw.line(screen, RED, (x - 20, y), (x + 20, y), 2)
    pygame.draw.line(screen, RED, (x, y - 20), (x, y + 20), 2)

# Main loop
running = True
while running:
    screen.fill(SKY)

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if bird.hit(mouse_pos):
                score += 1
                bird.reset()

    # Update
    bird.move()

    # Draw
    bird.draw()
    draw_crosshair(mouse_pos)

    # Score
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (20, 20))

    pygame.display.update()
    clock.tick(60)