from game import GameState
from snake_agents import MinimaxAgent, RandomAgent, AlphaBetaAgent


class SnakeMove():

    def __init__(self):
        pass

    def move(self, game_state):
        #print(f"State: {game_state}")
        state = GameState(game_state)
        recommendedMove = self.agent.getAction(state)

        return {"move": recommendedMove, "shout": ""}
   

class SnakeRandomMove(SnakeMove):

    def __init__(self):
        self.agent = RandomAgent()


class SnakeMinimaxMove(SnakeMove):

    def __init__(self):
        self.agent = MinimaxAgent(depth=3)


class SnakeAlphabetaMove(SnakeMove):

    def __init__(self):
        self.agent = AlphaBetaAgent(depth=3)
