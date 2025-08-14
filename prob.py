import pygame, sys, random, time
from fractions import Fraction
from math import comb

pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Probability Game")

# Colors
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
INPUT_COLOR = (50, 50, 50)
CORRECT_COLOR = (0, 255, 0)
WRONG_COLOR = (255, 0, 0)

# Fonts
font = pygame.font.SysFont("comicsansms", 36)
small_font = pygame.font.SysFont("comicsansms", 25)

# Game variables
score = 0
user_input = ""
feedback = ""
feedback_color = TEXT_COLOR
timer_start = None
time_limit = 25  # seconds per question

# Generate difficult probability question
def generate_question():
    global timer_start
    type_q = random.choice(["dice_two", "two_coins", "bag", "conditional"])
    
    if type_q == "dice_two":
        # Probability sum of two dice = 7
        question = "Probability that sum of 2 dice = 7"
        # 6 favorable outcomes / 36 total
        answer = Fraction(6,36)
    
    elif type_q == "two_coins":
        # Probability of exactly one head in 3 coin flips
        question = "Probability of exactly 1 Head in 3 coin flips"
        # 3 choose 1 = 3 favorable / 8 total
        answer = Fraction(comb(3,1), 8)
    
    elif type_q == "bag":
        # Bag with 5 red, 3 blue, 2 green, choose 2 balls randomly
        red, blue, green = 5, 3, 2
        total = red+blue+green
        # Probability both balls are red
        question = f"Bag has 5 red,3 blue,2 green. Probability both chosen balls are red"
        answer = Fraction(comb(red,2), comb(total,2))
    
    else:  # conditional
        # Conditional probability: bag with 2 red,3 blue; pick 1, then 2nd red
        question = "Bag has 2 red,3 blue. Pick 1 then 2nd red. Probability?"
        # P(first any) = 1, P(second red|first removed) = (remaining red)/remaining total
        answer = Fraction(1,5)  # For simplicity, precomputed
    
    timer_start = time.time()
    return question, answer

question, answer = generate_question()

# Draw screen
def draw_screen():
    screen.fill(BG_COLOR)
    score_text = small_font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10,10))
    
    # Timer
    if timer_start:
        elapsed = int(time.time() - timer_start)
        remaining = max(0, time_limit - elapsed)
        timer_text = small_font.render(f"Time left: {remaining}s", True, TEXT_COLOR)
        screen.blit(timer_text, (WIDTH-250,10))
    
    question_text = font.render(question, True, TEXT_COLOR)
    screen.blit(question_text, (50,150))
    
    input_box = pygame.Rect(50, 250, 800, 60)
    pygame.draw.rect(screen, INPUT_COLOR, input_box)
    input_text = font.render(user_input, True, TEXT_COLOR)
    screen.blit(input_text, (input_box.x+10, input_box.y+10))
    
    feedback_text = small_font.render(feedback, True, feedback_color)
    screen.blit(feedback_text, (50,350))
    
    pygame.display.update()

# Check answer
def check_answer(user_ans, correct_ans):
    try:
        if "/" in user_ans:
            user_frac = Fraction(user_ans)
        else:
            user_frac = Fraction(float(user_ans)).limit_denominator()
        return user_frac == correct_ans
    except:
        return False

# Main game loop
running = True
while running:
    draw_screen()
    
    if timer_start and time.time() - timer_start > time_limit:
        feedback = f"Time's up! Answer was {answer}"
        feedback_color = WRONG_COLOR
        user_input = ""
        question, answer = generate_question()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_input.strip() != "":
                    if check_answer(user_input, answer):
                        feedback = "Correct!"
                        feedback_color = CORRECT_COLOR
                        score += 1
                    else:
                        feedback = f"Wrong! Answer was {answer}"
                        feedback_color = WRONG_COLOR
                    user_input = ""
                    question, answer = generate_question()
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                # Allow numbers, fractions, decimal
                allowed_chars = "0123456789/."
                if event.unicode in allowed_chars:
                    user_input += event.unicode
