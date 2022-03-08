import pygame as pg
from .settings import SCALE_FACTOR_SETTING, WINDOW_SIZE_SETTING
import random


class Tile_Manager:
    def __init__(self, ID: str, TILE_SIZE: int):
        # Constants
        self.TILE_SIZE = TILE_SIZE

        # Data Storage
        self.ID = ID
        self.level_map = []  # 2D array of numbers from the tiles.txt file
        self.tile_rects = []
        self.sprites = {}
        # display_size = (WINDOW_SIZE_SETTING[0], WINDOW_SIZE_SETTING[1])
        display_size = (WINDOW_SIZE_SETTING[0]/SCALE_FACTOR_SETTING, WINDOW_SIZE_SETTING[1]/SCALE_FACTOR_SETTING)
        self.batch = pg.Surface(display_size).convert_alpha()

        # Load images
        self.load_sprites()
        # Load the 2D map array
        self.load_map('game/levels/')
        # Save collidible tiles to pass to other entity's movement collisions
        self.add_tile_rects()
        # Batch render dirt tiles, bushes, trees, etc.
        # self.load_batch()

    def load_batch(self):  # TODO batch renderer, still not working
        """ All static images used for only astestic get drawn to a single surface once, then just that surface gets drawn every frame.
        Includes dirt tiles, bushes, trees, etc. """
        y = 0
        # For each number of the 2D map array
        for layer in self.level_map:
            x = 0
            for tile in layer:
                # Check if the number is a static imagee
                if tile == '1':
                    self.batch.blit(self.sprites['dirt_tile'], (x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
                x += 1
            y += 1

    def load_map(self, path: str):
        """ Generates a 2D array from a text file """
        path = path + self.ID + '/tiles.txt'
        with open(path, 'r') as file:
            data = file.read()
            data = data.split('\n')
            for row in data:
                self.level_map.append(list(row))

    def load_sprites(self):
        """ Creates images for the tiles """
        self.sprites['grass_top'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_02.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_top_left'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_01.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_top_right'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_03.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_bottom_left'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_19.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_bottom_right'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_21.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_bottom_left_corner'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_22.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_bottom_right_corner'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_24.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_top_left_corner'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_04.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_top_right_corner'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_06.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_left'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_10.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_right'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_12.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_bottom'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_05.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_vertical_mid'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_50.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_vertical_top'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_49.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_vertical_bottom'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_51.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_horizontal_right'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_31.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_horizontal_left'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_29.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_horizontal_mid'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_30.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['dirt'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_11.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        # TODO - add trees, bushes
        # TODO - Random chance to draw a grass decorative on top of a top grass tile - much easier if we got the batch system working


    def add_tile_rects(self):
        """ Adds all collidible tiles to the tile rect array for collision detection for game entities. """
        y = 0
        for layer in self.level_map:
            x = 0
            for tile in layer:
                # Check if the tile is a collidable
                if tile in ['2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c']:
                    self.tile_rects.append(
                        pg.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
                x += 1
            y += 1

    def draw(self, scroll, TILE_SIZE, display):
        """ Iterates through the 2D map array, and blits a tile sprite depending on the number to a location
        which is a function of the array position and TILE_SIZE (size of the tile image). """
        # Iterate through 2D array
        y = 0
        # display.blit(self.batch, (-scroll[0], -scroll[1])) # Not working yet
        for layer in self.level_map:
            x = 0
            # Blit the tile associated with the number
            for tile in layer:
                # Dirt block
                if tile == '1':
                    # Use array position X TILE_SIZE to get positions
                    display.blit(self.sprites['dirt'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass top
                if tile == '2':
                    display.blit(self.sprites['grass_top'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass right
                if tile == '3':
                    display.blit(self.sprites['grass_right'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass left
                if tile == '4':
                    display.blit(self.sprites['grass_left'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass bottom
                if tile == '5':
                    display.blit(self.sprites['grass_bottom'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass top right
                if tile == '6':
                    display.blit(self.sprites['grass_top_right'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass top left
                if tile == '7':
                    display.blit(self.sprites['grass_top_left'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass vertical mid
                if tile == '8':
                    display.blit(self.sprites['grass_vertical_mid'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass vertical bottom
                if tile == '9':
                    display.blit(self.sprites['grass_vertical_bottom'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass vertical top
                if tile == 'a':
                    display.blit(self.sprites['grass_vertical_top'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass bottom right
                if tile == 'b':
                    display.blit(self.sprites['grass_bottom_right'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass bottom left
                if tile == 'c':
                    display.blit(self.sprites['grass_bottom_left'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass bottom left corner
                if tile == 'd':
                    display.blit(self.sprites['grass_bottom_left_corner'],(x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass bottom right corner
                if tile == 'e':
                    display.blit(self.sprites['grass_bottom_right_corner'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass top left corner
                if tile == 'f':
                    display.blit(self.sprites['grass_top_left_corner'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass top right corner
                if tile == 'g':
                    display.blit(self.sprites['grass_top_right_corner'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Oak tree
                if tile == 'l':
                    pass

                # Birch tree
                if tile == 'm':
                    pass

                # Pine tree
                if tile == 'n':
                    pass

                x += 1
            y += 1





