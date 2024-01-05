from typing import TYPE_CHECKING, List

from pygame.math import Vector2
from pygame.rect import Rect

from .Brick import Brick
from .Explosion import Explosion
from .Unit import Unit

if TYPE_CHECKING:
    from app.state.Powerup import Powerup
    from app.state.GameItem import GameItem
    from app.state.Bullet import Bullet
    from app.state.Enemy import Enemy


class GameState:
    def __init__(self) -> None:
        self.epoch = 0
        self.bulletSpeed = 0.1
        self.bulletDelay = 20
        self.worldSize = Vector2(21, 21)
        self.ground = [[Vector2(2, 26)] * 21 for x in range(21)]
        self.walls = self.__prepareWalls(21, 21)
        self.units: [Unit] = [
            Unit(self, Vector2(9, 8), Vector2(13, 1)),
        ]
        self.enemies = []
        self.bricks: [Brick] = [Brick(self, Vector2(1, 1))]
        self.explosions: [Explosion] = []
        self.bullets = []
        self.powerups: List[Powerup] = []

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

    def isWallAt(self, pos: Vector2):
        return not self.walls[int(pos.x)][int(pos.y)] is None

    def isBrickAt(self, pos: Vector2):
        return len(list(filter(lambda brick: brick.position == pos, self.bricks))) > 0

    def isWalkableAt(self, pos: Vector2):
        return not (self.isWallAt(pos) or self.isBrickAt(pos))

    def findCollidingPowerups(self, position: Vector2) -> List["Powerup"]:
        return [powerup for powerup in self.powerups if powerup.collideWith(position)]

    def findCollidingEnemies(self, position: Vector2) -> List["Enemy"]:
        return [enemy for enemy in self.enemies if enemy.collideWith(position)]

    def findCollidingUnits(self, position: Vector2) -> List[Unit]:
        return [unit for unit in self.units if unit.collideWith(position)]

    def findCollidingBullets(self, position: Vector2) -> List["Bullet"]:
        return [bullet for bullet in self.bullets if bullet.collideWith(position)]

    def isCollidingWithWallOrBrick(self, position):
        cellSize = 32
        posRect = Rect(position.x * cellSize, position.y * cellSize, cellSize, cellSize)

        for rowIndex, rowWall in enumerate(self.walls):
            for colIndex, wall in enumerate(rowWall):
                if wall is not None:
                    wallRect = Rect(
                        rowIndex * cellSize, colIndex * cellSize, cellSize, cellSize
                    )
                    if wallRect.colliderect(posRect):
                        return True

        for brick in self.bricks:
            brickRect = Rect(
                brick.position.x * cellSize,
                brick.position.y * cellSize,
                cellSize,
                cellSize,
            )
            if brickRect.colliderect(posRect):
                return True

        return False

    def findEnemiesAt(self, position: Vector2):
        return filter(lambda enemy: enemy.position == position, self.enemies)
