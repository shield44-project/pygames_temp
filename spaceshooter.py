import pygame
import sys
import random
import os

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

clock = pygame.time.Clock()
FPS = 60

# Player
player_width, player_height = 40, 50
player_x, player_y = WIDTH//2 - player_width//2, HEIGHT - player_height - 10
player_vel = 5

# Bullets
bullets = []

# Enemies
enemies = []
enemy_timer = 0
spawn_interval = 60

# Score
score = 0
font = pygame.font.SysFont(None, 35)

# High score
highscore_file = "space_highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        high_score = int(f.read())
else:
    high_score = 0

def reset_game():
    global enemies, bullets, score, high_score
    if score > high_score:
        high_score = score
        with open(highscore_file, "w") as f:
            f.write(str(high_score))
    enemies.clear()
    bullets.clear()
    score = 0

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            reset_game()
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_vel
    if keys[pygame.K_RIGHT] and player_x + player_width < WIDTH:
        player_x += player_vel
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:
            bullets.append(pygame.Rect(player_x + player_width//2 -2, player_y, 4, 10))

    # Spawn enemies
    enemy_timer += 1
    if enemy_timer >= spawn_interval:
        enemy_x = random.randint(0, WIDTH-40)
        enemies.append(pygame.Rect(enemy_x, -40, 40, 40))
        enemy_timer = 0

    # Move bullets
    for b in bullets[:]:
        b.y -= 10
        if b.y < 0:
            bullets.remove(b)

    # Move enemies
    for e in enemies[:]:
        e.y += 5
        if e.y > HEIGHT:
            reset_game()  # game over
        for b in bullets[:]:
            if e.colliderect(b):
                bullets.remove(b)
                enemies.remove(e)
                score += 1

    # Draw
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
    for b in bullets:
        pygame.draw.rect(screen, WHITE, b)
    for e in enemies:
        pygame.draw.rect(screen, RED, e)
    score_text = font.render(f"Score: {score}  High: {high_score}", True, WHITE)
    screen.blit(score_text, (10,10))
    pygame.display.update()

pygame.quit()
sys.exit()
