import pygame, sys, random
import math

pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Topology & Curve Challenge Game")

# Colors
BG_COLOR = (30,30,30)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (100,100,255)
YELLOW = (255,255,0)

# Fonts
font = pygame.font.SysFont("comicsansms", 36)
small_font = pygame.font.SysFont("comicsansms", 25)

# Game variables
score = 0
feedback = ""
feedback_color = WHITE

# Curves and shapes
shapes = ["circle", "ellipse", "donut"]
curves = ["sinx","cosx","parabola","hyperbola","logx"]

def generate_pair():
    """Generate a pair of shapes/curves with a 60% chance of being 'same' type"""
    type_pool = shapes + curves
    shape1 = random.choice(type_pool)
    if random.random() < 0.6:
        shape2 = shape1  # Same/homeomorphic
        answer = "same"
    else:
        shape2 = random.choice(type_pool)
        answer = "different"
    return {"shape1":shape1, "shape2":shape2, "answer":answer}

current_pair = generate_pair()

# Draw mathematical curves
def draw_curve(curve_type, center_x, center_y, color):
    points = []
    if curve_type == "sinx":
        for x in range(-200,201):
            y = 50*math.sin(x/20)
            points.append((center_x + x, center_y - y))
    elif curve_type == "cosx":
        for x in range(-200,201):
            y = 50*math.cos(x/20)
            points.append((center_x + x, center_y - y))
    elif curve_type == "parabola":
        for x in range(-100,101):
            y = 0.05*(x**2)
            points.append((center_x + x, center_y - y))
    elif curve_type == "hyperbola":
        for x in range(-100,-10):
            y = 500/(x+0.1)
            points.append((center_x + x, center_y - y))
        for x in range(10,101):
            y = 500/(x+0.1)
            points.append((center_x + x, center_y - y))
    elif curve_type == "logx":
        for x in range(1,201):
            y = 20*math.log(x)
            points.append((center_x + x - 100, center_y - y))
    else:
        # shapes
        if curve_type == "circle":
            pygame.draw.circle(screen, color, (center_x,center_y), 80, 5)
        elif curve_type == "ellipse":
            pygame.draw.ellipse(screen, color, (center_x-80, center_y-50,160,100), 5)
        elif curve_type == "donut":
            pygame.draw.circle(screen, color, (center_x, center_y), 80, 5)
            pygame.draw.circle(screen, BG_COLOR, (center_x, center_y), 40, 0)
        return
    
    if points:
        pygame.draw.lines(screen, color, False, points, 3)

# Draw screen
def draw_screen():
    screen.fill(BG_COLOR)
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10,10))
    
    feedback_text = small_font.render(feedback, True, feedback_color)
    screen.blit(feedback_text, (10, 40))
    
    draw_curve(current_pair["shape1"], 250, 250, BLUE)
    draw_curve(current_pair["shape2"], 650, 250, YELLOW)
    
    # Draw buttons
    pygame.draw.rect(screen, WHITE, (200,450,150,50), 2)
    pygame.draw.rect(screen, WHITE, (550,450,150,50), 2)
    yes_text = font.render("SAME", True, WHITE)
    no_text = font.render("DIFF", True, WHITE)
    screen.blit(yes_text, (210,455))
    screen.blit(no_text, (560,455))
    
    pygame.display.update()

# Main loop
running = True
while running:
    draw_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx,my = pygame.mouse.get_pos()
            clicked = None
            if 200 <= mx <= 350 and 450 <= my <= 500:
                clicked = "same"
            elif 550 <= mx <= 700 and 450 <= my <= 500:
                clicked = "different"
            
            if clicked:
                if clicked == current_pair["answer"]:
                    feedback = "Correct!"
                    feedback_color = GREEN
                    score += 1
                else:
                    feedback = f"Wrong! Correct: {current_pair['answer'].upper()}"
                    feedback_color = RED
                current_pair = generate_pair()
