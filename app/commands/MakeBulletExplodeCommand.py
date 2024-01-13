from typing import TYPE_CHECKING
from pygame.math import Vector2

from app.state import Explosion

from .Command import Command

if TYPE_CHECKING:
    from app.state.Bullet import Bullet
    from app.state.GameState import GameState


class MakeBulletExplodeCommand(Command):
    def __init__(self, state: "GameState", bullet: "Bullet") -> None:
        super().__init__()
        self.state = state
        self.bullet = bullet

    def run(self):
        self.bullet.status = "destroyed"
        self.createExplosions()

    def createExplosions(self):
        self.createCentralExplosion()
        self.createDirectionalExplosions()
        self.state.notifyBulletExploded()

    def createCentralExplosion(self):
        explosionCenter = Explosion(self.state, self.bullet.position)
        explosionCenter.setExplosionTile("center")
        self.state.explosions.append(explosionCenter)

    def createDirectionalExplosions(self):
        for vector in [
            Vector2(-1, 0),
            Vector2(1, 0),
            Vector2(0, 1),
            Vector2(0, -1),
        ]:
            for i in range(1, self.bullet.bulletRange + 1):
                newPosition = (
                    self.bullet.position.elementwise()
                    + vector.elementwise() * Vector2(i, i)
                )
                nextPosition = (
                    self.bullet.position.elementwise()
                    + vector.elementwise() * Vector2(i + 1, i + 1)
                )

                if not self.state.isInside(newPosition) or self.state.isWallAt(
                    newPosition
                ):
                    break

                explosion = Explosion(self.state, newPosition)
                explosion.setExplosionTile(
                    "horizontal" if vector.x == 0 else "vertical"
                )

                self.state.explosions.append(explosion)

                if (
                    not self.state.isInside(nextPosition)
                    or self.state.isWallAt(nextPosition)
                    or self.state.isBrickAt(newPosition)
                    or i == self.bullet.bulletRange
                ):
                    explosion.setExplosionTile(
                        "left"
                        if vector == Vector2(-1, 0)
                        else "right"
                        if vector == Vector2(1, 0)
                        else "bottom"
                        if vector == Vector2(0, 1)
                        else "top"
                    )

                    break
