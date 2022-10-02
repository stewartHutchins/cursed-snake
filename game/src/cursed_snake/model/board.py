from typing import Tuple, List, Any

from cursed_snake.model.snake import move_snake
from cursed_snake.model.snake_types import Coordinate, Snake, Direction, Head, Position


def grow_snake_with_wrap(
        snake: Snake,
        direction: Direction,
        x_limits: tuple[Position, Position],
        y_limits: tuple[Position, Position]
) -> Snake:
    head, tail = snake
    new_head = _wrap_snake_head(direction(head), x_limits, y_limits)
    new_tail = [head] + tail
    return new_head, new_tail


def move_with_wrap(
        snake: Snake,
        direction: Direction,
        x_limits: tuple[Position, Position],
        y_limits: tuple[Position, Position]
) -> Snake:
    unwrapped_snake: Snake = move_snake(snake, direction)
    head, tail = unwrapped_snake
    wrapped_snake: Head = _wrap_snake_head(head, x_limits, y_limits)
    return wrapped_snake, tail


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
