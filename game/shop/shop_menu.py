import pygame as pg
from .button import Button
from game.utils import draw_text
from collections import deque

vec = pg.math.Vector2

class Shop_Menu:
    def __init__(self, x, y, width, height):
        self.image = pg.transform.scale(pg.image.load('assets/images/shop/upgrades_menu_text.png').convert_alpha(), (width, height))

        # Offsets the menu from the shop's image
        self.OFFSET_X = -15
        self.OFFSET_Y = -110
        self.pos = vec(x + self.OFFSET_X, y + self.OFFSET_Y)
        self.buttons = []
        self.load_buttons()

        # Max amount of stat upgrades ap layer can get
        self.MAX_UPGRADES = 3
        # Tracks amount of upgrades done for each stat
        self.stat_upgrades = {
            'stamina': 0,
            'health': 0,
            'damage': 0 }

        # Costs for level 1, 2, and 3 stat upgrades
        COSTS = [25, 50, 100]
        # Tracks the current cost of a stat upgrade
        self.stat_upgrade_costs = {
            'health': deque([COSTS[0], COSTS[1], COSTS[2], None]),
            'stamina': deque([COSTS[0], COSTS[1], COSTS[2], None]),
            'damage': deque([COSTS[0], COSTS[1], COSTS[2], None]) }

    def load_buttons(self):
        """ Instantiates and adds buttons to self.buttons """
        BUTTON_WIDTH = 30
        BUTTON_HEIGHT = 15
        OFFSET_X = 142
        OFFSET_Y = 35
        SPACING_Y = 26
        button_1 = Button('health', self.pos.x + OFFSET_X, self.pos.y + OFFSET_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_2 = Button('stamina', self.pos.x + OFFSET_X, self.pos.y + OFFSET_Y + SPACING_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_3 = Button('damage', self.pos.x + OFFSET_X, self.pos.y + OFFSET_Y + SPACING_Y * 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.buttons.append(button_1)
        self.buttons.append(button_2)
        self.buttons.append(button_3)

    def check_mouse(self):
        """ If menu is showing, respond to the mouse inputs """
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()
        return mouse_pos, mouse_pressed

    def update(self, tile_rects, dt, player):
        """ Update the buttons, passing the the mouse pos and pressed """
        for button in self.buttons:
            button.update(self.check_mouse())

    def draw(self, display, scroll, hitbox=False, attack_box=False):
        """ Draw the menu background, then draw each button """
        # Draw the menu
        display.blit(self.image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

        # Draw the buttons
        for button in self.buttons:
            button.draw(display, scroll)

        # Draw the costs
        OFFSET_X = 10
        OFFSET_Y = 1
        draw_text(display, f'{self.stat_upgrade_costs["health"][0]}', 15, (255, 0, 0),
                  (self.buttons[0].pos.x - scroll[0] + OFFSET_X, self.buttons[0].pos.y - scroll[1] + OFFSET_Y))
        draw_text(display, f'{self.stat_upgrade_costs["stamina"][0]}', 15, (255, 0, 0),
                  (self.buttons[1].pos.x - scroll[0] + OFFSET_X, self.buttons[1].pos.y - scroll[1]+ OFFSET_Y))
        draw_text(display, f'{self.stat_upgrade_costs["damage"][0]}', 15, (255, 0, 0),
                  (self.buttons[2].pos.x - scroll[0] + OFFSET_X, self.buttons[2].pos.y - scroll[1]+ OFFSET_Y))

        # Draw the ability levels
        ABILITY_OFFSET_X = 40
        ABILITY_OFFSET_y = 50







