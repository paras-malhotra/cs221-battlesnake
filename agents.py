from game import GameState, Player
from search import minDistanceToFoodBfs
from typing import Optional, Tuple, List
import random

class Agent:
    def getAction(self, gameState: GameState) -> Optional[str]:
        raise NotImplementedError("Override me")
    
class RandomAgent(Agent):
    # futureState = None
    def getAction(self, gameState: GameState) -> Optional[str]:
        # print(f"Game state: {gameState}")
        legalMoves = gameState.getLegalActions()

        selectedChoice = random.choice(legalMoves) if len(legalMoves) > 0 else None

        # if self.futureState is not None and self.futureState.players != gameState.players:
        #     print(f"mismatch b/w predicted {self.futureState.players} and actual {gameState.players}")

        #print(f"At {gameState.players[0].head}, legal moves: {legalMoves}, selected: {selectedChoice}")
        # self.futureState = gameState.generateSuccessor(selectedChoice, 0)

        return selectedChoice
    
class RandomEnemyAgent(Agent):
    def __init__(self, playerIndex: int) -> None:
        self.playerIndex = playerIndex

    def getAction(self, gameState: GameState) -> Optional[str]:
        legalMoves = gameState.getLegalActions(self.playerIndex)

        selectedChoice = random.choice(legalMoves) if len(legalMoves) > 0 else None

        return selectedChoice
    
class MinimaxAgent(Agent):
    WIN_REWARD = 100000

    def __init__(self, depth: int) -> None:
        self.depth = depth

    def getAction(self, gameState: GameState) -> Optional[str]:
        # print(f"Game state: {gameState}")
        players = gameState.players

        if not players[0].ours:
            # our player is not alive
            return None

        (bestValue, bestMove) = self.vminimax(gameState, 0, self.depth)

        if bestMove is None:
            # certain death
            legalMoves = gameState.getLegalActions()
            if len(legalMoves) > 0:
                return self.moveTieBreaker(legalMoves, gameState)
            
        #print(f"At {gameState.players[0].head}, legal moves: {gameState.getLegalActions()}, selected: {bestMove}")

        return bestMove
        
    def vminimax(self, gameState: GameState, index: int, depth: int) -> Tuple[float, Optional[str]]:
        if depth == 0 or gameState.isEndState() or len(gameState.players) <= 1:
            return (self.evaluationFunction(gameState), None)
        
        if index == 0:
            # Our move (maximizing)
            legalMoves = gameState.getLegalActions(0)
            if (len(legalMoves) == 0):
                return (-MinimaxAgent.WIN_REWARD, None)

            values = [self.vminimax(gameState.generateSuccessor(move, 0), 1, depth)[0] for move in legalMoves]
            bestValue = max(values)
            bestMoves = [legalMoves[i] for i in range(len(values)) if values[i] == bestValue]
            # if depth != self.depth:
            #     print(f"vminimax at depth {depth}, index {index}: {(bestValue, bestMoves[0])}")
            
            return (bestValue, self.moveTieBreaker(bestMoves, gameState) if depth == self.depth and len(bestMoves) > 1 else bestMoves[0])
        
        else:
            # Opponent's move (minimizing)
            legalMoves = gameState.getLegalActions(index)
            
            if (len(legalMoves) == 0) or not gameState.players[index].alive:
                # go to the next agent
                return self.vminimax(gameState.generateSuccessor(None, index), self.getNextIndex(index, gameState), self.getNextDepth(index, depth, gameState))

            values = [self.vminimax(gameState.generateSuccessor(move, index), self.getNextIndex(index, gameState), self.getNextDepth(index, depth, gameState))[0] for move in legalMoves]
            bestValue = min(values)
            # print(f"vminimax at depth {depth}, index {index}: {(bestValue, bestMoves[0])}")

            return (bestValue, None)
        
    def evaluationFunction(self, gameState: GameState) -> float:
        if gameState.isWon():
            return MinimaxAgent.WIN_REWARD
        
        if gameState.isLost():
            return -MinimaxAgent.WIN_REWARD
        
        if gameState.isTie():
            return 0.0
        
        x, y = gameState.players[0].head
        
        if len(gameState.food) == 0:
            foodDistance = 0
            foodScore = 0
        else:
            foodDistance = minDistanceToFoodBfs(x, y, gameState.food, gameState.getWalls(), gameState.width, gameState.height)
            if minDistanceToFoodBfs == -1:
                foodScore = 0
            else:
                healthGainFromFood = Player.MAX_HEALTH - gameState.players[0].health
                foodScore = healthGainFromFood if foodDistance == 0 else (healthGainFromFood - 2) / foodDistance

        # print(f"food score: {foodScore}, distance: {foodDistance}, ({x}, {y}) to {gameState.food}")

        return gameState.players[0].health + foodScore
    
    def moveTieBreaker(self, moves: List[str], gameState: GameState) -> Optional[str]:
        return random.choice(moves)
    
    def getNextIndex(self, curIndex: int, gameState: GameState) -> int:
        # cycle over agents
        return (curIndex + 1) % len(gameState.players)
        
    
    def getNextDepth(self, curIndex: int, curDepth: int, gameState: GameState) -> int:
        # reduce depth on last agent, else same depth
        return (curDepth - 1) if curIndex == (len(gameState.players) - 1) else curDepth
    
class AlphaBetaAgent(MinimaxAgent):
    def getAction(self, gameState: GameState) -> Optional[str]:
        # print(f"Game state: {gameState}")
        players = gameState.players

        if not players[0].ours:
            # our player is not alive
            return None

        (bestValue, bestMove) = self.vpruned(gameState, 0, self.depth, None, None)

        if bestMove is None:
            # certain death
            legalMoves = gameState.getLegalActions()
            if len(legalMoves) > 0:
                return self.moveTieBreaker(legalMoves, gameState)
            
        # print(f"At {gameState.players[0].head}, legal moves: {gameState.getLegalActions()}, selected: {bestMove}")

        return bestMove
    
    def vpruned(self, gameState: GameState, index: int, depth: int, alpha: Optional[float], beta: Optional[float]) -> Tuple[float, Optional[str]]:
        if depth == 0 or gameState.isEndState() or len(gameState.players) <= 1:
            return (self.evaluationFunction(gameState), None)
        
        if index == 0:
            # Our move (maximizing)
            legalMoves = gameState.getLegalActions(0)
            if (len(legalMoves) == 0):
                return (-MinimaxAgent.WIN_REWARD, None)
            
            bestValue = None
            bestMoves = []

            for move in legalMoves:
                value = self.vpruned(gameState.generateSuccessor(move, 0), 1, depth, alpha, beta)[0]

                if bestValue is None or value > bestValue:
                    bestValue = value
                    bestMoves = [move]
                if value == bestValue:
                    bestMoves.append(move)
                if alpha is None or value > alpha:
                    alpha = value
                if beta is not None and beta <= alpha:
                    break

            # if depth != self.depth:
            #     print(f"vminimax at depth {depth}, index {index}: {(bestValue, bestMoves[0])}")
            
            return (bestValue, self.moveTieBreaker(bestMoves, gameState) if depth == self.depth and len(bestMoves) > 1 else bestMoves[0])
        
        else:
            # Opponent's move (minimizing)
            legalMoves = gameState.getLegalActions(index)
            
            if (len(legalMoves) == 0) or not gameState.players[index].alive:
                # go to the next agent
                return self.vpruned(gameState.generateSuccessor(None, index), self.getNextIndex(index, gameState), self.getNextDepth(index, depth, gameState), alpha, beta)
            
            bestValue = None
            bestMove = None

            for move in legalMoves:
                value = self.vpruned(gameState.generateSuccessor(move, index), self.getNextIndex(index, gameState), self.getNextDepth(index, depth, gameState), alpha, beta)[0]
                if bestValue is None or value < bestValue:
                      bestValue = value
                      bestMove = move
                if beta is None or value < beta:
                    beta = value
                if alpha is not None and beta <= alpha:
                    break

            # print(f"vminimax at depth {depth}, index {index}: {(bestValue, bestMoves[0])}")

            return (bestValue, bestMove)