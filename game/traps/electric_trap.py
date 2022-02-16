import pygame as pg
from game.engine import Entity

vec = pg.math.Vector2

class Electric_Trap(Entity):
    """ A trap which goes on and off"""
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0, rotate=None):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        self.pos = vec(x, y)
        self.width = width
        self.height = height
        self.DAMAGE = 25
        self.health = 100
        # Sets how long the trap remains off, along with its hitbox
        self.IDLE_TIME = 90
        self.animation_frames['electric_trap'] = self.load_animation('assets/animations/electric_trap', [self.IDLE_TIME, 10, 10, 10, 10, 10])
        self.rect = None

        # The electric trap only has one action which is to constantly turn on and off
        self.action = 'electric_trap'
        self.rotate = rotate

    def set_image(self, dt):
        """ Update the current image """
        self.frame_float += 1 * dt
        self.frame = int(round(self.frame_float, 0))

        if self.frame >= len(self.animation_frames[self.action]):
            self.frame = 0
            self.frame_float = 0

        image_id = self.animation_frames[self.action][self.frame]
        image = self.animation_images[image_id]
        self.image = image

    def hitboxes(self, dt, player):
        if self.frame >= self.IDLE_TIME:
            self.rect = pg.Rect(self.pos.x, self.pos.y, self.width, self.height)
            self.check_damage(player)
        else:
            self.rect = None

    def check_damage(self, player):
        if self.rect.colliderect(player.rect):
            player.lose_health(self.DAMAGE)

    def update(self, tile_rects, dt, player):
        self.set_image(dt)
        self.hitboxes(dt, player)

    def draw(self, display, scroll, hitbox=False, attack_box=False):
        display.blit(self.image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

        if self.rect is not None and hitbox:
            hit_rect = pg.Rect(self.pos.x - scroll[0], self.pos.y - scroll[1], self.width, self.height)
            pg.draw.rect(display, (0, 255, 0), hit_rect)

