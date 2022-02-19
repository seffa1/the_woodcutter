import pygame as pg

vec = pg.math.Vector2

class Shop_Menu:
    def __init__(self):
        self.image = pg.image.load('assets/animations/coin/coin_0').convert_alpha()
        self.load_buttons()
        self.buttons = []

    def load_buttons(self):
        """ Instantiates and adds buttons to self.buttons """
        pass

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


class Button:
    """ Move this to its own file """
    def __init__(self, name, x, y, width, height):
        self.image = None
        self.images = {
            'default': None,
            'hovered': None,
            'pressed': None
        }
        self.name = name
        self.pos = vec(x, y)
        self.width = width
        self.height = height

        # Button States
        self.hovered = False
        self.clicked = False



    def update(self, mouse_pos, mouse_pressed):
        # Check if mouse not within button, if so, return
        # Check if mouse is clicked, if so, pressed = true
        # Else, hovered = True
        # Set image accordingly
        # If clicked, activate a purchase method
        pass

    def draw(self, display, scroll, hitbox=False, attack_box=False):
        if self.image is not None:
            display.blit(self.image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))



