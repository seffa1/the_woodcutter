import pygame as pg
import game.engine as e


# Instantiates, stores, and kills entities for each level
class Entity_Manager:
    def __init__(self):
        self.groups = {}
        # self.groups = {'player': pg.sprite.Group(),
        #                'enemy': pg.sprite.Group()}

    def create_entity(self, x, y, width, height, type):
        """ Instantiates and entity and adds it to the appropriate group or creates a group for it """
        entity = e.Entity(x, y, width, height, type)
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
    def add_to_group(self, entity: e.Entity, group: str):
        """ Adds an entity to a group """
        self.group[group].add(entity)

    def create_group(self, group_name: str):
        """ Creates and stores a sprite group with a given name """
        group = pg.sprite.Group()
        self.groups[group_name] = group




