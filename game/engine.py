import pygame as pg

vec = pg.math.Vector2


# Any object in the game i think?
class Entity(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None):
        super().__init__()
        # Specifies the name of the entity which matches up with their animation files
        self.name = None
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect = pg.Rect(x, y, width, height)
        self.flip = False
        self.animation_type = type
        self.animation_config = {}  # Stores the frame durations and looping variable
        self.animation_images = {}  # Stores the images of the animation
        self.actions = {}  # Stores the state of actions defined by the animations, False by default
        self.static_image = None  # If theres no idle animation or any animations at all, like for scenery

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

    def set_position(self, x: int, y: int):
        self.pos.x = x
        self.pos.y = y
        self.rect.x = x
        self.rect.y = y

    def move(self, acceleration: list):



    def draw(self, screen):
        screen.blit(self.static_image, self.pos)




