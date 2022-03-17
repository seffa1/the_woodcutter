from game.engine import Entity
import pygame as pg


class Collectible(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str = None, WALK_ACC=0, FRIC=0, rotate=None):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        self.animation_frames['collectible'] = self.load_animation('assets/animations/collectible', [20, 10, 10])
        self.action = 'collectible'
        self.load_sound('pickup', 'assets/sounds/objects/collectible_pickup.wav')

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

    def check_pickup(self, player):
        """ If the player collides with our rect, kill ourselves """
        if self.rect.colliderect(player.rect):
            self.play_sound('pickup', .1)
            self.kill()

    def update(self, tile_rects, dt, player):
        self.set_image(dt)
        self.check_pickup(player)
