from typing import Literal

from pygame.math import Vector2

from .GameItem import GameItem

EXPLOSION_TILES = {
    "center": Vector2(0, 2),
    "top": Vector2(0, 0),
    "bottom": Vector2(0, 1),
    "left": Vector2(1, 0),
    "right": Vector2(2, 0),
    "horizontal": Vector2(1, 1),
    "vertical": Vector2(2, 1),
}


class Explosion(GameItem):
    def __init__(self, state, position, tile=Vector2(6, 4)):
        super().__init__(state, position, tile)
        self.epoch = self.state.epoch
        self.center = position
        self.range = 2
        self.frameIndex = 0
        self.timeToLive = 100

    def isTimeToDelete(self):
        return self.state.epoch >= (self.epoch + self.timeToLive)

    def setExplosionTile(
        self,
        explosionTile: Literal[
            "center", "top", "bottom", "left", "right", "horizontal", "vertical"
        ],
    ):
        self.tile = EXPLOSION_TILES[explosionTile]
