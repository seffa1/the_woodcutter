import pygame as pg


class Tile_Manager:
    def __init__(self, ID: str, TILE_SIZE: int):
        # Constants
        self.TILE_SIZE = TILE_SIZE

        # Data Storage
        self.ID = ID
        self.level_map = []  # 2D array of numbers from the tiles.txt file
        self.tile_rects = []
        self.sprites= {}

        # Level Generation
        self.load_sprites()  # Load images
        self.load_map('game/levels/')  # Load the 2D map array
        self.add_tile_rects()  # Save collidible tiles to pass to other entity's movement collisions




    # TODO This will eventually be the chunk system that updates the tiles and collidibles each frame
    def update(self):
        pass

    def draw(self, scroll, TILE_SIZE, display):
        y = 0
        for layer in self.level_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(self.sprites['dirt_tile'],
                                      (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '2':
                    display.blit(self.sprites['grass_tile_top'],
                                      (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                x += 1
            y += 1

    # TODO For performance this should be done with a chunk system, or have small levels
    def add_tile_rects(self):
        """ Adds all collidible tiles to the tile rect array """
        y = 0
        for layer in self.level_map:
            x = 0
            for tile in layer:
                if tile == '2':
                    self.tile_rects.append(
                        pg.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
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

