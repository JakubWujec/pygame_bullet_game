import unittest
from pygame.math import Vector2
from app.state import GameState, Unit, Powerup, Enemy, Bullet
from app.commands import (
    MoveCommand,
)


class TestMoveCommand(unittest.TestCase):
    def setUp(self):
        # Create a simple game state for testing
        self.gameState = GameState(Vector2(25, 25))

        # Create a unit for testing
        self.unit = Unit(self.gameState, Vector2(5, 5), Vector2(1, 0))

        # Create a move command for testing
        self.moveCommand = MoveCommand(self.gameState, self.unit, Vector2(1, 0))

    def test_can_walk_in_four_directions(self):
        for direction in [Vector2(1, 0), Vector2(0, 1), Vector2(0, -1), Vector2(-1, 0)]:
            gameState = GameState(Vector2(3, 3))
            unitInitialPosition = Vector2(1, 1)
            unit = Unit(gameState, unitInitialPosition, Vector2(1, 0))

            # one for change of orientation
            moveCommand = MoveCommand(gameState, unit, direction)
            moveCommand.run()
            moveCommand.run()

            self.assertNotEqual(unitInitialPosition, unit.position)

    def test_cant_walk_into_walls(self):
        for direction in [Vector2(1, 0), Vector2(0, 1), Vector2(0, -1), Vector2(-1, 0)]:
            gameState = GameState(Vector2(3, 3))
            gameState.setWall(0, 0)
            gameState.setWall(0, 1)
            gameState.setWall(0, 2)
            gameState.setWall(1, 0)
            gameState.setWall(1, 2)
            gameState.setWall(2, 0)
            gameState.setWall(2, 1)
            gameState.setWall(2, 2)
            unitInitialPosition = Vector2(1, 1)
            unit = Unit(gameState, unitInitialPosition, Vector2(1, 0))

            moveCommand = MoveCommand(gameState, unit, direction)
            moveCommand.run()
            moveCommand.run()
            moveCommand.run()

            self.assertEqual(unitInitialPosition, unit.position)


if __name__ == "__main__":
    unittest.main()
