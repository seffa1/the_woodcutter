import pygame as pg
from .settings import SCALE_FACTOR_SETTING, WINDOW_SIZE_SETTING


class Tile_Manager:
    def __init__(self, ID: str, TILE_SIZE: int):
        # Constants
        self.TILE_SIZE = TILE_SIZE

        # Data Storage
        self.ID = ID
        self.level_map = []  # 2D array of numbers from the tiles.txt file
        self.tile_rects = []
        self.sprites= {}
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
        self.sprites['grass_tile_top'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_02.png').convert_alpha(),
                                                 (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['dirt_tile'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_11.png').convert_alpha(),
                                            (self.TILE_SIZE, self.TILE_SIZE))

    def add_tile_rects(self):
        """ Adds all collidible tiles to the tile rect array for collision detection for game entities. """
        y = 0
        for layer in self.level_map:
            x = 0
            for tile in layer:
                # Check if the tile is a collidable
                if tile == '2':
                    self.tile_rects.append(
                        pg.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
                x += 1
            y += 1

    def draw(self, scroll, TILE_SIZE, display):
        """ Iterates through the 2D map array, and blits a tile sprite depending on the number to a location
        which is a function of the array position and TILE_SIZE (size of the tile image). """
        # Iterate through 2D array
        y = 0
        # display.blit(self.batch, (1000-scroll[0], -200-scroll[1])) # Not working yet
        for layer in self.level_map:
            x = 0
            # Blit the tile associated with the number
            for tile in layer:
                if tile == '1': # TODO Remove this once batch renderer is done
                    # Use array position X TILE_SIZE to get positions
                    display.blit(self.sprites['dirt_tile'],
                                      (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '2':
                    display.blit(self.sprites['grass_tile_top'],
                                      (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                x += 1
            y += 1





