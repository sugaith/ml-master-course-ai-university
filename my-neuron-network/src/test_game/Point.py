import random
from pygame import Surface, draw

WHITE_LABEL = 1
CYAN_LABEL = 0
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
cyan = (0, 255, 255)
radius = 36


class Point:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.x = random.randint(0, screen.get_width())
        self.y = random.randint(0, screen.get_height())
        self.label = WHITE_LABEL if self.x > self.y else CYAN_LABEL
        self.fill_color = black

    def draw(self):
        color = white if self.label == WHITE_LABEL else cyan

        # fill
        draw.circle(self.screen, self.fill_color, (self.x, self.y), radius / 2)
        # border
        draw.circle(self.screen, color, (self.x, self.y), radius, 9)

    def set_fill(self, color: tuple):
        self.fill_color = color
