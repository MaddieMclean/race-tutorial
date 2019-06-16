import random
import time
from typing import List, Tuple

import pygame

import race_tutorial.utils as utl


class GameObject(object):
    def __init__(self, img: pygame.Surface, starting_location: utl.Point, speed: int):
        self.img = img
        self.rect = img.get_rect()
        self.speed = speed

        self.bound_x = utl.bound(high=utl.WINDOW_SIZE.x - self.rect.width)
        self.bound_y = utl.bound(high=utl.WINDOW_SIZE.y - self.rect.height)

        self.x = starting_location.x
        self.y = starting_location.y

    @property
    def x(self) -> int:
        return self.rect.x

    @property
    def y(self) -> int:
        return self.rect.y

    @x.setter
    def x(self, v: int):
        self.rect.x = self.bound_x(v)

    @y.setter
    def y(self, v: int):
        self.rect.y = self.bound_y(v)

    def update_position(self, change: utl.Point):
        self.x += change.x
        self.y += change.y

    def draw(self) -> Tuple[pygame.Surface, Tuple[int, int]]:
        return self.img, utl.Point(x=self.x, y=self.y)


class Car(GameObject):
    def __init__(self, starting_location: utl.Point):
        speed = 10
        img = pygame.image.load(f"{utl.IMAGE_PATH}/racecar.png")
        super().__init__(img, starting_location, speed)

        self.crash_text = "You Crashed"

    def crash(self, surface: pygame.Surface):
        font = pygame.font.Font("freesansbold.ttf", 115)
        text_surface = font.render(self.crash_text, True, utl.BLACK)
        surface.blit(text_surface, utl.center_surface(text_surface))
        pygame.display.update()
        time.sleep(2)

    def collided(self, objects: List[GameObject]) -> bool:
        if self.rect.collidelist([obj.rect for obj in objects]) != -1:
            return True
        return False


class Obstacle(GameObject):
    def __init__(
        self,
        starting_location: utl.Point,
        dimensions: utl.Point,
        speed: int,
        colour: Tuple[int, int, int],
    ):
        img = pygame.Surface(dimensions)
        img.fill(colour)
        super().__init__(img, starting_location, speed)

    @property
    def y(self) -> int:
        return self.rect.y

    @y.setter
    def y(self, v: int):
        self.rect.y = v

    @classmethod
    def spawn(cls, number: int, width: int = 50):
        lanes = utl.build_lanes(width)
        start = utl.Point(x=lanes[random.randrange(len(lanes))], y=-100)
        dimensions = utl.Point(x=width, y=width)
        speed = random.randint(2, 8)
        return [
            Obstacle(start, dimensions, speed, colour=utl.RED) for _ in range(number)
        ]
