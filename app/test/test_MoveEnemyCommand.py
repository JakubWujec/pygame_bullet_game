import unittest
from unittest.mock import Mock
from pygame.math import Vector2
from app.state import Enemy, GameState
from app.commands import MoveEnemyCommand


class TestMoveEnemyCommand(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.enemy = Enemy(self.state, Vector2(1, 1))  # Provide necessary parameters
        self.moveEnemyCommand = MoveEnemyCommand(self.state, self.enemy)

    def test_can_move_to_valid_position(self):
        # Mocking isInside, isWallAt, isBrickAt, and isBulletAt methods as needed
        self.state.isInside = Mock(return_value=True)
        self.state.isWallAt = Mock(return_value=False)
        self.state.isBrickAt = Mock(return_value=False)
        self.state.isBulletAt = Mock(return_value=False)

        # Set up a valid position
        newPos = Vector2(2, 2)

        # Assert that can_move_to returns True for a valid position
        result = self.moveEnemyCommand.canMoveTo(newPos)
        self.assertTrue(result)

    def test_cannot_move_to_invalid_position(self):
        # Mocking isInside, isWallAt, isBrickAt, and isBulletAt methods as needed
        self.state.isInside = Mock(return_value=False)
        self.state.isWallAt = Mock(return_value=True)
        self.state.isBrickAt = Mock(return_value=False)
        self.state.isBulletAt = Mock(return_value=False)

        # Set up an invalid position
        newPos = Vector2(0, 0)

        # Assert that can_move_to returns False for an invalid position
        result = self.moveEnemyCommand.canMoveTo(newPos)
        self.assertFalse(result)
