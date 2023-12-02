from pygame.math import Vector2
from .Layer import Layer


class ArrayLayer(Layer):
    def __init__(self, ui, imageFile, gameState, array):
        super().__init__(ui, imageFile)
        self.gameState = gameState
        self.array = array

    def render(self, surface):
        for y in range(self.gameState.worldHeight):
            for x in range(self.gameState.worldWidth):
                tile = self.array[y][x]
                if not tile is None:
                    self.renderTile(surface, Vector2(x, y), tile)
