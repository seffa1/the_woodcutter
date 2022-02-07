import pygame as pg
from .Level import Level


class Level_Manager:
    def __init__(self):
        self.levels = {}
        self.current_level = None

        # Calls down to the current level's tile manager, and gets updated collidable rects each framee
        self.tile_rects = []


    def load_level(self, ID: str, TILE_SIZE: int):
        self.levels[ID] = Level(ID, TILE_SIZE)

    def set_level(self, ID: str):
        if ID in self.levels:
            self.current_level = ID
        else:
            raise "You are trying to set to a level that does not exist"

    def get_level(self):
        return self.levels[self.current_level]

    def update(self):
        self.tile_rects = self.get_level().tile_manager.tile_rects
        self.get_level().update()

    def draw(self, scroll, TILE_SIZE, display):
        self.get_level().draw(scroll, TILE_SIZE, display)
