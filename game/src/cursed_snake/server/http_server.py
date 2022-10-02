from flask import Flask
from flask import request

from cursed_snake.model.directions import north, east, south, west
from cursed_snake.truley_cursed import global_state
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def func() -> str:
    user_input = request.get_data().decode("UTF-8")
    global_state.last_request = {
                       "y+": north,
                       "x+": east,
                       "y-": south,
                       "x-": west
                   }.get(user_input) or global_state.last_request
    return "it's someone else's problem now"


def start_server() -> None:
    app.run(host="0.0.0.0", port=6969)



