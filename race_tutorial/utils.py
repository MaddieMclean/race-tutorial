from collections import namedtuple
from typing import Callable, List, Tuple

import pygame

from addict import Dict

IMAGE_PATH = "race_tutorial/images"

NEUTRAL = 0
LEFT = -1
RIGHT = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

GAME_EVENTS = (pygame.QUIT, pygame.USEREVENT)
CONTROLS = Dict(
    TYPES=(pygame.KEYUP, pygame.KEYDOWN), KEYS=(pygame.K_LEFT, pygame.K_RIGHT)
)

Point = namedtuple("Point", ["x", "y"])

WINDOW_SIZE = Point(x=800, y=600)
CENTER_POINT = Point(x=WINDOW_SIZE.x / 2, y=WINDOW_SIZE.y / 2)
STARTING_POINT = Point(x=WINDOW_SIZE.x * 0.45, y=WINDOW_SIZE.y * 0.8)


def bound(low: int = 0, high: int = WINDOW_SIZE.x) -> Callable[[int], int]:
    def bounded(val: int) -> int:
        return max(low, min(high, val))

    return bounded


def center_surface(surface: pygame.Surface) -> pygame.Rect:
    return position_rect(surface.get_rect(), CENTER_POINT)


def timer_settings(val: int) -> Tuple[int, int]:
    return pygame.USEREVENT, val * 1000


def position_rect(rect: pygame.Rect, point: Point) -> pygame.Rect:
    rect.center = point
    return rect


def valid_event(event: pygame.event) -> bool:
    if event.type in GAME_EVENTS or (
        event.type in CONTROLS.TYPES and event.key in CONTROLS.KEYS
    ):
        return True

    return False


def build_lanes(width: int) -> List[int]:
    return [n * width for n in range(int(WINDOW_SIZE.x / width))]
