from game import GameState
from snake_agents import MinimaxAgent, RandomAgent, AlphaBetaAgent


class SnakeMove():

    def __init__(self):
        pass

    def move(self, game_state):
        recommended = "idk move"
        shout = "let me check..."
        try:
            #print(f"State: {game_state}")
            state = GameState(game_state)
            recommended = self.agent.getAction(state)
        except Exception as e:
            shout = "SNAKE_MOVE_ERROR=" + str(e)
        return {"move": recommended, "shout": shout}
   

class SnakeRandomMove(SnakeMove):

    def __init__(self):
        self.agent = RandomAgent()


class SnakeMinimaxMove(SnakeMove):

    def __init__(self, depth):
        self.agent = MinimaxAgent(depth)


class SnakeAlphabetaMove(SnakeMove):

    def __init__(self, depth):
        self.agent = AlphaBetaAgent(depth)
