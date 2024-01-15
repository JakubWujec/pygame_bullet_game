from pygame.math import Vector2

from .Layer import Layer


class UnitsLayer(Layer):
    def __init__(self, cellSize, imageFile, gameState, units):
        super().__init__(cellSize, imageFile)
        self.gameState = gameState
        self.units = units

    def render(self, surface):
        for unit in self.units:
            self.renderTile(surface, unit.position, unit.tile)
