import math

from pygame.math import Vector2

from .Explosion import Explosion
from .GameItem import GameItem
from .Orientation import orientationToVector, vectorToOrientation


class Bullet(GameItem):
    def __init__(self, state, unit):
        super().__init__(state, unit.position, Vector2(3, 4))
        self.unit = unit
        self.startPosition = unit.position
        self.direction = Vector2(0, 0)
        self.epoch = state.epoch
        self.timeToLive = 300
        self.bulletRange = unit.bulletRange

    def isMoving(self):
        return self.direction.x != 0 or self.direction.y != 0

    def isTimeToExplode(self):
        return self.state.epoch >= (self.epoch + self.timeToLive)

    def explode(self):
        self.status = "destroyed"
        self.state.explosions.append(Explosion(self.state, self.position))

        for vector in [
            Vector2(-1, 0),
            Vector2(1, 0),
            Vector2(0, 1),
            Vector2(0, -1),
        ]:
            for i in range(1, self.bulletRange + 1):
                newPosition = (
                    self.position.elementwise() + vector.elementwise() * Vector2(i, i)
                )

                if not self.state.isInside(newPosition) or self.state.isWallAt(
                    newPosition
                ):
                    break

                self.state.explosions.append(Explosion(self.state, newPosition))

                if self.state.isBrickAt(newPosition):
                    break

    def currentStopPosition(self) -> Vector2:
        return self.nextStopPosition().elementwise() - self.direction

    def nextStopPosition(self) -> Vector2:
        positionX, positionY = math.floor(self.position.x), math.floor(self.position.y)
        directionX, directionY = self.direction.x, self.direction.y

        if directionX > 0:
            positionX += 1.0

        if directionY > 0:
            positionY += 1.0

        return Vector2(positionX, positionY)
