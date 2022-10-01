from cursed_snake.model.snake_types import Coordinate


def _offset(coord: Coordinate, x_offset: int, y_offset: int) -> Coordinate:
    x, y = coord
    return x + x_offset, y + y_offset


def west(coord: Coordinate) -> Coordinate:
    print(coord)
    return _offset(coord, -1, 0)


def east(coord: Coordinate) -> Coordinate:
    return _offset(coord, +1, 0)


def north(coord: Coordinate) -> Coordinate:
    return _offset(coord, 0, +1)


def south(coord: Coordinate) -> Coordinate:
    return _offset(coord, 0, -1)
