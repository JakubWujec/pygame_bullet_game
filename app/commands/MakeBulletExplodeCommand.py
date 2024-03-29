from typing import TYPE_CHECKING, Literal

from pygame.math import Vector2

from app.state import Explosion

from .Command import Command

if TYPE_CHECKING:
    from app.state.Bullet import Bullet
    from app.state.GameState import GameState

EXPLOSION_TILES = {
    "center": Vector2(0, 2),
    "top": Vector2(0, 0),
    "bottom": Vector2(0, 1),
    "left": Vector2(1, 0),
    "right": Vector2(2, 0),
    "horizontal": Vector2(1, 1),
    "vertical": Vector2(2, 1),
}


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
        self.setExplosionTile(explosionCenter, "center")
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

                if not self.state.isInside(newPosition) or self.state.isWallAt(
                    self.state.closestIntegerPosition(newPosition)
                ):
                    break

                explosion = Explosion(self.state, newPosition)
                self.setExplosionTile(
                    explosion, "horizontal" if vector.x == 0 else "vertical"
                )

                self.state.explosions.append(explosion)

                if self.isLastExplosionInDirection(newPosition, vector, i):
                    self.setExplosionTile(
                        explosion,
                        "left"
                        if vector == Vector2(-1, 0)
                        else "right"
                        if vector == Vector2(1, 0)
                        else "bottom"
                        if vector == Vector2(0, 1)
                        else "top",
                    )

                    break

    def isLastExplosionInDirection(
        self, newPosition: Vector2, direction: Vector2, index: int
    ):
        nextPosition = (
            self.bullet.position.elementwise()
            + direction.elementwise() * Vector2(index + 1, index + 1)
        )
        return (
            not self.state.isInside(nextPosition)
            or self.state.isWallAt(self.state.closestIntegerPosition(nextPosition))
            or self.state.isBrickAt(self.state.closestIntegerPosition(newPosition))
            or index == self.bullet.bulletRange
        )

    def setExplosionTile(
        self,
        explosion,
        explosionTile: Literal[
            "center", "top", "bottom", "left", "right", "horizontal", "vertical"
        ],
    ):
        explosion.tile = EXPLOSION_TILES[explosionTile]
