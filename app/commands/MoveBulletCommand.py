from typing import TYPE_CHECKING

from pygame.math import Vector2

from app.state import Explosion

from .Command import Command

if TYPE_CHECKING:
    from app.state import Bullet, Enemy, GameStateObserver, Powerup, GameState


class MoveBulletCommand(Command):
    def __init__(self, state: "GameState", bullet: "Bullet") -> None:
        super().__init__()
        self.state = state
        self.bullet = bullet

    def run(self):
        direction = self.bullet.direction
        newPosition = self.bullet.position + (self.state.bulletSpeed * direction)
        nextStopPosition = self.bullet.nextStopPosition()

        # Check for collisions
        if (
            self.isEnemyCollision(newPosition)
            or self.isUnitCollision(newPosition)
            or self.isStackedBulletCollision(nextStopPosition)
            or self.isWallOrBrickCollision(nextStopPosition)
        ):
            self.stopMoving()
        else:
            self.bullet.position = newPosition

    def isWallOrBrickCollision(self, position):
        return self.state.isInside(position) and (
            self.state.isWallAt(position) or self.state.isBrickAt(position)
        )

    def isStackedBulletCollision(self, position):
        return any(
            position == bullet.position and not bullet.isMoving()
            for bullet in self.state.bullets
        )

    def isUnitCollision(self, position):
        return any(position == unit.position for unit in self.state.units)

    def isEnemyCollision(self, position):
        return any(position == enemy.position for enemy in self.state.enemies)

    def stopMoving(self):
        self.bullet.position = self.bullet.currentStopPosition()
        self.bullet.direction = Vector2(0, 0)
