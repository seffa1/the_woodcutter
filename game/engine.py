import pygame as pg


vec = pg.math.Vector2


# Any object in the game i think?
class Entity(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, ACC=0, FRIC=0):
        super().__init__()
        # Specifies the name of the entity which matches up with their animation files
        self.name = None
        self.pos = vec(x, y)  # A funtion of out velocity and any collisions
        self.vel = vec(0, 0)  # A function of our current acceleration
        self.acc = vec(0, 0)  # A function of our current velocity and friction
        self.ACC = ACC  # How much we instead to accelerate when we press a key
        self.FRIC = FRIC  # How much friction, this causes a variable acceleration, so we reach a max speed with a curve
        self.GRAV = .4
        self.JUMP_VEL = -5
        self.jumping = False
        self.rect = pg.Rect(x, y, width, height)
        self.flip = False  # A function of self.movement
        self.animation_type = type
        self.animation_config = {}  # Stores the frame durations and looping variable
        self.animation_images = {}  # Stores the images of the animation
        self.actions = {}  # Stores the state of actions defined by the animations, False by default
        self.static_image = None  # If theres no idle animation or any animations at all, like for scenery
        self.acc_right = False  # A function of user keyboard inputs
        self.acc_left = False  # A function of user keyboard inputs
        self.movement = {'moving_right': False, 'moving_left': False}  # Used to update flip for drawing directionally
        self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        self.rect.topleft = self.pos
        self.AIR_TIME = 6  # How many frames of 'coyote time' you get before falling
        self.air_timer = 0 # Keeps track of how many frames youve been in 'coyote time'

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

    def move(self, tile_rects):
        # Reset collisions
        self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        # Reset acceleration
        self.acc.x = 0

        # Apply acceleration
        if self.acc_left:
            self.acc.x = -self.ACC
        if self.acc_right:
            self.acc.x = self.ACC
        # If we are holding both right and left controls, you dont move
        if self.acc_left and self.acc_right:
            self.acc.x = 0

        # The faster we are moving, the less we accelerate
        # The faster we are moving, the more we DEccelerate
        # Down side of this is we cant control the accerate and deccelerate curves independtently
        # We good make two FRIC values, and use one for speeding up, and one for slowing down
        # if abs(self.vel.x) < 0.0001: self.vel.x = 0
        self.acc.x += self.vel.x * self.FRIC

        # Adjust velocity
        self.vel.x += self.acc.x
        if abs(self.vel.x) < 0.01: self.vel.x = 0
        # If velocity ends up negative, flip the image
        if self.vel.x < 0:
            self.flip = True
        if self.vel.x > 0:
            self.flip = False

        # Adjust position
        self.pos.x += self.vel.x
        self.rect.topleft = self.pos


        # Check for collisions in the x axis
        # hit_list = self.collision_test(self.rect, tiles)

        # Y axis
        self.acc.y = self.GRAV
        self.vel.y += self.acc.y
        self.pos.y += self.vel.y
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

    def jump(self):
        if self.air_timer < self.AIR_TIME:
            self.vel.y = self.JUMP_VEL

    def jump_cancel(self):
        pass
        # if self.vel.y < -3:
        #     self.vel.y = -3

    def set_type(self, type: str):
        self.animation_type = type

    def set_static_image(self, path: str):
        self.static_image = pg.image.load(path).convert_alpha()

    # path = assets/animations/player/idle
    # frame_lengths = [10, 10, 20, 10] for each frame
    def load_animation(self, path: str, frame_lengths: list, looping=True):
        type = str(path.split('/')[-1])  # idle

        config = frame_lengths.append(looping)
        self.animation_config[type] = config

        image_list = []
        for index, frame in enumerate(frame_lengths):
            img_path = str(type) + '_' + str(index) + '.png'
            image = pg.image.load(img_path).convert_alpha()
            image_list.append(image)

        self.animation_images[type] = image_list
        self.actions[type] = False

    def update(self, tile_rects):
        self.move(tile_rects)
        if self.collision_types['bottom']:
            self.air_timer = 0
        else:
            self.air_timer += 1

    def draw(self, display, scroll, hitbox=False):
        if hitbox:
            hit_rect = pg.Rect(self.pos.x - scroll[0], self.pos.y - scroll[1], self.rect.width, self.rect.height)
            pg.draw.rect(display, (0, 255, 0), hit_rect)

        # Flip the image if we need to, and then blit it
        player_image = pg.transform.flip(self.static_image, self.flip, False)
        display.blit(player_image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))





