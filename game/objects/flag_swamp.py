from game.engine import Entity
import pygame as pg


class Flag_Swamp(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str = None, WALK_ACC=0, FRIC=0, rotate=None, entity_manager=None):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        self.animation_frames['flag_swamp'] = self.load_animation('assets/animations/flag_swamp', [25, 25, 25, 25], True)
        self.action = 'flag_swamp'

    def set_image(self, dt):
        """ Update the current image """
        self.frame_float += 1 * dt
        self.frame = int(round(self.frame_float, 0))

        # Only triggers after the opening animation
        if self.frame >= len(self.animation_frames[self.action]):
            self.frame = 0
            self.frame_float = 0

        image_id = self.animation_frames[self.action][self.frame]
        image = self.animation_images[image_id]
        self.image = image

    def update(self, tile_rects, dt, player):
        self.set_image(dt)

    def draw(self, display, scroll, hitbox=False, attack_box=False):
        display.blit(self.image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))