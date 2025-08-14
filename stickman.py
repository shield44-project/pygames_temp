import pygame
import sys
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Animated Platformer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 200, 0)
ORANGE = (255, 150, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
FPS = 60

# -----------------------------
# Stickman Class
# -----------------------------
class Stickman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 60
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 15
        self.gravity = 1
        self.on_ground = False
        self.moving = False
        self.attacking = False
        self.attack_cooldown = 0
        self.frame_count = 0  # animation frame

    def move(self, keys):
        self.vel_x = 0
        self.moving = False
        self.attacking = False

        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
            self.moving = True
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
            self.moving = True
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
        if keys[pygame.K_a] and self.attack_cooldown == 0:
            self.attacking = True
            self.attack_cooldown = 20

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self, screen):
        # Animate walking
        offset = 0
        if self.moving:
            self.frame_count += 1
            if (self.frame_count // 10) % 2 == 0:
                offset = 5
            else:
                offset = -5
        # Arms
        arm_y = 25
        if self.attacking:
            pygame.draw.line(screen, BLACK, (self.x, self.y + arm_y), (self.x + self.width + 20, self.y + arm_y), 2)
        else:
            pygame.draw.line(screen, BLACK, (self.x, self.y + arm_y), (self.x + self.width, self.y + arm_y + offset), 2)
        # Head
        pygame.draw.circle(screen, BLACK, (self.x + self.width//2, self.y), 15, 2)
        # Body
        pygame.draw.line(screen, BLACK, (self.x + self.width//2, self.y + 15), (self.x + self.width//2, self.y + 45), 2)
        # Legs
        leg_offset = 5 if not self.on_ground else offset
        pygame.draw.line(screen, BLACK, (self.x + self.width//2, self.y + 45), (self.x - 5, self.y + 75 + leg_offset), 2)
        pygame.draw.line(screen, BLACK, (self.x + self.width//2, self.y + 45), (self.x + self.width + 5, self.y + 75 - leg_offset), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

class Enemy:
    def __init__(self, x, y, width=30, height=30, speed=2):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def patrol(self):
        self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.x > WIDTH - self.rect.width:
            self.speed *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)

class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)

    def draw(self, screen):
        pygame.draw.circle(screen, ORANGE, (self.rect.x + 7, self.rect.y + 7), 7)

# Platforms
platforms = [
    pygame.Rect(0, 580, 800, 20),
    pygame.Rect(200, 450, 200, 10),
    pygame.Rect(500, 350, 200, 10),
]

# Goal
goal = pygame.Rect(700, 300, 50, 50)

# Create objects
player = Stickman(100, 500)
enemies = [Enemy(300, 425), Enemy(550, 325)]
coins = [Coin(random.randint(100, 700), random.randint(100, 500)) for _ in range(5)]
score = 0
font = pygame.font.SysFont(None, 35)

running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)
    player.apply_gravity()

    # Collision with platforms
    player_rect = player.get_rect()
    player.on_ground = False
    for plat in platforms:
        if player_rect.colliderect(plat) and player.vel_y >= 0:
            player.y = plat.top - player.height
            player.vel_y = 0
            player.on_ground = True

    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)

    # Draw goal
    pygame.draw.rect(screen, RED, goal)

    # Check win
    if player_rect.colliderect(goal):
        font_win = pygame.font.SysFont(None, 55)
        text = font_win.render("You Win!", True, BLUE)
        screen.blit(text, (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    # Update enemies
    for enemy in enemies[:]:
        enemy.patrol()
        enemy.draw(screen)
        if player_rect.colliderect(enemy.rect):
            score -= 1
        if player.attacking and player_rect.colliderect(enemy.rect):
            enemies.remove(enemy)
            score += 5

    # Update coins
    for coin in coins[:]:
        coin.draw(screen)
        if player_rect.colliderect(coin.rect):
            coins.remove(coin)
            score += 2

    # Draw player
    player.draw(screen)
    player.update_cooldown()

    # Draw score
    score_text = font.render(f"Score: {int(score)}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
sys.exit()
