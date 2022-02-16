import pygame as pg
from game.engine import Entity


class Spikes(Entity):
    """ Spikes that can be placed on the ground, walls, or ceiling which can retract """
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0, rotate=None):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC)
        self.rotate = rotate
        self.image = pg.transform.scale(pg.image.load('assets/images/traps/spikes/spikes_0.png').convert_alpha(),
                                        (width, height))
        if self.rotate:
            self.image = pg.transform.rotate(self.image, self.rotate)

        self.DAMAGE = 25

    def update(self, tile_rects, dt, player):
        if self.rect.colliderect(player.rect):
            player.lose_health(self.DAMAGE)

    def draw(self, display, scroll, hitbox=True, attack_box=False):
        display.blit(self.image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

