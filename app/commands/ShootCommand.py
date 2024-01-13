from typing import TYPE_CHECKING
from app.state import Bullet, Unit
from app.state.Orientation import orientationToVector

from .Command import Command

if TYPE_CHECKING:
    from app.state import GameState


class ShootCommand(Command):
    def __init__(self, state: "GameState", unit: "Unit") -> None:
        super().__init__()
        self.state = state
        self.unit = unit  # shooter

    def run(self):
        if not self.canUnitShoot():
            return

        bulletStartPosition = self.calculateBulletStartPosition()

        if self.state.isCollidingWithWallOrBrick(bulletStartPosition):
            return

        self.createAndFireBullet(bulletStartPosition)

    def canUnitShoot(self):
        return self.unit.status == "alive" and self.unit.canShoot()

    def calculateBulletStartPosition(self):
        bulletStartPosition = (
            self.unit.position
            + orientationToVector(self.unit.orientation).elementwise() * 0.8
        )

        return bulletStartPosition

    def createAndFireBullet(self, bulletStartPosition):
        self.unit.lastBulletEpoch = self.state.epoch
        bullet = Bullet(
            self.state,
            self.unit,
            bulletStartPosition,
        )
        self.state.bullets.append(bullet)
        self.state.notifyBulletFired()
