import math

from pygame.math import Vector2

from .Explosion import Explosion
from .GameItem import GameItem
from app.state.Orientation import orientationToVector, vectorToOrientation


class Bullet(GameItem):
    def __init__(self, state, unit, position):
        super().__init__(state, position, Vector2(3, 4))
        self.unit = unit
        self.startPosition = position
        self.epoch = state.epoch
        self.timeToLive = 300
        self.bulletRange = unit.bulletRange
        self.isMoving = False

    def setDirection(self, direction: Vector2):
        if direction == Vector2(0, 0):
            self.isMoving = False
            return
        self.orientation = vectorToOrientation(direction)
        self.isMoving = True

    def getDirection(self):
        if not self.isMoving:
            return Vector2(0, 0)
        return orientationToVector(self.orientation)

    def isTimeToExplode(self):
        return self.state.epoch >= (self.epoch + self.timeToLive)

    def currentStopPosition(self) -> Vector2:
        return self.nextStopPosition().elementwise() - self.getDirection()

    def nextStopPosition(self) -> Vector2:
        moveDirection = self.getDirection()
        positionX, positionY = math.floor(self.position.x), math.floor(self.position.y)

        if moveDirection.x > 0:
            positionX += 1.0

        if moveDirection.x < 0 and positionX == self.position.x:
            positionX -= 1.0

        if moveDirection.y > 0:
            positionY += 1.0

        if moveDirection.y < 0 and positionY == self.position.y:
            positionY -= 1.0

        return Vector2(positionX, positionY)
