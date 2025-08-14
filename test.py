import pygame, sys

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Platformer")

clock = pygame.time.Clock()
FPS = 60

# Player
player = pygame.Rect(50, 300, 40, 50)
vel_x, vel_y = 0, 0
speed = 5
jump = -12
gravity = 0.5
on_ground = False

# Platforms
platforms = [pygame.Rect(0, 350, WIDTH, 50),
             pygame.Rect(150, 250, 100, 20),
             pygame.Rect(350, 180, 120, 20)]

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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

    # Gravity
    vel_y += gravity
    player.x += vel_x
    player.y += vel_y

    # Collision with platforms
    on_ground = False
    for plat in platforms:
        if player.colliderect(plat) and vel_y >= 0:
            player.bottom = plat.top
            vel_y = 0
            on_ground = True

    # Draw
    screen.fill((100, 200, 250))
    pygame.draw.rect(screen, (200,50,50), player)
    for plat in platforms:
        pygame.draw.rect(screen, (0,200,0), plat)
    pygame.display.update()

pygame.quit()
sys.exit()
