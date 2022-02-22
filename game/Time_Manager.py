import pygame as pg
import time, math
from .utils import draw_text
from .settings import WINDOW_SIZE_SETTING


class Time_Manager:
    def __init__(self):
        self.best_times = {'1-1': None,
                           '2-1': None,
                           '3-1': None }

        self.current_level = None
        self.level_start_time = 0
        self.level_end_time = 0

        self.show_current_time = False

    def start_timer(self, level_ID):
        self.current_level = level_ID
        self.level_start_time = time.time()
        self.show_current_time = True

    def stop_timer(self):
        """ Stops timer and updates best time if your time was lower """
        self.level_end_time = time.time()
        level_time = round(self.level_end_time - self.level_start_time, 2)
        # Check for a new best timee
        if self.best_times[self.current_level] == None:
            self.best_times[self.current_level] = level_time

        elif level_time < self.best_times[self.current_level]:
            self.best_times[self.current_level] = level_time

        self.show_current_time = False

    def update(self):
        pass

    def draw_timer(self, screen):
        # For debugging
        # draw_text(screen, f'Best Times: {self.best_times}', 25, (255, 0, 0), (WINDOW_SIZE_SETTING[0] / 2 - 540, 35))

        # Timer is drawn to the screen
        if not self.show_current_time:
            return
        timer = round(time.time()  - self.level_start_time, 2)
        draw_text(screen, f'Current Time: {timer}', 25, (255, 0, 0), (WINDOW_SIZE_SETTING[0] / 2 - 140, 10))

    def draw_best_times(self, scroll, display, triggers):
        #  Configs
        SIZE = 15
        X_OFFSET = -30
        Y_OFFSEET = -30

        # The best times for each level are drawn to the display
        draw_text(display, f'Best Time: {self.best_times["1-1"]}', SIZE, (255, 0, 0), (triggers['1-1'].x - scroll[0] + X_OFFSET, triggers['1-1'].y + Y_OFFSEET - scroll[1]))
        draw_text(display, f'Best Time: {self.best_times["2-1"]}', SIZE, (255, 0, 0), (triggers['2-1'].x - scroll[0] + X_OFFSET, triggers['2-1'].y + Y_OFFSEET - scroll[1]))
        draw_text(display, f'Best Time: {self.best_times["3-1"]}', SIZE, (255, 0, 0), (triggers['3-1'].x - scroll[0] + X_OFFSET, triggers['3-1'].y + Y_OFFSEET - scroll[1]))


