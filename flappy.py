import pygame
import sys
import random

pygame.init()

# ------------------------
# Screen
# ------------------------
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird with Toggle God Mode")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# ------------------------
# Game Variables
# ------------------------
bird_x = 50
bird_y = HEIGHT // 2
bird_radius = 15
bird_vel = 0
gravity = 0.5
jump_power = -10

pipe_width = 60
pipe_gap = 150
pipe_vel = 3
pipes = []

score = 0
high_score = 0
font = pygame.font.SysFont(None, 40)

flap_frame = 0  # animation frame
hack_active = False  # God mode toggle
hack_toggle_pressed = False  # To detect single key press

# ------------------------
# Functions
# ------------------------
def create_pipes():
    pipes.clear()
    for i in range(2):
        x = WIDTH + i * 200
        height_top = random.randint(100, HEIGHT - pipe_gap - 100)
        pipes.append({"x": x, "top": height_top, "passed": False})

def draw_bird():
    global flap_frame
    flap_frame = (flap_frame + 1) % 20
    radius = bird_radius + (3 if flap_frame < 10 else -3)
    pygame.draw.circle(screen, YELLOW, (bird_x, int(bird_y)), radius)

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe["x"], 0, pipe_width, pipe["top"]))
        bottom_height = HEIGHT - pipe["top"] - pipe_gap
        pygame.draw.rect(screen, GREEN, (pipe["x"], HEIGHT - bottom_height, pipe_width, bottom_height))

def collision_check():
    for pipe in pipes:
        if (bird_x + bird_radius > pipe["x"] and bird_x - bird_radius < pipe["x"] + pipe_width):
            if bird_y - bird_radius < pipe["top"] or bird_y + bird_radius > HEIGHT - (HEIGHT - pipe["top"] - pipe_gap):
                return True
    if bird_y - bird_radius < 0 or bird_y + bird_radius > HEIGHT:
        return True
    return False

def move_pipes():
    global score
    for pipe in pipes:
        pipe["x"] -= pipe_vel
        # Recycle pipe
        if pipe["x"] + pipe_width < 0:
            pipe["x"] = WIDTH
            pipe["top"] = random.randint(100, HEIGHT - pipe_gap - 100)
            pipe["passed"] = False
        # Update score
        if not pipe["passed"] and pipe["x"] + pipe_width < bird_x:
            score += 1
            pipe["passed"] = True

def start_screen():
    waiting = True
    while waiting:
        screen.fill(BLUE)
        title = font.render("Press SPACE to Start", True, WHITE)
        screen.blit(title, (WIDTH//2 - 120, HEIGHT//2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            waiting = False

def game_over_screen():
    global score, high_score
    if score > high_score:
        high_score = score
    waiting = True
    while waiting:
        screen.fill(RED)
        text1 = font.render("GAME OVER!", True, WHITE)
        text2 = font.render(f"Score: {score}", True, WHITE)
        text3 = font.render(f"High Score: {high_score}", True, WHITE)
        text4 = font.render("Press SPACE to Restart", True, WHITE)

        screen.blit(text1, (WIDTH//2 - 100, HEIGHT//2 - 90))
        screen.blit(text2, (WIDTH//2 - 50, HEIGHT//2 - 30))
        screen.blit(text3, (WIDTH//2 - 70, HEIGHT//2 + 10))
        screen.blit(text4, (WIDTH//2 - 140, HEIGHT//2 + 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            waiting = False
            reset_game()

def reset_game():
    global bird_y, bird_vel, score, hack_active
    bird_y = HEIGHT // 2
    bird_vel = 0
    score = 0
    hack_active = False
    create_pipes()

# ------------------------
# Main Game Loop
# ------------------------
start_screen()
create_pipes()

running = True
while running:
    clock.tick(FPS)
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Toggle hack mode
    if keys[pygame.K_h]:
        if not hack_toggle_pressed:
            hack_active = not hack_active
            hack_toggle_pressed = True
    else:
        hack_toggle_pressed = False

    # Normal jump
    if keys[pygame.K_SPACE] and not hack_active:
        bird_vel = jump_power

    # Apply gravity or God mode
    if not hack_active:
        bird_vel += gravity
        bird_y += bird_vel
    else:
        # God mode: auto-fly through next pipe
        next_pipe = min([p for p in pipes if p["x"] + pipe_width > bird_x],
                        key=lambda p: p["x"] + pipe_width)
        target_y = next_pipe["top"] + pipe_gap // 2
        if bird_y < target_y:
            bird_y += 4
        elif bird_y > target_y:
            bird_y -= 4

    # Draw everything
    draw_bird()
    move_pipes()
    draw_pipes()

    # Collision check (ignore if hack active)
    if not hack_active and collision_check():
        game_over_screen()

    # Draw score, high score, and hack indicator
    score_text = font.render(f"Score: {score}  High: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if hack_active:
        hack_text = font.render("GOD MODE ON", True, RED)
        screen.blit(hack_text, (WIDTH - 150, 10))

    pygame.display.update()

pygame.quit()
sys.exit()
