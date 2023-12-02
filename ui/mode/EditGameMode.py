from typing import Tuple, Optional

from pygame.rect import Rect
from pygame.surface import Surface
from core.state import World
from ui.LayerComponent import LayerComponent

from ui.Theme import Theme
from ui.mode.GameMode import GameMode


class EditGameMode(GameMode):
    def __init__(self, theme: Theme, world: World):
        super().__init__(theme)
        self.__world = world
        self.__mouseButtonDown = False
        self.__layers = [
            LayerComponent(theme, world.getLayer(name), name)
            for name in ["ground", "impassable", "objects"]
        ]
        # self.__font = theme.getFont("default")

        # Brush
        self.__brushLayer = "impassable"

    def processInput(self):
        pass

    def update(self):
        pass

    def render(self, surface: Surface):
        theme = self.theme
        tileWidth = theme.tileWidth
        tileHeight = theme.tileHeight
        tiles = theme.tiles
        tileset = theme.tileset
        for y in range(self.__world.height):
            for x in range(self.__world.width):
                tile = tiles[self.__world.getValue(x, y)]
                tileRect = Rect(
                    tile[0] * tileWidth, tile[1] * tileHeight, tileWidth, tileHeight
                )
                tileCoords = (x * tileWidth, y * tileHeight)
                surface.blit(tileset, tileCoords, tileRect)
