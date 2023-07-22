from snake_move import SnakeRandomMove, SnakeMinimaxMove, SnakeAlphabetaMove


class SnakeApi():

    def info(self, web_app):
        self.web_app = flask_aweb_apppp
        # print("INFO")
        return {
            "apiversion": "1",
            "author": "bigbrains-snake",  # TODO: Your Battlesnake Username
            "color": "#19A7CE",  # TODO: Choose color
            "head": "evil",  # TODO: Choose head
            "tail": "hook",  # TODO: Choose tail
        }
    
    def start(self, game_state):
        self.web_app.logger.info('%s logged in successfully', game_state['board'])
        # print(f"GAME START at {game_state['board']}")
        return "start"

    def end(self, game_state):
        print("GAME OVER\n")
        return "end"


class SnakeBrain(SnakeApi):

    RANDOM_BRAIN = "RANDOM_BRAIN".lower()
    MINIMAX_BRAIN = "MINIMAX_BRAIN".lower()
    ALPHABETA_BRAIN = "ALPHABETA_BRAIN".lower()

    def __init__(self):
        self.brain_bucket = {}
        self.max_depth = 10
        # random
        self.brain_bucket[SnakeBrain.RANDOM_BRAIN] = SnakeRandomMove()
        # minimax
        for depth in range(self.max_depth):
            self.brain_bucket[SnakeBrain.MINIMAX_BRAIN + "_" + str(depth)] = SnakeMinimaxMove(depth)
        # alpha beta 
        for depth in range(self.max_depth):
            self.brain_bucket[SnakeBrain.ALPHABETA_BRAIN + "_" + str(depth)] = SnakeAlphabetaMove(depth)
    
    def move(self, game_state, snake_name):
        snake_brain = self.brain_bucket[snake_name.lower()]
        return snake_brain.move(game_state)
            

