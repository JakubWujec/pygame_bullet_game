from pygame.math import Vector2
from app.state import Bullet, Unit
from app.state.Orientation import orientationToVector

from .Command import Command


class ShootCommand(Command):
    def __init__(self, state, unit) -> None:
        super().__init__()
        self.state = state
        self.unit = unit  # shooter

    def run(self):
        if not self.unit.status == "alive":
            return

        if not self.unit.canShoot():
            return

        bulletStartPosition = (
            self.unit.position
            + orientationToVector(self.unit.orientation).elementwise() * 0.8
        )

        if self.state.isCollidingWithWallOrBrick(bulletStartPosition):
            return False

        self.unit.lastBulletEpoch = self.state.epoch
        bullet = Bullet(
            self.state,
            self.unit,
            bulletStartPosition,
        )
        self.state.bullets.append(bullet)
