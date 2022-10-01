from typing import Tuple, List, Any

from cursed_snake.model.snake import move_snake
from cursed_snake.model.snake_types import Coordinate, Snake, Direction, Head, Position

_MIN_X = 0
_MIN_Y = 0
_MAX_X = 50
_MAX_Y = 50


def define_board_limits() -> tuple[tuple[Position, Position], tuple[Position, Position]]:
    return (_MIN_X, _MAX_X), (_MIN_Y, _MAX_Y)


def move_on_board(snake: Snake, direction: Direction) -> Snake:
    unwrapped_snake: Snake = move_snake(snake, direction)
    head, tail = unwrapped_snake
    wrapped_snake: Snake = _wrap_snake_head(head, (_MIN_X, _MAX_X), (_MIN_Y, _MAX_Y))
    return wrapped_snake


def _wrap_snake_head(head: Head, x_limits: tuple[Position, Position], y_limits: tuple[Position, Position]) -> Head:
    x, y = head
    x_new = _wrap(x, x_limits)
    y_new = _wrap(y, y_limits)
    return x_new, y_new


def _wrap(value: int, limits: tuple[Position, Position]) -> int:
    min_lim, max_lim = limits
    if value < min_lim:
        return max_lim
    elif value > max_lim:
        return min_lim
    else:
        return value
