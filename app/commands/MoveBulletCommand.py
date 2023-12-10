from pygame.math import Vector2

from app.state.GameItems import Explosion

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
        nextStopPosition = self.bullet.nextStopPosition()
        currentStopPosition = self.bullet.currentStopPosition()

        # Don't allow positions outside the world
        # if not self.state.isInside(newPos):
        #     self.bullet.status = "destroyed"
        #     return

        if self.bullet.isTimeToExplode():
            self.bullet.explode()

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