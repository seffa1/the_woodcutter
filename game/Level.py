import pygame as pg
from .entity_manager import Entity_Manager
from .tile_manager import Tile_Manager
from .Level_Trigger import Level_Trigger
from .settings import WINDOW_SIZE_SETTING, SCALE_FACTOR_SETTING


class Level:
    def __init__(self, level_ID: str, TILE_SIZE: int, display):
        self.level_ID = level_ID
        self.TILE_SIZE = TILE_SIZE
        self.display = display
        self.background_images = []  # [scaled_img, paralax, offset_y]
        self.entity_manager = Entity_Manager(level_ID)
        self.tile_manager = Tile_Manager(level_ID, TILE_SIZE)
        self.level_triggers = {}  # '0-1': Level_trigger ---> Contains level_trigger objects with name of the level they go to
        self.respawn_point = [0, 0]

        self.load_triggers('game/levels/')
        self.load_background('game/levels/')
        self.load_respawn_point('game/levels/')

        self.collided_trigger = None

    def respawn_level(self):
        self.entity_manager = Entity_Manager(self.level_ID)

    def update(self, player, tile_rects, dt):
        self.tile_manager.update()
        self.entity_manager.update(tile_rects, dt, player)
        self.check_triggers(player)

    def load_background(self, path):
        file_path = path + self.level_ID + '/backgrounds.txt'
        with open(file_path, 'r') as file:
            for line in file:
                line = line.split(',')
                # How much paralax gets added to each layer
                paralax_dif = line[1]
                # Keeps track of paralax so different layers get different amount of paralax
                paralax = 0
                # Loads the images
                total_images = line[2]
                # Offset Y
                offset_y = int(line[3])
                # Scale
                scale = int(line[4])
                for i in range(0, int(total_images)):
                    # Load the image
                    img_path = line[0] + str(i + 1) + '.png'
                    image = pg.image.load(img_path).convert_alpha()

                    # Scale the image
                    blit_size = (WINDOW_SIZE_SETTING[0]/SCALE_FACTOR_SETTING * scale, WINDOW_SIZE_SETTING[1]/SCALE_FACTOR_SETTING * scale)
                    scaled_img = pg.transform.scale(image, blit_size)

                    # Add image to array
                    self.background_images.append([scaled_img, paralax, offset_y, scale])
                    # Increment paralax for next layer
                    paralax += float(paralax_dif)

    def draw_background(self, scroll, display):
        for image in self.background_images:
            paralax_x = image[1]
            paralax_y = 1
            # paralax = 0
            OFFSET_Y = image[2]
            # Draw the background 3 times wide
            display.blit(image[0], (-paralax_x * scroll[0], -paralax_y * scroll[1] + OFFSET_Y))
            display.blit(image[0], (-paralax_x * scroll[0] + image[0].get_width(), -paralax_y * scroll[1] + OFFSET_Y))
            display.blit(image[0], (-paralax_x * scroll[0] + image[0].get_width()*2, -paralax_y * scroll[1] + OFFSET_Y))

    def draw_tiles(self, scroll, TILE_SIZE, display):
        self.tile_manager.draw(scroll, TILE_SIZE, display)

    def draw_entities(self, scroll, display, screen):
        self.entity_manager.draw(display, scroll, screen)

    def draw_triggers(self, scroll, display):
        for level_trigger in self.level_triggers.values():
            level_trigger.draw(display, scroll)

    def load_triggers(self, path):
        file_path = path + self.level_ID + '/level_triggers.txt'
        with open(file_path, 'r') as file:
            for line in file:
                line = line.split(',')
                trigger = Level_Trigger(int(line[0]), int(line[1]), int(line[2]), int(line[3]), line[4], line[5])
                self.level_triggers[line[4]] = trigger

    def load_respawn_point(self, path):
        file_path = path + self.level_ID + '/respawn.txt'
        with open(file_path, 'r') as file:
            for line in file:
                line = line.split(',')
                self.respawn_point = [int(line[0]), int(line[1])]

    def check_triggers(self, player):
        self.collided_trigger = None
        for level_trigger in self.level_triggers.values():
            level_trigger.update(player)
            if level_trigger.collided:
                self.collided_trigger = level_trigger
