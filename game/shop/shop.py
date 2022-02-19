import pygame as pg
from collections import deque
from .shop_menu import Shop_Menu
vec = pg.math.Vector2



class Shop:
    def __init__(self, player, x, y):
        self.shop_menu = Shop_Menu()
        self.player = player
        self.image = pg.image.load('assets/animations/chest/chest_3').convert_alpha()
        self.pos = vec(x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

        # Max amount of stat upgrades ap layer can get
        self.MAX_UPGRADES = 3
        # Tracks amount of upgrades done for each stat
        self.stat_upgrades = {
            'stamina': 0,
            'health': 0,
            'damage': 0
        }

        # Costs for level 1, 2, and 3 stat upgrades
        COSTS = [25, 50, 100]
        # Tracks the current cost of a stat upgrade
        self.stat_upgrade_costs = {
            'stamina': deque([COSTS[0], COSTS[1], COSTS[2], None]),
            'health': deque([COSTS[0], COSTS[1], COSTS[2], None]),
            'damage': deque([COSTS[0], COSTS[1], COSTS[2], None]),
        }

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
            self.shop_menu.update()

    def draw(self, display, scroll, hitbox=False, attack_box=False):
        # Draw the shop
        display.blit(self.image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

        # Draw the menu
        if self.show_menu:
            self.shop_menu.draw()

