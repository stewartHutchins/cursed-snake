from cursed_snake.model.snake_types import Snake, Coordinate, Direction

_STARTING_LENGTH: int = 3
_STARTING_POSITION: Coordinate = (0, 0)


def create_starting_snake() -> Snake:
    return [_STARTING_POSITION]


def move_snake(snake: Snake, direction: Direction) -> Snake:
    head, tail = snake
    new_head = direction(head)
    new_tail = [head] + tail[:-1]
    return new_head, new_tail


def grow_snake(snake: Snake, direction: Direction) -> Snake:
    head, tail = snake
    new_head = direction(head)
    new_tail = [head] + tail
    return new_head, new_tail
