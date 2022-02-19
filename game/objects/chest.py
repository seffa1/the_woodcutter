from game.engine import Entity
import pygame as pg
import random
from game.objects.coin import Coin


class Chest(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str = None, WALK_ACC=0, FRIC=0, rotate=None, entity_manager=None):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        self.animation_frames['chest'] = self.load_animation('assets/animations/chest', [10, 10, 10, 10], True)

        # Image is default to closed
        self.image = pg.image.load('assets/animations/chest/chest_0.png').convert_alpha()
        self.flip = False

        self.entity_manager = entity_manager

        # Actions
        self.closed = True  # Causes the image to be hard set to the closed image instead of animating
        self.opened = False  # Causes the image to be hard set to the open image instead of animating

        # Triggers the opening animation, after, the image is set to open perennially
        self.chest = False  # Triggers the opening animation
        self.action = None

    def drop_loot(self):
        """ This function must be defined the the children classes """
        amount = random.randint(5, 10)
        for i in range(0, amount):
            coin = Coin(self.pos.x, self.pos.y, 9, 9, 'coin', 0, 0, 0)
            x_vel = random.randint(-4, 4)
            y_vel = random.randint(-5, -0)
            coin.vel.y = y_vel
            coin.vel.x = x_vel
            self.entity_manager.add_entity(coin, coin.type)

    def set_image(self, dt):
        """ Update the current image """
        if self.action == None:
            return
        self.frame_float += 1 * dt
        self.frame = int(round(self.frame_float, 0))

        # Only triggers after the opening animation
        if self.frame >= len(self.animation_frames[self.action]):
            self.frame = 0
            self.frame_float = 0

            self.drop_loot()
            # Image gets set to the open image permanently
            self.image = pg.image.load('assets/animations/chest/chest_3.png').convert_alpha()
            self.action = None  # The action can only happen once
            self.opened = True

        # Only update the image if its in the opening action
        if self.action:
            image_id = self.animation_frames[self.action][self.frame]
            image = self.animation_images[image_id]
            self.image = image

    def change_actions(self, current_action, current_frame, frame_float, new_action):
        """ Only reset animation frames if going from one animation to another """
        if current_action != new_action:
            current_action = new_action
            current_frame = 0
            frame_float = 0
        return current_action, current_frame, frame_float

    def actions(self, dt):
        """ Determine the current action and update the image accordingly """
        # If the chest is being opened
        if self.chest and not self.opened:
            self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'chest')

    def check_pickup(self, player):
        """ If the player collides with our rect, kill ourselves """
        if self.rect.colliderect(player.rect):
            # Opens the chest, I know, its a confusing variable name
            self.chest = True

    def update(self, tile_rects, dt, player):
        self.actions(dt)
        self.set_image(dt)
        self.check_pickup(player)

    def draw(self, display, scroll, hitbox=False, attack_box=False):
        display.blit(self.image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

