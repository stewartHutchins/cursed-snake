import threading

from cursed_snake.controller.game_controller import run_game_loop
from cursed_snake.server.http_server import start_server


def main() -> None:
    tasks = [start_server, run_game_loop]
    for task in tasks:
        thread = threading.Thread(target=task)
        thread.start()


if __name__ == '__main__':
    main()