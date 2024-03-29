import math
from typing import TYPE_CHECKING

from pygame.math import Vector2

from app.state import GameItem


if TYPE_CHECKING:
    from app.state import GameState, Unit


class Bullet(GameItem):
    def __init__(self, state: "GameState", unit: "Unit", position: Vector2):
        super().__init__(state, position, Vector2(0, 0))
        self.unit = unit
        self.startPosition = position
        self.direction = Vector2(0, 0)
        self.epoch = state.epoch
        self.timeToLive: int = 200
        self.bulletRange = unit.bulletRange

    def isMoving(self):
        return self.direction.x != 0 or self.direction.y != 0

    def isTimeToExplode(self):
        return self.state.epoch >= (self.epoch + self.timeToLive)

    def currentStopPosition(self) -> Vector2:
        return self.nextStopPosition().elementwise() - self.direction

    def nextStopPosition(self) -> Vector2:
        moveVector = self.direction
        positionX, positionY = math.floor(self.position.x), math.floor(self.position.y)

        if moveVector.x > 0:
            positionX += 1.0

        if moveVector.x < 0 and positionX == self.position.x:
            positionX -= 1.0

        if moveVector.y > 0:
            positionY += 1.0

        if moveVector.y < 0 and positionY == self.position.y:
            positionY -= 1.0

        return Vector2(positionX, positionY)
