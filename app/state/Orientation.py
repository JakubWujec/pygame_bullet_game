from enum import IntEnum
from pygame.math import Vector2


class Orientation(IntEnum):
    LEFT = -90
    TOP = 0
    RIGHT = 90
    DOWN = 180


def orientationToVector(orientation: Orientation):
    if orientation == Orientation.LEFT:
        return Vector2(-1, 0)
    if orientation == Orientation.RIGHT:
        return Vector2(1, 0)
    if orientation == Orientation.DOWN:
        return Vector2(0, -1)
    if orientation == Orientation.TOP:
        return Vector2(0, 1)

    raise NotImplementedError


def vectorToOrientation(vector: Vector2):
    if vector == Vector2(-1, 0):
        return Orientation.LEFT
    if vector == Vector2(1, 0):
        return Orientation.RIGHT
    if vector == Vector2(0, -1):
        return Orientation.DOWN
    if vector == Vector2(0, 1):
        return Orientation.TOP

    raise NotImplementedError
