import pygame as pg
import engine as e


# Instantiates and kills entities
class World_Manager:
    def __init__(self):
        self.groups = {}

    def add_group(self, name: str):
        self.groups[name] = pg.sprite.Group()

    def add_to_group(self, entity: e.Entity, group: str):
        self.group[group].add(entity)

    def create_entity(self, name, x, y, width, height):
        name = e.Entity(x, y, width, height)
        self.add_to_group(name, )


