from unittest import TestCase

from core.state import World
from core.constants import LayerValue


class TestWorld(TestCase):
    def test_setget(self):
        world = World(14, 7)
        self.assertEqual(14, world.width)
        self.assertEqual(7, world.height)

        groundLayer = world.ground
        for y in range(world.height):
            for x in range(world.width):
                self.assertEqual(LayerValue.GROUND_SEA, groundLayer.getValue(x, y))

        groundLayer.setValue(3, 4, LayerValue.GROUND_EARTH)
        for y in range(world.height):
            for x in range(world.width):
                if x == 3 and y == 4:
                    self.assertEqual(
                        LayerValue.GROUND_EARTH, groundLayer.getValue(x, y)
                    )
                else:
                    self.assertEqual(LayerValue.GROUND_SEA, groundLayer.getValue(x, y))
