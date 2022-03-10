from game.engine import Entity
import pygame as pg
from game.utils import calc_distance, Color
from game.objects.coin import Coin
import random, math
from .bullet import Bullet


class Projectile(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0, rotate=None, entity_manager=None):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        self.animation_frames['shoot'] = self.load_animation('assets/animations/rusty_gun/shoot', [10, 3, 5, 5, 5, 10], True)
        self.animation_frames['death'] = self.load_animation('assets/animations/rusty_gun/death', [5, 5, 5, 5, 5, 5, 5, 5], True)
        self.animation_frames['idle'] = self.load_animation('assets/animations/rusty_gun/idle', [1], True)

        # AI Constants
        self.AGGRO_RANGE = 200
        self.DEAGGRO_RANGE = 400
        self.PROJECTILE_SPEED = 3
        self.ATTACK_COOLDOWN = 120

        # AI Controller use
        self.aggro = False
        self.attack_cooldown = 0  # Used when we are not in aggro
        self.attack_cooldown_float = 0
        self.rotate = rotate
        self.entity_manager = entity_manager
        self.shoot = False
        self.idle = True

        # Debugging
        self.aim_rect = pg.Rect(x, y, 10, 5)

    def check_aggro(self, player):
        """ Checks if the player is within certain aggro distances """
        if calc_distance(self.rect.center[0], self.rect.center[1], player.rect.center[0], player.rect.center[1]) <= self.AGGRO_RANGE:
            self.aggro = True
        else:
            self.aggro = False
            self.shoot = False

    def projectile_AI(self, dt, player):
        """ If player in range, rotates and shoots a projectile at the play"""
        # Check if aggrod
        if not self.aggro:
            return
        # Check if dying
        if self.death:
            return
        # check if attack cool down isn't zero, reduce it, then return
        if self.attack_cooldown > 0:
            self.attack_cooldown_float -= 1 * dt
            self.attack_cooldown = int(round(self.attack_cooldown_float, 0))
            self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'idle')
            return
        else:
            self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'shoot')

        # Check if we are on the correct frame to spawn a bullet
        if not self.frame > 12:
            return

        # Calc vector pointing to player
        delta_x = player.pos.x - self.pos.x
        delta_y = player.pos.y - self.pos.y

        # Normalize the vector to the speed we want
        magnitude = math.sqrt(delta_y ** 2 + delta_x ** 2)
        normalizer = self.PROJECTILE_SPEED / magnitude
        X_vel = delta_x * normalizer
        Y_vel = delta_y * normalizer

        # Instantiate a bullet projectile with X vel and Y vel
        # Bullet projectile will check for collisions with the player, or get destroyed at a coordinate ( out of bounds)
        self.rotate = math.atan(X_vel / Y_vel) * 360 / (math.pi * 2)
        bullet = Bullet(self.pos.x + 30, self.pos.y + 6, 10, 10)
        bullet.vel.x = X_vel
        bullet.vel.y = Y_vel
        self.entity_manager.add_entity(bullet, bullet.type)
        self.attack_cooldown_float = self.ATTACK_COOLDOWN
        self.attack_cooldown = self.ATTACK_COOLDOWN

    def actions(self, dt):
        """ Determine the current action and update the image accordingly """
        # Death check
        if self.death:
            self.shoot = False
            self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'death')
            return

    def set_image(self, dt):
        """ Update the current image """
        self.frame_float += 1 * dt
        self.frame = int(round(self.frame_float, 0))

        # If your animation frames come to an end
        if self.frame >= len(self.animation_frames[self.action]):
            if self.action == 'death':
                self.kill()
            # Any non-looping actions get reset here
            self.shoot = False
            self.attack_timer = 0
            self.attack_timer_float = 0
            self.attack_rect = None
            self.frame = 0
            self.frame_float = 0

        image_id = self.animation_frames[self.action][self.frame]
        image = self.animation_images[image_id]
        self.image = image

    def check_damage(self, player):
        if not player.attack_rect:
            return
        if player.attack_rect.colliderect(self.rect):
            self.death = True

    def draw(self, display, scroll, hitbox=False, attack_box=False, aim_rect=False):
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
        self.check_damage(player)
        self.actions(dt)  # Determine the player's action
        self.set_image(dt)  # Set the image based on the player's action
