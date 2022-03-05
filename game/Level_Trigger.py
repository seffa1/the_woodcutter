import pygame as pg
from .utils import draw_text



class Level_Trigger:
    def __init__(self, x, y, width, height, level_to_go_to, image_path):
        self.x = x
        self.y = y
        self.level_to_go_to = level_to_go_to
        self.image = pg.transform.scale(pg.image.load(image_path).convert_alpha(), (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 0, 255)
        self.color = (255, 0, 0)
        self.collided = False

    def update(self, player):
        """ Checks if the player has attacked the trigger and reports it to the level manager """
        if player.attack_rect:
            if self.rect.colliderect(player.attack_rect):
                self.color = self.GREEN
                self.collided = True

        else:
            self.color = self.RED
            self.collided = False

    def draw(self, display, scroll, hitbox=True):
        if self.image is not None:
            display.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))
        if hitbox:
            scrolled_rect = pg.Rect(self.x - scroll[0], self.y - scroll[1], self.rect.width, self.rect.height)
        pg.draw.rect(display, self.color, scrolled_rect)
        if self.collided:
            draw_text(display, f'Travel to {self.level_to_go_to}', 15, (0, 0, 0), (self.x - scroll[0] + self.rect.width + 5, self.y - scroll[1] - 5))

