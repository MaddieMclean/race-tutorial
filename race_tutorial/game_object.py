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
        self.collision_rect = self.build_collision_rect(0.2)

    def update_position(self, change: utl.Point):
        super().update_position(change)
        self.collision_rect.center = self.rect.center

    def build_collision_rect(self, shrink_factor: float) -> pygame.Rect:
        width = -int(self.rect.width * shrink_factor)
        height = -int(self.rect.height * shrink_factor)
        return self.rect.copy().inflate(width, height)

    def crash(self, surface: pygame.Surface):
        font = pygame.font.Font("freesansbold.ttf", 115)
        text_surface = font.render(self.crash_text, True, utl.BLACK)
        surface.blit(text_surface, utl.center_surface(text_surface))
        pygame.display.update()
        time.sleep(2)

    def collided(self, objects: List[GameObject]) -> bool:
        if self.collision_rect.collidelist([obj.rect for obj in objects]) != -1:
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
        self.score_value = int((dimensions.x * dimensions.y) / 100)
        super().__init__(img, starting_location, speed)

    @property
    def y(self) -> int:
        return self.rect.y

    @y.setter
    def y(self, v: int):
        self.rect.y = v
