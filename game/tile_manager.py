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
        # Decorations --------------------------------------------------------------------------------------------------
        self.sprites['grass_1'] = pg.transform.scale(pg.image.load('assets/images/decorations/grass/1.png').convert_alpha(), (14, 9))
        self.sprites['grass_2'] = pg.transform.scale(pg.image.load('assets/images/decorations/grass/2.png').convert_alpha(), (16, 13))
        self.sprites['grass_3'] = pg.transform.scale(pg.image.load('assets/images/decorations/grass/3.png').convert_alpha(), (8, 7))
        self.sprites['grass_4'] = pg.transform.scale(pg.image.load('assets/images/decorations/grass/6.png').convert_alpha(), (16, 11))
        self.sprites['tree_1'] = pg.transform.scale(pg.image.load('assets/images/decorations/trees/1.png').convert_alpha(), (176, 240))
        self.sprites['tree_2'] = pg.transform.scale(pg.image.load('assets/images/decorations/trees/2.png').convert_alpha(), (96, 128))
        self.sprites['tree_3'] = pg.transform.scale(pg.image.load('assets/images/decorations/trees/3.png').convert_alpha(), (96, 128))
        self.sprites['tree_4'] = pg.transform.scale(pg.image.load('assets/images/decorations/trees/5.png').convert_alpha(), (96, 144))
        self.sprites['tree_5'] = pg.transform.scale(pg.image.load('assets/images/decorations/trees/6.png').convert_alpha(), (96, 144))
        self.sprites['tree_6'] = pg.transform.scale(pg.image.load('assets/images/decorations/trees/pine/1.png').convert_alpha(), (37, 204))
        self.sprites['tree_7'] = pg.transform.scale(pg.image.load('assets/images/decorations/trees/pine/3.png').convert_alpha(), (23, 112))

        # Tiles --------------------------------------------------------------------------------------------------------
        self.sprites['dirt'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_11.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
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
        self.sprites['grass_corners_1'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_18.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_corners_2'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_27.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_corners_3'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_33.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_corners_4'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_35.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_corners_5'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_37.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_corners_6'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_39.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_corners_7'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_48.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_corners_8'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_42.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_corners_9'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_26.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_corners_10'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_17.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['grass_corners_11'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_40.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))

    def add_tile_rects(self):
        """ Adds all collidible tiles to the tile rect array for collision detection for game entities. """
        y = 0
        for layer in self.level_map:
            x = 0
            for tile in layer:
                # Check if the tile is a collidable
                if tile in ['2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'h', 'i', 'j', 'p', 'r']:
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
            # Tiles ----------------------------------------------------------------------------------------------------
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
                # Grass horizontal right
                if tile == 'h':
                    display.blit(self.sprites['grass_horizontal_right'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                # Grass horizontal left
                if tile == 'i':
                    display.blit(self.sprites['grass_horizontal_left'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                # Grass horizontal mid
                if tile == 'j':
                    display.blit(self.sprites['grass_horizontal_mid'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                # Grass corner left vertical high
                if tile == 'k':
                    display.blit(self.sprites['grass_corners_3'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                # Grass corner right vertical high
                if tile == 'l':
                    display.blit(self.sprites['grass_corners_8'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                # Grass corners double top
                if tile == 'm':
                    display.blit(self.sprites['grass_corners_9'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                # Grass corners double bottom
                if tile == 'n':
                    display.blit(self.sprites['grass_corners_10'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                # Grass corner left vertical low
                if tile == 'o':
                    display.blit(self.sprites['grass_corners_4'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                # Grass corner top horizontal right low
                if tile == 'p':
                    display.blit(self.sprites['grass_corners_6'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass corner right vertical low
                if tile == 'q':
                    display.blit(self.sprites['grass_corners_11'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # Grass corner top horizontal left low
                if tile == 'r':
                    display.blit(self.sprites['grass_corners_5'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                # DECORATIONS ------------------------------------------------------------------------------------------

                # Decorative Grass 1 - grass
                if tile == 's':
                    display.blit(self.sprites['grass_1'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] + 15))
                # Decorative Grass 2 - flower
                if tile == 't':
                    display.blit(self.sprites['grass_2'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] + 13))
                # Decorative Grass 3 - grass
                if tile == 'u':
                    display.blit(self.sprites['grass_3'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] + 18))
                # Decorative Grass 4 - flower
                if tile == 'v':
                    display.blit(self.sprites['grass_4'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] + 13))
                # Decorative Tree 1 - oak
                if tile == 'w':
                    display.blit(self.sprites['tree_1'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] - 210))
                # Decorative Tree 2 - oak
                if tile == 'x':
                    display.blit(self.sprites['tree_2'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] - 100))
                # Decorative Tree 3 - Oak
                if tile == 'y':
                    display.blit(self.sprites['tree_3'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] - 100))
                # Decorative Tree 4 - birch
                if tile == 'z':
                    display.blit(self.sprites['tree_4'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] - 110))
                # Decorative Tree 5 - birch
                if tile == '!':
                    display.blit(self.sprites['tree_5'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] - 100))
                # Decorative Tree 6 - pine
                if tile == '@':
                    display.blit(self.sprites['tree_6'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] - 100))
                # Decorative Tree 7 - Pine
                if tile == '#':
                    display.blit(self.sprites['tree_7'], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] - 80))




                # Oak tree
                if tile == 'w':
                    pass

                # Birch tree
                if tile == 'x':
                    pass

                # Pine tree
                if tile == 'y':
                    pass

                x += 1
            y += 1





