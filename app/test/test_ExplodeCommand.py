import unittest
from unittest.mock import Mock

from pygame.math import Vector2

from app.commands import ExplodeCommand
from app.state import Brick, Explosion, GameState


class TestExplodeCommand(unittest.TestCase):
    def setUp(self):
        self.gameState = Mock(spec=GameState)
        self.explosion = Mock(spec=Explosion)
        self.command = ExplodeCommand(self.gameState, self.explosion)

    def test_findBricksToDestroy(self):
        gameState = GameState(Vector2(25, 25))
        brick1 = Brick(gameState, Vector2(1, 1))
        brick2 = Brick(gameState, Vector2(5, 5))
        explosion = Explosion(gameState, Vector2(1, 1))
        gameState.bricks = [brick1, brick2]
        gameState.explosions = [explosion]

        command = ExplodeCommand(gameState, explosion)
        bricksToDestroy = command.findBricksToDestroy()

        self.assertEqual(len(bricksToDestroy), 1)
        self.assertIn(brick1, bricksToDestroy)
        self.assertNotIn(brick2, bricksToDestroy)

    def test_findBricksToDestroyShouldReturnBrickWhenItsRoughlyInTheSamePositionAsExplosion(
        self,
    ):
        gameState = GameState(Vector2(25, 25))
        brick1 = Brick(gameState, Vector2(1, 1))
        explosion1 = Explosion(gameState, Vector2(0.51, 1.49))
        gameState.bricks = [brick1]
        gameState.explosions = [explosion1]

        command = ExplodeCommand(gameState, explosion1)
        bricksToDestroy = command.findBricksToDestroy()

        self.assertEqual(len(bricksToDestroy), 1)
        self.assertIn(brick1, bricksToDestroy)


if __name__ == "__main__":
    unittest.main()
