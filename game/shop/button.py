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
        self.pos = vec(x, y)
        self.rect = pg.Rect(x, y, width, height)
        self.rect.topleft = self.pos
        self.name = name

        # Button States
        self.clicked = False
        self.mouse_rect = None

    def update(self, mouse_rect, mouse_action):
        self.mouse_rect = mouse_rect
        self.image = self.images['default']
        # If the mouse is over the button
        if mouse_rect.colliderect(self.rect):
            # If we are left clicking
            if mouse_action[0]:
                self.image = self.images['pressed']

    def draw(self, display, scroll, hitbox=True, attack_box=False):
        if self.image is not None:
            display.blit(self.image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

        if hitbox:
            # hit_rect = pg.Rect(self.pos.x - scroll[0], self.pos.y - scroll[1], self.rect.width, self.rect.height)
            # pg.draw.rect(display, (255, 255, 255), hit_rect)

            if self.mouse_rect:
                mouse_rect = pg.Rect(self.mouse_rect.x - scroll[0], self.mouse_rect.y - scroll[1], self.mouse_rect.width, self.mouse_rect.height)
                pg.draw.rect(display, (255, 255, 255), mouse_rect)


