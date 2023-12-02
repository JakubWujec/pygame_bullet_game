from unittest import TestCase

from state import World
from state.constants import LAYER_GROUND_SEA, LAYER_GROUND_EARTH


class TestWorld(TestCase):

    def test_setget(self):
        world = World(14, 7)
        self.assertEqual(14, world.width)
        self.assertEqual(7, world.height)

        for y in range(world.height):
            for x in range(world.width):
                self.assertEqual(LAYER_GROUND_SEA, world.getValue(x, y))

        world.setValue(3, 4, LAYER_GROUND_EARTH)
        for y in range(world.height):
            for x in range(world.width):
                if x == 3 and y == 4:
                    self.assertEqual(LAYER_GROUND_EARTH, world.getValue(x, y))
                else:
                    self.assertEqual(LAYER_GROUND_SEA, world.getValue(x, y))
