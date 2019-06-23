import pygame

import race_tutorial.utils as utl
from race_tutorial import game_object, manager


class GameLoop(object):
    def __init__(self, caption, window, frame_limit, level=1, level_time=20):
        pygame.init()
        pygame.time.set_timer(*utl.timer_settings(level_time))
        pygame.display.set_caption(caption)

        self._level = 0
        self.score = 0
        self.bound_level = utl.bound(high=10)
        self.game_display = pygame.display.set_mode(window)
        self.clock = pygame.time.Clock()
        self.frame_limit = frame_limit
        self.level = level
        self.font = pygame.font.SysFont(None, 25)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, v: int):
        self._level = self.bound_level(v)

    def run(self):
        crashed = False
        car_change = utl.NEUTRAL
        car = game_object.Car(utl.STARTING_POINT)
        obstacles = manager.ObstacleManager()

        while not crashed:
            car_change = self.event(car_change)
            crashed = self.update(car, obstacles, car_change)
            self.draw(car, obstacles, crashed)
            self.clock.tick(self.frame_limit)

    def event(self, car_change: int) -> int:
        events = [e for e in pygame.event.get() if utl.valid_event(e)]

        for e in events:
            if e.type == pygame.QUIT:
                return pygame.QUIT
            elif e.type == pygame.USEREVENT:
                self.level += 1
            elif e.type == pygame.KEYUP:
                car_change = utl.NEUTRAL
            else:
                if e.key == pygame.K_RIGHT:
                    car_change = utl.RIGHT
                elif e.key == pygame.K_LEFT:
                    car_change = utl.LEFT

        return car_change

    def update(
        self, car: game_object.Car, obstacles: manager.ObstacleManager, car_change: int
    ) -> bool:
        if car_change == pygame.QUIT:
            return True

        car.update_position(utl.Point(x=car_change * car.speed, y=0))
        obstacles.spawn(self.level)
        self.score = obstacles.update(self.score)
        return car.collided(obstacles.objects)

    def draw(
        self, car: game_object.Car, obstacles: manager.ObstacleManager, crashed: bool
    ):
        self.game_display.fill(utl.WHITE)
        self.draw_objects(car, *obstacles.objects)
        self.draw_score()

        if crashed:
            car.crash(self.game_display)

        pygame.display.update()

    def draw_objects(self, *args: game_object.GameObject):
        for obj in args:
            img, position = obj.draw()
            self.game_display.blit(img, position)

    def draw_score(self):
        text = self.font.render(f"Score: {self.score}", True, utl.BLACK)
        self.game_display.blit(text, (0, 0))
