from cursed_snake.model.directions import west

from cursed_snake.model.snake_types import Snake, Coordinate, Direction
from itertools import accumulate

_STARTING_LENGTH: int = 3
_STARTING_HEAD_COORDINATE: Coordinate = (5, 5)


def _create_snake(head_coordinate: Coordinate, direction: Direction, length: int) -> Snake:
    head, *tail = list(accumulate(range(length - 1), lambda acc, _: direction(acc), initial=head_coordinate))
    return head, tail


def create_starting_snake() -> Snake:
    return _create_snake(_STARTING_HEAD_COORDINATE, west, _STARTING_LENGTH)


def move_snake(snake: Snake, direction: Direction) -> Snake:
    head, tail = snake
    new_head = direction(head)
    new_tail = [head] + tail[:-1]
    return new_head, new_tail
