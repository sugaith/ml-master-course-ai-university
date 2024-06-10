from typing import List
import random
import numpy as np
from pygame import Surface, draw, SRCALPHA
from src.model.NeuralNet import NeuralNet
from src.model.activation_functions import sigmoid
from src.model.initialization_functons import xavier_normal_distribution

BIRD_X_POS = 50
BIRD_RADIUS = 10
CYAN = (0, 133, 133)
RED = (255, 0, 0)
PIPE_WIDTH = 30
MIN_PIPE_GAP = BIRD_RADIUS * 2 * 1.5
MAX_PIPE_GAP = 150
JUMP_STRENGTH = -4.5
WHITE = (255, 255, 255)


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
    def __init__(self,
                 screen: Surface, gravity: float, y: int = None, x: int = BIRD_X_POS, color=WHITE,
                 brain: NeuralNet | None = None) -> None:
        self.screen = screen
        self.color = color
        self.gravity = gravity
        self.x = x
        self.y = screen.get_height() // 2
        self.bird_velocity = 0
        """" for now on NeuralNet, lets get only the first pipe as input:
          input1: self y position
          input2: closest pipe x pos
          input3: closest bottom pipe y (or bottom y of gap)
          input4: closest upper pipe y (or top y of gap)
        """
        if brain is None:
            self.brain = NeuralNet(
                4, 4, 1,
                # initialization=xavier_normal_distribution,
                activation=sigmoid,
                learning_rate=np.float32(.3)
            )
        else:
            self.brain = brain

        self.score = 1
        self.fitness = 0

    def jump(self):
        self.bird_velocity = JUMP_STRENGTH
        if self.y < 0 or self.y > self.screen.get_height():
            self.bird_velocity += self.gravity
            self.y += self.bird_velocity

    def think(self, closest_pipe: Pipe):
        inputs = np.array([
            self.y / self.screen.get_height(),
            closest_pipe.x_position / self.screen.get_width(),
            closest_pipe.up_pipe_height / self.screen.get_height(),
            (closest_pipe.up_pipe_height + closest_pipe.gap) / self.screen.get_height()
        ])
        action = self.brain.feed_forward(inputs)
        if action > .6:
            self.jump()

    def does_it_collide(self, pipes: List[Pipe]) -> bool:
        bird_x = self.x + BIRD_RADIUS
        bird_y_up = self.y + BIRD_RADIUS
        bird_y_down = self.y - BIRD_RADIUS

        for pipe in pipes:
            if pipe.x_position < bird_x < pipe.x_position + PIPE_WIDTH:
                if not (bird_y_up < pipe.up_pipe_height or bird_y_down > pipe.up_pipe_height + pipe.gap):
                    self.score += 1
                    return False
                else:
                    return True

    def fly(self) -> None:
        # cant go bellow the ground
        if self.y < self.screen.get_height():
            self.bird_velocity += self.gravity
            self.y += self.bird_velocity

        # all of this code for transparency... sigh
        circle_surface = Surface((BIRD_RADIUS * 2, BIRD_RADIUS * 2), SRCALPHA)
        transparent_color = self.color + (128,)
        draw.circle(circle_surface, transparent_color, (BIRD_RADIUS, BIRD_RADIUS), BIRD_RADIUS)
        self.screen.blit(circle_surface, (self.x - BIRD_RADIUS, self.y - BIRD_RADIUS))


def calc_fitness(population: List[Bird]):
    score_sum = 0
    for bird in population:
        score_sum += bird.score

    for bird in population:
        bird.fitness = bird.score / score_sum


def spawn_bird_generation(screen: Surface, gravity, count: int, previous_gen: None | List[Bird] = None) -> List[Bird]:
    if previous_gen is None:
        return [Bird(screen=screen, gravity=gravity) for _ in range(count)]

    calc_fitness(previous_gen)
    previous_gen.sort(key=lambda dead_bird: dead_bird.fitness, reverse=True)

    best_ones = previous_gen[:9]
    for i, bird in enumerate(reversed(best_ones)):
        bird.score += i

    print('previous_gen_count')
    print(len(previous_gen))
    previous_gen[:] = previous_gen[:3000]

    next_gen = [*best_ones]

    children_count = (count - len(best_ones)) // len(best_ones)

    mutation_rate = np.float32(.09)
    for best_one in best_ones:
        next_gen += [
            Bird(screen=screen, gravity=gravity, brain=best_one.brain.clone_and_mutate(mutation_rate))
            for _ in range(children_count)
        ]

    return next_gen
