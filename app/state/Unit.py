import math

from pygame.math import Vector2

from .GameItem import GameItem
from .Orientation import orientationToVector


class Unit(GameItem):
    def __init__(self, state, position, tile):
        super().__init__(state, position, tile)
        self.lastBulletEpoch = -1 * self.state.bulletDelay
        self.bulletLimit = 1
        self.bulletRange = 1

    def canShoot(self):
        if self.state.epoch - self.lastBulletEpoch < self.state.bulletDelay:
            return False

        unitBullets = sum(1 for bullet in self.state.bullets if bullet.unit == self)

        return unitBullets < self.bulletLimit

    def nextStopPosition(self) -> Vector2:
        direction = orientationToVector(self.orientation)
        positionX, positionY = math.floor(self.position.x), math.floor(self.position.y)
        directionX, directionY = direction.x, direction.y

        if directionX > 0:
            positionX += 1.0

        if directionY > 0:
            positionY += 1.0

        return Vector2(positionX, positionY)
