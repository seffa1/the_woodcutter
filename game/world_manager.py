import pygame as pg
import engine as e


# Instantiates, kills, updates, and draws entities
class Entity_Manager:
    def __init__(self):
        self.groups = {}

    def create_group(self, group_name: str):
        self.groups[group_name] = pg.sprite.Group()

    def create_entity(self, entity_name, x, y, width, height):
        entity = e.Entity(x, y, width, height, entity_name)
        self.add_to_group(entity)

    def add_to_group(self, entity: e.Entity, group: str):
        self.group[group].add(entity)




