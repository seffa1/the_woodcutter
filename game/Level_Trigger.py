import pygame as pg




class Level_Trigger:
    def __init__(self, x, y, width, height, level_to_go_to):
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, width, height)
        self.image = None
        self.RED = (255, 0, 0)
        self.GREEN = (0, 0, 255)
        self.color = (255, 0, 0)

    def update(self, player):
        """ Checks if the player has collided, then prompts them to press enter """
        if self.rect.colliderect(player.rect):
            self.color = self.GREEN
        else:
            self.color = self.RED

    def draw(self, display, scroll):
        if self.image is not None:
            display.blit(self.image, self.x - scroll[0], self.y - scroll[1])
        pg.draw.rect(display, self.color, self.rect)


