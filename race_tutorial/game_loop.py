import pygame

import race_tutorial.game_object as game_object
import race_tutorial.utils as utl


class GameLoop(object):
    def __init__(self, caption, window, frame_limit, level=1, level_time=5):
        pygame.init()
        pygame.time.set_timer(*utl.timer_settings(level_time))
        pygame.display.set_caption(caption)

        self.objects = list()
        self.game_display = pygame.display.set_mode(window)
        self.clock = pygame.time.Clock()
        self.frame_limit = frame_limit
        self.level = level

    def run(self):
        crashed = False
        car_change = utl.NEUTRAL
        car = game_object.Car(utl.STARTING_POINT)

        while not crashed:
            car_change = self.event(car_change)
            crashed = self.update(car, car_change)
            self.draw(car, crashed)
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

    def update(self, car: game_object.Car, car_change: int) -> bool:
        if car_change == pygame.QUIT:
            return True

        car.update_position(utl.Point(x=car_change * car.speed, y=0))
        self.update_obstacles(max_on_screen=self.level)
        return car.collided(self.objects)

    def update_obstacles(self, max_on_screen: int):
        to_delete = list()

        if len(self.objects) < max_on_screen:
            number_to_spawn = max_on_screen - len(self.objects)
            self.objects.extend(game_object.Obstacle.spawn(number_to_spawn))

        for i, obstacle in enumerate(self.objects):
            obstacle.update_position(utl.Point(y=obstacle.speed, x=0))
            if obstacle.y > utl.WINDOW_SIZE.y:
                to_delete.append(i)

        for i in sorted(to_delete, reverse=True):
            self.objects.pop(i)

    def draw(self, car: game_object.Car, crashed: bool):
        self.game_display.fill(utl.WHITE)
        self.draw_objects(car, *self.objects)

        if crashed:
            car.crash(self.game_display)

        pygame.display.update()

    def draw_objects(self, *args: game_object.GameObject):
        for obj in args:
            img, position = obj.draw()
            self.game_display.blit(img, position)
