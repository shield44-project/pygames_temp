import pygame
import sys
import random
import os

pygame.init()

# Screen
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)

# Clock
clock = pygame.time.Clock()
FPS = 10
block = 20

# Snake
snake = [(WIDTH//2, HEIGHT//2)]
dx, dy = 0, 0
snake_length = 1

# Food
food = (random.randrange(0, WIDTH, block), random.randrange(0, HEIGHT, block))

# Fonts
font = pygame.font.SysFont(None, 35)

# High score file
highscore_file = "snake_highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        high_score = int(f.read())
else:
    high_score = 0

def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, block, block))

def draw_food():
    pygame.draw.rect(screen, RED, (*food, block, block))

def reset_game():
    global snake, dx, dy, snake_length, food, high_score
    if len(snake) - 1 > high_score:
        high_score = len(snake) - 1
        with open(highscore_file, "w") as f:
            f.write(str(high_score))
    snake = [(WIDTH//2, HEIGHT//2)]
    dx, dy = 0, 0
    snake_length = 1
    food = (random.randrange(0, WIDTH, block), random.randrange(0, HEIGHT, block))

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            reset_game()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -block, 0
            if event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = block, 0
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -block
            if event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, block

    # Move snake
    head = (snake[-1][0] + dx, snake[-1][1] + dy)
    snake.append(head)
    if len(snake) > snake_length:
        snake.pop(0)

    # Collision
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in snake[:-1]:
        pygame.time.delay(500)
        reset_game()

    # Eat food
    if head == food:
        snake_length += 1
        food = (random.randrange(0, WIDTH, block), random.randrange(0, HEIGHT, block))

    # Draw
    screen.fill(BLACK)
    draw_snake()
    draw_food()
    score_text = font.render(f"Score: {snake_length-1}  High: {high_score}", True, WHITE)
    screen.blit(score_text, (10,10))
    pygame.display.update()

pygame.quit()
sys.exit()
