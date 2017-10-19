# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #return successorGameState.getScore()

        maxManhattanDist = successorGameState.getWalls().width + successorGameState.getWalls().height

        # find the distance of the nearest ghost
        minDistGhost = maxManhattanDist
        for ghostState in newGhostStates:
            dist2Ghost = manhattanDistance(newPos, ghostState.getPosition())
            if dist2Ghost < minDistGhost:
                minDistGhost = dist2Ghost

        # find the distance of the nearst food
        minDistFoodCur = maxManhattanDist
        minDistFoodNew = maxManhattanDist
        curPos = currentGameState.getPacmanPosition()
        curFood = currentGameState.getFood()
        for fd in curFood.asList():
            dist2FoodCur = manhattanDistance(curPos, fd)
            dist2FoodNew = manhattanDistance(newPos, fd)
            if dist2FoodCur < minDistFoodCur:
                minDistFoodCur = dist2FoodCur
            if dist2FoodNew < minDistFoodNew:
                minDistFoodNew = dist2FoodNew

        ### choice a ratio between food and ghost
        # alway not go to corner if there is no food
        if len(successorGameState.getLegalActions()) <= 2 and not curFood[newPos[0]][newPos[1]]:
            return -maxManhattanDist - 1
        if minDistGhost <= 1:
            return -maxManhattanDist
        # if minDistGhost <= 2:
        #     return minDistGhost + 0.25 * len(successorGameState.getLegalActions())
        # if there is food at newPos
        if curFood[newPos[0]][newPos[1]]:
            return maxManhattanDist
        # keep moving maybe good
        if action is Directions.STOP:
            return -maxManhattanDist + 1
        # if minDistFoodCur == minDistFoodNew and minDistFoodNew != 1:
        #     return -maxManhattanDist + 1
        return -minDistFoodNew + 0.5 * len(successorGameState.getLegalActions()) + 0.2 * minDistGhost

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # rootValue = self.value(gameState, 0, self.index)
        # action = rootValue[1]
        # return action
        return self.value(gameState, 0, self.index)[1]

    def value(self, gameState, curDepth, agentIndex):
        """
          call maxValue or minValue
          return (value, action)
        """

        if agentIndex == gameState.getNumAgents():
            curDepth += 1
            agentIndex = 0

        legalMoves = gameState.getLegalActions(agentIndex)
        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)

        if len(legalMoves) == 0:
            return (self.evaluationFunction(gameState), None)

        if curDepth == self.depth:
            return (self.evaluationFunction(gameState), None)

        if agentIndex == 0:
            return self.maxValue(gameState, curDepth, agentIndex)
        else:
            return self.minValue(gameState, curDepth, agentIndex)

    def maxValue(self, gameState, curDepth, agentIndex):

        legalMoves = gameState.getLegalActions(agentIndex)
        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)

        # scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # bestScore = max(scores)
        # bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # chosenIndex = random.choice(bestIndices)
        # return [bestScore, legalMoves[chosenIndex]]

        theValue = -9999999
        theAction = legalMoves[0]

        for action in legalMoves:
            nextState = gameState.generateSuccessor(agentIndex, action)
            evaluationValue = self.value(nextState, curDepth, agentIndex + 1)[0]

            if evaluationValue >= theValue:
                theValue = evaluationValue
                theAction = action

        return (theValue, theAction)

    def minValue(self, gameState, curDepth, agentIndex):

        legalMoves = gameState.getLegalActions(agentIndex)
        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)

        scores = [self.value(gameState.generateSuccessor(agentIndex, action), curDepth, agentIndex + 1)[0] for action in legalMoves]
        worstScore = min(scores)
        # bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # chosenIndex = random.choice(bestIndices)
        return (worstScore, None)

        # theValue = 9999999
        # theAction = legalMoves[0]

        # for action in legalMoves:
        #     nextState = gameState.generateSuccessor(agentIndex, action)
        #     evaluationValue = self.value(nextState, curDepth, agentIndex + 1)[0]

        #     if evaluationValue <= theValue:
        #         theValue = evaluationValue
        #         theAction = action

        # return (theValue, theAction)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # rootValue = self.value(gameState, 0, self.index, -9999999 , 9999999)
        # action = rootValue[1]
        # return action
        return self.value(gameState, 0, self.index, -9999999 , 9999999)[1]

    def value(self, gameState, curDepth, agentIndex, alpha, beta):

        if agentIndex == gameState.getNumAgents():
            curDepth += 1
            agentIndex = 0

        legalMoves = gameState.getLegalActions(agentIndex)
        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)

        if len(legalMoves) == 0:
            return (self.evaluationFunction(gameState), None)

        if curDepth == self.depth:
            return (self.evaluationFunction(gameState), None)

        if agentIndex == 0:
            return self.maxValue(gameState, curDepth, agentIndex, alpha, beta)
        else:
            return self.minValue(gameState, curDepth, agentIndex, alpha, beta)

    def maxValue(self, gameState, curDepth, agentIndex, alpha, beta):

        legalMoves = gameState.getLegalActions(agentIndex)
        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)

        theValue = -9999999
        theAction = legalMoves[0]

        for action in legalMoves:
            nextState = gameState.generateSuccessor(agentIndex, action)
            evaluationValue = self.value(nextState, curDepth, agentIndex + 1, alpha, beta)[0]

            if evaluationValue >= theValue:
                theValue = evaluationValue
                theAction = action

            if theValue > alpha:
                alpha = theValue

            if theValue > beta:
                return (theValue, theAction)

        return (theValue, theAction)

    def minValue(self, gameState, curDepth, agentIndex, alpha, beta):

        legalMoves = gameState.getLegalActions(agentIndex)
        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)

        theValue = 9999999
        theAction = legalMoves[0]

        for action in legalMoves:
            nextState = gameState.generateSuccessor(agentIndex, action)
            evaluationValue = self.value(nextState, curDepth, agentIndex + 1, alpha, beta)[0]

            if evaluationValue <= theValue:
                theValue = evaluationValue
                theAction = action

            if theValue < beta:
                beta = theValue

            if theValue < alpha:
                return (theValue, theAction)

        return (theValue, theAction)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # rootValue = self.value(gameState, 0, self.index)
        # action = rootValue[1]
        # return action
        return self.value(gameState, 0, self.index)[1]

    def value(self, gameState, curDepth, agentIndex):
        """
        call maxValue or minValue
        return (value, action)
        """

        if agentIndex == gameState.getNumAgents():
            curDepth += 1
            agentIndex = 0

        legalMoves = gameState.getLegalActions(agentIndex)
        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)

        if len(legalMoves) == 0:
            return (self.evaluationFunction(gameState), None)

        if curDepth == self.depth:
            return (self.evaluationFunction(gameState), None)

        if agentIndex == 0:
            return self.maxValue(gameState, curDepth, agentIndex)
        else:
            return self.expValue(gameState, curDepth, agentIndex)

    def maxValue(self, gameState, curDepth, agentIndex):

        legalMoves = gameState.getLegalActions(agentIndex)
        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)

        theValue = -9999999
        theAction = legalMoves[0]

        for action in legalMoves:
            nextState = gameState.generateSuccessor(agentIndex, action)
            evaluationValue = self.value(nextState, curDepth, agentIndex + 1)[0]

            if evaluationValue >= theValue:
                theValue = evaluationValue
                theAction = action

        return (theValue, theAction)

    def expValue(self, gameState, curDepth, agentIndex):

        legalMoves = gameState.getLegalActions(agentIndex)
        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)

        scores = [self.value(gameState.generateSuccessor(agentIndex, action), curDepth, agentIndex + 1)[0] for action in legalMoves]

        theValue = 1.0 * sum(scores) / len(scores)
        theAction = None

        # closestNum = 9999999
        # keyIndex = 0
        # for index in range(len(scores)):
        #     temp = abs(scores[index] - theValue)
        #     if  temp < closestNum:
        #         closestNum = temp
        #         keyIndex = index
        # theAction = legalMoves[keyIndex]

        return (theValue, theAction)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

    position = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    scaredGhosts = [ghost for ghost in ghostStates if ghost.scaredTimer > 0] 
    normalGhosts = [ghost for ghost in ghostStates if ghost.scaredTimer == 0]

    nearestScaredGhost = min([manhattanDistance(position, ghost.getPosition()) for ghost in scaredGhosts]) if scaredGhosts else 0
    nearestNormalGhost = min([manhattanDistance(position, ghost.getPosition()) for ghost in normalGhosts]) if normalGhosts else 0
    nearestCapsule = min([manhattanDistance(position, cap) for cap in capsules]) if capsules else 0
    nearestFood = min([manhattanDistance(position, food) for food in foodList]) if foodList else 0

    # runaway from normal ghost
    # if nearestNormalGhost <= 1:
    #     return -99999999
    # scaredGhost > capsule > food
    # if nearestScaredGhost == 1:
    #     return 99999999
    # if nearestCapsule == 1:
    #     return 99999999 - 100000
    # if nearestFood == 1:
    #    return 99999999 - 200000

    # maxManhattanDist = currentGameState.getWalls().width + currentGameState.getWalls().height

    # if scaredGhosts:
    #     return 5 * (maxManhattanDist - 1.0 * nearestScaredGhost) + 1.0 * nearestNormalGhost - 100 * len(scaredGhosts)
    # if capsules:
    #     return 5 * (maxManhattanDist -1.0 * nearestCapsule) + 1.0 * nearestNormalGhost - 100 * len(capsules)

    # return 0
    # return -1 * nearestScaredGhost - 2 * nearestCapsule - 10 * nearestFood - 100 * len(foodList) + 0.5 * nearestNormalGhost

    WEIGHT_NORMAL_GHOST = 10.0
    WEIGHT_SCARED_GHOST = 100.0
    WEIGHT_FOOD = 10.0
    WEIGHT_CAPSULE = 30.0

    score = currentGameState.getScore()

    if scaredGhosts and nearestScaredGhost > 0:
        score += WEIGHT_SCARED_GHOST / nearestScaredGhost
    if normalGhosts and nearestNormalGhost > 0:
        score -= WEIGHT_NORMAL_GHOST / nearestNormalGhost
    if capsules:
        score += WEIGHT_CAPSULE / nearestCapsule
    if foodList:
        score += WEIGHT_FOOD / nearestFood

    return score

# Abbreviation
better = betterEvaluationFunction

