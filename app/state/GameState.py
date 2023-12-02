from pygame.math import Vector2


class GameState:
    def __init__(self) -> None:
        self.tankPos = Vector2(8, 8)
        self.worldSize = Vector2(16, 16)
        self.block1 = Vector2(9, 9)
        self.block2 = Vector2(10, 10)

    def update(self, moveTankCommand: Vector2):
        newTankPos = self.tankPos + moveTankCommand

        if (
            self.isPositionInsideWorld(newTankPos)
            and newTankPos != self.block1
            and newTankPos != self.block2
        ):
            self.tankPos = newTankPos

    def isPositionInsideWorld(self, pos: Vector2):
        return (
            pos.x >= 0
            and pos.x < self.worldSize.x
            and pos.y >= 0
            and pos.y < self.worldSize.y
        )
