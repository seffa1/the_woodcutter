import pygame as pg
from game.game import Game
from game.menu import StartMenu, GameMenu
from game.settings import WINDOW_SIZE_SETTING, SCALE_FACTOR_SETTING


def main():
    # Initialize pygame
    pg.init()
    pg.mixer.init()

    # Configure game settings
    # WINDOW_SIZE = (1280, 1024)  # non-laptop
    WINDOW_SIZE = WINDOW_SIZE_SETTING  # laptop
    screen = pg.display.set_mode(WINDOW_SIZE, 0, 32)
    SCALE_FACTOR = SCALE_FACTOR_SETTING
    display = pg.Surface((WINDOW_SIZE[0]/SCALE_FACTOR, WINDOW_SIZE[1]/SCALE_FACTOR))
    clock = pg.time.Clock()

    # implement menus
    start_menu = StartMenu(screen, clock)
    game_menu = GameMenu(screen, clock)

    # implement game
    game = Game(screen, clock, display, WINDOW_SIZE, SCALE_FACTOR)

    # Program loop
    running = True
    while running:

        # start menu goes here
        playing = start_menu.run()
        playing = True

        while playing:
            # game loop here
            game.run()
            # pause loop here
            playing = game_menu.run(game)
            running = playing


if __name__ == "__main__":
    main()
