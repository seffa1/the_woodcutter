import pygame as pg
import math


vec = pg.math.Vector2


# Any object in the game i think?
class Entity(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0, rotate=None):
        super().__init__()
        # Physics
        self.rotate = rotate
        self.type = type
        self.height = height
        self.pos = vec(x, y)  # A funtion of out velocity and any collisions
        self.vel = vec(0, 0)  # A function of our current acceleration
        self.acc = vec(0, 0)  # A function of our current velocity and friction
        self.rect = pg.Rect(x, y, width, height)
        self.rect.topleft = self.pos
        self.attack_rect = None  # Used to create a hitbox rect for attack collision detection. Gets created as we attack

        # Timers
        self.air_timer = 0  # Keeps track of how many frames youve been in 'coyote time'
        self.attack_1_timer = 0  # Keeps track of the attack_1 frames for hitbox creation
        self.attack_1_timer_float = 0  # Uses dt to track percise frame rate independent adjustments
        self.invincible_timer = 0
        self.invincible_timer_float = 0
        self.wall_jump_timer = 0

        # 'Constants' that can be leveled up
        self.run_acc = .2  # Gets added to the walking speed
        self.DAMAGES = {'attack_1': 25}

        # Constants
        self.WALK_ACC = WALK_ACC  # How much we instead to accelerate when we press a key
        self.FRIC = FRIC  # How much friction, this causes a variable acceleration, so we reach a max speed with a curve
        self.GRAV = .3
        self.JUMP_VEL = -7
        self.AIR_TIME = 6  # How many frames of 'coyote time' you get before falling
        self.MAX_FALL_SPEED = 6
        self.ROLL_VEL = 4
        self.INVINCIBLE_FRAMES = 20
        self.KILL_LIMIT_Y = 600  # The y value an entity gets killed at
        self.ROLL_HEIGHT = 35  # The height of the entities hitbox when they are rolling

        # Actions
        self.jumping = False
        self.walk_right = False  # A function of user keyboard inputs
        self.walk_left = False  # A function of user keyboard inputs
        self.run = False  # Running only applies if the player is already walking in a direction
        self.roll = False
        self.invincible = False  # For the rolling i-frame
        self.attacking = False  # Applies to any attack at all
        self.hurt = False  # When you get hit this animation triggers, and you cant take damage during it
        self.death = False  # Triggers the death animation, which once ended, kills the entity
        self.attack = {}  # Keeps track of which attack we are using, replace nums with attack names
        self.charge_up = False
        self.hold = False
        self.damage = 0  # Keeps track of how much damage our current attack is doing
        self.wall_jump = False
        self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}

        # Animation / Rendering
        self.action = 'idle'
        self.flip = False  # A function of self.movement
        self.animation_frames = {}  # 'idle': ['idle_1', 'idle_1', 'idle_1'....., 'idle_2', 'idle_2'...]
        self.animation_images = {}  # 'idle_1': idle_1_img, 'idle_2': idle_2_image, ....
        self.image = None  # Current image, gets updated if there are animations with this entitiy
        self.frame = 0  # Keeps track of the current animation frame
        self.frame_float = 0

    # path = assets/animations/player/idle
    # frame_lengths = [10, 10, 20, 10] for each frame
    def load_animation(self, path: str, frame_lengths: list, flip=False):
        name = str(path.split('/')[-1])  # 'idle'

        animation_frame_data = []  # ['idle_1', 'idle_1', 'idle_1'....., 'idle_2', 'idle_2'...]

        for index, frame in enumerate(frame_lengths):  # [(0, 10), (0-1, 10), (2, 10), (3, 10)]
            image_id = name + '_' + str(index)  # 'idle_0'
            img_path = path + '/' + image_id + '.png'  # 'assets/animations/player/idle/idle_0.png'
            image = pg.image.load(img_path).convert_alpha()
            if flip:
                image = pg.transform.flip(image, True, False)
            if self.rotate != 0 and self.rotate is not None:
                image = pg.transform.rotate(image, self.rotate)
            self.animation_images[image_id] = image.copy()
            for i in range(frame):
                animation_frame_data.append(image_id)

        return animation_frame_data  # ['idle_1', 'idle_1', 'idle_1'....., 'idle_2', 'idle_2'...]

    def respawn(self):
        respawn_event = pg.event.Event(pg.USEREVENT + 1)
        pg.event.post(respawn_event)

    def set_position(self, x, y):
        self.pos.x = x
        self.pos.y = y
        self.rect.topleft = self.pos

    def collision_test(self, rect, tile_rects: list):
        hit_list = []
        for tile in tile_rects:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def lose_health(self, amount: int):
        if not self.hurt and not self.invincible:
            self.hurt = True
            self.health -= amount
            if self.health < 0:
                self.health = 0
            self.check_dead()

    def check_dead(self):
        if self.health <= 0 or self.pos.y >= self.KILL_LIMIT_Y:
            self.death = True

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
            if self.walk_right:
                self.acc.x = self.WALK_ACC
                if self.run:
                    self.acc.x += self.run_acc
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

    def change_actions(self, current_action, current_frame, frame_float, new_action):
        """ Only reset animation frames if going from one animation to another """
        if current_action != new_action:
            current_action = new_action
            current_frame = 0
            frame_float = 0
        return current_action, current_frame, frame_float

    def actions(self, dt):
        """ Determine the current action and update the image accordingly """
        walk_threshold = 0.5

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

        # Damage check
        if self.hurt:
            self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'hurt')
            return

        # Walking, running, and idle animations only get played if we arent attacking, rolling, jumping, or getting hurt
        if not self.roll and not self.attacking and not self.jumping and not self.hurt and not self.charge_up and not self.hold:
            # Idle check
            if abs(self.vel.x) <= walk_threshold:
                self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'idle')

            # Walking / Running Check
            if self.vel.x > walk_threshold:
                if not self.run:
                    self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'walk')
                else:
                    self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'run')
            if self.vel.x < -walk_threshold:
                if not self.run:
                    self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'walk')
                else:
                    self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'run')

        else:
            # Roll Check - Will cancel attacks
            if self.roll:
                self.action, self.frame, self.frame_float, = self.change_actions(self.action, self.frame, self.frame_float, 'roll')
                self.invincible_timer_float -= 1 * dt
                self.invincible_timer = int(round(self.invincible_timer_float, 0))
                if self.invincible_timer_float <= 0:
                    self.invincible_timer_float = 0
                    self.invincible = False
                # Change the hitbox height for rolling
                self.rect.height = self.ROLL_HEIGHT

            # Charge Check
            if self.charge_up:
                self.action, self.frame, self.frame_float, = self.change_actions(self.action, self.frame, self.frame_float, 'charge_up')

            # Hold check
            if self.hold:
                self.action, self.frame, self.frame_float, = self.change_actions(self.action, self.frame, self.frame_float, 'hold')

            # Attack Check
            if self.attacking:
                # Basic attack
                if self.attack['1']:
                    self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'attack_1')
                # Swing attack
                if self.attack['2']:
                    self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'swing')

            # Jumping Check
            if self.jumping and not self.attacking:
                self.action, self.frame, self.frame_float, = self.change_actions(self.action, self.frame, self.frame_float, 'jump')

    def drop_loot(self, loot_pool=None):
        """ This function must be defined the the children classes """
        if not loot_pool:
            return

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
            self.frame = 0
            self.frame_float = 0
            self.attacking = False
            self.hurt = False
            self.roll = False
            self.attack['1'] = False
            self.attack['2'] = False
            self.attack_1_timer = 0
            self.attack_1_timer_float = 0
            self.jumping = False
            self.attack_rect = None
            self.invincible = False
            self.rect.height = self.height


        image_id = self.animation_frames[self.action][self.frame]
        image = self.animation_images[image_id]
        self.image = image


        # self.rect.width = self.image.get_width()
        # self.rect.height = self.image.get_height()

    def hitboxes(self, dt):
        if not self.attacking:
            self.damage = 0
            return

        if self.attack['1']:
            self.damage = self.DAMAGES['attack_1']
            self.attack_1_timer_float += 1 * dt
            self.attack_1_timer = int(round(self.attack_1_timer_float, 0))

            if self.attack_1_timer > 24:  # 10 is to be adjusted as we go
                if not self.flip:
                    self.attack_rect = pg.Rect(self.rect.right, self.rect.centery - 8, 10, 23)
                else:
                    self.attack_rect = pg.Rect(self.rect.left, self.rect.centery - 8, 10, 23)
            if self.attack_1_timer > 30:
                self.attack_rect = None

    def update(self, tile_rects, dt, player=None):
        self.check_dead()
        self.move(tile_rects, dt)  # Update players position
        self.actions(dt)  # Determine the player's action
        self.set_image(dt)  # Set the image based on the player's action
        self.hitboxes(dt)  # Update any hit boxes from player's attack

    def jump(self):
        if self.air_timer < self.AIR_TIME:
            self.jumping = True
            self.vel.y = self.JUMP_VEL

    def set_type(self, type: str):
        self.animation_type = type

    def set_static_image(self, path: str):
        self.image = pg.image.load(path).convert_alpha()

    def draw(self, display, scroll, hitbox=False, attack_box=False):
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





