import pygame as pg
from .entity_manager import Entity_Manager
from .tile_manager import Tile_Manager


class Level:
    def __init__(self, level_ID: str, TILE_SIZE: int):
        self.level_ID = str
        self.connecting_levels = {}
        self.entity_manager = Entity_Manager(level_ID)
        self.tile_manager = Tile_Manager(level_ID, TILE_SIZE)

    def update(self):
        self.tile_manager.update()
        self.entity_manager.update()

    def draw(self, scroll, TILE_SIZE, display):
        self.tile_manager.draw(scroll, TILE_SIZE, display)
        self.entity_manager.draw()

    def add_connection(self, ID: str, level):
        self.connecting_levels[ID] = level