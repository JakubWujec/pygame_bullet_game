import tmx
import os
from pygame.math import Vector2

from app.state import Unit, Brick, Enemy, Orientation, Powerup
from .Command import Command


class LoadLevelCommand(Command):
    def __init__(self, playGameMode, fileName) -> None:
        super().__init__()
        self.fileName = fileName
        self.playGameMode = playGameMode

    def run(self):
        if not os.path.exists(self.fileName):
            raise RuntimeError(f"No file {self.fileName}")
        tileMap = tmx.TileMap.load(self.fileName)
        if tileMap.orientation != "orthogonal":
            raise RuntimeError(f"Error in {self.fileName}: invalid orientation")
        if len(tileMap.layers) != 8:
            raise RuntimeError(
                f"Error in {self.fileName}: 8 layers are expected. Got {len(tileMap.layers)}"
            )

        state = self.playGameMode.gameState
        worldSize = Vector2(tileMap.width, tileMap.height)
        state.worldSize = worldSize

        # Ground
        tileset, array = self.decodeArrayLayer(tileMap, tileMap.layers[0])
        cellSize = Vector2(tileset.tilewidth, tileset.tileheight)
        state.ground[:] = array
        imageFile = tileset.image.source
        self.playGameMode.layers[0].setTileset(cellSize, imageFile)

        # Walls
        tileset, array = self.decodeArrayLayer(tileMap, tileMap.layers[1])
        if tileset.tilewidth != cellSize.x or tileset.tileheight != cellSize.y:
            raise RuntimeError(
                "Error in {}: tile sizes must be the same in all layers".format(
                    self.fileName
                )
            )
        state.walls[:] = array
        imageFile = tileset.image.source
        self.playGameMode.layers[1].setTileset(cellSize, imageFile)  # walls

        # Bricks
        tileset, array = self.decodeBricksLayer(state, tileMap, tileMap.layers[2])
        if tileset.tilewidth != cellSize.x or tileset.tileheight != cellSize.y:
            raise RuntimeError(
                "Error in {}: tile sizes must be the same in all layers".format(
                    self.fileName
                )
            )
        state.bricks[:] = array
        imageFile = tileset.image.source
        self.playGameMode.layers[2].setTileset(cellSize, imageFile)

        # Units
        tileset, array = self.decodeUnitsLayer(state, tileMap, tileMap.layers[3])
        if tileset.tilewidth != cellSize.x or tileset.tileheight != cellSize.y:
            raise RuntimeError(
                "Error in {}: tile sizes must be the same in all layers".format(
                    self.fileName
                )
            )
        state.units[:] = array
        imageFile = tileset.image.source
        self.playGameMode.layers[3].setTileset(cellSize, imageFile)

        # Enemies
        tileset, array = self.decodeEnemiesLayer(state, tileMap, tileMap.layers[4])
        if tileset.tilewidth != cellSize.x or tileset.tileheight != cellSize.y:
            raise RuntimeError(
                "Error in {}: tile sizes must be the same in all layers".format(
                    self.fileName
                )
            )
        state.enemies[:] = array
        imageFile = tileset.image.source
        self.playGameMode.layers[4].setTileset(cellSize, imageFile)

        # Powerups
        tileset, array = self.decodePowerupsLayer(state, tileMap, tileMap.layers[5])
        imageFile = tileset.image.source
        state.powerups[:] = array
        self.playGameMode.layers[5].setTileset(cellSize, imageFile)

        # Bullets
        tileset = self.decodeLayer(tileMap, tileMap.layers[6])
        imageFile = tileset.image.source
        state.bullets[:] = []
        self.playGameMode.layers[6].setTileset(cellSize, imageFile)

        # Explosions
        tileset = self.decodeLayer(tileMap, tileMap.layers[7])
        imageFile = tileset.image.source
        state.explosions[:] = []
        self.playGameMode.layers[7].setTileset(cellSize, imageFile)

        self.playGameMode.cellSize = cellSize
        self.playGameMode.playerUnit = state.units[0]
        self.playGameMode.notifyResizeRequested(cellSize.elementwise() * worldSize)
        self.playGameMode.gameOver = False

    def decodeArrayLayer(self, tileMap, layer):
        tileset = self.decodeLayer(tileMap, layer)

        array = [None] * tileMap.height
        for y in range(tileMap.height):
            array[y] = [None] * tileMap.width
            for x in range(tileMap.width):
                tile = layer.tiles[x + y * tileMap.width]
                if tile.gid == 0:
                    continue
                lid = tile.gid - tileset.firstgid
                if lid < 0 or lid >= tileset.tilecount:
                    raise RuntimeError(
                        "Error in {}: invalid tile id".format(self.fileName)
                    )
                tileX = lid % tileset.columns
                tileY = lid // tileset.columns
                array[y][x] = Vector2(tileX, tileY)

        return tileset, array

    def decodeEnemiesLayer(self, state, tileMap, layer):
        tileset = self.decodeLayer(tileMap, layer)
        array = []
        for y in range(tileMap.height):
            for x in range(tileMap.width):
                tile = layer.tiles[x + y * tileMap.width]
                if tile.gid == 0:
                    continue
                enemy = Enemy(state, Vector2(x, y))
                enemy.orientation = self.getTileOrientation(tile)
                array.append(enemy)
        return tileset, array

    def decodePowerupsLayer(self, state, tileMap, layer):
        tileset = self.decodeLayer(tileMap, layer)
        array = []
        for y in range(tileMap.height):
            for x in range(tileMap.width):
                tile = layer.tiles[x + y * tileMap.width]
                if tile.gid == 0:
                    continue
                lid = tile.gid - tileset.firstgid
                if lid < 0 or lid >= tileset.tilecount:
                    raise RuntimeError(
                        "Error in {}: invalid tile id".format(self.fileName)
                    )
                tileX = lid % tileset.columns
                tileY = lid // tileset.columns

                array.append(Powerup(state, Vector2(x, y)))
        return tileset, array

    def getTileOrientation(self, tile):
        orientationMapping = {
            (False, False): Orientation.TOP,
            (False, True): Orientation.DOWN,
            (True, False): Orientation.LEFT,
            (True, True): Orientation.RIGHT,
        }

        flipFlags = (tile.dflip, tile.vflip)

        return orientationMapping.get(flipFlags, Orientation.TOP)

    def decodeBricksLayer(self, state, tileMap, layer):
        tileset = self.decodeLayer(tileMap, layer)
        array = []
        for y in range(tileMap.height):
            for x in range(tileMap.width):
                tile = layer.tiles[x + y * tileMap.width]
                if tile.gid == 0:
                    continue
                array.append(Brick(state, Vector2(x, y)))
        return tileset, array

    def decodeUnitsLayer(self, state, tileMap, layer):
        tileset = self.decodeLayer(tileMap, layer)
        array = []
        for y in range(tileMap.height):
            for x in range(tileMap.width):
                tile = layer.tiles[x + y * tileMap.width]
                if tile.gid == 0:
                    continue
                lid = tile.gid - tileset.firstgid
                if lid < 0 or lid >= tileset.tilecount:
                    raise RuntimeError(
                        "Error in {}: invalid tile id".format(self.fileName)
                    )
                tileX = lid % tileset.columns
                tileY = lid // tileset.columns
                array.append(Unit(state, Vector2(x, y), Vector2(tileX, tileY)))
        return tileset, array

    def decodeLayer(self, tileMap, layer):
        if not isinstance(layer, tmx.Layer):
            raise RuntimeError("Error in {}: invalid layer type".format(self.fileName))
        if len(layer.tiles) != tileMap.width * tileMap.height:
            raise RuntimeError("Error in {}: invalid tiles count".format(self.fileName))

        # Guess which tileset is used by this layer
        gid = None
        for tile in layer.tiles:
            if tile.gid != 0:
                gid = tile.gid
                break
        if gid is None:
            if len(tileMap.tilesets) == 0:
                raise RuntimeError("Error in {}: no tilesets".format(self.fileName))
            tileset = tileMap.tilesets[0]
        else:
            tileset = None
            for t in tileMap.tilesets:
                if gid >= t.firstgid and gid < t.firstgid + t.tilecount:
                    tileset = t
                    break
            if tileset is None:
                raise RuntimeError(
                    "Error in {}: no corresponding tileset".format(self.fileName)
                )

        # Check the tileset
        if tileset.columns <= 0:
            raise RuntimeError(
                "Error in {}: invalid columns count".format(self.fileName)
            )
        if tileset.image.data is not None:
            raise RuntimeError(
                "Error in {}: embedded tileset image is not supported".format(
                    self.fileName
                )
            )

        return tileset
