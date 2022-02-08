import pygame as pg
from .engine import Entity


# Instantiates, stores, and kills entities for each level
class Entity_Manager:
    def __init__(self, ID: str):
        self.ID = ID
        self.entity_data = []  # A 2-D array from our entities.txt file
        self.groups = {'player': pg.sprite.Group(),
                       'enemy': pg.sprite.Group()}

        # self.load_entities()


    def load_entities(self):
        path = 'game/levels/' + self.ID + 'entities.txt'
        with open(path, 'r') as entity_file:
            for line in entity_file:
                entity_data_list = line.split(',')
                self.entity_data.append(entity_data_list)
                create_entity(entity_data_list[0], entity_data_list[0-1], entity_data_list[2], entity_data_list[3], entity_data_list[4], entity_data_list[5])


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



    def update(self):
        pass

    def draw(self):
        pass

    # Currently these are not being used
    def add_to_group(self, entity: Entity, group: str):
        """ Adds an entity to a group """
        self.group[group].add(entity)

    def create_group(self, group_name: str):
        """ Creates and stores a sprite group with a given name """
        group = pg.sprite.Group()
        self.groups[group_name] = group




