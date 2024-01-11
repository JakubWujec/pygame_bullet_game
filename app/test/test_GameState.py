import unittest
from pygame.math import Vector2
from app.state import GameState


class TestGameState(unittest.TestCase):
    def setUp(self):
        # Initialize GameState for testing
        self.game_state = GameState(Vector2(25, 25))

    def test_is_inside(self):
        self.assertTrue(self.game_state.isInside(Vector2(0, 0)))
        self.assertTrue(self.game_state.isInside(Vector2(5, 5)))
        self.assertTrue(self.game_state.isInside(Vector2(24, 24)))
        self.assertFalse(self.game_state.isInside(Vector2(25, 25)))
