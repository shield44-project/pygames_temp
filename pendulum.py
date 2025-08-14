import pygame, sys, math

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum Physics")

clock = pygame.time.Clock()
FPS = 60

# Pendulum properties
origin = (WIDTH//2, 50)
length = 200
angle = math.pi/4
angular_velocity = 0
gravity = 0.01

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Physics
    angular_acceleration = -gravity / length * math.sin(angle)
    angular_velocity += angular_acceleration
    angular_velocity *= 0.99  # damping
    angle += angular_velocity

    # Pendulum position
    x = origin[0] + length * math.sin(angle)
    y = origin[1] + length * math.cos(angle)

    # Draw
    screen.fill((30,30,30))
    pygame.draw.line(screen, (255,255,255), origin, (x, y), 2)
    pygame.draw.circle(screen, (255,0,0), (int(x), int(y)), 15)
    pygame.display.update()

pygame.quit()
sys.exit()
