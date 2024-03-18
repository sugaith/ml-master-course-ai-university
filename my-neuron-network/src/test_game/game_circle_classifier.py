import numpy as np
import pygame as pygame
from src.test_game.Point import Point
from typing import List
from src.model.Perceptron import Perceptron
from src.model.activation_functions import step

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
green = (0, 255, 0)
white = (255, 255, 255)

# Fill the background with black color
screen.fill(black)

# initiate points
points: List[Point] = [Point(screen) for _ in range(100)]

perceptron = Perceptron(step)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for point in points:
        point.draw()
        guess = perceptron.guess(np.array([point.x, point.y]))
        point.set_fill(green if guess == point.label else red)
        # pygame.time.delay(3)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
