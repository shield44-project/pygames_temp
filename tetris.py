import pygame, random

# Initialize pygame
pygame.init()

# Screen size
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
COLORS = [
    (0, 255, 255),   # Cyan
    (0, 0, 255),     # Blue
    (255, 165, 0),   # Orange
    (255, 255, 0),   # Yellow
    (0, 255, 0),     # Green
    (128, 0, 128),   # Purple
    (255, 0, 0)      # Red
]

# Tetris shapes
SHAPES = [
    [[1,1,1,1]],          # I
    [[1,1,1],[0,1,0]],    # T
    [[1,1,0],[0,1,1]],    # S
    [[0,1,1],[1,1,0]],    # Z
    [[1,1],[1,1]],        # O
    [[1,0,0],[1,1,1]],    # L
    [[0,0,1],[1,1,1]]     # J
]

# Create grid
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

# Piece class
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

def rotate(shape):
    return [ [ shape[y][x] for y in range(len(shape)) ] for x in range(len(shape[0])-1,-1,-1)]

def valid_move(piece, grid, dx=0, dy=0, rotated_shape=None):
    shape = rotated_shape if rotated_shape else piece.shape
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                nx = piece.x + x + dx
                ny = piece.y + y + dy
                if nx < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT:
                    return False
                if ny >= 0 and grid[ny][nx]:
                    return False
    return True

def lock_piece(piece, grid):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[piece.y + y][piece.x + x] = piece.color

def clear_lines(grid):
    lines_cleared = 0
    for i in range(len(grid)-1, -1, -1):
        if 0 not in grid[i]:
            del grid[i]
            grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            lines_cleared += 1
    return lines_cleared

def draw_grid(screen, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = grid[y][x] if grid[y][x] else BLACK
            pygame.draw.rect(screen, color, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, WHITE, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Game loop
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5
current_piece = Piece(GRID_WIDTH//2 - 1, 0, random.choice(SHAPES))
score = 0
running = True

while running:
    screen.fill(BLACK)
    fall_time += clock.get_rawtime()
    clock.tick()

    # Piece falling
    if fall_time/1000 > fall_speed:
        fall_time = 0
        if valid_move(current_piece, grid, dy=1):
            current_piece.y += 1
        else:
            lock_piece(current_piece, grid)
            score += clear_lines(grid)
            current_piece = Piece(GRID_WIDTH//2 - 1, 0, random.choice(SHAPES))
            if not valid_move(current_piece, grid):
                print("Game Over! Score:", score)
                running = False

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and valid_move(current_piece, grid, dx=-1):
                current_piece.x -= 1
            elif event.key == pygame.K_RIGHT and valid_move(current_piece, grid, dx=1):
                current_piece.x += 1
            elif event.key == pygame.K_DOWN and valid_move(current_piece, grid, dy=1):
                current_piece.y += 1
            elif event.key == pygame.K_UP:
                rotated = rotate(current_piece.shape)
                if valid_move(current_piece, grid, rotated_shape=rotated):
                    current_piece.shape = rotated

    # Draw current piece
    for y, row in enumerate(current_piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_piece.color, ((current_piece.x + x)*BLOCK_SIZE, (current_piece.y + y)*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    draw_grid(screen, grid)
    pygame.display.update()
