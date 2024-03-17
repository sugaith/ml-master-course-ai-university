import pygame as pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Random Circles")

# Define colors
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)


# Function to draw circles
def draw_circle(x, y):
    radius = 45  # Randomize the radius

    color = red if x > y else black

    pygame.draw.circle(screen, color, (x, y), radius)
    pygame.draw.circle(screen, white, (x, y), radius, 3)  # White border


positions = [
    {'x': random.randint(0, screen_width), 'y': random.randint(0, screen_height)}
    for _ in range(60)
]

# Fill the background with black color
screen.fill(black)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for pos in positions:
        draw_circle(pos['x'], pos['y'])

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
