import pygame as pg
from game.engine import Entity


class Bullet(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str = None, WALK_ACC=0, FRIC=0, rotate=None):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC, rotate)

        self.animation_frames['bullet'] = self.load_animation('assets/animations/bullet', [1], True)
        self.action = 'bullet'
        self.DAMAGE = 10
        self.rect = pg.Rect(x, y, width, height)

    def move(self, dt):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        self.rect.topleft = self.pos

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

    def check_damage(self, player):
        if self.rect.colliderect(player.rect):
            player.lose_health(self.DAMAGE)
            self.kill()

        if self.pos.y > 1000:
            self.kill()

        if self.pos.x < -1000:
            self.kill()

        if self.pos.x > 1000:
            self.kill()

        if self.pos.y < -1000:
            self.kill()

    def update(self, tile_rects, dt, player):
        self.move(dt)
        self.set_image(dt)
        self.check_damage(player)
