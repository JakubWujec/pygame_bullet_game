from pygame.math import Vector2
from app.state import Bullet, Unit

from .Command import Command


class ShootCommand(Command):
    def __init__(self, state, unit) -> None:
        super().__init__()
        self.state = state
        self.unit = unit  # shooter

    def run(self):
        if not self.unit.status == "alive":
            return

        if self.state.epoch - self.unit.lastBulletEpoch < self.state.bulletDelay:
            return

        self.unit.lastBulletEpoch = self.state.epoch
        bullet = Bullet(self.state, self.unit)
        self.state.bullets.append(bullet)
