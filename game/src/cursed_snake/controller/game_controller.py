import time
from itertools import accumulate

from typing import Iterable

from cursed_snake.model.board import move_snake
from cursed_snake.gui.game_screen import gui
from cursed_snake.model.snake import create_starting_snake
from cursed_snake.model.snake_types import Direction, Snake, Food
from cursed_snake.server import http_server
from cursed_snake.truley_cursed import global_state


def direction_reader() -> Iterable[Direction]:
    while True:
        if global_state.last_request is None:
            time.sleep(1)
        else:
            yield global_state.last_request


def run_game_loop() -> None:
    initial_snake = create_starting_snake()
    initial_food = (10, 20)
    directions: Iterable[Direction] = direction_reader()
    game_frames: Iterable[tuple[Snake, Food]] = accumulate(
        directions,
        lambda tup, direction: (move_snake(tup[0], direction), tup[1]),
        initial=(initial_snake, initial_food)
    )
    gui(
        game_frames
    )


if __name__ == '__main__':
    run_game_loop()
