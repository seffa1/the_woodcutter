import pygame as pg
from .engine import Entity


# Instantiates, stores, and kills entities for each level
class Entity_Manager:
    def __init__(self, ID: str):
        self.ID = ID
        self.entity_data = []  # A 2-D array from our entities.txt file
        self.groups = {'enemy': pg.sprite.Group()}
        # self.load_entities()

    def load_entities(self):
        path = 'game/levels/' + self.ID + 'entities.txt'
        with open(path, 'r') as entity_file:
            for line in entity_file:
                entity_data_list = line.split(',')
                self.entity_data.append(entity_data_list)
                self.create_entity(entity_data_list[0], entity_data_list[1], entity_data_list[2],
                                   entity_data_list[3], entity_data_list[4], entity_data_list[5], entity_data_list[6])

    def create_entity(self, x, y, width, height, type, WALK_ACC, FRIC):
        """ Instantiates and entity and adds it to the appropriate group or creates a group for it """
        entity = Entity(x, y, width, height, type, WALK_ACC, FRIC)
        # If theres not already a group for this type of entity
        if not self.groups[type]:
            # Create that group
            group = pg.sprite.Group()
            self.groups[type] = group
        # If there is already a group made for that entity
        else:
            # Add this entity to that group
            self.groups[type].add(entity)

    def update(self, tile_rects, dt, player):
        for enemy in self.groups['enemy']:
            enemy.update(tile_rects, dt, player)

    def draw(self, display, scroll):
        for enemy in self.groups['enemy']:
            enemy.draw(display, scroll)






