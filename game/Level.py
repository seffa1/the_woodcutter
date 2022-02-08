import pygame as pg
from .entity_manager import Entity_Manager
from .tile_manager import Tile_Manager
from .Level_Trigger import Level_Trigger


class Level:
    def __init__(self, level_ID: str, TILE_SIZE: int):
        self.level_ID = level_ID
        self.connecting_levels = {}
        self.entity_manager = Entity_Manager(level_ID)
        self.tile_manager = Tile_Manager(level_ID, TILE_SIZE)
        self.level_triggers = {}  # '0-2': Level_trigger ---> Contains level_trigger objects with name of the level they go to
        self.load_triggers('game/levels/')


    def update(self, player):
        self.tile_manager.update()
        self.entity_manager.update()
        for level_trigger in self.level_triggers.values():
            level_trigger.update(player)

    def draw(self, scroll, TILE_SIZE, display):
        self.tile_manager.draw(scroll, TILE_SIZE, display)
        self.entity_manager.draw()
        for level_trigger in self.level_triggers.values():
            level_trigger.draw(display, scroll)


    def load_triggers(self, path):
        file_path = path + self.level_ID + '/level_triggers.txt'
        with open (file_path, 'r') as file:
            for line in file:
                line = line.split(',')
                trigger = Level_Trigger(int(line[0]), int(line[1]), int(line[2]), int(line[3]), line[4])
                self.level_triggers[line[4]] = trigger
                # self.add_connection(trigger[4])


    def add_connection(self, ID: str, level):
        self.connecting_levels[ID] = level