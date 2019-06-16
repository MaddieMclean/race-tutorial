import random
import time
from typing import List, Tuple

import pygame

import race_tutorial.utils as utl


class GameObject(object):
    def __init__(
        self,
        img: pygame.Surface,
        starting_location: utl.Point,
        dimensions: utl.Point,
        speed: int,
    ):
        self.img = img
        self.rect = img.get_rect()
        self.speed = speed
        self.width = dimensions.x
        self.height = dimensions.y

        self.bound_x = utl.bound(high=utl.WINDOW_SIZE.x - self.width)
        self.bound_y = utl.bound(high=utl.WINDOW_SIZE.y - self.height)

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
        speed = 5
        dimensions = utl.Point(x=73, y=0)
        img = pygame.image.load(f"{utl.IMAGE_PATH}/racecar.png")
        super().__init__(img, starting_location, dimensions, speed)

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
        super().__init__(img, starting_location, dimensions, speed)

    @property
    def y(self) -> int:
        return self.rect.y

    @y.setter
    def y(self, v: int):
        self.rect.y = v

    @staticmethod
    def spawn(number: int):
        start = utl.Point(x=random.randint(0, utl.WINDOW_SIZE.x), y=-100)
        dimensions = utl.Point(x=50, y=50)
        speed = random.randint(2, 8)
        return [
            Obstacle(start, dimensions, speed, colour=utl.RED) for _ in range(number)
        ]
