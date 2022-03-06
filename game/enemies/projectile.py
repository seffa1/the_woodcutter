from game.engine import Entity
import pygame as pg
from game.utils import calc_distance, Color
from game.objects.coin import Coin
import random, math
from .bullet import Bullet


class Projectile(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0, rotate=None, entity_manager=None):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        self.animation_frames['idle'] = self.load_animation('assets/animations/electric_trap', [10, 10, 10, 10, 10, 10], True)

        # AI Constants
        self.AGGRO_RANGE = 200
        self.DEAGGRO_RANGE = 400
        self.PROJECTILE_SPEED = 3
        self.ATTACK_COOLDOWN = 40

        # AI Controller use
        self.aggro = False
        self.attack_cooldown = 0  # Used when we are not in aggro
        self.attack_cooldown_float = 0
        self.rotate = rotate
        self.entity_manager = entity_manager

        # Debugging
        self.aim_rect = pg.Rect(x, y, 10, 5)
        self.x_vel = 0
        self.y_vel = 0

    def check_aggro(self, player):
        """ Checks if the player is within certain aggro distances """
        if calc_distance(self.rect.center[0], self.rect.center[1], player.rect.center[0], player.rect.center[1]) <= self.AGGRO_RANGE:
            self.aggro = True
        if calc_distance(self.rect.center[0], self.rect.center[1], player.rect.center[0], player.rect.center[1]) >= self.DEAGGRO_RANGE:
            self.aggro = False

    def projectile_AI(self, dt, player):
        """ If player in range, rotates and shoots a projectile at the play"""
        # if not agro, return
        if not self.aggro:
            return

        # check if attack cool down isn't zero, reduce it, then return
        if self.attack_cooldown > 0:
            self.attack_cooldown_float -= 1 * dt
            self.attack_cooldown = int(round(self.attack_cooldown_float, 0))
            return

        # Calc vector pointing to player
        delta_x = player.pos.x - self.pos.x
        delta_y = player.pos.y - self.pos.y

        # Normalize the vector to the speed we want
        magnitude = math.sqrt(delta_y ** 2 + delta_x ** 2)
        normalizer = self.PROJECTILE_SPEED / magnitude
        X_vel = delta_x * normalizer
        Y_vel = delta_y * normalizer

        self.x_vel, self.y_vel = X_vel, Y_vel
        # print(f'magnitude {magnitude}')
        # print(f'normalizer {normalizer}')
        # print(f'X {self.x_vel}')
        # print(f'Y {self.y_vel}\n')

        # Instantiate a bullet projectile with X vel and Y vel
        # Bullet projectile will check for collisions with the player, or get destroyed at a coordinate ( out of bounds)
        self.rotate = math.atan(X_vel / Y_vel) * 360 / (math.pi * 2)
        bullet = Bullet(self.pos.x, self.pos.y, 10, 10)
        bullet.vel.x = X_vel
        bullet.vel.y = Y_vel
        self.entity_manager.add_entity(bullet, bullet.type)
        self.attack_cooldown_float = self.ATTACK_COOLDOWN
        self.attack_cooldown = self.ATTACK_COOLDOWN

    def actions(self, dt):
        """ Determine the current action and update the image accordingly """

        # Flip check
        if self.vel.x > 0:
            self.flip = False
        if self.vel.x < 0:
            self.flip = True

        # Death check
        if self.death:
            self.walk_right = False
            self.walk_left = False
            self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'death')
            return

        # Attack Check
        if self.attacking:
            # Basic attack
            if self.attack['1']:
                self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'attack_1')

    def set_image(self, dt):
        """ Update the current image """
        self.frame_float += 1 * dt
        self.frame = int(round(self.frame_float, 0))

        # If your animation frames come to an end
        if self.frame >= len(self.animation_frames[self.action]):
            if self.action == 'death':
                self.kill()

            # Any non-looping actions get reset here
            self.attacking = False
            self.attack['1'] = False
            self.attack_timer = 0
            self.attack_timer_float = 0
            self.attack_rect = None
            self.frame = 0
            self.frame_float = 0

        image_id = self.animation_frames[self.action][self.frame]
        image = self.animation_images[image_id]
        self.image = image

    def draw(self, display, scroll, hitbox=False, attack_box=False, aim_rect=True):
        if hitbox:
            hit_rect = pg.Rect(self.pos.x - scroll[0], self.pos.y - scroll[1], self.rect.width, self.rect.height)
            pg.draw.rect(display, (0, 255, 0), hit_rect)

        # Flip the image if we need to, and then blit it
        player_image = pg.transform.flip(self.image, self.flip, False)
        display.blit(player_image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

        if attack_box:
            if self.attack_rect is not None:
                attack_rect_scrolled = pg.Rect(self.attack_rect.x - scroll[0],
                                                        self.attack_rect.y - scroll[1],
                                                        self.attack_rect.width, self.attack_rect.height)
                pg.draw.rect(display, (255, 0, 0), attack_rect_scrolled)

        if aim_rect:
            # arrow = pg.image.load('assets/images/ui/arrow.png').convert_alpha()
            # pg.transform.rotate(arrow, int(self.rotate))
            # display.blit(arrow, (self.pos.x - scroll[0], self.pos.y - scroll[1]))
            aimer = pg.Rect(self.pos.x + self.x_vel - scroll[0], self.pos.y + self.y_vel - scroll[1], 10, 10)
            pg.draw.rect(display, (0, 255, 0), aimer)

    def update(self, tile_rects, dt, player=None):
        self.projectile_AI(dt, player)
        self.check_aggro(player)
        self.actions(dt)  # Determine the player's action
        self.set_image(dt)  # Set the image based on the player's action
