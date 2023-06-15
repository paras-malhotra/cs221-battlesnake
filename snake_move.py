from game import GameState
from agents import MinimaxAgent, RandomAgent, AlphaBetaAgent


class SnakeMove():

    def __init__(self):
        pass

    def move(self, game_state):
        #print(f"State: {game_state}")
        state = GameState(game_state)
        agent = AlphaBetaAgent(3)
        recommendedMove = agent.getAction(state)

        return {"move": recommendedMove, "shout": ""}