import random
from typing import TYPE_CHECKING
from .GameItem import GameItem
from pygame.math import Vector2

if TYPE_CHECKING:
    from app.state import Unit


class Powerup(GameItem):
    def __init__(self, state, position, tile=Vector2(0, 15)):
        super().__init__(state, position, tile)
        self.epoch = self.state.epoch
        self.timeToLive = 200

    def apply(self, unit):
        unit.bulletLimit += 1
        self.status = "destroyed"

    def isTimeToDelete(self):
        return self.state.epoch >= (self.epoch + self.timeToLive)


class IncreaseBulletLimitPowerup(Powerup):
    def __init__(self, state, position, tile=Vector2(0, 15)):
        super().__init__(state, position, tile)

    def apply(self, unit):
        unit.bulletLimit += 1
        self.status = "destroyed"


class IncreaseBulletRangePowerup(Powerup):
    def __init__(self, state, position, tile=Vector2(0, 16)):
        super().__init__(state, position, tile)

    def apply(self, unit):
        unit.bulletRange += 1
        self.status = "destroyed"


class AllowBulletPushPowerup(Powerup):
    def __init__(self, state, position, tile=Vector2(0, 17)):
        super().__init__(state, position, tile)

    def apply(self, unit: "Unit"):
        unit.canPushBullets = True
        self.status = "destroyed"


class PowerupFactory:
    @staticmethod
    def createRandomPowerup(state, position):
        powerups = [
            IncreaseBulletLimitPowerup,
            IncreaseBulletRangePowerup,
            AllowBulletPushPowerup,
        ]
        return random.choice(powerups)(state, position)

    # @staticmethod
    # def createFromTileVector(state, position, tileVector):
    #     return None
