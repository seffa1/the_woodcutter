import pygame as pg




class Level_Trigger:
    def __init__(self, x, y, width, height, level_to_go_to, image_path):
        self.x = x
        self.y = y
        self.image = pg.transform.scale(pg.image.load(image_path).convert_alpha(), (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 0, 255)
        self.color = (255, 0, 0)

    def update(self, player):
        """ Checks if the player has collided, then prompts them to press enter """
        if self.rect.colliderect(player.rect):
            self.color = self.GREEN
        else:
            self.color = self.RED

    def draw(self, display, scroll, hitbox=True):
        if self.image is not None:
            display.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))
        if hitbox:
            scrolled_rect = pg.Rect(self.x - scroll[0], self.y - scroll[1], self.rect.width, self.rect.height)
        pg.draw.rect(display, self.color, scrolled_rect)


