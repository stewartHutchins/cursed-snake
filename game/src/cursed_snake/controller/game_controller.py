import time
from itertools import accumulate
from random import random

from typing import Iterable, Iterator, Callable

from cursed_snake.model.board import move_snake, move_with_wrap
from cursed_snake.gui.game_screen import gui
from cursed_snake.model.directions import south, east
from cursed_snake.model.snake import create_starting_snake, grow_snake
from cursed_snake.model.snake_types import Direction, Snake, Food, Position
from cursed_snake.server import http_server
from cursed_snake.settings import MIN_X, MAX_Y, MAX_X, MIN_Y
from cursed_snake.truley_cursed import global_state


def direction_reader() -> Iterable[Direction]:
    while True:
        if global_state.last_request is None:
            time.sleep(0.2)
        else:
            yield global_state.last_request


def update_game_frame(
        current_snake: Snake,
        current_food: Food,
        direction: Direction,
        food_generator: Iterator[Food]
) -> tuple[Snake, Food]:
    head, _ = current_snake
    new_head_pos = direction(head)
    if new_head_pos == current_food:
        return grow_snake(current_snake, direction), next(food_generator)
    else:
        return move_with_wrap(current_snake, direction, (MIN_X, MAX_X), (MIN_Y, MAX_Y)), current_food


def _game_frames(
        directions: Iterator[Direction],
        initial_snake,
        food_generator: Iterator[Food]
) -> Iterable[tuple[Snake, Food]]:
    return accumulate(
        directions,
        lambda tup, direction: update_game_frame(tup[0], tup[1], direction, food_generator),
        initial=(initial_snake, next(food_generator))
    )


def _food_generator(x_limits: tuple[Position, Position], y_limits: tuple[Position, Position]) -> Iterator[Food]:
    while True:
        yield random.randint(*x_limits), random.randint(*y_limits),


def run_game_loop(
        get_directions: Callable[[], Iterator[Direction]] = direction_reader,
        get_food_gen: Callable[[], Iterator[Food]] = lambda: _food_generator((MIN_X, MAX_X), (MIN_Y, MAX_Y))
) -> None:
    initial_snake = create_starting_snake()
    directions: Iterator[Direction] = get_directions()
    foods: Iterator[Food] = get_food_gen()
    frames = _game_frames(directions, initial_snake, foods)
    gui(frames)


from itertools import repeat, chain


def psudo_directions() -> Iterator[Direction]:
    return chain(
        repeat(south, 10),
        repeat(east, 10),
        repeat(south, 10),
        repeat(south, 5),
        repeat(east, 100)
    )

def psudo_food()-> Iterator[Food]:
    return chain([(10, 5), (30, 20)], repeat((10, 5)))

if __name__ == '__main__':
    run_game_loop(psudo_directions, psudo_food)
