from typing import TYPE_CHECKING, List

from pygame.math import Vector2
from pygame.rect import Rect

from .Brick import Brick
from .Explosion import Explosion
from .Unit import Unit

if TYPE_CHECKING:
    from app.state import GameStateObserver, Enemy, Bullet, Powerup

WALL_VECTOR = Vector2(4, 26)


class GameState:
    def __init__(self, worldSize: Vector2 = Vector2(21, 21)) -> None:
        self.epoch: int = 0
        self.bulletSpeed: float = 0.1
        self.bulletDelay: int = 20
        self.worldSize = worldSize
        self.ground = [
            [Vector2(2, 26)] * self.worldWidth for _ in range(self.worldHeight)
        ]
        self.walls = [[None] * self.worldWidth for x in range(self.worldHeight)]
        self.units: List[Unit] = []
        self.enemies: List[Enemy] = []
        self.bricks: List[Brick] = []
        self.explosions: List[Explosion] = []
        self.bullets: List[Bullet] = []
        self.powerups: List[Powerup] = []

        self.__observers: List[GameStateObserver] = []

    @property
    def worldWidth(self):
        return int(self.worldSize.x)

    @property
    def worldHeight(self):
        return int(self.worldSize.y)

    def setWall(self, x: int, y: int):
        self.walls[x][y] = WALL_VECTOR

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

    def closestIntegerPosition(self, position) -> Vector2:
        return Vector2(round(position.x), round(position.y))

    def addObserver(self, observer):
        self.__observers.append(observer)

    def removeObserver(self, observer):
        self.__observers.remove(observer)

    def notifyBulletFired(self):
        for observer in self.__observers:
            observer.bulletFired()

    def notifyBulletExploded(self):
        for observer in self.__observers:
            observer.bulletExploded()

    def notifyUnitMoved(self, unit):
        for observer in self.__observers:
            observer.unitMoved(unit)
