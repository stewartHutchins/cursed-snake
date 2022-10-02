import time
from itertools import accumulate
from random import randint 

from typing import Iterable, Iterator, Callable

from cursed_snake.model.board import move_snake, move_with_wrap, grow_snake_with_wrap
from cursed_snake.gui.game_screen import gui
from cursed_snake.model.directions import south, east, north
from cursed_snake.model.snake import create_starting_snake
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


def death_screen() -> tuple[Snake, Food]:
    snake = (3, 3), [(3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17), (3, 18), (3, 21), (3, 22), (3, 23), (3, 24), (3, 25), (3, 26), (3, 27), (3, 30), (3, 31), (3, 32), (3, 33), (3, 34), (3, 35), (3, 36), (4, 3), (4, 12), (4, 18), (4, 21), (4, 24), (4, 27), (4, 30), (5, 3), (5, 12), (5, 18), (5, 21), (5, 24), (5, 27), (5, 30), (6, 3), (6, 12), (6, 18), (6, 21), (6, 24), (6, 27), (6, 30), (7, 3), (7, 12), (7, 18), (7, 21), (7, 24), (7, 27), (7, 30), (8, 3), (8, 12), (8, 13), (8, 14), (8, 15), (8, 16), (8, 17), (8, 18), (8, 21), (8, 24), (8, 27), (8, 30), (9, 3), (9, 6), (9, 7), (9, 8), (9, 9), (9, 12), (9, 18), (9, 21), (9, 27), (9, 30), (9, 31), (9, 32), (9, 33), (9, 34), (10, 3), (10, 9), (10, 12), (10, 18), (10, 21), (10, 27), (10, 30), (11, 3), (11, 9), (11, 12), (11, 18), (11, 21), (11, 27), (11, 30), (12, 3), (12, 9), (12, 12), (12, 18), (12, 21), (12, 27), (12, 30), (13, 3), (13, 9), (13, 12), (13, 18), (13, 21), (13, 27), (13, 30), (14, 3), (14, 4), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 12), (14, 18), (14, 19), (14, 21), (14, 27), (14, 30), (14, 31), (14, 32), (14, 33), (14, 34), (14, 35), (14, 36), (18, 14), (18, 15), (18, 16), (18, 17), (18, 18), (18, 19), (18, 20), (18, 23), (18, 29), (18, 32), (18, 33), (18, 34), (18, 35), (18, 36), (18, 37), (18, 38), (18, 41), (18, 42), (18, 43), (18, 44), (18, 45), (18, 46), (19, 14), (19, 20), (19, 23), (19, 29), (19, 32), (19, 41), (19, 46), (20, 14), (20, 20), (20, 23), (20, 29), (20, 32), (20, 41), (20, 46), (21, 14), (21, 20), (21, 23), (21, 29), (21, 32), (21, 41), (21, 46), (22, 14), (22, 20), (22, 24), (22, 28), (22, 32), (22, 41), (22, 46), (23, 14), (23, 20), (23, 24), (23, 28), (23, 32), (23, 41), (23, 46), (24, 14), (24, 20), (24, 24), (24, 28), (24, 32), (24, 33), (24, 34), (24, 35), (24, 36), (24, 41), (24, 42), (24, 43), (24, 44), (24, 45), (24, 46), (25, 14), (25, 20), (25, 24), (25, 28), (25, 32), (25, 41), (25, 43), (26, 14), (26, 20), (26, 25), (26, 27), (26, 32), (26, 41), (26, 43), (27, 14), (27, 20), (27, 25), (27, 27), (27, 32), (27, 41), (27, 44), (28, 14), (28, 20), (28, 25), (28, 27), (28, 32), (28, 41), (28, 44), (29, 14), (29, 20), (29, 25), (29, 27), (29, 32), (29, 41), (29, 45), (30, 14), (30, 15), (30, 16), (30, 17), (30, 18), (30, 19), (30, 20), (30, 26), (30, 32), (30, 33), (30, 34), (30, 35), (30, 36), (30, 37), (30, 38), (30, 41), (30, 45)]
    food = (0,0)
    return snake, food

def death_condition(current_snake: Snake) -> bool:
    head, tail = current_snake
    return head in tail

death_flag = False
def update_game_frame(
        current_snake: Snake,
        current_food: Food,
        direction: Direction,
        food_generator: Iterator[Food]
) -> tuple[Snake, Food]:
    global death_flag
    if death_flag:
        return death_screen()
    head, _ = current_snake
    new_head_pos = direction(head)
    x_limits = (MIN_X, MAX_X)
    y_limits = (MIN_Y, MAX_Y)
    new_snake: Snake
    if new_head_pos == current_food:
        new_snake= grow_snake_with_wrap(current_snake, direction, x_limits, y_limits), next(food_generator)
    else:
        new_snake = move_with_wrap(current_snake, direction, x_limits, y_limits), current_food
    death_flag = death_condition(new_snake)
    return new_snake

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
        yield randint(*x_limits), randint(*y_limits),


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
        repeat(south, 1),
        repeat(north, 1),
        repeat(south, 10),
        repeat(south, 5),
        repeat(east, 100)
    )


def psudo_food() -> Iterator[Food]:
    return chain([(10, 5), (30, 20), (30, 50)], repeat((10, 5)))


if __name__ == '__main__':
    #death_flag = True
    run_game_loop(psudo_directions, psudo_food)
