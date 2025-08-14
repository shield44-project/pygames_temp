import pygame, sys, math

pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projectile Motion")

clock = pygame.time.Clock()
FPS = 60

# Projectile properties
x, y = 50, HEIGHT-50
vel = 15
angle = 45  # degrees
rad = math.radians(angle)
vel_x = vel * math.cos(rad)
vel_y = -vel * math.sin(rad)
gravity = 0.5

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Physics
    vel_y += gravity
    x += vel_x
    y += vel_y

    # Ground collision
    if y > HEIGHT-10:
        y = HEIGHT-10
        vel_y *= -0.5  # bounce a bit
        vel_x *= 0.9

    # Draw
    screen.fill((0,0,0))
    pygame.draw.circle(screen, (50,200,50), (int(x), int(y)), 10)
    pygame.draw.line(screen, (255,255,255), (0, HEIGHT-10), (WIDTH, HEIGHT-10), 2)
    pygame.display.update()

pygame.quit()
sys.exit()
