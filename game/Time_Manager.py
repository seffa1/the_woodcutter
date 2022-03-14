import pygame as pg
import time, math, datetime
from .utils import draw_text
from .settings import WINDOW_SIZE_SETTING, SCALE_FACTOR_SETTING


class Time_Manager:
    """ Keeps track of the time spent on a world, saves the lowest times, and draws them when needed. """
    def __init__(self):
        self.best_times = {'1-1': None,
                           '2-1': None,
                           '3-1': None}

        self.medals = {'1-1': None,
                       '2-1': None,
                       '3-1': None}

        self.medal_thresholds = {'1-1': {'bronze': datetime.time(0,5,0), 'silver': datetime.time(0,3,0), 'gold': datetime.time(0,2,0)},
                                '2-1': {'bronze': datetime.time(0,5,0), 'silver': datetime.time(0,3,0), 'gold': datetime.time(0,2,0)},
                                '3-1': {'bronze': datetime.time(0,5,0), 'silver': datetime.time(0,3,0), 'gold': datetime.time(0,2,0)}
                                 }

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

            # Set the medal earned for the level after converting to a datetime object for comparrison
            minutes = int(level_time//60)
            seconds = int(round(level_time - minutes*60))
            level_time_dt = datetime.time(0, minutes, seconds)  # If seconds is > 60 this doesnt work
            if level_time_dt <= self.medal_thresholds[self.current_level]['bronze']:
                # Dont set the medal if you have already got a better score
                if self.medals[self.current_level] not in ['silver', 'gold']:
                    self.medals[self.current_level] = 'bronze'
            if level_time_dt <= self.medal_thresholds[self.current_level]['silver']:
                if self.medals[self.current_level] not in ['gold']:
                    self.medals[self.current_level] = 'silver'
            if level_time_dt <= self.medal_thresholds[self.current_level]['gold']:
                self.medals[self.current_level] = 'gold'

        elif level_time < self.best_times[self.current_level]:
            self.best_times[self.current_level] = level_time

        print(self.medals)
        self.show_current_time = False

    def draw_timer(self, screen):
        # Timer is drawn to the screen
        if not self.show_current_time:
            return
        timer = round(time.time() - self.level_start_time, 2)
        draw_text(screen, f'Current Time: {timer}', 25, (255, 255, 255), (700, 10))

    def draw_best_times(self, scroll, triggers, screen):
        #  Configs
        SIZE = 35
        X_OFFSET = -30
        Y_OFFSET = -30

        # The best times for each level are drawn to the screen
        # Drawn at the triggers location, with an offset, with the scroll. The scale factor lets you draw to the screen like you would the display
        draw_text(screen, f'Best Time: {self.best_times["1-1"]}', SIZE, (255, 255, 255), ((triggers['1-1'].x + X_OFFSET - scroll[0]) * SCALE_FACTOR_SETTING, (triggers['1-1'].y + Y_OFFSET - scroll[1]) * SCALE_FACTOR_SETTING))
        draw_text(screen, f'Best Time: {self.best_times["2-1"]}', SIZE, (255, 255, 255), ((triggers['2-1'].x + X_OFFSET - scroll[0]) * SCALE_FACTOR_SETTING, (triggers['2-1'].y + Y_OFFSET - scroll[1]) * SCALE_FACTOR_SETTING))
        draw_text(screen, f'Best Time: {self.best_times["3-1"]}', SIZE, (255, 255, 255), ((triggers['3-1'].x + X_OFFSET - scroll[0]) * SCALE_FACTOR_SETTING, (triggers['3-1'].y + Y_OFFSET - scroll[1]) * SCALE_FACTOR_SETTING))



