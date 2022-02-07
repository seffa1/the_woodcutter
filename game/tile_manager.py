import pygame as pg


class Tile_Manager:
    def __init__(self, ID: str):
        self.tiles = []
        self.sprites= {}

    def load_map(self, path: str):
        with open(path, 'r') as file:
            data = file.read()
            data = data.split('\n')
            game_map = []
            for row in data:
                game_map.append(list(row))
            return game_map

    def load_sprites(self):
        self.sprites['grass_tile_top'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_02.png').convert_alpha(),
                                                 (self.TILE_SIZE, self.TILE_SIZE))
        self.sprites['dirt_tile'] = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_11.png').convert_alpha(),
                                            (self.TILE_SIZE, self.TILE_SIZE))
    def update(self):
        pass

    # TODO break up getting tile rects from drawing them, to pass up to the level manager
    def return_tile_rects(self):
        tile_rects = []
        y = 0
        for layer in self.load_map('game/levels/0-1/tiles.txt'):
            x = 0
            for tile in layer:
                #TODO if tile is within a certain distaince from the player?
                if tile == '2':
                    self.tile_rects.append(
                        pg.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
                x += 1
            y += 1
        return tile_rects


    def draw(self, scroll, TILE_SIZE):
        # Temp tile rendering
        self.tile_rects = []
        y = 0
        for layer in self.load_map('game/levels/0-1/tiles.txt'):
            x = 0
            for tile in layer:
                if tile == '0-1':
                    self.display.blit(self.dirt_tile,
                                      (x * self.TILE_SIZE - self.scroll[0], y * self.TILE_SIZE - self.scroll[1]))
                if tile == '2':
                    self.display.blit(self.grass_tile_top,
                                      (x * self.TILE_SIZE - self.scroll[0], y * self.TILE_SIZE - self.scroll[1]))
                    self.tile_rects.append(
                        pg.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
                x += 1
            y += 1