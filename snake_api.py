

class SnakeApi():

    def __init__(self, snake_move):
        self.snake_move = snake_move

    def info(self):
        # print("INFO")
        return {
            "apiversion": "1",
            "author": "bigbrains-snake",  # TODO: Your Battlesnake Username
            "color": "#19A7CE",  # TODO: Choose color
            "head": "evil",  # TODO: Choose head
            "tail": "hook",  # TODO: Choose tail
        }
    
    def start(self, game_state):
        print(f"GAME START at {game_state['board']}")
        return "start"

    def end(self, game_state):
        print("GAME OVER\n")
        return "end"
    
    def move(self, game_state):
        return self.snake_move.move(game_state)
