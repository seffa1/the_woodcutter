import pygame as pg
from .utils import draw_text



class Level_Trigger:
    def __init__(self, x, y, width, height, level_to_go_to, image_path, type):
        self.x = x
        self.y = y
        self.level_to_go_to = level_to_go_to
        self.image = pg.transform.scale(pg.image.load(image_path).convert_alpha(), (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 0, 255)
        self.color = (255, 0, 0)
        self.collided = False
        self.collide_text = False


        self.animation_frames = {}
        self.animation_images = {}
        self.frame = 0
        self.frame_float = 0
        if type == 1:
            self.animation_frames['flag_home'] = self.load_animation('assets/animations/flag_home', [25, 25, 25, 25], True)
            self.action = 'flag_home'
        else:
            self.animation_frames['flag_swamp'] = self.load_animation('assets/animations/flag_swamp', [25, 25, 25, 25], True)
            self.action = 'flag_swamp'



    def load_animation(self, path: str, frame_lengths: list, flip=False):
        name = str(path.split('/')[-1])  # 'idle'

        animation_frame_data = []  # ['idle_1', 'idle_1', 'idle_1'....., 'idle_2', 'idle_2'...]

        for index, frame in enumerate(frame_lengths):  # [(0, 10), (0-1, 10), (2, 10), (3, 10)]
            image_id = name + '_' + str(index)  # 'idle_0'
            img_path = path + '/' + image_id + '.png'  # 'assets/animations/player/idle/idle_0.png'
            image = pg.image.load(img_path).convert_alpha()
            self.animation_images[image_id] = image.copy()
            for i in range(frame):
                animation_frame_data.append(image_id)
        return animation_frame_data
    def set_image(self, dt):
        """ Update the current image """
        self.frame_float += 1 * dt
        self.frame = int(round(self.frame_float, 0))

        if self.frame >= len(self.animation_frames[self.action]):
            self.frame = 0
            self.frame_float = 0

        image_id = self.animation_frames[self.action][self.frame]
        image = self.animation_images[image_id]
        self.image = image

    def update(self, player, dt):
        """ Checks if the player has attacked the trigger and reports it to the level manager """
        # Update the image
        self.set_image(dt)

        # Check for collision
        if self.rect.colliderect(player.rect):
            self.color = self.GREEN
            self.collided = True
        else:
            self.color = self.RED
            self.collided = False


    def draw(self, display, scroll, hitbox=False):
        if hitbox:
            scrolled_rect = pg.Rect(self.x - scroll[0], self.y - scroll[1], self.rect.width, self.rect.height)
            pg.draw.rect(display, self.color, scrolled_rect)
        if self.collide_text:
            draw_text(display, f'Travel to {self.level_to_go_to}', 15, (0, 0, 0), (self.x - scroll[0] + self.rect.width + 5, self.y - scroll[1] - 5))

        display.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))

