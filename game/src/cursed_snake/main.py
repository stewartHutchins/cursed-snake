import threading

from cursed_snake.controller.game_controller import run_game_loop
from cursed_snake.server.http_server import start_server


def main() -> None:
    tasks = [start_server]
    for task in tasks:
        thread = threading.Thread(target=task)
        thread.start()
    run_game_loop()


if __name__ == '__main__':
    main()
