import numpy as np
import pygame as pygame
from typing import List
from Point import Point, UP_RIGHT, UP_LEFT, DOWN_LEFT, DOWN_RIGHT
from src.model.Perceptron import Perceptron
from src.model.activation_functions import step, sigmoid, hyperbolic_tangent
from src.model.normalization_functions import normalize_value

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1200
screen_height = 1200
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
points: List[Point] = [Point(screen) for _ in range(90)]
# centerPoint = Point(screen)
# centerPoint.x = 123
# centerPoint.y = screen_height / 2 - 232
# points: List[Point] = [centerPoint]


def custom_activation(value: np.float32) -> np.float32:
    print(value, 'value')
    print(sigmoid(value), 'sigmoid(value)')
    # to return a float [1 and 5]
    return 4 * sigmoid(value) + 1


def get_guess_color(guess: np.float32, label: int) -> tuple:
    quadrant = 0
    if 1 <= guess < 2:
        quadrant = UP_LEFT
    elif 2 <= guess < 3:
        quadrant = DOWN_LEFT
    elif 3 <= guess < 4:
        quadrant = UP_RIGHT
    elif 4 <= guess <= 5:
        quadrant = DOWN_RIGHT
    return green if quadrant == label else red


perceptron = Perceptron(
    activation_function=custom_activation,
    number_of_params=2
)


def main_loop_content():
    for point in points:
        point.draw()

        point_data = np.array([
            normalize_value(point.x, np.float32(screen_width)),
            normalize_value(point.y, np.float32(screen_height)),
        ])

        perceptron.train(point_data, point.get_label())
        guess = perceptron.guess(point_data)

        point.set_fill(get_guess_color(guess, point.get_label()))


# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    main_loop_content()
    # pygame.time.delay(3)
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
