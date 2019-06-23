import random
from typing import Tuple

from race_tutorial import game_object
from race_tutorial import utils as utl


class ObstacleManager(object):
    def __init__(
        self,
        colour: Tuple[tuple] = (utl.RED, utl.BLUE, utl.GREEN),
        dimension: Tuple[int] = (50, 100, 150, 200),
        speed: range = range(2, 6),
    ):
        self.objects = list()
        self.colour = colour
        self.dimension = dimension
        self.speed = speed

    def update(self, score: int) -> int:
        to_delete = list()

        for i, obstacle in enumerate(self.objects):
            obstacle.update_position(utl.Point(y=obstacle.speed, x=0))
            if obstacle.y > utl.WINDOW_SIZE.y:
                to_delete.append(i)

        for i in sorted(to_delete, reverse=True):
            obj = self.objects.pop(i)
            score += obj.score_value

        return score

    def spawn(self, level: int):
        max_on_screen = level * 2
        if len(self.objects) < max_on_screen:
            number_to_spawn = max_on_screen - len(self.objects)
            self.objects.extend(
                [self.random_obstacle() for _ in range(number_to_spawn)]
            )

    def random_obstacle(self) -> game_object.Obstacle:
        position = utl.Point(x=random.randrange(0, utl.WINDOW_SIZE.x, 50), y=-300)
        dimensions = utl.Point(
            x=random.choice(self.dimension), y=random.choice(self.dimension)
        )
        speed = random.choice(self.speed)
        colour = random.choice(self.colour)
        return game_object.Obstacle(position, dimensions, speed, colour)
