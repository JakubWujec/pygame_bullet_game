from pygame.math import Vector2
from .Command import Command


class MoveBulletCommand(Command):
    def __init__(self, state, bullet) -> None:
        super().__init__()
        self.state = state
        self.bullet = bullet

    def run(self):
        # Compute new position
        direction = self.__getDirection()
        newPos = self.bullet.position + self.state.bulletSpeed * direction

        # Don't allow positions outside the world
        if (
            newPos.x < 0
            or newPos.x >= self.state.worldWidth
            or newPos.y < 0
            or newPos.y >= self.state.worldHeight
        ):
            return

        # Don't allow another bullet position
        if newPos in map(lambda bullet: bullet.position, self.state.bullets):
            return False

        # Don't allow wall positions
        if not self.state.walls[int(newPos.y)][int(newPos.x)] is None:
            return

        # # Don't allow other unit positions
        # for otherUnit in self.state.units:
        #     if newPos == otherUnit.position:
        #         return

        self.bullet.position = newPos

    def __getDirection(self):
        return Vector2(1, 0)
