import random
from typing import List
from pygame import Surface, draw, Rect, mask

BIRD_RADIUS = 10
CYAN = (0, 133, 133)
RED = (255, 0, 0)
PIPE_WIDTH = 30
MIN_PIPE_GAP = BIRD_RADIUS * 6
MAX_PIPE_GAP = 300


class Pipe:
    def __init__(self, screen: Surface, ini_x_position: int | None) -> None:
        self.screen = screen
        self.up_pipe_height = 0
        self.down_pipe_height = 0
        self.gap = 0
        self.x_position = ini_x_position if ini_x_position is not None else screen.get_width()

        self.reset_pipe_structure()

    def reset_pipe_structure(self):
        self.gap = random.randint(MIN_PIPE_GAP, MAX_PIPE_GAP)
        print(self.gap)
        self.down_pipe_height = random.randint(0, self.screen.get_height() - self.gap)
        self.up_pipe_height = self.screen.get_height() - self.gap - self.down_pipe_height

    def draw(self) -> None:
        # up pipe
        draw.rect(self.screen, CYAN, (self.x_position, 0, PIPE_WIDTH, self.up_pipe_height))
        # gap
        draw.rect(self.screen, RED, (self.x_position, self.up_pipe_height, PIPE_WIDTH, self.gap))
        # down pipe
        down_pipe_ini = self.gap + self.up_pipe_height
        draw.rect(self.screen, CYAN, (self.x_position, down_pipe_ini, PIPE_WIDTH, self.down_pipe_height))


class Bird:
    def __init__(self, screen: Surface, y: int, x: int = 50) -> None:
        self.screen = screen
        self.x = x
        self.y = y

    def does_it_collide(self, pipes: List[Pipe]) -> bool:
        bird_x = self.x + BIRD_RADIUS
        bird_y_up = self.y + BIRD_RADIUS
        bird_y_down = self.y - BIRD_RADIUS

        for pipe in pipes:
            if pipe.x_position < bird_x < pipe.x_position + PIPE_WIDTH:
                if bird_y_up < pipe.up_pipe_height or bird_y_down > pipe.up_pipe_height + pipe.gap:
                    return True

        return False

    def draw(self) -> None:
        draw.circle(self.screen, CYAN, (self.x, self.y), BIRD_RADIUS)
