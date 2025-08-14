import pygame, sys, random

# Initialize Pygame
pygame.init()

# Settings
GRID_SIZE = 10
TILE_SIZE = 40
NUM_MINES = 15
SCREEN_SIZE = GRID_SIZE * TILE_SIZE
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Minesweeper")

# Colors
BG_COLOR = (192, 192, 192)
TILE_COLOR = (220, 220, 220)
REVEALED_COLOR = (169, 169, 169)
MINE_COLOR = (255, 0, 0)
FLAG_COLOR = (0, 0, 255)
TEXT_COLOR = (0, 0, 0)
font = pygame.font.SysFont("comicsansms", 20)

# Create grid
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
revealed = [[False]*GRID_SIZE for _ in range(GRID_SIZE)]
flags = [[False]*GRID_SIZE for _ in range(GRID_SIZE)]

# Place mines
mines = random.sample(range(GRID_SIZE*GRID_SIZE), NUM_MINES)
for m in mines:
    i, j = divmod(m, GRID_SIZE)
    grid[i][j] = -1  # -1 represents a mine

# Calculate numbers
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        if grid[i][j] == -1:
            continue
        count = 0
        for x in range(max(0, i-1), min(GRID_SIZE, i+2)):
            for y in range(max(0, j-1), min(GRID_SIZE, j+2)):
                if grid[x][y] == -1:
                    count += 1
        grid[i][j] = count

# Functions
def draw_grid():
    screen.fill(BG_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if revealed[i][j]:
                pygame.draw.rect(screen, REVEALED_COLOR, rect)
                if grid[i][j] > 0:
                    text = font.render(str(grid[i][j]), True, TEXT_COLOR)
                    screen.blit(text, text.get_rect(center=rect.center))
                elif grid[i][j] == -1:
                    pygame.draw.circle(screen, MINE_COLOR, rect.center, TILE_SIZE//4)
            else:
                pygame.draw.rect(screen, TILE_COLOR, rect)
                if flags[i][j]:
                    pygame.draw.circle(screen, FLAG_COLOR, rect.center, TILE_SIZE//4)
            pygame.draw.rect(screen, BG_COLOR, rect, 1)
    pygame.display.update()

def reveal(i, j):
    if revealed[i][j] or flags[i][j]:
        return
    revealed[i][j] = True
    if grid[i][j] == 0:
        for x in range(max(0,i-1), min(GRID_SIZE,i+2)):
            for y in range(max(0,j-1), min(GRID_SIZE,j+2)):
                if not revealed[x][y]:
                    reveal(x, y)

def check_win():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] != -1 and not revealed[i][j]:
                return False
    return True

# Game loop
running = True
game_over = False
while running:
    draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_over:
            continue
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            i, j = y//TILE_SIZE, x//TILE_SIZE
            if event.button == 1:  # Left click
                if grid[i][j] == -1:
                    revealed[i][j] = True
                    game_over = True
                    print("Game Over! You hit a mine.")
                else:
                    reveal(i,j)
                    if check_win():
                        game_over = True
                        print("Congratulations! You cleared all safe tiles.")
            elif event.button == 3:  # Right click
                flags[i][j] = not flags[i][j]
