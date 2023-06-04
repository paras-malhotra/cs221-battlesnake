import random
from typing import Any, List, Optional, Tuple
from agents import Agent
from game import Actions, GameRules, GameState, Player
import util
import json

class TrainableAgent(Agent):
    def learn(self, beforeState: GameState, afterState: GameState, action: str):
        raise NotImplementedError

class CustomEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if(isinstance(o, GameState) or isinstance(o, Player)):
            return o.__dict__
        return super().default(o)

class DataDumpAgent(TrainableAgent):
    def __init__(self) -> None:
        self.dataset = []

    def getAction(self, gameState: GameState) -> Optional[str]:
        legalMoves = gameState.getLegalActions()
        selectedChoice = random.choice(legalMoves) if len(legalMoves) > 0 else None

        return selectedChoice

    def learn(self, beforeState: GameState, afterState: GameState, action: str):
        self.dataset.append({'gameState': beforeState, 'action': action, 'reward': self.getReward(beforeState, afterState)})

    def getReward(self, beforeState: GameState, afterState: GameState) -> float:
        if afterState.isEndState():
            if afterState.isWon():
                return 1.0
            elif afterState.isLost():
                return -1.0
            elif afterState.isTie():
                return 0.0
        else:
            if afterState.players[0].health > beforeState.players[0].health:
                return 0.1
            else:
                return 0.0

    def dump(self, filename: str):
        print(f"Dumped {len(self.dataset)} records")
        out_file = open(filename, 'w')
        json.dump(self.dataset, out_file, indent=4, cls=CustomEncoder)

class Trainer:
    def __init__(self, enemyAgents: List[Agent], width: int = 11, height: int = 11) -> None:
        self.numEnemies = len(enemyAgents)
        self.enemyAgents = enemyAgents
        self.numEpisodes = 0
        self.width = width
        self.height = height

    def train(self, agent: TrainableAgent, numEpisodes: int):
        currentEpisodes = self.numEpisodes
        endEpisodes = currentEpisodes + numEpisodes

        while self.numEpisodes < endEpisodes:
            # new game episode
            currentState = GameSimulator.getRandomGameState(self.width, self.height, self.numEnemies)
            while not currentState.isEndState():
                alivePlayers = currentState.getAlivePlayers()
                beforeState = currentState.deepCopy()
                for player in alivePlayers:
                    action = agent.getAction(currentState) if player.ours else self.enemyAgents[player.id - 2].getAction(currentState)
                    if action is None or action not in GameRules.getLegalActions(currentState, player.id - 1):
                        player.alive = False
                    else:
                        player.move(action, currentState.width, currentState.height, currentState.food, currentState.hazards)
                    
                    if player.ours:
                        agent.learn(beforeState, currentState, action)
                
                currentState.accountForEndState()
                GameSimulator.ensureMinimumFood(currentState)
            self.numEpisodes = self.numEpisodes + 1
        
class GameSimulator:
    def getRandomGameState(width: int, height: int, numEnemies: int) -> GameState:
        playerLocation = (random.randint(0, width - 1), random.randint(0, height - 1))
        enemyLocations = []
        
        while len(enemyLocations) < numEnemies:
            enemyLoc = (random.randint(0, width - 1), random.randint(0, height - 1))
            if enemyLoc == playerLocation or enemyLoc in enemyLocations:
                continue
            else:
                enemyLocations.append(enemyLoc)

        gameState = GameState({
            'board': {
                'width': width,
                'height': height,
                'food': [],
                'hazards': [],
                'snakes': [{
                    'health': Player.MAX_HEALTH,
                    'body': util.getDictCoordinates([playerLocation]),
                    'length': 1,
                    'id': 1,
                    'alive': True,
                }] + [{
                    'health': Player.MAX_HEALTH,
                    'body': util.getDictCoordinates([enemyLocations[i]]),
                    'length': 1,
                    'id': i + 2,
                    'alive': True
                } for i in range(len(enemyLocations))]
            },
            'you': {
                'id': 1
            }
        })

        GameSimulator.ensureMinimumFood(gameState)

        return gameState
    getRandomGameState = staticmethod(getRandomGameState)
    
    def ensureMinimumFood(gameState: GameState, minFoodPellets: int = 0) -> None:
        alivePlayers = gameState.getAlivePlayers()
        
        if minFoodPellets == 0:
            minFoodPellets = len(alivePlayers)
        
        food = []
        while(len(food) < minFoodPellets):
            foodPelletLocation = (random.randint(0, gameState.width - 1), random.randint(0, gameState.height - 1))
            for player in alivePlayers:
                if foodPelletLocation in player.body:
                    continue
            
            food.append(foodPelletLocation)
        
        gameState.food = food
    ensureMinimumFood = staticmethod(ensureMinimumFood)

