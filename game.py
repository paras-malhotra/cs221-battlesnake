from __future__ import annotations
from typing import Dict, List, Optional, Tuple
import util

class GameState:
    def __init__(self, state: Dict) -> None:
        self.height = int(state['board']['height'])
        self.width = int(state['board']['width'])
        self.food = util.getCoordinates(state['board']['food'])
        self.hazards = util.getCoordinates(state['board']['hazards'])
        self.players: List[Player] = []
        self.endState = False
        self.won = False
        self.lost = False
        self.tie = False

        for snake in state['board']['snakes']:
            if state['you']['id'] == snake['id']:
                # make sure first player is us
                self.players.insert(0, Player(snake, True))
            else:
                self.players.append(Player(snake, False))
        
    def isEndState(self) -> bool:
        return self.endState
    
    def isWon(self) -> bool:
        return self.won
    
    def isLost(self) -> bool:
        return self.lost
    
    def isTie(self) -> bool:
        return self.tie
    
    def getLegalActions(self, playerIndex: int = 0) -> List[str]:
        if self.isWon() or self.isLost(): return []

        return GameRules.getLegalActions(self, playerIndex)
    
    def getAlivePlayers(self) -> List[Player]:
        return [player for player in self.players if player.alive]
    
    def accountForEndState(self) -> None:
        if self.endState:
            # already accounted for
            return
        if len(self.getAlivePlayers()) == 0:
            self.tie = True
            self.endState = True
        elif not self.players[0].ours or not self.players[0].alive:
            self.lost = True
            self.endState = True
        elif len(self.getAlivePlayers()) == 1:
            self.won = True
            self.endState = True
    
    def deepCopy(self) -> GameState:
        return GameState({
            'board': {
                'height': self.height,
                'width': self.width,
                'food': util.getDictCoordinates(self.food),
                'hazards': util.getDictCoordinates(self.hazards),
                'snakes': [{
                    'health': player.health,
                    'body': util.getDictCoordinates(player.body),
                    'length': player.length,
                    'id': player.id,
                    'alive': player.alive,
                } for player in self.players],
            },
            'you': {
                'id': self.players[0].id if len(self.players) > 0 and self.players[0].ours else None
            }
        })
    
    def generateSuccessor(self, action: Optional[str], playerIndex: int) -> GameState:
        nextState = self.deepCopy()

        if(len(nextState.getAlivePlayers()) <= 1):
            # game already over
            return nextState
        
        player = nextState.players[playerIndex]
        
        # if the player did an illegal move, eliminate the player
        if action is None or action not in GameRules.getLegalActions(nextState, playerIndex) or not player.alive:
            player.alive = False
        else:
            player.move(action, nextState.width, nextState.height, nextState.food, nextState.hazards)
            newx, newy = player.head
            playerHealth = player.health
            
            # check head to head collision elimination
            for i in range(len(nextState.players)):
                if i == playerIndex:
                    continue

                curPlayer = nextState.players[i]

                if not curPlayer.alive:
                    continue

                # Head to head collision
                if curPlayer.head == (newx, newy):
                    # Eliminate the player with lower health
                    if curPlayer.health < playerHealth and i < playerIndex:
                        # cur player already played move and is of lower health, so dies
                        curPlayer.alive = False
                        nextState.accountForEndState()
                        if nextState.endState:
                            break
                    else:
                        # either cur player is yet to play (head to body collision) or is higher health, so moving player dies
                        player.alive = False
                        break
                        

            # check food consumption
            if (newx, newy) in nextState.food:
                nextState.food.remove((newx, newy))

        # end state accounting
        nextState.accountForEndState()

        return nextState
    
    def getWalls(self) -> List[Tuple[int, int]]:
        walls = []
        for player in self.players:
            if not player.alive:
                continue
            walls = walls + player.futureBody()
        
        return walls
    
    def __repr__(self) -> str:
        return {
            'width': self.width,
            'height': self.height,
            'food': self.food,
            'hazards': self.hazards,
            'players': self.players.__str__(),
            'endState': self.endState,
            'won': self.won,
            'lost': self.lost,
            'tie': self.tie
        }.__str__()
    
class Player:
    MAX_HEALTH = 100
    MIN_LENGTH = 3
    HAZARD_DAMAGE = 15
    def __init__(self, player: Dict, ours: bool) -> None:
        self.health = int(player['health'])
        # take unique while preserving order
        self.body = list(dict.fromkeys(util.getCoordinates(player['body'])))
        self.head = self.body[0] if len(self.body) > 0 else None
        self.length = len(self.body)
        self.id = player['id']
        if 'alive' not in player:
            self.alive = True
        else:
            self.alive = player['alive']
        self.ours = bool(ours)

    def move(self, action: str, width: int, height: int, food: List[Tuple[int, int]], hazards: List[Tuple[int, int]]) -> None:
        if not self.alive:
            raise RuntimeError("Dead players cant move")

        newHead = Actions.getSuccessor(action, self, width, height)
        self.body.insert(0, newHead)
        if newHead in food:
            # increase health to max if food is consumed
            self.health = Player.MAX_HEALTH
        else:
            # truncate from tail if food not consumed
            if(len(self.body) > Player.MIN_LENGTH):
                del self.body[len(self.body) - 1]
            self.health = self.health - 1
        
        # account for hazards
        if newHead in hazards:
            self.health = self.health - Player.HAZARD_DAMAGE

        self.length = len(self.body)
        self.head = newHead

        if self.health <= 0:
            self.alive = False

    def futureBody(self) -> List[Tuple[int, int]]:
        if len(self.body) <= Player.MIN_LENGTH:
            return self.body
        else:
            return self.body[0:-1]
        
    def __repr__(self) -> str:
        return {
            'id': self.id,
            'health': self.health,
            'head': self.head,
            'body': self.body,
            'length': self.length,
            'alive': self.alive,
            'ours': self.ours
        }.__str__()

class GameRules:
    WRAPPED = False

    def getLegalActions(gameState: GameState, playerIndex: int) -> List[str]:
        return Actions.getPossibleActions(gameState.players, gameState.width, gameState.height, playerIndex)
    getLegalActions = staticmethod(getLegalActions)

class Directions:
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

class Actions:
    _directions = {
        Directions.UP: (0, 1),
        Directions.DOWN: (0, -1),
        Directions.LEFT: (-1, 0),
        Directions.RIGHT: (1, 0),
    }

    _directionsAsList = list(_directions.items())

    def vectorToDirection(vector: Tuple[int, int]) -> str:
        dx, dy = vector
        if dy > 0:
            return Directions.UP
        if dy < 0:
            return Directions.DOWN
        if dx < 0:
            return Directions.LEFT
        if dx > 0:
            return Directions.RIGHT
    vectorToDirection = staticmethod(vectorToDirection)

    def getPossibleActions(players: List[Player], width: int, height: int, index: int = 0) -> List[str]:
        possible = []
        x, y = players[index].head

        if not players[index].alive:
            return []

        for direction, vector in Actions._directionsAsList:
            dx, dy = vector
            nextx = (x + dx) % width
            nexty = (y + dy) % height

            for i in range(len(players)):
                if not players[i].alive:
                    continue
                if (nextx, nexty) in players[i].futureBody()[1:]:
                    # head to body collision
                    break
                # else:
                #     print(f"{(nextx, nexty)} not in {players[i].futureBody()[1:]}")
                if i >= index and (nextx, nexty) == players[i].head:
                    # head to body collision
                    break
                # else:
                #     print(f"{i} < {index} or  {(nextx, nexty)} not equal to {players[i].head}")
                if i < index and (nextx, nexty) == players[i].body[-1]:
                    # head to body collision
                    break
                # else:
                #     print(f"{i} >= {index} or {(nextx, nexty)} not equal to {players[i].body[-1]}")
                if i < index and (nextx, nexty) == players[i].head and players[index].health <= players[i].health:
                    # head to head collision with lower or equal health
                    # i < index is to determine players that have already moved and their head position is the "next" head
                    break
                if Actions.collidesWithBoundaries((x, y), vector, width, height):
                    # board boundaries for unwrapped games
                    break
                # else:
                #     print(f"{vector} vector does not collide for {(x, y)}")
            else:
                possible.append(direction)
        
        return possible
    getPossibleActions = staticmethod(getPossibleActions)

    def collidesWithBoundaries(position: Tuple[int, int], vector: Tuple[int, int], width: int, height: int) -> bool:
        x, y = position
        dx, dy = vector

        if not GameRules.WRAPPED and ((x + dx) >= width or (y + dy) >= height or (x + dx) < 0 or (y + dy) < 0):
            return True
        
        return False
    collidesWithBoundaries = staticmethod(collidesWithBoundaries)

    def getSuccessor(action: str, player: Player, width: int, height: int) -> Tuple[int, int]:
        if action not in Actions._directions:
            raise RuntimeError("Invalid action")
        
        dx, dy = Actions._directions[action]
        x, y = player.head

        if Actions.collidesWithBoundaries((x, y), (dx, dy), width, height):
            raise RuntimeError("Action collides with boundaries")
        
        return ((x + dx) % width, (y + dy) % height)
    getSuccessor = staticmethod(getSuccessor)