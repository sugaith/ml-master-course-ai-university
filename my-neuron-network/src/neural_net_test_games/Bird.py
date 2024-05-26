
from pygame import Surface, draw
BIRD_RADIUS = 10
WHITE = (255, 255, 255)


class Bird:
    def __init__(self, screen: Surface, y: int, x: int = 50) -> None:
        self.screen = screen
        self.x = x
        self.y = y

    def draw(self) -> None:
        draw.circle(self.screen, WHITE, (self.x, self.y), BIRD_RADIUS)
