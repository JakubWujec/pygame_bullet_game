from pygame.math import Vector2
from .Command import Command


class MoveBulletCommand(Command):
    def __init__(self, state, bullet) -> None:
        super().__init__()
        self.state = state
        self.bullet = bullet

    def run(self):
        # Should only stop at 0.0, 1.0 etc
        # Compute new position
        direction = self.bullet.direction
        newPos = self.bullet.position + (self.state.bulletSpeed * direction)
        nextStopPosition = self.__nextStopPosition()
        currentStopPosition = nextStopPosition.elementwise() - direction

        # Don't allow positions outside the world
        # if not self.state.isInside(newPos):
        #     self.bullet.status = "destroyed"
        #     return

        for bullet in self.state.bullets:
            if bullet.isTimeToExplode():
                self.bullet.status = "destroyed"

        # Don't allow another bullet position
        if newPos in map(lambda bullet: bullet.position, self.state.bullets):
            return

        # Don't allow wall positions
        if self.state.isInside(nextStopPosition):
            if self.state.isWall(nextStopPosition):
                self.bullet.direction = Vector2(0, 0)
                self.bullet.position = currentStopPosition
                return

        # Dont't alow to stack bombs
        for otherBullet in self.state.bullets:
            if nextStopPosition == otherBullet.position and not otherBullet.isMoving():
                self.bullet.direction = Vector2(0, 0)
                self.bullet.position = currentStopPosition
                return

        # # Don't allow other unit positions
        for otherUnit in self.state.units:
            if newPos == otherUnit.position:
                self.bullet.direction = Vector2(0, 0)
                self.bullet.position = currentStopPosition
                return

        self.bullet.position = newPos

    def __nextStopPosition(self):
        direction = self.bullet.direction.copy()
        nextStop = self.bullet.position.copy()

        if direction.x != 0:
            decimal = round(self.bullet.position.x - int(self.bullet.position.x), 1)

            if decimal.is_integer():
                nextStop.x = self.bullet.position.x + direction.x
            else:
                nextStop.x = self.bullet.position.x + direction.x * decimal

        if direction.y != 0:
            decimal = round(self.bullet.position.y - int(self.bullet.position.y), 1)
            if decimal.is_integer():
                nextStop.y = self.bullet.position.y + direction.y
            else:
                nextStop.y = self.bullet.position.y + direction.y * decimal

        return Vector2(round(nextStop.x, 1), round(nextStop.y, 1))
