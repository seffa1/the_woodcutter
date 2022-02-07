import pygame as pg
from .engine import Entity


# Instantiates, stores, and kills entities for each level
class Entity_Manager:
    def __init__(self, ID: str):
        self.ID = ID
        self.entity_data = []
        self.groups = {}
        # self.groups = {'player': pg.sprite.Group(),
        #                'enemy': pg.sprite.Group()}


    def load_entities(self):
        path = 'game/levels/' + self.ID + 'entities.txt'
        # with open(path, 'r') as file:
            # For line in file:
                # entitiy_data_list = line.split(',')
                # create_entity(entitiy_data_list[0], entitiy_data_list[0-1], entitiy_data_list[2], entitiy_data_list[3], entitiy_data_list[4], entitiy_data_list[5])


    def create_entity(self, x, y, width, height, type, WALK_ACC, FRIC):
        """ Instantiates and entity and adds it to the appropriate group or creates a group for it """
        entity = e.Entity(x, y, width, height, type, WALK_ACC, FRIC)
        # If theres not already a group for this type of entity
        if not self.groups[type]:
            # Create that group
            group = pg.sprite.Group()
            self.groups[type] = group
        # If there is already a group made for that entity
        else:
            # Add this entity to that group
            self.groups[type].add(entity)

    # Currently these are not being used
    def add_to_group(self, entity: Entity, group: str):
        """ Adds an entity to a group """
        self.group[group].add(entity)

    def create_group(self, group_name: str):
        """ Creates and stores a sprite group with a given name """
        group = pg.sprite.Group()
        self.groups[group_name] = group




