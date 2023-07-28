from flask import Flask, request

from snake_api import SnakeBrain

### app
snake_app = Flask(__name__)
snake_brain = SnakeBrain(snake_app)

### routes
@snake_app.route("/")
def hello_world():
    return snake_brain.info()

@snake_app.route("/favicon.ico")
def fav_ico():
    return snake_brain.info()

@snake_app.post("/start")
def on_start():
    game_state = request.get_json()
    snake_brain.start(game_state)
    return "ok"

@snake_app.post("/move")
def on_move():
    game_state = request.get_json()
    snake_name = request.args["snake_name"]
    return snake_brain.move(game_state, snake_name)

@snake_app.post("/end")
def on_end():
    game_state = request.get_json()
    snake_brain.end(game_state)
    return "ok"

@snake_app.after_request
def identify_server(response):
    response.headers.set(
        "server", "battlesnake/github/starter-snake-python"
    )
    return response

if __name__ == "__main__":
    ### NGROK
    # snake_app.config['FLASK_DEBUG'] = True
    # snake_app.logger.setLevel(logging.INFO)
    snake_app.run(port=5000)
    ### LOCAL
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    # snake_app.run(host="127.0.0.1", port=8080, debug=True)



# app.logger.debug('This is a DEBUG message')
# app.logger.info('This is an INFO message')
# app.logger.warning('This is a WARNING message')
# app.logger.error('This is an ERROR message')    