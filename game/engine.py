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
        self.GRAV = .5
        self.rect = pg.Rect(x, y, width, height)
        self.flip = False  # A function of self.movement
        self.animation_type = type
        self.animation_config = {}  # Stores the frame durations and looping variable
        self.animation_images = {}  # Stores the images of the animation
        self.actions = {}  # Stores the state of actions defined by the animations, False by default
        self.static_image = None  # If theres no idle animation or any animations at all, like for scenery
        self.acc_right = False  # A function of user keyboard inputs
        self.acc_left = False# A function of user keyboard inputs
        self.movement = {'moving_right': False, 'moving_left': False}  # Used to update flip for drawing directionally
        self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}

    def set_type(self, type: str):
        self.animation_type = type

    def set_static_image(self, path: str):
        self.static_image = pg.image.load(path).convert_alpha()

    def set_MAX_X_VEL(self, vel: int):
        self.MAX_X_VEL = vel

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

    def set_position(self, x: int, y: int):
        self.pos.x = x
        self.pos.y = y
        self.rect.x = x
        self.rect.y = y

    def move_position(self, x: int, y: int):
        self.pos.x += x
        self.pos.y += y
        self.rect.x += x
        self.rect.y += y

    def collision_test(self, rect, tiles: list):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, tiles):
        # Reset collisions
        self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        # Reset acceleration
        self.acc.x = 0
        self.acc.y = self.GRAV
        # Apply acceleration
        if self.acc_right:
            self.acc.x = self.ACC
            print(self.ACC)
            # print(self.acc.x)
        if self.acc_left:
            self.acc.x = -self.ACC
        # If we are holding both right and left controls, you dont move
        if self.acc_left and self.acc_right:
            self.acc.x = 0

        # The faster we are moving, the less we accelerate
        # The faster we are moving, the more we DEccelerate
        # Down side of this is we cant control the accerate and deccelerate curves independtently
        # We good make two FRIC values, and use one for speeding up, and one for slowing down
        self.acc.x += self.vel.x * self.FRIC

        # Adjust velocity
        self.vel.x += self.acc.x

        # Adjust position
        delta_x = self.vel.x + 0.5 * self.acc.x
        self.move_position(delta_x, 0)

        # Check for collisions in the x axis
        # hit_list = self.collision_test(self.rect, tiles)

        # Y axis
        self.vel.y += self.acc.y
        self.move_position(0, self.vel.y)

        # Check for collisions in the y axis
        hit_list = self.collision_test(self.rect, tiles)
        for tile in hit_list:
            # If you are falling
            if self.vel.y > 0:
                self.collision_types['bottom'] = True
                self.rect.bottom = tile.top  # Change the rect's position because of convientient methods
                self.set_position(self.rect.x, self.rect.y)  # Move everything else based on that
                self.vel.y = 1

    def update(self, tiles):
        self.move(tiles)

    def draw(self, display, scroll, hitbox=True):
        if hitbox:
            pg.draw.rect(display, (0, 255, 0), self.rect)
        display.blit(self.static_image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))





