import pygame as pg
from collections import deque
from .shop_menu import Shop_Menu
vec = pg.math.Vector2
from game.engine import Entity



class Shop(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0, rotate=None):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        self.image = pg.image.load('assets/images/shop/House.png').convert_alpha()
        self.pos = vec(x, y)
        self.rect = pg.Rect(x - 100, y - 50, self.image.get_width(), self.image.get_height())
        self.rect.topleft = self.pos


    def update(self, tile_rects, dt, player):
        return
        # Update the menu
        #

    def draw(self, display, scroll, hitbox=False, attack_box=False):
        # Draw the shop
        display.blit(self.image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

