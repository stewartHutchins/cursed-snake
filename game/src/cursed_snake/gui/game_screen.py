from typing import Iterable, Callable, Tuple, Any, Iterator

from cursed_snake.model.snake_types import Food
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
import numpy.typing as npt
import numpy as np

from cursed_snake.model.snake import create_starting_snake, move_snake
from cursed_snake.model.snake_types import Snake, Position, Coordinate
from cursed_snake.settings import *

from itertools import accumulate, repeat
from cursed_snake.model.directions import west, east

_INTERVAL = 100
_FOOD = 3
_HEAD = 2
_TAIL = 1
_NONE = 0


def _snake_to_heatmap(snake: Snake, food: Coordinate, x_limit: Position, y_limit: Position) -> npt.NDArray[int]:
    head, tail = snake
    board = np.zeros((x_limit, y_limit))
    board[head[0], head[1]] = _HEAD
    board[food[0], food[1]] = _FOOD
    for coord in tail:
        board[coord[0], coord[1]] = _TAIL
    return board


def draw_board(snake: Snake, food: Food, *, ax: plt.Axes) -> plt.Axes:
    initial_heatmap = _snake_to_heatmap(snake, food, MAX_X+1, MAX_Y+1)
    return sns.heatmap(initial_heatmap, ax=ax, cbar=False)


def _initialize(initial_snake: Snake, initial_food: Coordinate, *, ax) -> plt.Axes:
    ax = draw_board(initial_snake, initial_food, ax=ax)
    ax.set_title("SNEK!")
    return ax


def gui(frames: Iterable[tuple[Snake, Food]]) -> None:
    fig, ax = plt.subplots()

    update: Callable[[tuple[Snake, Food]], plt.Axes] = lambda tup: draw_board(tup[0], tup[1], ax=ax)
    frames_iterator = iter(frames)
    initial_snake, initial_food = next(frames_iterator)

    animate = FuncAnimation(
        fig,
        func=lambda frame, *fargs: update(next(frames_iterator)),
        init_func=lambda: _initialize(initial_snake, initial_food, ax=ax),
        interval=_INTERVAL
    )
    plt.show()


def movement(initial_snake: Snake, initial_food: Coordinate) -> Iterable[tuple[Snake, Food]]:
    return accumulate(
        repeat(1),
        lambda acc, elm: (move_snake(acc[0], east), initial_food),
        initial=(initial_snake, initial_food)
    )


def main() -> None:
    initial_snake = create_starting_snake()
    initial_food = (10, 20)
    gui(iter(movement(initial_snake, initial_food)))


if __name__ == '__main__':
    main()
