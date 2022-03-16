import pygame as pg
from .engine import Entity
from .enemies.troll import Troll
from .enemies.projectile import Projectile
from .traps.spikes import Spikes
from .traps.electric_trap import Electric_Trap
from .objects.coin import Coin
from .objects.old_man import Old_Man
from .objects.collectible import Collectible
from .objects.chest import Chest
from.shop.shop import Shop


# Instantiates, stores, and kills entities for each level
class Entity_Manager:
    def __init__(self, ID: str):
        self.ID = ID
        self.groups = {}
        self.shop_object = []  # Stores the shop here for easy access by the game to update it independently
        self.load_entities()

    def load_entities(self):
        """ Loads all non-enemies for a level. Enemy generation is separate because it has to happen more than once. """
        path = 'game/levels/' + self.ID + '/entities.txt'
        with open(path, 'r') as entity_file:
            for line in entity_file:
                entity_data_list = line.split(',')
                if entity_data_list[4] not in ['troll', 'collectible']:
                    self.create_entity(int(entity_data_list[0]), int(entity_data_list[1]), int(entity_data_list[2]),
                                       int(entity_data_list[3]), entity_data_list[4], float(entity_data_list[5]),
                                       float(entity_data_list[6]), float(entity_data_list[7]))

    def load_enemies(self):  # and collectibles
        """ Regenerates the enemies and collectibles for a level when you travel to it. This is called by the level manager since it
        will happen each time you travel to a world. """
        path = 'game/levels/' + self.ID + '/entities.txt'
        with open(path, 'r') as entity_file:
            for line in entity_file:
                entity_data_list = line.split(',')
                # Only create entities that are enemy types
                if entity_data_list[4] in ['troll', 'collectible']:
                    self.create_entity(int(entity_data_list[0]), int(entity_data_list[1]), int(entity_data_list[2]),
                                       int(entity_data_list[3]), entity_data_list[4], float(entity_data_list[5]),
                                       float(entity_data_list[6]), float(entity_data_list[7]))

    def create_entity(self, x, y, width, height, type, WALK_ACC, FRIC, rotate):
        """ Instantiates and entity and adds it to the appropriate group or creates a group for it """
        if type == 'troll':
            entity = Troll(x, y, width, height, type, WALK_ACC, FRIC, rotate, self)
        elif type == 'old_man':
            entity = Old_Man(x, y, width, height, type, WALK_ACC, FRIC, rotate)
            self.shop_object.append(entity)
            return
        elif type == 'chest':
            entity = Chest(x, y, width, height, type, WALK_ACC, FRIC, rotate, self)
        elif type == 'spikes':
            entity = Spikes(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        elif type == 'electric_trap':
            entity = Electric_Trap(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        elif type == 'coin':
            entity = Coin(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        elif type == 'collectible':
            entity = Collectible(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        elif type == 'shop':
            entity = Shop(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        elif type == 'projectile':
            entity = Projectile(x, y, width, height, type, WALK_ACC, FRIC, rotate, self)
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

        for entity in self.shop_object:
            entity.update(tile_rects, dt, player)

    def draw(self, display, scroll, screen):
        for group in list(self.groups.values()):
            for entity in group:
                if entity.image is not None:  # Shop gets drawn separately, in a different way
                    entity.draw(display, scroll)









