from pygame.math import Vector2
from .Command import Command


class MoveBulletCommand(Command):
    def __init__(self, state, bullet) -> None:
        super().__init__()
        self.state = state
        self.bullet = bullet

    def run(self):
        # Compute new position
        direction = self.bullet.direction
        newPos = self.bullet.position + (self.state.bulletSpeed * direction)
        newRoundedPos = Vector2(
            int(round(self.bullet.position.x)), int(round(self.bullet.position.y))
        )

        # Don't allow positions outside the world
        if not self.state.isInside(newPos):
            self.bullet.status = "destroyed"
            return

        # Don't allow another bullet position
        if newPos in map(lambda bullet: bullet.position, self.state.bullets):
            return

        # Don't allow wall positions
        if self.state.isInside(newRoundedPos):
            if self.state.isWall(newRoundedPos):
                self.bullet.position = (
                    Vector2(round(newPos.x), round(newPos.y)).elementwise() - direction
                )
                self.bullet.direction = Vector2(0, 0)
                return

        # # Don't allow other unit positions
        for otherUnit in self.state.units:
            if newPos == otherUnit.position:
                self.bullet.direction = Vector2(0, 0)
                return

        self.bullet.position = newPos
