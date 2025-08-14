import pygame
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Note class
class Note:
    def __init__(self, x, key):
        self.x = x
        self.y = -50
        self.key = key
        self.hit = False
    
    def move(self):
        self.y += 5  # Falling speed
    
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, 50, 50))

# Key mapping
key_mapping = {
    pygame.K_a: 100,
    pygame.K_s: 200,
    pygame.K_d: 300,
    pygame.K_f: 400
}

# List of notes
notes = []

# Game loop
running = True
spawn_timer = 0
score = 0

while running:
    screen.fill(BLACK)
    spawn_timer += 1

    # Spawn notes randomly
    if spawn_timer > 60:  # Every 1 second
        key = random.choice(list(key_mapping.keys()))
        notes.append(Note(key_mapping[key], key))
        spawn_timer = 0

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            for note in notes:
                if note.key == event.key and HEIGHT - 100 <= note.y <= HEIGHT - 50:
                    note.hit = True
                    score += 10

    # Move and draw notes
    for note in notes:
        note.move()
        if not note.hit:
            note.draw()
    
    # Remove notes that passed
    notes = [note for note in notes if note.y < HEIGHT and not note.hit]

    # Draw hit line
    pygame.draw.line(screen, WHITE, (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 5)

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
