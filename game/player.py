import pygame as pg
from collections import deque
from .engine import Entity


class Player(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC)

        self.set_static_image('assets/animations/player/idle/idle_0.png')
        self.animation_frames['idle'] = self.load_animation('assets/animations/player/idle',[10, 10, 10, 10])
        self.animation_frames['walk'] = self.load_animation('assets/animations/player/walk',[5, 5, 5, 5, 5, 5])
        self.animation_frames['run'] = self.load_animation('assets/animations/player/run',[5, 5, 5, 5, 5, 5])
        self.animation_frames['roll'] = self.load_animation('assets/animations/player/roll',[2, 2, 5, 5, 2, 2])
        self.animation_frames['attack_1'] = self.load_animation('assets/animations/player/attack_1',[10, 10, 6, 5, 5, 5])
        self.animation_frames['jump'] = self.load_animation('assets/animations/player/jump',[5, 5, 7, 7, 7, 7])
        self.animation_frames['hurt'] = self.load_animation('assets/animations/player/hurt',[5, 10, 5])
        self.animation_frames['death'] = self.load_animation('assets/animations/player/death',[5, 5, 10, 10, 20, 30])
        self.set_type('player')

        # Player stats
        self.coins = 100
        self.STAMINA_PER_LEVEL = 10  # How much leveling up stamina increases max stamina
        self.HEALTH_PER_LEVEL = 10
        self.SPEED_PER_LEVEL = .01  # Increases your running speed
        self.run_acc = .2  # Gets added to the walking speed
        self.WALL_JUMP_VEL = 15

        # Player Health
        self.health = 100
        self.max_health = 100

        # Player Stamina
        self.stamina = 200
        self.stamina_float = 200
        self.max_stamina = 200
        self.STAMINA_RUN_DRAIN = .3
        self.STAMINA_REGEN_RATE = 5.25
        self.STAMINA_USE = {'attack_1': 15, 'roll': 20, 'jump': 10}

        # Player Attacking
        self.DAMAGES = {'attack_1': 25}
        self.DAMAGE_COOLDOWN = 25  # How many frames you are invinciple for after taking damage

    def add_coin(self, amount):
        """ Adds coins """
        self.coins += int(amount)

    def use_stamina(self, amount):
        """ For fixed stamina use like attacks, rolling, and jumping"""
        self.stamina_float -= amount
        self.stamina = int(round(self.stamina_float, 0))
        if self.stamina_float <= 0:
            self.stamina_float = 0

    def drain_stamina(self, amount, dt):
        """ For stamina use that has to consider dt, like running """
        self.stamina_float -= amount * dt
        self.stamina = int(round(self.stamina_float, 0))
        if self.stamina_float <= 0:
            self.stamina_float = 0

    def gain_stamina(self, dt):
        """ For stamina recovery """
        if self.run or self.attacking or self.roll:
            return
        self.stamina_float += self.STAMINA_REGEN_RATE * dt
        self.stamina = int(round(self.stamina_float, 0))
        if self.stamina_float >= self.max_stamina:
            self.stamina_float = self.max_stamina

    def move(self, tile_rects, dt):
        # Reset collisions
        self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        # Reset acceleration
        self.acc.x = 0

        # Calculate acceleration
        if not self.roll:
            if self.walk_left:
                self.acc.x = -self.WALK_ACC
                if self.run:
                    self.acc.x -= self.run_acc
                    self.drain_stamina(self.STAMINA_RUN_DRAIN, dt)
            if self.walk_right:
                self.acc.x = self.WALK_ACC
                if self.run:
                    self.acc.x += self.run_acc
                    self.drain_stamina(self.STAMINA_RUN_DRAIN, dt)
            # If we are holding both right and left controls, you dont move
            if self.walk_left and self.walk_right:
                self.acc.x = 0

            # The faster we are moving, the less we accelerate
            # The faster we are moving, the more we DEccelerate
            # Down side of this is we cant control the accerate and deccelerate curves independtently
            # We good make two FRIC values, and use one for speeding up, and one for slowing down
            # if abs(self.vel.x) < 0.0001: self.vel.x = 0
            self.acc.x += self.vel.x * self.FRIC

        # Adjust velocity
            self.vel.x += self.acc.x
            # This is to prevent velocity from decreasing infinetly when we slow down as the friction equation above
            # Creates an asymptot at our max speed and at zero
            if abs(self.vel.x) < 0.01:
                self.vel.x = 0
        else:
            # Whatever direction we are facing is what direction we roll with a fixed speed
            if not self.flip:  # Facing right
                self.vel.x = self.ROLL_VEL
            else:  # Facing left
                self.vel.x = -self.ROLL_VEL

        # Adjust position
        self.pos.x += self.vel.x * dt
        self.rect.topleft = self.pos

        # Check for collisions in the x axis
        hit_list = self.collision_test(self.rect, tile_rects)
        for tile in hit_list:
            if self.vel.x > 0:
                self.collision_types['right'] = True
                self.rect.right = tile.left
                self.pos.x = self.rect.topleft[0]
            if self.vel.x < 0:
                self.collision_types['left'] = True
                self.rect.left = tile.right
                self.pos.x = self.rect.topleft[0]

        # X-axis collision updates


        # Y axis
        self.acc.y = self.GRAV * dt
        self.vel.y += self.acc.y
        if self.vel.y > self.MAX_FALL_SPEED:
            self.vel.y = self.MAX_FALL_SPEED


        self.pos.y += self.vel.y * dt
        self.rect.topleft = self.pos

        # Check for collisions in the y axis
        hit_list = self.collision_test(self.rect, tile_rects) # TODO The hit list is growing over time, causing the program to crash
        for tile in hit_list:
            # If you are falling
            if self.vel.y > 0:
                self.collision_types['bottom'] = True
                self.rect.bottom = tile.top  # Change the rect's position because of convientient methods
                self.pos.y = self.rect.topleft[1]
                self.vel.y = 1
            if self.vel.y < 1:
                self.collision_types['top'] = True
                self.rect.top = tile.bottom
                self.pos.y = self.rect.topleft[1]
                self.vel.y = 0

        # Updates from y-axis collisions
        if self.collision_types['bottom'] or self.collision_types['right'] or self.collision_types['left']:
            self.air_timer = 0
            self.wall_jump_timer = 0
            self.jumping = False
        else:
            self.air_timer += 1

        # Wall grab check
        if self.walk_right and self.collision_types['right'] and not self.collision_types['bottom'] and not self.walk_left and self.vel.y > 0:
            self.vel.y = 1
        if self.walk_left and self.collision_types['left'] and not self.collision_types['bottom'] and not self.walk_right and self.vel.y > 0:
            self.vel.y = 1

    def jump(self):
        if self.air_timer < self.AIR_TIME:
            self.jumping = True
            if self.collision_types['right'] and not self.collision_types['bottom']:
                self.vel.x = -self.WALL_JUMP_VEL
            if self.collision_types['left'] and not self.collision_types['bottom']:
                self.vel.x = self.WALL_JUMP_VEL
            self.vel.y = self.JUMP_VEL

    def update(self, tile_rects, dt, player=None):
        self.check_dead()
        self.move(tile_rects, dt)  # Update players position
        self.actions(dt)  # Determine the player's action
        self.gain_stamina(dt)  # Regain stamina
        self.set_image(dt)  # Set the image based on the player's action
        self.hitboxes(dt)  # Update any hit boxes from player's attack






