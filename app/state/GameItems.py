from pygame.math import Vector2
from app.state.Orientation import Orientation, orientationToVector
import math


class GameItem:
    def __init__(self, state, position, tile):
        self.state = state
        self.status = "alive"
        self.position = position
        self.tile = tile
        self.orientation = 0


class Unit(GameItem):
    def __init__(self, state, position, tile):
        super().__init__(state, position, tile)
        self.lastBulletEpoch = -100


class Bullet(GameItem):
    def __init__(self, state, unit):
        super().__init__(state, unit.position, Vector2(3, 4))
        self.unit = unit
        self.startPosition = unit.position
        self.direction = orientationToVector(self.unit.orientation)
        self.epoch = state.epoch
        self.ttl = 300

    def isMoving(self):
        return self.direction.x != 0 or self.direction.y != 0

    def isTimeToExplode(self):
        return self.state.epoch >= (self.epoch + self.ttl)

    def explode(self):
        self.status = "destroyed"
        self.state.explosions.append(Explosion(self.state, self.position))
        for vector in [Vector2(-1, 0), Vector2(1, 0), Vector2(0, 1), Vector2(0, -1)]:
            newPosition = self.position.elementwise() + vector
            if self.state.isInside(newPosition) and not self.state.isWall(newPosition):
                self.state.explosions.append(Explosion(self.state, newPosition))

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


class Explosion(GameItem):
    def __init__(self, state, position):
        super().__init__(state, position, Vector2(15, 30))
        self.epoch = self.state.epoch
        self.center = position
        self.range = 2
        self.frameIndex = 0
        self.ttl = 300

    def isTimeToDelete(self):
        return self.state.epoch >= (self.epoch + self.ttl)
