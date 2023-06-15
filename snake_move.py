from game import GameState
from agents import MinimaxAgent, RandomAgent, AlphaBetaAgent


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
        self.agent = MinimaxAgent(3)



class SnakeAlphabetaMove(SnakeMove):

    def __init__(self):
        self.agent = AlphaBetaAgent(3)
