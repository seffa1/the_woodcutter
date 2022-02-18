import pygame as pg
from game import Level_Manager
from .objects.coin import Coin
import random


class Loot_Generator:
    def __init__(self, level_manager: Level_Manager):
        self.level_manager = level_manager

    def spawn_coins(self, amount, position: list):
        for i in range(0, amount):
            coin = Coin(position[0], position[1], 9, 9, coin, 0, 0, 0)
            x_vel = random.randint(-4, 4)
            y_vel = random.randint(0, -5)
            coin.vel.y = y_vel
            coin.vel.x = x_vel
            self.level_manager.get_level().entity_manager.add_entity(coin, coin)


