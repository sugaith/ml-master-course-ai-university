from typing import List
import random
import numpy as np
from pygame import Surface, draw, Rect, mask
from src.model.NeuralNet import NeuralNet
from src.model.activation_functions import sigmoid
from src.model.initialization_functons import xavier_normal_distribution

BIRD_X_POS = 50
BIRD_RADIUS = 10
CYAN = (0, 133, 133)
RED = (255, 0, 0)
PIPE_WIDTH = 30
MIN_PIPE_GAP = BIRD_RADIUS * 6
MAX_PIPE_GAP = 300
JUMP_STRENGTH = -4


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


def get_closest_pipe(pipes: List[Pipe]) -> Pipe:
    closest_pipe = pipes[0]
    for pipe in pipes:
        if BIRD_X_POS < pipe.x_position < closest_pipe.x_position:
            closest_pipe = pipe

    return closest_pipe


class Bird:
    def __init__(self, screen: Surface, gravity: float, y: int, x: int = BIRD_X_POS, color=CYAN) -> None:
        self.gravity = gravity
        self.bird_velocity = 0
        self.color = color
        self.screen = screen
        self.x = x
        self.y = y
        """" for now, lets get only the first pipe as input:
          input1: self y position
          input2: closest pipe x pos
          input3: closest bottom pipe y (or bottom y of gap)
          input4: closest upper pipe y (or top y of gap)
        """
        self.brain = NeuralNet(
            4, 4, 1,
            initialization=xavier_normal_distribution,
            activation=sigmoid,
            learning_rate=np.float32(.3)
        )

    def jump(self):
        self.bird_velocity = JUMP_STRENGTH

    def think(self, closest_pipe: Pipe):
        inputs = np.array([
            self.y / self.screen.get_height(),
            closest_pipe.x_position / self.screen.get_width(),
            closest_pipe.up_pipe_height / self.screen.get_height(),
            (closest_pipe.up_pipe_height + closest_pipe.gap) / self.screen.get_height()
        ])
        action = self.brain.feed_forward(inputs)
        print("action....")
        print(action)
        if action > .6:
            self.jump()

    def does_it_collide(self, pipes: List[Pipe]) -> bool:
        bird_x = self.x + BIRD_RADIUS
        bird_y_up = self.y + BIRD_RADIUS
        bird_y_down = self.y - BIRD_RADIUS

        for pipe in pipes:
            if pipe.x_position < bird_x < pipe.x_position + PIPE_WIDTH:
                if bird_y_up < pipe.up_pipe_height or bird_y_down > pipe.up_pipe_height + pipe.gap:
                    return True
        return False

    def fly(self) -> None:
        self.bird_velocity += self.gravity
        self.y += self.bird_velocity
        draw.circle(self.screen, self.color, (self.x, self.y), BIRD_RADIUS)
