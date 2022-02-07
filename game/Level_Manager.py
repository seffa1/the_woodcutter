import pygame as pg
from Level import Level


class Level_Manager:
    def __init__(self):
        self.levels = {}
        self.current_level = None

        # Calls down to the current level's tile manager, and gets updated collidable rects each framee
        self.tile_rects = []


    def load_level(self, ID: str):
        pass

    def get_level(self):
        return self.levels[self.current_level]

    def get_tile_rects(self):
        level = self.get_level()
        self.tile_rects = level.return_tile_rects()
        pass

    def update(self):
        self.get_tile_rects()
        pass

    def draw(self):
        pass