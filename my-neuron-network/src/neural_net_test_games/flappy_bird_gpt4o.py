import pygame
import random
from src.neural_net_test_games.Bird import BIRD_RADIUS, Bird

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game variables
my_bird = Bird(y=HEIGHT//2, screen=screen)

bird_radius = BIRD_RADIUS
bird_velocity = 0

gravity = 0.4
jump_strength = -5

pipe_width = 30
pipe_gap_min = 150
pipe_gap_max = 260
pipe_velocity = -3
pipes = []

score = 0

# Font for score
font = pygame.font.SysFont(None, 36)


# Function to create new pipe
def create_pipe():
    pipe_height = random.randint(0, HEIGHT // 3)
    pipe_gap = random.randint(pipe_gap_min, pipe_gap_max)
    return [WIDTH, pipe_height, pipe_height // 2 + pipe_gap]


# Main game loop
running = True
clock = pygame.time.Clock()

# Create initial pipes
for i in range(2):
    pipes.append(create_pipe())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity = jump_strength

    # Update bird position
    bird_velocity += gravity
    my_bird.y += bird_velocity

    # Update pipes
    pipes = [[x + pipe_velocity, h1, h2] for x, h1, h2 in pipes if x + pipe_velocity > -pipe_width]

    # Add new pipe if needed
    if pipes[-1][0] < WIDTH // 2:
        pipes.append(create_pipe())

    # Check for collisions
    for x, h1, h2 in pipes:
        if my_bird.x + bird_radius > x and my_bird.x - bird_radius < x + pipe_width:
            if my_bird.y - bird_radius < h1 or my_bird.y + bird_radius > h2:
                running = False

    if my_bird.y + bird_radius > HEIGHT or my_bird.y - bird_radius < 0:
        running = False

    # Increment score 
    # if pipes[0][0] < bird_x + bird_radius and running:
    #     score += 1

    # Draw everything
    screen.fill(BLACK)
    # pygame.draw.circle(screen, WHITE, (bird_x, my_bird.y), bird_radius)
    my_bird.draw()
    for x, h1, h2 in pipes:
        pygame.draw.rect(screen, WHITE, (x, 0, pipe_width, h1))
        pygame.draw.rect(screen, WHITE, (x, h2, pipe_width, HEIGHT - h2))

    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
