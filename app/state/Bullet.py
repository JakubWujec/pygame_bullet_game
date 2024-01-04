import math

from pygame.math import Vector2

from .Explosion import Explosion
from .GameItem import GameItem
from .Orientation import orientationToVector, vectorToOrientation


class Bullet(GameItem):
    def __init__(self, state, unit, position):
        super().__init__(state, position, Vector2(3, 4))
        self.unit = unit
        self.startPosition = position
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
        explosionCenter = Explosion(self.state, self.position)
        explosionCenter.setExplosionTile("center")
        self.state.explosions.append(explosionCenter)

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
                nextPosition = (
                    self.position.elementwise()
                    + vector.elementwise() * Vector2(i + 1, i + 1)
                )

                if not self.state.isInside(newPosition) or self.state.isWallAt(
                    newPosition
                ):
                    break

                explosion = Explosion(self.state, newPosition)
                explosion.setExplosionTile(
                    "horizontal" if vector.x == 0 else "vertical"
                )

                self.state.explosions.append(explosion)

                if (
                    not self.state.isInside(nextPosition)
                    or self.state.isWallAt(nextPosition)
                    or self.state.isBrickAt(newPosition)
                    or i == self.bulletRange
                ):
                    explosion.setExplosionTile(
                        "left"
                        if vector == Vector2(-1, 0)
                        else "right"
                        if vector == Vector2(1, 0)
                        else "bottom"
                        if vector == Vector2(0, 1)
                        else "top"
                    )

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
