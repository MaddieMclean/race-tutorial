import pygame

import race_tutorial.utils as utl
from race_tutorial.game_loop import GameLoop


def main():
    game_loop = GameLoop(caption="A bit Racey", window=utl.WINDOW_SIZE, frame_limit=60)
    game_loop.run()
    pygame.quit()


if __name__ == "__main__":
    main()
