import pygame, random, sys

# Initialize pygame
pygame.init()

# Screen settings
SIZE = 400
GRID_SIZE = 4
TILE_SIZE = SIZE // GRID_SIZE
MARGIN = 5

# Colors
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_COLOR = (205, 193, 180)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
FONT_COLOR = (119, 110, 101)

# Initialize screen
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("2048")
font = pygame.font.SysFont("comicsansms", 40)

# Initialize grid
grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]

# Functions
def add_new_tile(grid):
    empty = [(i,j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j]==0]
    if empty:
        i,j = random.choice(empty)
        grid[i][j] = 2 if random.random()<0.9 else 4

def draw_grid(grid):
    screen.fill(BACKGROUND_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = grid[i][j]
            color = TILE_COLORS.get(value, EMPTY_COLOR) if value else EMPTY_COLOR
            pygame.draw.rect(screen, color, (j*TILE_SIZE+MARGIN, i*TILE_SIZE+MARGIN, TILE_SIZE-2*MARGIN, TILE_SIZE-2*MARGIN), 0)
            if value:
                text = font.render(str(value), True, FONT_COLOR)
                text_rect = text.get_rect(center=(j*TILE_SIZE+TILE_SIZE//2, i*TILE_SIZE+TILE_SIZE//2))
                screen.blit(text, text_rect)
    pygame.display.update()

def slide_left(row):
    new_row = [i for i in row if i!=0]
    for i in range(len(new_row)-1):
        if new_row[i]==new_row[i+1]:
            new_row[i]*=2
            new_row[i+1]=0
    new_row = [i for i in new_row if i!=0]
    return new_row + [0]*(GRID_SIZE-len(new_row))

def move(grid, direction):
    moved = False
    if direction=='left':
        for i in range(GRID_SIZE):
            new_row = slide_left(grid[i])
            if new_row != grid[i]:
                moved = True
            grid[i] = new_row
    elif direction=='right':
        for i in range(GRID_SIZE):
            new_row = slide_left(grid[i][::-1])[::-1]
            if new_row != grid[i]:
                moved = True
            grid[i] = new_row
    elif direction=='up':
        grid[:] = list(map(list, zip(*grid)))  # transpose
        for i in range(GRID_SIZE):
            new_row = slide_left(grid[i])
            if new_row != grid[i]:
                moved = True
            grid[i] = new_row
        grid[:] = list(map(list, zip(*grid)))  # transpose back
    elif direction=='down':
        grid[:] = list(map(list, zip(*grid)))  # transpose
        for i in range(GRID_SIZE):
            new_row = slide_left(grid[i][::-1])[::-1]
            if new_row != grid[i]:
                moved = True
            grid[i] = new_row
        grid[:] = list(map(list, zip(*grid)))  # transpose back
    return moved

def check_game_over(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j]==0:
                return False
            if j<GRID_SIZE-1 and grid[i][j]==grid[i][j+1]:
                return False
            if i<GRID_SIZE-1 and grid[i][j]==grid[i+1][j]:
                return False
    return True

# Start game
add_new_tile(grid)
add_new_tile(grid)
draw_grid(grid)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                moved = move(grid, 'left')
            elif event.key==pygame.K_RIGHT:
                moved = move(grid, 'right')
            elif event.key==pygame.K_UP:
                moved = move(grid, 'up')
            elif event.key==pygame.K_DOWN:
                moved = move(grid, 'down')
            else:
                moved = False

            if moved:
                add_new_tile(grid)
                draw_grid(grid)
                if check_game_over(grid):
                    print("Game Over!")
                    running = False
