import pygame
import sys
import random
import mysql.connector

# Initialize Pygame
pygame.init()
# Constants Declaration
WIDTH, HEIGHT = 800, 600
FPS = 10
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# Snake properties
snake_size = 20
snake_speed = 20
snake = [(100, 100), (90, 100), (80, 100)]
snake_direction = (snake_speed, 0)
# Food properties
food_size = 20
food_position = (random.randrange(1, (WIDTH // food_size)) * food_size,
                 random.randrange(1, (HEIGHT // food_size)) * food_size)
# Score initialize with 0
score = 0
# Database initialization
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hb57115",
    database="snake"
)
cursor = conn.cursor()
# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS scores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    score INT
                )''')
# Game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
# Font for displaying text
font = pygame.font.SysFont('Arial', 50)


# Function to draw snake on the screen
def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], snake_size, snake_size))


# Function to draw food on the screen
def draw_food():
    pygame.draw.rect(screen, RED, pygame.Rect(food_position[0], food_position[1], food_size, food_size))


# Function to display score on the screen
def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


# Function to display game over screen
def show_game_over():
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))


# Function to display high score message in a dialog box
def show_high_score_message():
    high_score_text = font.render("Congratulations! You got a high score!", True, WHITE)
    screen.blit(high_score_text, (WIDTH // 2 - 300, HEIGHT // 2 - 100))


# Function to handle game over logic
def game_over():
    global score
    show_game_over()
    check_high_score(score)
    pygame.display.flip()
    pygame.time.delay(2000)  # Delay for 2 seconds before quitting
    pygame.quit()
    sys.exit()


# Function to check high score
def check_high_score(scores):
    cursor.execute("SELECT MAX(score) FROM scores")
    highest_score = cursor.fetchone()[0]
    if highest_score is None or scores > highest_score:
        # Minimize the game window
        pygame.display.iconify()
        name = input("Enter your name: ")
        cursor.execute("INSERT INTO scores (name, score) VALUES (%s, %s)", (name, scores))
        conn.commit()
        print("High score saved successfully!")
        show_high_score_message()


# Set running to True
running = True
# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != (0, snake_speed):
                snake_direction = (0, -snake_speed)
            elif event.key == pygame.K_DOWN and snake_direction != (0, -snake_speed):
                snake_direction = (0, snake_speed)
            elif event.key == pygame.K_LEFT and snake_direction != (snake_speed, 0):
                snake_direction = (-snake_speed, 0)
            elif event.key == pygame.K_RIGHT and snake_direction != (-snake_speed, 0):
                snake_direction = (snake_speed, 0)
    snake_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
    snake.insert(0, snake_head)
    if snake[0] == food_position:
        food_position = (random.randrange(1, (WIDTH // food_size)) * food_size,
                         random.randrange(1, (HEIGHT // food_size)) * food_size)
        score += 1
    else:
        snake.pop()
    if (snake_head[0] < 0 or snake_head[0] >= WIDTH or
            snake_head[1] < 0 or snake_head[1] >= HEIGHT or
            snake_head in snake[1:]):
        game_over()
    screen.fill(BLACK)
    draw_snake()
    draw_food()
    show_score()
    pygame.display.flip()

    pygame.time.Clock().tick(FPS)
# Quit Pygame
pygame.quit()
sys.exit()
