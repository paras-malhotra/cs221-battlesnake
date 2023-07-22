from flask import Flask, request
from flask_ngrok import run_with_ngrok

from snake_api import SnakeBrain

# app
snake_app = Flask(__name__)
snake_api = SnakeBrain()

### run 
# runs on GCP defined by app.yml
run_with_ngrok(snake_app)


@snake_app.route("/")
def hello():
    """Return a friendly HTTP greeting.

    Returns:
        A string with the words 'Hello World!'.
    """
    return snake_api.info()
    # return "Hello World!"

@snake_app.get("/args")
def args():
    # game_state = request.get_json()
    # snake_api.end(game_state)
    # return jsonify(request.get_json())
    return request.args

@snake_app.post("/start")
def on_start():
    game_state = request.get_json()
    snake_api.start(game_state)
    return "ok"

@snake_app.post("/move")
def on_move():
    game_state = request.get_json()
    snake_name = request.args["snake_name"]
    return snake_api.move(game_state, snake_name)

@snake_app.post("/end")
def on_end():
    game_state = request.get_json()
    snake_api.end(game_state)
    return "ok"

@snake_app.after_request
def identify_server(response):
    response.headers.set(
        "server", "battlesnake/github/starter-snake-python"
    )
    return response


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    snake_app.run(host="127.0.0.1", port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]