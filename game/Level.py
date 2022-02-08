import pygame as pg
from .entity_manager import Entity_Manager
from .tile_manager import Tile_Manager
from .Level_Trigger import Level_Trigger


class Level:
    def __init__(self, level_ID: str, TILE_SIZE: int, display):
        self.level_ID = level_ID
        self.display = display
        self.background_images = []
        self.connecting_levels = {}
        self.entity_manager = Entity_Manager(level_ID)
        self.tile_manager = Tile_Manager(level_ID, TILE_SIZE)
        self.level_triggers = {}  # '0-2': Level_trigger ---> Contains level_trigger objects with name of the level they go to

        self.load_triggers('game/levels/')
        self.load_background('game/levels/')


        self.collided_trigger = None

    def update(self, player, tile_rects, dt):
        self.tile_manager.update()
        self.entity_manager.update(tile_rects, dt)
        self.check_triggers(player)

    def draw(self, scroll, TILE_SIZE, display):
        for image in self.background_images:
            display.blit(image[0], (-image[1]*scroll[0], -image[1]*scroll[1] - image[0].get_height()/3))
        self.tile_manager.draw(scroll, TILE_SIZE, display)
        self.entity_manager.draw(display, scroll)
        for level_trigger in self.level_triggers.values():
            level_trigger.draw(display, scroll)

    def load_triggers(self, path):
        file_path = path + self.level_ID + '/level_triggers.txt'
        with open (file_path, 'r') as file:
            for line in file:
                line = line.split(',')
                trigger = Level_Trigger(int(line[0]), int(line[1]), int(line[2]), int(line[3]), line[4], line[5])
                self.level_triggers[line[4]] = trigger
                # self.add_connection(trigger[4])

    def check_triggers(self, player):
        self.collided_trigger = None
        for level_trigger in self.level_triggers.values():
            level_trigger.update(player)
            if level_trigger.collided:
                self.collided_trigger = level_trigger

    def load_background(self, path):
        file_path = path + self.level_ID + '/backgrounds.txt'
        with open (file_path, 'r') as file:
            for line in file:
                line = line.split(',')
                paralax_dif = line[1]
                paralax = 0
                total_images = line[2]
                for i in range(0, int(total_images)):
                    img_path = line[0] + str(i + 1) + '.png'
                    image = pg.image.load(img_path).convert_alpha()
                    scaled_img = pg.transform.scale(image, (self.display.get_width()*float(line[3]), self.display.get_height()*float(line[3])))
                    self.background_images.append([scaled_img, paralax])
                    paralax += float(paralax_dif)

    def add_connection(self, ID: str, level):
        self.connecting_levels[ID] = level