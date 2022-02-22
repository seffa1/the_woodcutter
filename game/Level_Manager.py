import pygame as pg
from .Level import Level
from .Time_Manager import Time_Manager


class Level_Manager:
    def __init__(self):
        self.levels = {}
        self.current_level = None

        # Calls down to the current level's tile manager, and gets updated collidable rects each framee
        self.tile_rects = []
        self.collided_trigger = None

        # Create time manager to keep track of each levels best timers
        self.time_manager = Time_Manager()

    def load_level(self, ID: str, TILE_SIZE: int, display):
        self.levels[ID] = Level(ID, TILE_SIZE, display)

    def set_level(self, ID: str, player):
        """ Changes the current level getting updated, then moves the player to that levels respawn point """
        if ID in self.levels:
            self.current_level = ID
            level = self.get_level()
            player.set_position(level.respawn_point[0], level.respawn_point[1])
        else:
            raise "You are trying to set to a level that does not exist"

    def get_level(self):
        """ Returns the current level object """
        return self.levels[self.current_level]

    def update(self, player, dt):
        self.tile_rects = self.get_level().tile_manager.tile_rects
        self.get_level().update(player, self.tile_rects, dt)
        self.time_manager.update()

    def draw_background(self, scroll, display):
        self.get_level().draw_background(scroll, display)

    def draw_tiles(self, scroll, TILE_SIZE, display):
        self.get_level().draw_tiles(scroll, TILE_SIZE, display)

    def draw_entities(self, scroll, display):
        self.get_level().draw_entities(scroll, display)

    def draw_triggers(self, scroll, display):
        self.get_level().draw_triggers(scroll, display)

    def draw_best_times(self, scroll, display):
        """ Draws the best timers by the level entrances in the base world """
        if self.current_level == '0-1':
            triggers = self.levels['0-1'].level_triggers
            self.time_manager.draw_best_times(scroll, display, triggers)

    def draw_timer(self, screen):
        self.time_manager.draw_timer(screen)

    def check_change_level(self, player):
        """ Only gets called when the player presses enter from the game event loop,
        then checks if a player is colliding with a level trigger. """
        if not self.get_level().collided_trigger:
            return

        trigger = self.get_level().collided_trigger
        self.set_level(trigger.level_to_go_to, player)

        # If its the starting level in a world, start the timer
        if trigger.level_to_go_to in ['1-1', '2-1', '3-1']:
            self.time_manager.start_timer(trigger.level_to_go_to)

        # If we are going back to the main world, stop the timer
        if trigger.level_to_go_to == '0-1':
            self.time_manager.stop_timer()

