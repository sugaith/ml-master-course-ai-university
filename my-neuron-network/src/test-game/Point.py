import random
from pygame import Surface, draw

WHITE_LABEL = 1
BLACK_LABEL = 0
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
radius = 45


class Point:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.x = random.randint(0, screen.get_width())
        self.y = random.randint(0, screen.get_height())
        self.label = WHITE_LABEL if self.x > self.y else BLACK_LABEL

    def draw(self):
        color = white if self.label == WHITE_LABEL else black

        draw.circle(self.screen, color, (self.x, self.y), radius)
        # White border
        draw.circle(self.screen, white, (self.x, self.y), radius, 3)
