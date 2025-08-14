import pygame
import sys
import os

pygame.init()
WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Mario")

WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,200,0)

clock = pygame.time.Clock()
FPS = 60

# Player
player = pygame.Rect(50, 300, 30, 50)
vel_x, vel_y = 0, 0
speed = 5
jump = -10
gravity = 0.5
on_ground = False

# Platforms
platforms = [pygame.Rect(0, 350, WIDTH, 50), pygame.Rect(150, 250, 100, 20), pygame.Rect(300, 180, 100, 20)]

# Score
score = 0
font = pygame.font.SysFont(None, 35)

# High score
highscore_file = "mario_highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        high_score = int(f.read())
else:
    high_score = 0

def reset_game():
    global player, vel_x, vel_y, score, high_score
    if score > high_score:
        high_score = score
        with open(highscore_file, "w") as f:
            f.write(str(high_score))
    player.x, player.y = 50, 300
    vel_x, vel_y = 0, 0
    score = 0

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            reset_game()
            running = False

    keys = pygame.key.get_pressed()
    vel_x = 0
    if keys[pygame.K_LEFT]:
        vel_x = -speed
    if keys[pygame.K_RIGHT]:
        vel_x = speed
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump
        on_ground = False

    vel_y += gravity
    player.x += vel_x
    player.y += vel_y

    on_ground = False
    for plat in platforms:
        if player.colliderect(plat) and vel_y >= 0:
            player.bottom = plat.top
            vel_y = 0
            on_ground = True

    # Update score by horizontal distance
    score = max(score, player.x)

    # Reset if fall off screen
    if player.y > HEIGHT:
        reset_game()

    # Draw
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player)
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)
    score_text = font.render(f"Score: {score}  High: {high_score}", True, (0,0,0))
    screen.blit(score_text, (10,10))
    pygame.display.update()

pygame.quit()
sys.exit()
