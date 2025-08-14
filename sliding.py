import pygame, sys, random

# Initialize Pygame
pygame.init()

# Screen settings
GRID_SIZE = 3
TILE_SIZE = 100
MARGIN = 5
SCREEN_SIZE = GRID_SIZE * TILE_SIZE
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Sliding Puzzle")

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
TILE_COLOR = (173, 216, 230)
FONT_COLOR = (0,0,0)
font = pygame.font.SysFont("comicsansms", 50)

# Create the puzzle grid
tiles = list(range(1, GRID_SIZE*GRID_SIZE))
tiles.append(0)  # 0 will represent the empty space
random.shuffle(tiles)
grid = [tiles[i*GRID_SIZE:(i+1)*GRID_SIZE] for i in range(GRID_SIZE)]

def draw_grid(grid):
    screen.fill(BLACK)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = grid[i][j]
            rect = pygame.Rect(j*TILE_SIZE+MARGIN, i*TILE_SIZE+MARGIN, TILE_SIZE-2*MARGIN, TILE_SIZE-2*MARGIN)
            if value != 0:
                pygame.draw.rect(screen, TILE_COLOR, rect)
                text = font.render(str(value), True, FONT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, BLACK, rect)
    pygame.display.update()

def find_empty(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return (i,j)

def move_tile(grid, direction):
    i,j = find_empty(grid)
    if direction == "up" and i < GRID_SIZE-1:
        grid[i][j], grid[i+1][j] = grid[i+1][j], grid[i][j]
    elif direction == "down" and i > 0:
        grid[i][j], grid[i-1][j] = grid[i-1][j], grid[i][j]
    elif direction == "left" and j < GRID_SIZE-1:
        grid[i][j], grid[i][j+1] = grid[i][j+1], grid[i][j]
    elif direction == "right" and j > 0:
        grid[i][j], grid[i][j-1] = grid[i][j-1], grid[i][j]

def check_win(grid):
    correct = list(range(1, GRID_SIZE*GRID_SIZE)) + [0]
    flat = [cell for row in grid for cell in row]
    return flat == correct

# Draw initial grid
draw_grid(grid)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_tile(grid, "up")
            elif event.key == pygame.K_DOWN:
                move_tile(grid, "down")
            elif event.key == pygame.K_LEFT:
                move_tile(grid, "left")
            elif event.key == pygame.K_RIGHT:
                move_tile(grid, "right")
            draw_grid(grid)
            if check_win(grid):
                print("Congratulations! You solved the puzzle!")
                running = False
