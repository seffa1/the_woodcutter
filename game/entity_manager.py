import pygame as pg
from .engine import Entity
from .enemies.troll import Troll


# Instantiates, stores, and kills entities for each level
class Entity_Manager:
    def __init__(self, ID: str):
        self.ID = ID
        self.entity_data = []  # A 2-D array from our entities.txt file
        self.groups = {'troll': pg.sprite.Group()}
        self.load_entities()

    def load_entities(self):
        path = 'game/levels/' + self.ID + '/entities.txt'
        with open(path, 'r') as entity_file:
            for line in entity_file:
                entity_data_list = line.split(',')
                self.entity_data.append(entity_data_list)
                self.create_entity(int(entity_data_list[0]), int(entity_data_list[1]), int(entity_data_list[2]),
                                   int(entity_data_list[3]), entity_data_list[4], float(entity_data_list[5]), float(entity_data_list[6]))
                print(f'loading entity of type {entity_data_list[4]}')

    def create_entity(self, x, y, width, height, type, WALK_ACC, FRIC):
        """ Instantiates and entity and adds it to the appropriate group or creates a group for it """
        if type == 'troll':
            entity = Troll(x, y, width, height, type, WALK_ACC, FRIC)
        else:
            entity = Entity(x, y, width, height, type, WALK_ACC, FRIC)


        # Add this entity to that group
        self.groups[type].add(entity)
        print(f'{type} type entity created.')
        print(f'entity groups: {self.groups}')

    def update(self, tile_rects, dt, player):
        for group in self.groups.values():
            for entity in group:
                entity.update(tile_rects, dt, player)

    def draw(self, display, scroll):
        for group in self.groups.values():
            for entity in group:
                entity.draw(display, scroll)






