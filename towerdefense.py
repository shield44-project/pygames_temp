import pygame
import sys
import os

pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense Simple")

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

clock = pygame.time.Clock()
FPS = 60

# Towers
towers = [pygame.Rect(100, 400, 40, 40), pygame.Rect(300, 400, 40, 40)]
tower_range = 100
tower_damage = 1

# Enemies
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.health = 5
        self.speed = 2

enemies = [Enemy(0, 50)]

# Score
score = 0
font = pygame.font.SysFont(None, 35)

# High score
highscore_file = "td_highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        high_score = int(f.read())
else:
    high_score = 0

def reset_game():
    global enemies, score, high_score
    if score > high_score:
        high_score = score
        with open(highscore_file, "w") as f:
            f.write(str(high_score))
    enemies.clear()
    enemies.append(Enemy(0, 50))
    score = 0

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            reset_game()
            running = False

    # Move enemies
    for e in enemies[:]:
        e.rect.x += e.speed
        if e.rect.x > WIDTH:
            reset_game()

    # Towers shoot enemies
    for t in towers:
        for e in enemies[:]:
            if t.centerx - tower_range < e.rect.centerx < t.centerx + tower_range and t.centery - tower_range < e.rect.centery < t.centery + tower_range:
                e.health -= tower_damage
                if e.health <= 0:
                    enemies.remove(e)
                    score += 1

    # Draw
    screen.fill(WHITE)
    for t in towers:
        pygame.draw.rect(screen, BLUE, t)
    for e in enemies:
        pygame.draw.rect(screen, RED, e.rect)
    score_text = font.render(f"Score: {score}  High: {high_score}", True, (0,0,0))
    screen.blit(score_text, (10,10))
    pygame.display.update()

pygame.quit()
sys.exit()
