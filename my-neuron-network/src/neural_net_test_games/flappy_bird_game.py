import pygame
from src.neural_net_test_games.game_objects import Bird, Pipe, PIPE_WIDTH, get_closest_pipe

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255, .5)

# Game variables
gravity = 0.2
pipe_velocity = -3

pipes = []
my_bird = Bird(y=HEIGHT//2, screen=screen, gravity=gravity)
ai_birds = [Bird(y=HEIGHT//2, screen=screen, gravity=gravity, color=WHITE)]

# Main game loop
running = True
clock = pygame.time.Clock()

# Create initial pipes
for i in range(4):
    ini_pos = screen.get_width() + i * 300
    pipes.append(Pipe(screen, ini_pos))

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            my_bird.jump()

    for ai_bird in ai_birds:
        ai_bird.think(get_closest_pipe(pipes))

    # Update pipes
    for pipe in pipes:
        if pipe.x_position + pipe_velocity > -PIPE_WIDTH:
            pipe.x_position += pipe_velocity
        else:
            pipe.x_position = screen.get_width()
            pipe.reset_pipe_structure()

    # Check for collisions
    # running = not my_bird.does_it_collide(pipes)

    # FLY THE BIRDS
    my_bird.fly()
    for ai_bird in ai_birds:
        ai_bird.fly()

    # DRAW PIPES
    for pipe in pipes:
        pipe.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
