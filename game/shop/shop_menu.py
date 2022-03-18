import pygame as pg
from .button import Button
from game.utils import draw_text, Color
from collections import deque
from game.settings import SCALE_FACTOR_SETTING

vec = pg.math.Vector2

class Shop_Menu:
    def __init__(self, x, y, width, height):
        self.image = pg.transform.scale(pg.image.load('assets/images/shop/upgrades_menu_text.png').convert_alpha(), (width, height))

        self.OFFSET_X = -15  # Offsets the menu from the shop's image
        self.OFFSET_Y = -110
        # self.OFFSET_X = -170  # Offsets the menu from the shop's image
        # self.OFFSET_Y = 10
        self.pos = vec(x + self.OFFSET_X, y + self.OFFSET_Y)
        self.buttons = []
        self.load_buttons()
        self.scroll = None

        COSTS = [25, 50, 100]  # Costs for level 1, 2, and 3 stat upgrades
        # Tracks the current cost of a stat upgrade
        self.stat_upgrade_costs = {
            'health': deque([COSTS[0], COSTS[1], COSTS[2], 'Max']),
            'stamina': deque([COSTS[0], COSTS[1], COSTS[2], 'Max']),
            'damage': deque([COSTS[0], COSTS[1], COSTS[2], 'Max']) }

        # Tracks amount of upgrades done for each stat
        self.stat_upgrades = {
            'health': 0,
            'stamina': 0,
            'damage': 0
        }
        # Buy switch stops the game from buying upgrades when you hold the mouse
        # You must let go of the mouse to then buy another upgrade
        self.buy_switch = True

        # Sounds
        self.sounds = {}
        self.load_sound('upgrade', 'assets/sounds/ui/shop_purchase.wav')

    def load_sound(self, name: str, path: str) -> None:
        self.sounds[name] = path

    def play_sound(self, name, volume):
        """ Plays a stored sound file with a given volume from 0 to 1. """
        sound_effect = pg.mixer.Sound(self.sounds[name])
        sound_effect.set_volume(volume)
        sound_effect.play()
        # Only one music track can be playing at a time
        # Volume ranges from 0 to 1. Use decimal values


    def load_buttons(self):
        """ Instantiates and adds buttons to self.buttons """
        BUTTON_WIDTH = 90
        BUTTON_HEIGHT = 45
        OFFSET_X = 142
        OFFSET_Y = 35
        SPACING_Y = 26
        button_1 = Button('health', self.pos.x + OFFSET_X, self.pos.y + OFFSET_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_2 = Button('stamina', self.pos.x + OFFSET_X, self.pos.y + OFFSET_Y + SPACING_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_3 = Button('damage', self.pos.x + OFFSET_X, self.pos.y + OFFSET_Y + SPACING_Y * 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.buttons.append(button_1)
        self.buttons.append(button_2)
        self.buttons.append(button_3)

    def buy_upgrade(self, button, player):
        """ If player has enough money, and their are upgrades available for the button that was pressed,
        removes player's coins and upgrades their stats """

        # How much the stats get upgraded each time they level up
        UPGRADE_AMOUNTS = {
            'health': 33,
            'stamina': 50,
            'damage': 25
        }

        # HEALTH #
        # Check which button was pressed
        if button.name == 'health':
            # Check if there are any more upgrades to get
            if self.stat_upgrade_costs['health'][0] == 'Max':
                return
            # Check if player has enough coins
            if player.coins < self.stat_upgrade_costs['health'][0]:
                return
            # Remove the players coins, remove this cost from the upgrade menu
            player.coins -= self.stat_upgrade_costs['health'].popleft()
            self.stat_upgrades['health'] += 1
            # Upgrade the player's stats
            self.play_sound('upgrade', .2)
            player.max_health += UPGRADE_AMOUNTS['health']
            player.health += UPGRADE_AMOUNTS['health']

        # STAMINA #
        elif button.name == 'stamina':
            if self.stat_upgrade_costs['stamina'][0] == 'Max':
                return
            if player.coins < self.stat_upgrade_costs['stamina'][0]:
                return
            player.coins -= self.stat_upgrade_costs['stamina'].popleft()
            self.stat_upgrades['stamina'] += 1
            # Upgrade the player's stats
            self.play_sound('upgrade', .2)
            player.max_stamina += UPGRADE_AMOUNTS['stamina']
            player.stamina_float = player.max_stamina
            player.stamina = player.max_stamina

        # DAMAGE #
        elif button.name == 'damage':
            if self.stat_upgrade_costs['damage'][0] == 'Max':
                return
            if player.coins < self.stat_upgrade_costs['damage'][0]:
                return
            player.coins -= self.stat_upgrade_costs['damage'].popleft()
            self.stat_upgrades['damage'] += 1
            # Upgrade the player's stats
            self.play_sound('upgrade', .2)
            player.damages['attack_1'] += UPGRADE_AMOUNTS['damage']
            player.MAX_CHARGE_DAMAGE = player.damages['attack_1'] * 2

    def update(self, tile_rects, dt, player):
        """ Update the buttons, passing in a mouse rect and mouse actions"""
        if not self.scroll:
            return
        mouse_pos = pg.mouse.get_pos()  # (x, y)
        mouse_action = pg.mouse.get_pressed()  # action[2] = right click, action[0] = left click
        # If you are not holding down left click, resets the buy switch
        if not mouse_action[0]:
            self.buy_switch = True
        mouse_rect = pg.Rect(mouse_pos[0] / SCALE_FACTOR_SETTING + self.scroll[0] , mouse_pos[1] / SCALE_FACTOR_SETTING + self.scroll[1] , 1, 1)


        for button in self.buttons:
            button.update(mouse_rect, mouse_action)
            if button.pressed:
                if self.buy_switch:
                    self.buy_upgrade(button, player)
                    self.buy_switch = False

    def draw(self, display, scroll, screen, hitbox=True, attack_box=False):
        """ Draw the menu background, then draw each button """

        self.scroll = scroll
        # Draw the menu
        screen.blit(self.image, ((self.pos.x - scroll[0])*SCALE_FACTOR_SETTING, (self.pos.y - scroll[1])*SCALE_FACTOR_SETTING))

        # Draw the buttons
        for button in self.buttons:
            button.draw(display, scroll, screen)

        # Draw the costs
        OFFSET_X = 5
        OFFSET_Y = 0
        SIZE = 36

        draw_text(screen, f'{self.stat_upgrade_costs["health"][0]}', SIZE, Color.HEALTH.value,((self.buttons[0].pos.x - scroll[0] + OFFSET_X) * SCALE_FACTOR_SETTING,(self.buttons[0].pos.y - scroll[1] + OFFSET_Y) * SCALE_FACTOR_SETTING))
        draw_text(screen, f'{self.stat_upgrade_costs["stamina"][0]}', SIZE, Color.HEALTH.value,((self.buttons[1].pos.x - scroll[0] + OFFSET_X) * SCALE_FACTOR_SETTING,(self.buttons[1].pos.y - scroll[1] + OFFSET_Y) * SCALE_FACTOR_SETTING))
        draw_text(screen, f'{self.stat_upgrade_costs["damage"][0]}', SIZE, Color.HEALTH.value, ((self.buttons[2].pos.x - scroll[0] + OFFSET_X) * SCALE_FACTOR_SETTING, (self.buttons[2].pos.y - scroll[1] + OFFSET_Y) * SCALE_FACTOR_SETTING))

        # Draw the upgrade levels symbols
        WIDTH = 36
        HEIGHT = 27
        ABILITY_OFFSET_X = -70
        ABILITY_OFFSET_y = 2
        SPACING_X = 18
        SPACING_Y = 25

        # Draw the health levels
        if self.stat_upgrades['health'] > 0:
            for i in range(0, self.stat_upgrades['health']):
                health_rect = pg.Rect((self.buttons[0].pos.x + ABILITY_OFFSET_X + SPACING_X * i - scroll[0])*SCALE_FACTOR_SETTING, (self.buttons[0].pos.y + ABILITY_OFFSET_y - scroll[1])*SCALE_FACTOR_SETTING, WIDTH, HEIGHT)
                pg.draw.rect(screen, Color.HEALTH.value, health_rect)

        # Draw the stamina levels
        if self.stat_upgrades['stamina'] > 0:
            for i in range(0, self.stat_upgrades['stamina']):
                stamina_rect = pg.Rect((self.buttons[0].pos.x + ABILITY_OFFSET_X + SPACING_X * i - scroll[0])*SCALE_FACTOR_SETTING, (self.buttons[0].pos.y + ABILITY_OFFSET_y + SPACING_Y - scroll[1])*SCALE_FACTOR_SETTING, WIDTH, HEIGHT)
                pg.draw.rect(screen, Color.STAMINA.value, stamina_rect)

        # Draw the damagee levels
        if self.stat_upgrades['damage'] > 0:
            for i in range(0, self.stat_upgrades['damage']):
                damage_rect = pg.Rect((self.buttons[0].pos.x + ABILITY_OFFSET_X + SPACING_X * i - scroll[0])*SCALE_FACTOR_SETTING, (self.buttons[0].pos.y + ABILITY_OFFSET_y + SPACING_Y * 2- scroll[1])*SCALE_FACTOR_SETTING, WIDTH, HEIGHT)
                pg.draw.rect(screen, Color.DAMAGE.value, damage_rect)









