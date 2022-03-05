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
        self.animation_frames['attack_1'] = self.load_animation('assets/animations/player/attack_1',[2, 2, 4, 4, 4, 4])
        self.animation_frames['jump'] = self.load_animation('assets/animations/player/jump',[5, 5, 7, 7, 7, 7])
        self.animation_frames['hurt'] = self.load_animation('assets/animations/player/hurt',[5, 10, 5])
        self.animation_frames['death'] = self.load_animation('assets/animations/player/death',[5, 5, 10, 10, 20, 30])
        # Charge attack - in progress
        self.animation_frames['charge_up'] = self.load_animation('assets/animations/player/charge_up',[3, 4, 6])
        self.animation_frames['hold'] = self.load_animation('assets/animations/player/hold',[1])
        self.animation_frames['swing'] = self.load_animation('assets/animations/player/swing',[5, 5, 5])
        self.set_type('player')

        # Player stats
        self.coins = 300
        self.STAMINA_PER_LEVEL = 10  # How much leveling up stamina increases max stamina
        self.HEALTH_PER_LEVEL = 10
        self.SPEED_PER_LEVEL = .01  # Increases your running speed
        self.run_acc = .2  # Gets added to the walking speed
        self.WALL_JUMP_VEL = 15

        # Player Health
        self.health = 100
        self.max_health = 100

        # Player Stamina
        self.stamina = 100
        self.stamina_float = 100
        self.max_stamina = 100
        self.STAMINA_RUN_DRAIN = .3
        self.STAMINA_REGEN_RATE = 5.25
        self.STAMINA_USE = {'attack_1': 5, 'roll': 20, 'jump': 10}

        # Player Attacking
        self.damages = {'attack_1': 25,
                        'charge_up': 0}
        self.charge_damage_float = 0
        self.CHARGE_SPEED = 5
        self.MAX_CHARGE_DAMAGE = 100
        self.DAMAGE_COOLDOWN = 25  # How many frames you are invinciple for after taking damage
        self.attack = {'1': False, '2': False}

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
        if self.run or self.attacking or self.roll or self.hold:
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
                # self.vel.x = -self.WALL_JUMP_VEL
                self.vel.x -= self.WALL_JUMP_VEL
            if self.collision_types['left'] and not self.collision_types['bottom']:
                # self.vel.x = self.WALL_JUMP_VEL
                self.vel.x += self.WALL_JUMP_VEL
            self.vel.y = self.JUMP_VEL

    def hitboxes(self, dt):
        ''' Creates a hitbox which starts and stops from a timer after an attack is used. '''
        # Check if we are attacking
        if not self.attacking:
            self.damage = 0
            self.attack_timer_float = 0
            return

        # Hit box spawner could be made into a general use function instead of being specific
        if self.attack['1']:
            self.damage = self.damages['attack_1']
            self.attack_timer_float += 1 * dt
            self.attack_timer = int(round(self.attack_timer_float, 0))

            if self.attack_timer > 14:  # 10 is to be adjusted as we go
                if not self.flip:
                    self.attack_rect = pg.Rect(self.rect.right, self.rect.centery - 8, 10, 23)
                else:
                    self.attack_rect = pg.Rect(self.rect.left, self.rect.centery - 8, 10, 23)
            # if self.attack_timer > 30:
            #     self.attack_rect = None

        if self.attack['2']:
            self.damage = self.damages['charge_up']
            self.attack_timer_float += 1 * dt
            self.attack_timer = int(round(self.attack_timer_float, 0))

            if self.attack_timer > 4:  # 10 is to be adjusted as we go
                if not self.flip:
                    self.attack_rect = pg.Rect(self.rect.right - (10 + (0.15 * self.damage))/2, self.rect.centery - 8, 10 + (0.15 * self.damage), 23)
                else:
                    self.attack_rect = pg.Rect(self.rect.left - (10 + (0.15 * self.damage))/2, self.rect.centery - 8, 10 + (0.15 * self.damage), 23)
            if self.attack_timer > 30:
                self.attack_rect = None

    def set_image(self, dt):
        """ Update the current image """
        self.frame_float += 1 * dt
        self.frame = int(round(self.frame_float, 0))

        # If your animation frames come to an end
        if self.frame >= len(self.animation_frames[self.action]):
            if self.action == 'death':
                if self.type != 'player':
                    self.kill()
                    self.drop_loot()
                else:
                    self.respawn()

            # When the charge animation finished, it goes to hold
            if self.action == 'charge_up':
                self.hold = True
                self.charge_up = False
                return

            # Any non-looping actions get reset here
            self.attacking = False
            self.hurt = False
            self.roll = False
            self.attack['1'] = False
            # self.attack['2'] = False
            self.attack_timer = 0
            self.attack_timer_float = 0
            self.jumping = False
            self.attack_rect = None
            self.invincible = False
            self.rect.height = self.height

            # If it is a looping animation, loops it
            # A janky 'fix' for inherantly stupid code
            # When an animation gets fixed, it resets the frames, THEN, it sets the image again
            # So at the end of the animation it re-draws the first frame BEFORE switching to the next animation
            # You can notice it except for the charge attack, so i manually am getting around it here
            # Since i cant figure out a better fix right nowd
            if not self.attack['2']:
                self.frame = 0
                self.frame_float = 0
            else:
                self.frame = len(self.animation_frames[self.action]) - 1

                # Resets charge attack damage variable once animation ends
                self.damages['charge_up'] = 0
                self.charge_damage_float = 0

            self.attack['2'] = False

        image_id = self.animation_frames[self.action][self.frame]
        image = self.animation_images[image_id]
        self.image = image

    def draw(self, display, scroll, hitbox=False, attack_box=True):
        # Draw the player hitbox ( DEBUGGING )
        if hitbox:
            hit_rect = pg.Rect(self.pos.x - scroll[0], self.pos.y - scroll[1], self.rect.width, self.rect.height)
            pg.draw.rect(display, (0, 255, 0), hit_rect)


        # Draw the player
        player_image = pg.transform.flip(self.image, self.flip, False)
        display.blit(player_image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

        # Draw the attack hitbox ( DEBUGGING )
        if attack_box:
            if self.attack_rect is not None:
                attack_rect_scrolled = pg.Rect(self.attack_rect.x - scroll[0],
                                                        self.attack_rect.y - scroll[1],
                                                        self.attack_rect.width, self.attack_rect.height)
                pg.draw.rect(display, (255, 0, 0), attack_rect_scrolled)

    def charge_attack(self, dt):
        ''' Update the charge damage if we are holding the charge '''
        if not self.hold:
            return
        # If we have no more stamina
        if self.stamina <= 0:
            return

        # Charge up the damage value for the charge attack hold
        self.charge_damage_float += self.CHARGE_SPEED * dt
        if self.charge_damage_float > self.MAX_CHARGE_DAMAGE:
            self.charge_damage_float = self.MAX_CHARGE_DAMAGE

        # Set the damage variable
        self.damages['charge_up'] = int(round(self.charge_damage_float, 0))
        self.damage = self.damages['charge_up']

        # Drain stamina
        self.drain_stamina(1, dt)


    def update(self, tile_rects, dt, player=None):
        self.check_dead()
        self.move(tile_rects, dt)  # Update players position
        self.actions(dt)  # Determine the player's action
        self.gain_stamina(dt)  # Regain stamina
        self.set_image(dt)  # Set the image based on the player's action
        self.charge_attack(dt)
        self.hitboxes(dt)  # Update any hit boxes from player's attack






