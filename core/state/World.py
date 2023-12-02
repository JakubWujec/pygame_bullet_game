from typing import List
from core.constants import LayerValue
from core.state.Layer import Layer


class World:
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__layers = {
            "ground": Layer(width, height, LayerValue.GROUND_SEA),
            "impassable": Layer(width, height, LayerValue.NONE),
            "objects": Layer(width, height, LayerValue.NONE),
        }

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def ground(self) -> Layer:
        return self.__layers["ground"]

    @property
    def impassable(self) -> Layer:
        return self.__layers["impassable"]

    @property
    def objects(self) -> Layer:
        return self.__layers["objects"]

    def getLayer(self, name: str) -> Layer:
        if name not in self.__layers:
            raise ValueError(f"No layer {name}")
        return self.__layers[name]
