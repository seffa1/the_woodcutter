import pygame as pg
from .Level import Level


class Level_Manager:
    def __init__(self):
        self.levels = {}
        self.current_level = None

        # Calls down to the current level's tile manager, and gets updated collidable rects each framee
        self.tile_rects = []
        self.collided_trigger = None

    def load_level(self, ID: str, TILE_SIZE: int, display):
        self.levels[ID] = Level(ID, TILE_SIZE, display)

    def set_level(self, ID: str):
        if ID in self.levels:
            self.current_level = ID
        else:
            raise "You are trying to set to a level that does not exist"

    def get_level(self):
        return self.levels[self.current_level]

    def update(self, player):
        self.tile_rects = self.get_level().tile_manager.tile_rects
        self.get_level().update(player)

    def draw(self, scroll, TILE_SIZE, display):
        self.get_level().draw(scroll, TILE_SIZE, display)

    def check_change_level(self):
        """ Only gets called when the player presses enter """
        if not self.get_level().collided_trigger:
            return

        trigger = self.get_level().collided_trigger
        self.set_level(trigger.level_to_go_to)
