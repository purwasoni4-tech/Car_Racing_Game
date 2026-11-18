
import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (30, 150, 50)
DARK_GREEN = (20, 110, 35)
GREY = (65, 65, 65)
YELLOW = (255, 220, 0)
RED = (220, 30, 30)
BLUE = (30, 100, 255)

# Clock and fonts
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25, bold=True)
big_font = pygame.font.SysFont("Arial", 38, bold=True)
small_font = pygame.font.SysFont("Arial", 20)

# Car settings
CAR_WIDTH = 45
CAR_HEIGHT = 80

# Player car
player_x = 177
player_y = 480
player_speed = 5

# Obstacle cars
obstacles = []
obstacle_speed = 5

# Score
score = 0
game_over = False

# Road settings
road_x = 60
road_width = 280
line_y = 0


def draw_car(x, y, color):
    # Car body
    pygame.draw.rect(
        screen, color,
        (x, y, CAR_WIDTH, CAR_HEIGHT),
        border_radius=8
    )

    # Windows
    pygame.draw.rect(
        screen, (150, 220, 255),
        (x + 8, y + 12, 29, 18),
        border_radius=4
    )

    pygame.draw.rect(
        screen, (150, 220, 255),
        (x + 8, y + 48, 29, 15),
        border_radius=4
    )

    # Wheels
    pygame.draw.rect(screen, BLACK, (x - 5, y + 12, 7, 18))
    pygame.draw.rect(screen, BLACK, (x + 43, y + 12, 7, 18))
    pygame.draw.rect(screen, BLACK, (x - 5, y + 53, 7, 18))
    pygame.draw.rect(screen, BLACK, (x + 43, y + 53, 7, 18))


def create_obstacle():
    x = random.choice([85, 175, 265])
    y = -CAR_HEIGHT
    color = random.choice([RED, BLUE, YELLOW])
    return [x, y, color]


def reset_game():
    global player_x, obstacles, score
    global obstacle_speed, game_over, line_y

    player_x = 177
    obstacles = []
    score = 0
    obstacle_speed = 5
    game_over = False
    line_y = 0


def draw_road():
    global line_y

    screen.fill(GREEN)

    # Road
    pygame.draw.rect(
        screen, GREY,
        (road_x, 0, road_width, HEIGHT)
    )

    # Road borders
    pygame.draw.rect(
        screen, WHITE,
        (road_x, 0, 5, HEIGHT)
    )

    pygame.draw.rect(
        screen, WHITE,
        (road_x + road_width - 5, 0, 5, HEIGHT)
    )

    # Moving road divider
    for y in range(-40, HEIGHT, 100):
        pygame.draw.rect(
            screen, WHITE,
            (197, y + line_y, 6, 50)
        )

    line_y += obstacle_speed

    if line_y >= 100:
        line_y = 0


def show_score():
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))


# Main game loop
running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over:

        # Player movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Keep player inside road
        player_x = max(65, min(player_x, 290))

        # Draw background and road
        draw_road()

        # Create obstacles
        if len(obstacles) == 0:
            obstacles.append(create_obstacle())

        if obstacles[-1][1] > 160 and len(obstacles) < 3:
            obstacles.append(create_obstacle())

        # Move and draw obstacles
        for obstacle in obstacles[:]:

            obstacle[1] += obstacle_speed

            draw_car(
                obstacle[0],
                obstacle[1],
                obstacle[2]
            )

            # Collision detection
            player_rect = pygame.Rect(
                player_x, player_y,
                CAR_WIDTH, CAR_HEIGHT
            )

            obstacle_rect = pygame.Rect(
                obstacle[0], obstacle[1],
                CAR_WIDTH, CAR_HEIGHT
            )

            if player_rect.colliderect(obstacle_rect):
                game_over = True

            # Remove obstacles after leaving screen
            if obstacle[1] > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

                # Increase difficulty
                if score % 5 == 0:
                    obstacle_speed += 1

        # Draw player car
        draw_car(player_x, player_y, BLUE)

        # Display score
        show_score()

    else:

        # Game over screen
        screen.fill(BLACK)

        game_over_text = big_font.render(
            "GAME OVER", True, RED
        )

        score_text = font.render(
            "Final Score: " + str(score),
            True, WHITE
        )

        restart_text = small_font.render(
            "Press R to Restart",
            True, YELLOW
        )

        quit_text = small_font.render(
            "Press X to Exit",
            True, WHITE
        )

        screen.blit(
            game_over_text,
            (WIDTH // 2 - game_over_text.get_width() // 2, 200)
        )

        screen.blit(
            score_text,
            (WIDTH // 2 - score_text.get_width() // 2, 270)
        )

        screen.blit(
            restart_text,
            (WIDTH // 2 - restart_text.get_width() // 2, 340)
        )

        screen.blit(
            quit_text,
            (WIDTH // 2 - quit_text.get_width() // 2, 380)
        )

        keys = pygame.key.get_pressed()

        if keys[pygame.K_x]:
            running = False

    pygame.display.update()

pygame.quit()
sys.exit()
