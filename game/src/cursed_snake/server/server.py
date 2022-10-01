from flask import Flask 
from flask import request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def func() -> str:
    # Get the data and stuffs
    str = request.get_data().decode("utf-8")
    print(str)
    return "good"


def start_server(callback: func) -> None:
    app.run(host = "0.0.0.0", port=6969)


if __name__=='__main__':
    app.debug = True
    start_server(None)

