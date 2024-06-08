import pygame
import random
from src.neural_net_test_games.game_objects import BIRD_RADIUS, Bird, Pipe, PIPE_WIDTH

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game variables
my_bird = Bird(y=HEIGHT//2, screen=screen)

bird_radius = BIRD_RADIUS
bird_velocity = 0

gravity = 0.2
jump_strength = -3

pipe_width = 30
pipe_gap_min = 150
pipe_gap_max = 260
pipe_velocity = -3
pipes = []

score = 0

# Font for score
font = pygame.font.SysFont(None, 36)

# Main game loop
running = True
clock = pygame.time.Clock()

# Create initial pipes
for i in range(4):
    ini_pos = screen.get_width() + i * 300
    pipes.append(Pipe(screen, ini_pos))

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
    for pipe in pipes:
        if pipe.x_position + pipe_velocity > -PIPE_WIDTH:
            pipe.x_position += pipe_velocity
        else:
            pipe.x_position = screen.get_width()
            pipe.reset_pipe_structure()

    # Check for collisions
    print('does it collide?  ', my_bird.does_it_collide(pipes))
    running = not my_bird.does_it_collide(pipes)

    # Increment score 
    # if pipes[0][0] < bird_x + bird_radius and running:
    #     score += 1

    # DRAW ALL THE SHIT
    screen.fill(BLACK)

    my_bird.draw()

    for pipe in pipes:
        pipe.draw()

    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
