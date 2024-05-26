import random

from pygame import Surface, draw

WHITE_LABEL = 1
CYAN_LABEL = 0
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_CYAN = (0, 255, 255)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
POINT_RADIUS = 36

UP_LEFT = 1
DOWN_LEFT = 2
UP_RIGHT = 3
DOWN_RIGHT = 4


class Point:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.x = random.randint(0, screen.get_width())
        self.y = random.randint(0, screen.get_height())
        self.fill_color = COLOR_BLACK

    def get_label(self):
        middle_width = int(self.screen.get_width() / 2)
        middle_height = int(self.screen.get_height() / 2)

        if self.x < middle_width and self.y < middle_height:
            return UP_LEFT
        elif self.x < middle_width and self.y > middle_height:
            return DOWN_LEFT
        elif self.x > middle_width and self.y < middle_height:
            return UP_RIGHT
        elif self.x > middle_width and self.y > middle_height:
            return DOWN_RIGHT

    def draw(self):
        color = COLOR_WHITE if self.get_label() == UP_LEFT \
            else COLOR_BLUE if self.get_label() == UP_RIGHT \
            else COLOR_CYAN if self.get_label() == DOWN_LEFT \
            else COLOR_YELLOW

        # fill
        draw.circle(self.screen, self.fill_color, (self.x, self.y), POINT_RADIUS / 2)
        # border
        draw.circle(self.screen, color, (self.x, self.y), POINT_RADIUS, 9)

    def set_fill(self, color: tuple):
        self.fill_color = color
