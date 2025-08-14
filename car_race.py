import pygame
import sys
import random

pygame.init()

# ------------------------
# Screen
# ------------------------
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Car Race Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# ------------------------
# Game Variables
# ------------------------
player_width = 40
player_height = 70
player_x = WIDTH//2 - player_width//2
player_y = HEIGHT - player_height - 10
player_vel = 5

obstacle_width = 40
obstacle_height = 70
obstacles = []

obstacle_base_vel = 5
spawn_timer = 0
spawn_interval = 60  # frames

score = 0
high_score = 0
font = pygame.font.SysFont(None, 40)

# Road scrolling
road_scroll = 0
scroll_speed = 5

# Power-up
powerups = []
powerup_timer = 0
powerup_interval = 600
boost_active = False
boost_timer = 0

# ------------------------
# Classes
# ------------------------
class Obstacle:
    def __init__(self, x, y, width, height, vel):
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = vel

class PowerUp:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

# ------------------------
# Functions
# ------------------------
def draw_player():
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

def draw_obstacles():
    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs.rect)

def move_obstacles():
    global score
    for obs in obstacles:
        obs.rect.y += obs.vel
    # Remove obstacles that went off screen
    for obs in obstacles[:]:
        if obs.rect.y > HEIGHT:
            obstacles.remove(obs)
            score += 1

def draw_powerups():
    for pu in powerups:
        pygame.draw.rect(screen, GREEN, pu.rect)

def move_powerups():
    for pu in powerups:
        pu.rect.y += obstacle_base_vel

def check_collision():
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for obs in obstacles:
        if player_rect.colliderect(obs.rect):
            return True
    for pu in powerups[:]:
        if player_rect.colliderect(pu.rect):
            activate_boost()
            powerups.remove(pu)
    return False

def spawn_obstacle():
    lane_x = random.choice([WIDTH//4 - obstacle_width//2,
                            WIDTH//2 - obstacle_width//2,
                            3*WIDTH//4 - obstacle_width//2])
    new_obs = Obstacle(lane_x, -obstacle_height, obstacle_width, obstacle_height,
                       obstacle_base_vel + random.randint(0, 2))
    obstacles.append(new_obs)

def spawn_powerup():
    lane_x = random.choice([WIDTH//4 - 15, WIDTH//2 - 15, 3*WIDTH//4 - 15])
    new_pu = PowerUp(lane_x, -30, 30, 30)
    powerups.append(new_pu)

def activate_boost():
    global boost_active, boost_timer
    boost_active = True
    boost_timer = FPS * 3  # lasts 3 seconds

def draw_road():
    global road_scroll
    screen.fill(GRAY)
    # Draw lanes
    pygame.draw.line(screen, WHITE, (WIDTH//3, 0), (WIDTH//3, HEIGHT), 5)
    pygame.draw.line(screen, WHITE, (2*WIDTH//3, 0), (2*WIDTH//3, HEIGHT), 5)
    # Scroll road effect
    road_scroll += scroll_speed
    if road_scroll >= HEIGHT:
        road_scroll = 0

# ------------------------
# Main Game Loop
# ------------------------
running = True
while running:
    clock.tick(FPS)

    draw_road()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_vel
    if keys[pygame.K_RIGHT] and player_x + player_width < WIDTH:
        player_x += player_vel

    # Spawn obstacles
    spawn_timer += 1
    if spawn_timer >= spawn_interval:
        spawn_obstacle()
        spawn_timer = 0

    # Spawn power-ups
    powerup_timer += 1
    if powerup_timer >= powerup_interval:
        spawn_powerup()
        powerup_timer = 0

    # Move obstacles and power-ups
    move_obstacles()
    move_powerups()

    # Apply boost effect
    if boost_active:
        boost_timer -= 1
        for obs in obstacles:
            obs.rect.y -= 2  # slow obstacles while boosted
        if boost_timer <= 0:
            boost_active = False

    # Draw everything
    draw_player()
    draw_obstacles()
    draw_powerups()

    # Collision check
    if check_collision():
        if score > high_score:
            high_score = score
        # Game over
        game_over_text = font.render(f"GAME OVER! Score: {score}", True, YELLOW)
        screen.blit(game_over_text, (WIDTH//2 - 140, HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(2000)
        # Reset game
        obstacles.clear()
        powerups.clear()
        player_x = WIDTH//2 - player_width//2
        player_y = HEIGHT - player_height - 10
        score = 0
        spawn_timer = 0
        powerup_timer = 0
        boost_active = False
        continue

    # Draw score and high score
    score_text = font.render(f"Score: {score}  High: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Boost indicator
    if boost_active:
        boost_text = font.render("BOOST ACTIVE!", True, GREEN)
        screen.blit(boost_text, (WIDTH - 180, 10))

    pygame.display.update()

pygame.quit()
sys.exit()
