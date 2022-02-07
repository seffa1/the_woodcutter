import pygame as pg
from entity_manager import Entity_Manager
from tile_manager import Tile_Manager


class Level:
    def __init__(self, level_ID: str):
        self.level_ID = str
        self.connecting_levels = {}
        self.entity_manager = Entity_Manager(level_ID)
        self.tile_manager = Tile_Manager(level_ID)

    def update(self):
        self.tile_manager.update()
        self.entity_manager.update()

    def draw(self):
        self.tile_manager.draw()
        self.entity_manager.draw()