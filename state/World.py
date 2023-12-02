from state.constants import LAYER_GROUND_SEA


class World:
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__cells = []
        for y in range(height):
            row = [LAYER_GROUND_SEA] * width
            self.__cells.append(row)

    @property
    def width(self) -> int:
        assert self.__width == len(self.__cells[0])
        return self.__width

    @property
    def height(self) -> int:
        assert self.__height == len(self.__cells)
        return self.__height

    def getValue(self, x: int, y: int) -> int:
        assert 0 <= x < self.__width, f"Invalid x={x}"
        assert 0 <= y < self.__height, f"Invalid y={y}"
        return self.__cells[y][x]

    def setValue(self, x: int, y: int, value: int):
        assert 0 <= x < self.__width, f"Invalid x={x}"
        assert 0 <= y < self.__height, f"Invalid y={y}"
        self.__cells[y][x] = value
