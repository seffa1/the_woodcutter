import pygame as pg
from collections import deque
from .shop_menu import Shop_Menu
vec = pg.math.Vector2
from game.engine import Entity




class Shop(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0, rotate=None):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        self.shop_menu = Shop_Menu(x, y, 540, 330)
        self.image = pg.image.load('assets/images/shop/House.png').convert_alpha()
        self.pos = vec(x, y)
        self.rect = pg.Rect(x - 100, y - 50, self.image.get_width(), self.image.get_height())
        self.rect.topleft = self.pos

        self.show_menu = False

    def check_collision(self, player):
        """ Checks if the player has collided, if so, shows the buy menu """
        if self.rect.colliderect(player.rect):
            self.show_menu = True
        else:
            self.show_menu = False

    def update(self, tile_rects, dt, player):
        self.check_collision(player)

        # Update the menu
        if self.show_menu:
            self.shop_menu.update(tile_rects, dt, player)

    def draw(self, display, scroll, screen, hitbox=False, attack_box=False):
        # Draw the shop
        display.blit(self.image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

        # # Draw the menu
        # if self.show_menu:
        #     self.shop_menu.draw(display, scroll, screen, hitbox=False, attack_box=False)

    def draw_menu(self, display, scroll, screen):
        # Draw the menu
        if self.show_menu:
            self.shop_menu.draw(display, scroll, screen, hitbox=False, attack_box=False)

