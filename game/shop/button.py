import pygame as pg

vec = pg.math.Vector2

class Button:
    """ Move this to its own file """
    def __init__(self, name, x, y, width, height):
        self.image = pg.transform.scale(pg.image.load('assets/images/shop/button_default.png').convert_alpha(),(width, height))
        self.images = {
            'default': pg.transform.scale(pg.image.load('assets/images/shop/button_default.png').convert_alpha(),(width, height)),
            'pressed':pg.transform.scale(pg.image.load('assets/images/shop/button_pressed.png').convert_alpha(),(width, height))
        }
        self.name = name
        self.pos = vec(x, y)
        self.width = width
        self.height = height

        # Button States
        self.clicked = False

    def update(self, mouse_info):
        mouse_pos = mouse_info[0]
        mouse_pressed = mouse_info[1]
        # Check if mouse not within button, if so, return
        # Check if mouse is clicked, if so, pressed = true
        # Else, hovered = True
        # Set image accordingly
        # If clicked, activate a purchase method
        pass

    def draw(self, display, scroll, hitbox=False, attack_box=False):
        if self.image is not None:
            display.blit(self.image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))