import pygame, sys, random, time
from sympy import symbols, diff, integrate, sin, cos, exp, limit, oo, simplify, sympify

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Calculus Challenge Game")

# Colors
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
INPUT_COLOR = (50, 50, 50)
CORRECT_COLOR = (0, 255, 0)
WRONG_COLOR = (255, 0, 0)

# Fonts
font = pygame.font.SysFont("comicsansms", 40)
small_font = pygame.font.SysFont("comicsansms", 25)

# Symbol for math
x = symbols('x')

# Game variables
score = 0
user_input = ""
feedback = ""
feedback_color = TEXT_COLOR
difficulty = 'Medium'  # Easy / Medium / Hard
timer_start = None
time_limit = 15  # seconds per question

# Preprocess user input to normalize
def normalize_input(user_ans):
    user_ans = user_ans.replace("^", "**")
    user_ans = user_ans.replace("sinx", "sin(x)").replace("cosx", "cos(x)").replace("expx", "exp(x)")
    return user_ans

# Check answer
def check_answer(user_ans, correct_ans):
    try:
        user_expr = sympify(normalize_input(user_ans))
        correct_expr = sympify(correct_ans)
        return simplify(user_expr) == simplify(correct_expr)
    except:
        return False

# Generate calculus question
def generate_question():
    global timer_start
    kind = random.choice(['diff', 'int', 'limit'])
    # Difficulty controls complexity
    if difficulty == 'Easy':
        funcs = [x, x**2, sin(x), cos(x)]
    elif difficulty == 'Medium':
        funcs = [x**2, x**3, sin(x), cos(x), exp(x)]
    else:  # Hard
        funcs = [x**3, x**4, sin(x)*x, cos(x)*x, exp(x)*x]

    if kind == 'diff':
        expr = random.choice(funcs)
        question = f"d/dx {expr}"
        answer = diff(expr, x)
    elif kind == 'int':
        expr = random.choice(funcs)
        question = f"∫ {expr} dx"
        answer = integrate(expr, x)
    else:  # limit
        expr = random.choice(funcs)
        point = random.choice([0, 1, -1, oo])
        question = f"lim x→{point} {expr}"
        answer = limit(expr, x, point)

    timer_start = time.time()
    return str(question), str(answer)

question, answer = generate_question()

# Draw screen
def draw_screen():
    screen.fill(BG_COLOR)
    # Score
    score_text = small_font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10,10))
    # Difficulty
    diff_text = small_font.render(f"Difficulty: {difficulty}", True, TEXT_COLOR)
    screen.blit(diff_text, (10, 40))
    # Timer
    if timer_start:
        elapsed = int(time.time() - timer_start)
        remaining = max(0, time_limit - elapsed)
        timer_text = small_font.render(f"Time left: {remaining}s", True, TEXT_COLOR)
        screen.blit(timer_text, (WIDTH-200, 10))
    # Question
    question_text = font.render(question, True, TEXT_COLOR)
    screen.blit(question_text, (50,150))
    # Input box
    input_box = pygame.Rect(50, 250, 800, 60)
    pygame.draw.rect(screen, INPUT_COLOR, input_box)
    input_text = font.render(user_input, True, TEXT_COLOR)
    screen.blit(input_text, (input_box.x+10, input_box.y+10))
    # Feedback
    feedback_text = small_font.render(feedback, True, feedback_color)
    screen.blit(feedback_text, (50, 350))
    pygame.display.update()

# Main game loop
running = True
while running:
    draw_screen()
    # Timer check
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
            elif event.key == pygame.K_1:
                difficulty = 'Easy'
            elif event.key == pygame.K_2:
                difficulty = 'Medium'
            elif event.key == pygame.K_3:
                difficulty = 'Hard'
            else:
                # Robust input handling
                allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-+*/^()."
                if event.unicode in allowed_chars:
                    user_input += event.unicode
                elif pygame.K_0 <= event.key <= pygame.K_9:
                    user_input += str(event.key - pygame.K_0)
                elif pygame.K_KP0 <= event.key <= pygame.K_KP9:
                    user_input += str(event.key - pygame.K_KP0)
                elif event.key == pygame.K_PERIOD or event.key == pygame.K_KP_PERIOD:
                    user_input += "."
