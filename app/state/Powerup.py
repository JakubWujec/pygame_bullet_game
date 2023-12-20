import random
from .GameItem import GameItem
from pygame.math import Vector2


class Powerup(GameItem):
    def __init__(self, state, position):
        super().__init__(state, position, Vector2(0, 15))
        self.timeToLive = 200

    def apply(self, unit):
        unit.bulletLimit += 1
        self.status = "destroyed"


class IncreaseBulletLimitPowerup(Powerup):
    def apply(self, unit):
        unit.bulletLimit += 1
        self.status = "destroyed"


class IncreaseBulletRangePowerup(Powerup):
    def apply(self, unit):
        unit.bulletRange += 1
        self.status = "destroyed"


class PowerupFactory:
    @staticmethod
    def createRandomPowerup(state, position):
        powerups = [IncreaseBulletLimitPowerup, IncreaseBulletRangePowerup]
        return random.choice(powerups)(state, position)

    # @staticmethod
    # def createFromTileVector(state, position, tileVector):
    #     return None
