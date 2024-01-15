from typing import TYPE_CHECKING
from pygame.math import Vector2
from app.state.Orientation import Orientation, orientationToVector, vectorToOrientation

from .Command import Command

if TYPE_CHECKING:
    from app.state import Unit
    from app.state import GameState
    from app.state import Bullet


class MoveCommand(Command):
    def __init__(self, state: "GameState", unit: "Unit", moveVector: Vector2) -> None:
        super().__init__()
        self.state = state
        self.unit = unit
        self.moveVector = moveVector
        self.moveLength = 0.2
        self.alignThreshold = 0.41

    def needAligning(self):
        desiredPosition = (
            self.unit.closestIntegerPosition().elementwise() + self.moveVector
        )
        neededShiftVector = (
            self.unit.closestIntegerPosition().elementwise() - self.unit.position
        )
        if neededShiftVector.x == 0 and neededShiftVector.y == 0:
            return False

        # if not perpendicular then return False
        if neededShiftVector.normalize() * self.moveVector.normalize() != 0:
            return False

        if not self.state.isWalkableAt(
            self.unit.closestIntegerPosition()
        ) or not self.state.isWalkableAt(desiredPosition):
            return False
        if (
            0 < abs(neededShiftVector.x) <= self.alignThreshold
            and neededShiftVector.y == 0
        ) or (
            0 < abs(neededShiftVector.y) <= self.alignThreshold
            and neededShiftVector.x == 0
        ):
            return True

        return False

    def run(self):
        if vectorToOrientation(self.moveVector) != self.unit.orientation:
            self.unit.orientation = vectorToOrientation(self.moveVector)
            return

        # Compute new position
        newPos = round(
            self.unit.position
            + self.moveVector.elementwise() * Vector2(self.moveLength, self.moveLength),
            2,
        )

        if self.needAligning():
            newPos = self.unit.closestIntegerPosition()

        # Don't allow positions outside the world
        if not self.state.isInside(newPos):
            return

        if self.state.isCollidingWithWallOrBrick(newPos):
            return

        enemies = self.state.findCollidingEnemies(newPos)
        if len(enemies) > 0:
            self.unit.status = "destroyed"

        collidingBullets = self.state.findCollidingBullets(newPos)
        for bullet in collidingBullets:
            if self.isUnitStandingAtBullet(bullet):
                continue

            if self.unit.nextStopPosition() == bullet.currentStopPosition():
                if self.unit.canPushBullets:
                    self.pushBullet(bullet)
                return

        powerups = self.state.findCollidingPowerups(newPos)
        for powerup in powerups:
            powerup.apply(self.unit)

        self.unit.position = newPos

    def pushBullet(self, bullet: "Bullet"):
        bullet.direction = orientationToVector(self.unit.orientation)

    def isUnitStandingAtBullet(self, bullet: "Bullet"):
        return self.unit.collideWith(bullet.position)
