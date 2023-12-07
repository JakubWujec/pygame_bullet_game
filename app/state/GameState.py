from pygame.math import Vector2
from .GameItems import Unit, Explosion


class GameState:
    def __init__(self) -> None:
        self.worldSize = Vector2(17, 17)
        self.ground = [[Vector2(2, 26)] * 17 for x in range(17)]
        self.walls = self.__prepareWalls(17, 17)
        self.units: [Unit] = [
            Unit(self, Vector2(9, 8), Vector2(13, 1)),
        ]
        self.explosions = []
        self.bullets = []
        self.bulletSpeed = 0.1
        self.bulletRange = self.worldHeight
        self.bulletDelay = self.worldHeight

        self.epochs = 100

    @property
    def worldWidth(self):
        return int(self.worldSize.x)

    @property
    def worldHeight(self):
        return int(self.worldSize.y)

    def __prepareWalls(self, width, height):
        _walls = [[None] * width for x in range(height)]
        for i in range(width):
            _walls[0][i] = Vector2(4, 26)
            _walls[height - 1][i] = Vector2(4, 26)

        for i in range(height):
            _walls[i][0] = Vector2(4, 26)
            _walls[i][width - 1] = Vector2(4, 26)

        for x in range(2, width, 2):
            for y in range(2, height, 2):
                _walls[x][y] = Vector2(4, 26)
        return _walls

    def isInside(self, pos: Vector2):
        return 0 <= pos.x < self.worldWidth and 0 <= pos.y < self.worldHeight

    def isWall(self, pos: Vector2):
        return not self.walls[int(pos.x)][int(pos.y)] is None
