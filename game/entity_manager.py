import pygame as pg
from .engine import Entity
from .enemies.troll import Troll
from .traps.spikes import Spikes
from .traps.electric_trap import Electric_Trap
from .objects.coin import Coin
from .objects.chest import Chest
from.shop.shop import Shop



# Instantiates, stores, and kills entities for each level
class Entity_Manager:
    def __init__(self, ID: str):
        self.ID = ID
        self.groups = {}
        self.load_entities()

    def load_entities(self):
        path = 'game/levels/' + self.ID + '/entities.txt'
        with open(path, 'r') as entity_file:
            for line in entity_file:
                entity_data_list = line.split(',')
                self.create_entity(int(entity_data_list[0]), int(entity_data_list[1]), int(entity_data_list[2]),
                                   int(entity_data_list[3]), entity_data_list[4], float(entity_data_list[5]),
                                   float(entity_data_list[6]), float(entity_data_list[7]))


    def create_entity(self, x, y, width, height, type, WALK_ACC, FRIC, rotate):
        """ Instantiates and entity and adds it to the appropriate group or creates a group for it """
        if type == 'troll':
            entity = Troll(x, y, width, height, type, WALK_ACC, FRIC, rotate, self)
        elif type == 'chest':
            entity = Chest(x, y, width, height, type, WALK_ACC, FRIC, rotate, self)
        elif type == 'spikes':
            entity = Spikes(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        elif type == 'electric_trap':
            entity = Electric_Trap(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        elif type == 'coin':
            entity = Coin(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        elif type == 'shop':
            entity = Shop(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        else:
            raise 'Entity Type was not defined'

        # Add this entity to that group
        self.add_entity(entity, type)

    def add_entity(self, entity, type):
        """ Entities which are instantiated on level creation, like loot drops, can use this.
        They will have a creator such as a chest once opened, or enemy when killed """

        try:
            self.groups[type].add(entity)
        except KeyError:
            self.groups[type] = pg.sprite.Group()
        finally:
            self.groups[type].add(entity)


    def update(self, tile_rects, dt, player):
        for group in list(self.groups.values()):
            for entity in group:
                entity.update(tile_rects, dt, player)

    def draw(self, display, scroll):
        for group in list(self.groups.values()):
            for entity in group:
                if entity.image is not None:
                    entity.draw(display, scroll)






