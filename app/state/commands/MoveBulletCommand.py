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
        newRoundedPos = (
            Vector2(
                int(self.bullet.position.x), int(self.bullet.position.y)
            ).elementwise()
            + direction
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
            if not self.state.walls[int(newRoundedPos.x)][int(newRoundedPos.y)] is None:
                self.bullet.direction = Vector2(0, 0)
                return

        # # Don't allow other unit positions
        for otherUnit in self.state.units:
            if newPos == otherUnit.position:
                return

        self.bullet.position = newPos
