from pygame.surface import Surface

from core.constants import LayerValue, LayerValueRanges
from core.state import Layer
from ui.Theme import Theme


class LayerComponent:
    def __init__(self, theme: Theme, layer: Layer, name: str):
        self.__theme = theme
        self.__layer = layer
        self.__name = name
        minValue = LayerValueRanges[name][0]
        maxValue = LayerValueRanges[name][1]
        self.__tilesRect = theme.getTilesRect(name, minValue, maxValue)

    def render(self, surface: Surface):
        theme = self.__theme
        tileset = theme.getTileset(self.__name)
        tileWidth, tileHeight = theme.getTileSize(self.__name)
        for y in range(self.__layer.height):
            for x in range(self.__layer.width):
                value = self.__layer.getValue(x, y)
                if value == LayerValue.NONE:
                    continue
                tileRect = self.__tilesRect[value]
                tileCoords = (x * tileWidth, y * tileHeight)
                surface.blit(tileset, tileCoords, tileRect)
