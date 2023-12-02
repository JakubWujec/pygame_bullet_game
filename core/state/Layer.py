from core.constants import LayerValue


class Layer:
    def __init__(self, width: int, height: int, defaultValue: LayerValue):
        self.__width = width
        self.__height = height
        self.__cells = []
        for y in range(height):
            row = [defaultValue] * width
            self.__cells.append(row)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    def getValue(self, x: int, y: int) -> LayerValue:
        assert 0 <= x < self.__width, f"Invalid x={x}"
        assert 0 <= y < self.__height, f"Invalid y={y}"
        return self.__cells[y][x]

    def setValue(self, x: int, y: int, value: LayerValue):
        assert 0 <= x < self.__width, f"Invalid x={x}"
        assert 0 <= y < self.__height, f"Invalid y={y}"
        self.__cells[y][x] = value
