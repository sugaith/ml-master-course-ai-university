import random
from pygame import Surface, draw

WHITE_LABEL = 1
CYAN_LABEL = 0
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_CYAN = (0, 255, 255)
POINT_RADIUS = 36


class Point:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.x = random.randint(0, screen.get_width())
        self.y = random.randint(0, screen.get_height())
        self.label = WHITE_LABEL if self.x > self.y else CYAN_LABEL
        self.fill_color = COLOR_BLACK

    def draw(self):
        color = COLOR_WHITE if self.label == WHITE_LABEL else COLOR_CYAN

        # fill
        draw.circle(self.screen, self.fill_color, (self.x, self.y), POINT_RADIUS / 2)
        # border
        draw.circle(self.screen, color, (self.x, self.y), POINT_RADIUS, 9)

    def set_fill(self, color: tuple):
        self.fill_color = color
