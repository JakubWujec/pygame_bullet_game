import os
from typing import Dict, Tuple, Union, List, cast, Optional

import pygame
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface

from core.constants import LayerValue


class Theme:
    def __init__(self):
        self.__fontsDef = {"default": {"file": "font/prstart/prstartk.ttf", "size": 8}}
        self.__fontColors = {"default": (100, 75, 50)}
        self.__fonts = {}

        self.__tilesets: Dict[str, Surface] = {}
        self.__tilesDefs = {
            "ground": {
                "imageFile": "toen/ground.png",
                "tileWidth": 16,
                "tileHeight": 16,
                "tiles": {
                    LayerValue.GROUND_SEA: (4, 7),
                    LayerValue.GROUND_EARTH: (2, 7),
                },
            },
            "impassable": {
                "imageFile": "toen/impassable.png",
                "tileWidth": 16,
                "tileHeight": 16,
                "tiles": {
                    LayerValue.IMPASSABLE_RIVER: (0, 1),
                    LayerValue.IMPASSABLE_POND: (1, 0),
                    LayerValue.IMPASSABLE_MOUNTAIN: (4, 0),
                },
            },
            "objects": {
                "imageFile": "toen/objects.png",
                "tileWidth": 16,
                "tileHeight": 16,
                "tiles": {
                    LayerValue.OBJECTS_SIGN: (1, 0),
                    LayerValue.OBJECTS_HILL: (4, 0),
                    LayerValue.OBJECTS_ROCKS: (6, 1),
                    LayerValue.OBJECTS_TREES: (5, 0),
                    LayerValue.OBJECTS_MILL: (0, 1),
                    LayerValue.OBJECTS_HOUSES: (1, 2),
                    LayerValue.OBJECTS_ROAD_DIRT: (0, 3),
                    LayerValue.OBJECTS_ROAD_STONE: (4, 3),
                    LayerValue.OBJECTS_FARM: (8, 0),
                    LayerValue.OBJECTS_CAMP: (8, 1),
                },
            },
        }

    # Tiles

    def getTileset(self, name: str) -> Surface:
        if name not in self.__tilesets:
            imageFile = os.path.join("assets", self.__tilesDefs[name]["imageFile"])
            if not os.path.exists(imageFile):
                raise ValueError(f"No file '{imageFile}'")
            self.__tilesets[name] = pygame.image.load(imageFile).convert_alpha()
        return self.__tilesets[name]

    def getTileSize(self, name: str) -> Tuple[int, int]:
        tileset = self.__tilesDefs[name]
        return tileset["tileWidth"], tileset["tileHeight"]

    def __computeTileRects(
        self,
        tileOrList: Union[Tuple[int, int], List[Tuple[int, int]]],
        tileWidth: int,
        tileHeight: int,
    ) -> List[Rect]:
        def buildRect(tile: Tuple[int, int]) -> Rect:
            return pygame.Rect(
                tile[0] * tileWidth, tile[1] * tileHeight, tileWidth, tileHeight
            )

        rects = []
        if type(tileOrList) == list:
            tileList = cast(List[Tuple[int, int]], tileOrList)
            for subTile in tileList:
                rects.append(buildRect(subTile))
        else:
            tile = cast(Tuple[int, int], tileOrList)
            rects.append(buildRect(tile))
        return rects

    def getTilesRect(self, name: str, minValue: int, maxValue: int) -> Dict[int, Rect]:
        if name not in self.__tilesDefs:
            raise ValueError(f"No tiledef {name}")
        tilesDef = self.__tilesDefs[name]
        tiles = tilesDef["tiles"]
        tileWidth = tilesDef["tileWidth"]
        tileHeight = tilesDef["tileHeight"]
        tilesRect = {}
        for value in range(minValue, maxValue):
            if value not in tiles:
                raise ValueError(
                    "No tile definition for layer '{}' value {}".format(name, value)
                )
            tile = tiles[value]
            tilesRect[value] = Rect(
                tile[0] * tileWidth, tile[1] * tileHeight, tileWidth, tileHeight
            )
        return tilesRect

    # Text

    def getFont(self, name: Optional[str] = None) -> Font:
        if name is None:
            name = "default"
        if name not in self.__fontsDef:
            raise ValueError("No font {}".format(name))
        fontDef = self.__fontsDef[name]
        file = os.path.join("assets", fontDef["file"])
        size = fontDef["size"]
        fontId = file, size
        if fontId not in self.__fonts:
            self.__fonts[fontId] = pygame.font.Font(file, size)
        return self.__fonts[fontId]

    def getFontColor(self, name: Union[None, str] = None) -> Tuple[int, int, int]:
        if name is None:
            name = "default"
        if name not in self.__fontColors:
            raise ValueError("No font color {}".format(name))
        return self.__fontColors[name]
