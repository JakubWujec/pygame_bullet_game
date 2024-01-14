import unittest
from unittest.mock import Mock
from pygame.math import Vector2
from app.state import GameItem, GameState


class TestGameItem(unittest.TestCase):
    def setUp(self):
        # Create a dummy state for testing
        self.mockState = Mock(spec=GameState)

    def testCollideWithShouldReturnTrueWhenCollisionOccurs(self):
        item = GameItem(self.mockState, Vector2(2, 2), Vector2(0, 0))

        collidingPositions = [
            Vector2(1.1, 1.1),
            Vector2(2.1, 2.1),
        ]

        for position in collidingPositions:
            result = item.collideWith(position)

            self.assertTrue(result, "Collision should occur")

    def testCollideWithShouldReturnFalseWhenNoCollisionOccurs(self):
        item = GameItem(self.mockState, Vector2(2, 2), Vector2(0, 0))

        nonCollidingPositions = [
            Vector2(1, 1),
            Vector2(3, 3),
            Vector2(3, 2),
            Vector2(1, 2),
        ]

        for position in nonCollidingPositions:
            result = item.collideWith(position)

        self.assertFalse(result, "No collision should occur")


if __name__ == "__main__":
    unittest.main()
