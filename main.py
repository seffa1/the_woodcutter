import pygame as pg
from game.game import Game
from game.menu import StartMenu, GameMenu
from game.settings import WINDOW_SIZE_SETTING, SCALE_FACTOR_SETTING, START_MENU_ON, RUN_PROFILER


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

    # Program loop
    running = True
    while running:

        # Start menu returns true if you dont quick, and returns load data if you loaded
        if START_MENU_ON:
            start_data = start_menu.run()
            playing = start_data[0]
            load_data = start_data[1]
        else:
            load_data = None
            playing = True

        # Start the main game loop, with optional data
        # create game object
        game = Game(screen, clock, display, WINDOW_SIZE, SCALE_FACTOR, load_data)
        while playing:

            # game loop here
            game.run()
            # pause loop here
            playing = game_menu.run(game)
            running = playing


if __name__ == "__main__":
    if RUN_PROFILER:
        import cProfile
        import pstats

        with cProfile.Profile() as pr:
            main()

        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()
        stats.dump_stats(filename='main_profiling.prof')

    else:
        main()