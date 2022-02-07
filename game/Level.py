import pygame as pg
from entity_manager import Entity_Manager
from tile_manager import Tile_Manager


class Level:
    def __init__(self, level_ID: str):
        self.level_ID = str
        self.connecting_levels = {}
        self.entitiy_manager = Entity_Manager(level_ID)
        self.tile_manager = Tile_Manager(level_ID)

    def update_entities(self):
        pass
        # For entitiy in self.entitity_manager:
            # entity.update()

    def update_tiles(self):
        pass

    def draw_entities(self):
        pass

    def draw_tiles(self):
        pass

    def update(self):
        self.update_tiles()
        self.update_entities()

    def draw(self):
        self.draw_tiles()
        self.draw_entities()