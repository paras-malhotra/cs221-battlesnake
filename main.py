from flask import Flask, request
from flask_ngrok import run_with_ngrok
# from flask import has_request_context
# from flask.logging import default_handler
# import logging

from snake_api import SnakeBrain

### app
snake_app = Flask(__name__)
snake_api = SnakeBrain(snake_app)

### run 
## NGROK: https://www.youtube.com/watch?v=wBCEDCiQh3Q
run_with_ngrok(snake_app)
## GCP: defined by app.yml


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

# class RequestFormatter(logging.Formatter):
#     def format(self, record):
#         if has_request_context():
#             record.url = request.url
#             record.remote_addr = request.remote_addr
#         else:
#             record.url = None
#             record.remote_addr = None

#         return super().format(record)
# formatter = RequestFormatter(
#     '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
#     '%(levelname)s in %(module)s: %(message)s'
# )
# default_handler.setFormatter(formatter)

if __name__ == "__main__":
    ### NGROK
    snake_app.config['FLASK_DEBUG'] = True
    # snake_app.logger.setLevel(logging.INFO)
    snake_app.run()
    ### LOCAL
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    # snake_app.run(host="127.0.0.1", port=8080, debug=True)