from typing import TYPE_CHECKING

from pygame.math import Vector2

from app.state import Orientation
from app.layer import Layer

if TYPE_CHECKING:
    from app.state import Unit

UNIT_TILES = {
    "RIGHT": [Vector2(0, 0), Vector2(1, 0)],
    "LEFT": [Vector2(0, 1), Vector2(1, 1)],
    "DOWN": [Vector2(0, 2), Vector2(1, 2)],
    "TOP": [Vector2(0, 3), Vector2(1, 3)],
}


class UnitsLayer(Layer):
    def __init__(self, cellSize, imageFile, gameState, units):
        super().__init__(cellSize, imageFile)
        self.gameState = gameState
        self.units = units
        self.tileAnimationIndex = 0

    def render(self, surface):
        for unit in self.units:
            self.renderTile(surface, unit.position, unit.tile)

    def unitMoved(self, unit: "Unit"):
        self.animateWalk(unit)

    def animateWalk(self, unit):
        self.tileAnimationIndex = (self.tileAnimationIndex + 1) % 2
        unit.tile = UNIT_TILES[Orientation(unit.orientation).name][
            self.tileAnimationIndex
        ]
