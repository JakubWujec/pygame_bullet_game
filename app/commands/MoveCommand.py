from pygame.math import Vector2
from pygame import Rect
from app.state.Orientation import Orientation, orientationToVector, vectorToOrientation
from .Command import Command


class MoveCommand(Command):
    def __init__(self, state, unit, moveVector: Vector2) -> None:
        super().__init__()
        self.state = state
        self.unit = unit
        self.moveVector = moveVector
        self.moveLength = 0.2

    def run(self):
        if vectorToOrientation(self.moveVector) != self.unit.orientation:
            self.unit.orientation = vectorToOrientation(self.moveVector)
            return

        # Update unit orientation
        if self.moveVector.x < 0:
            self.unit.orientation = Orientation.LEFT
        elif self.moveVector.x > 0:
            self.unit.orientation = Orientation.RIGHT
        if self.moveVector.y < 0:
            self.unit.orientation = Orientation.DOWN
        elif self.moveVector.y > 0:
            self.unit.orientation = Orientation.TOP

        # Compute new position
        newPos = round(
            self.unit.position
            + self.moveVector.elementwise() * Vector2(self.moveLength, self.moveLength),
            2,
        )
        nextStopPosition = self.unit.nextStopPosition()

        # Don't allow positions outside the world
        if (
            newPos.x < 0
            or newPos.x >= self.state.worldWidth
            or newPos.y < 0
            or newPos.y >= self.state.worldHeight
        ):
            return

        # Dont allow (2.3,3.6) both float position
        if not newPos.x.is_integer() and not newPos.y.is_integer():
            return

        # Don't allow wall positions
        if self.state.isWallAt(nextStopPosition):
            return

        if self.state.isBrickAt(nextStopPosition):
            return

        if self.state.isPowerupAt(nextStopPosition):
            powerup = next(
                (
                    powerup
                    for powerup in self.state.powerups
                    if powerup.position == newPos
                ),
                None,
            )
            if powerup:
                powerup.apply(self.unit)

        for enemy in self.state.enemies:
            if nextStopPosition == enemy.position:
                self.unit.status = "destroyed"

        # Push bullet
        for bullet in self.state.bullets:
            if nextStopPosition == bullet.currentStopPosition():
                bullet.direction = orientationToVector(self.unit.orientation)
                return

        self.unit.position = newPos
