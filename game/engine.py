import pygame as pg


vec = pg.math.Vector2


# Any object in the game i think?
class Entity(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0):
        super().__init__()
        # Physics
        self.pos = vec(x, y)  # A funtion of out velocity and any collisions
        self.vel = vec(0, 0)  # A function of our current acceleration
        self.acc = vec(0, 0)  # A function of our current velocity and friction
        self.rect = pg.Rect(x, y, width, height)
        self.rect.topleft = self.pos

        # Timers
        self.air_timer = 0  # Keeps track of how many frames youve been in 'coyote time'
        self.roll_timer = None

        # Constants
        self.WALK_ACC = WALK_ACC  # How much we instead to accelerate when we press a key
        self.FRIC = FRIC  # How much friction, this causes a variable acceleration, so we reach a max speed with a curve
        self.GRAV = .4
        self.JUMP_VEL = -5
        self.RUN_ACC = .2  # Gets added to the walking speed
        self.AIR_TIME = 6  # How many frames of 'coyote time' you get before falling
        self.MAX_FALL_SPEED = 6
        self.ROLL_VEL = 3

        # Actions
        self.jumping = False
        self.walk_right = False  # A function of user keyboard inputs
        self.walk_left = False  # A function of user keyboard inputs
        self.run = False  # Running only applies if the player is already walking in a direction
        self.roll = False
        self.attacking = False  # Applies to any attack at all
        self.attack = {}  # Keeps track of which attack we are using, replace nums with attack names
        self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}


        # Animation / Rendering
        self.action = 'idle'
        self.flip = False  # A function of self.movement
        self.animation_frames = {}  # 'idle': ['idle_1', 'idle_1', 'idle_1'....., 'idle_2', 'idle_2'...]
        self.animation_images = {}  # 'idle_1': idle_1_img, 'idle_2': idle_2_image, ....
        self.image = None  # Current image, gets updated if there are animations with this entitiy
        self.frame = 0  # Keeps track of the current animation frame

    # path = assets/animations/player/idle
    # frame_lengths = [10, 10, 20, 10] for each frame
    def load_animation(self, path: str, frame_lengths: list):
        name = str(path.split('/')[-1])  # 'idle'

        animation_frame_data = []  # ['idle_1', 'idle_1', 'idle_1'....., 'idle_2', 'idle_2'...]

        for index, frame in enumerate(frame_lengths):  # [(0, 10), (1, 10), (2, 10), (3, 10)]
            image_id = name + '_' + str(index)  # 'idle_0'
            img_path = path + '/' + image_id + '.png'  # 'assets/animations/player/idle/idle_0.png'
            image = pg.image.load(img_path).convert_alpha()
            self.animation_images[image_id] = image.copy()
            for i in range(frame):
                animation_frame_data.append(image_id)

        return animation_frame_data  # ['idle_1', 'idle_1', 'idle_1'....., 'idle_2', 'idle_2'...]

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
                    self.acc.x -= self.RUN_ACC
            if self.walk_right:
                self.acc.x = self.WALK_ACC
                if self.run:
                    self.acc.x += self.RUN_ACC
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
        self.acc.y = self.GRAV
        self.vel.y += self.acc.y
        if self.vel.y > self.MAX_FALL_SPEED:
            self.vel.y = self.MAX_FALL_SPEED
        self.pos.y += self.vel.y * dt
        self.rect.topleft = self.pos

        # Check for collisions in the y axis
        hit_list = self.collision_test(self.rect, tile_rects) # TODO The hit list is growing over time, causing the program to crash
        for tile in hit_list:
            # If you are falling
            if self.vel.y > 1:
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
        if self.collision_types['bottom']:
            self.air_timer = 0
            self.jumping = False
        else:
            self.air_timer += 1

    def change_actions(self, current_action, current_frame, new_action):
        """ Only reset animation frames if going from one animation to another """
        if current_action != new_action:
            current_action = new_action
            current_frame = 0
        return current_action, current_frame

    def actions(self):
        """ Determine the current action and update the image accordingly """
        walk_threshold = 0.5

        # Walking, running, and idle animations only get played if we arent attacking, rolling, or jumping
        if not self.roll and not self.attacking and not self.jumping:
            # Idle check
            if abs(self.vel.x) <= walk_threshold:
                self.action, self.frame = self.change_actions(self.action, self.frame, 'idle')

            # Walking / Running Check
            if self.vel.x > walk_threshold:
                if not self.run:
                    self.action, self.frame = self.change_actions(self.action, self.frame, 'walk')
                else:
                    self.action, self.frame = self.change_actions(self.action, self.frame, 'run')
                self.flip = False
            if self.vel.x < -walk_threshold:
                if not self.run:
                    self.action, self.frame = self.change_actions(self.action, self.frame, 'walk')
                else:
                    self.action, self.frame = self.change_actions(self.action, self.frame, 'run')
                self.flip = True

        else:
            # Roll Check
            if self.roll:
                self.action, self.frame = self.change_actions(self.action, self.frame, 'roll')

            # Attack Check
            if self.attacking:
                if self.attack['1']:
                    self.action, self.frame = self.change_actions(self.action, self.frame, 'attack_1')

            # Jumping Check
            if self.jumping and not self.attacking:
                self.action, self.frame = self.change_actions(self.action, self.frame, 'jump')

    def set_image(self):
        """ Update the current image """
        self.frame += 1
        if self.frame >= len(self.animation_frames[self.action]):
            self.frame = 0
            # Any non-looping actions get reset here
            self.roll = False
            self.attacking = False
            self.attack['1'] = False
            self.jumping = False
        image_id = self.animation_frames[self.action][self.frame]
        image = self.animation_images[image_id]
        self.image = image

    def update(self, tile_rects, dt):
        self.move(tile_rects, dt)
        self.actions()
        self.set_image()

    def jump(self):
        if self.air_timer < self.AIR_TIME:
            self.jumping = True
            self.vel.y = self.JUMP_VEL

    def set_type(self, type: str):
        self.animation_type = type

    def set_static_image(self, path: str):
        self.image = pg.image.load(path).convert_alpha()

    def draw(self, display, scroll, hitbox=False):
        if hitbox:
            hit_rect = pg.Rect(self.pos.x - scroll[0], self.pos.y - scroll[1], self.rect.width, self.rect.height)
            pg.draw.rect(display, (0, 255, 0), hit_rect)

        # Flip the image if we need to, and then blit it
        player_image = pg.transform.flip(self.image, self.flip, False)
        display.blit(player_image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))





