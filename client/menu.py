import pygame
import socket
import sys

# Initialize Pygame
pygame.init()

GAME_NAME = "CTRL ALT THINK"

# Game Window dimensions
WIDTH, HEIGHT = 1980, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_NAME)

# Fonts
font = pygame.font.SysFont("Menlo", 36)
button_font = pygame.font.SysFont("Menlo", 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (50, 150, 255)


# Function to draw the main menu screen
def draw_main_menu(player_name):
    screen.fill(WHITE)

    title_text = font.render(GAME_NAME, True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    name_input_box = pygame.Rect(WIDTH // 2 - 150, 200, 300, 60)
    pygame.draw.rect(screen, BLACK, name_input_box, 2)
    name_text = font.render(player_name, True, BLACK)
    screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, 200 + 10))

    # Buttons
    start_button = pygame.Rect(WIDTH // 2 - 150, 300, 300, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, start_button)
    start_text = button_font.render("Start Game", True, WHITE)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 310))

    pygame.display.flip()


# Function to handle events for the main menu
def main_menu():
    # Textbox for player name
    player_name = ""

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_RETURN and player_name:
                    return player_name  # Proceed to the game with the player name
                else:
                    player_name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # if start_button.collidepoint(mouse_x, mouse_y):
                #     if player_name:
                #         return player_name  # Proceed to the game
        draw_main_menu(player_name)


# Challenge Screen
def draw_challenge_screen(challenge, code_input, feedback):
    screen.fill(WHITE)

    # Title text
    title_text = font.render(f"Challenge: {challenge}", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # Code Editor Box
    code_input_box = pygame.Rect(50, 150, WIDTH - 100, 300)
    pygame.draw.rect(screen, BLACK, code_input_box, 2)
    pygame.draw.rect(screen, WHITE, code_input_box)  # Fill white so we can see the text inside

    # Render the player's code (simulating an editor)
    code_text = font.render(code_input, True, BLACK)
    screen.blit(code_text, (60, 160))

    # Feedback Section
    feedback_text = font.render(f"Feedback: {feedback}", True, BLACK)
    screen.blit(feedback_text, (WIDTH // 2 - feedback_text.get_width() // 2, 500))

    pygame.display.flip()


# A function to simulate sending the code to the server and receiving feedback
def send_solution_to_server(solution_code):
    # Here, you'd normally send the solution to the server and get feedback
    # For now, we'll simulate it with a fixed feedback
    return "Correct!" if solution_code.strip() == "print('Hello, World!')" else "Try again!"


# Handle challenge screen input
def challenge_screen():

    # Simulated Challenge Data
    challenge = "Print 'Hello, World!'"

    code_input = ""
    feedback = "Enter your solution above..."

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    code_input = code_input[:-1]
                elif event.key == pygame.K_RETURN:
                    # Simulate sending code to server and getting feedback
                    feedback = send_solution_to_server(code_input)
                else:
                    code_input += event.unicode
        draw_challenge_screen(challenge, code_input, feedback)


def draw_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 150, 50))


if __name__ == "__main__":
    # Run the main menu to get the player name
    player_name = main_menu()
    # Run the challenge screen
    challenge_screen()
