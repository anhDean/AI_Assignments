import pac

from pac import util
from pac import search
from pac import layout
from pac import pacman
from math import fabs

from pac.ghostAgents import RandomGhost
from pac.searchAgents import SearchAgent
from pac.searchAgents import PositionSearchProblem
from pac.game import Actions, Directions
from pac.util import Queue, Stack, PriorityQueue
from pac import graphicsDisplay

rules = pacman.ClassicGameRules(0)


def depthFirstSearch(problem):
    Q = Stack()

    actions = {}  # (parent)(child):(action)
    parents = {}  # (child):(parent)
    visited = []  # states visited
    discovered = []  # states discovered
    goal_state = []
    path = []
    init_state = problem.getStartState()
    Q.push(init_state)

    while not Q.isEmpty():
        current_state = Q.pop()
        visited.append(current_state)

        if problem.isGoalState(current_state):
            goal_state = current_state
            break

        successors = problem.getSuccessors(current_state)
        for u in successors:
            if u[0] not in visited and u[0] not in discovered:
                Q.push(u[0])
                discovered.append(u[0])
                parents[u[0]] = current_state
                actions[(current_state, u[0])] = u[1]
            if u[0] in discovered and u[0] not in visited:  # parent update
                parents[u[0]] = current_state
                actions[(current_state, u[0])] = u[1]

    parent = goal_state
    while parent is not init_state:
        child = parent
        parent = parents[child]
        action = actions[(parent, child)]
        path.append(action)

    path.reverse()
    return path


def breadthFirstSearch(problem):
    Q = Queue()

    actions = {}  # (parent)(child):(action)
    parents = {}  # (child):(parent)
    visited = []  # states visited
    discovered = []  # states discovered
    goal_state = []
    path = []
    init_state = problem.getStartState()
    Q.push(init_state)

    while not Q.isEmpty():
        current_state = Q.pop()
        visited.append(current_state)

        if problem.isGoalState(current_state):
            goal_state = current_state
            break

        successors = problem.getSuccessors(current_state)
        for u in successors:
            if u[0] not in visited and u[0] not in discovered:
                Q.push(u[0])
                discovered.append(u[0])
                parents[u[0]] = current_state
                actions[(current_state, u[0])] = u[1]

    parent = goal_state
    while parent is not init_state:
        child = parent
        parent = parents[child]
        action = actions[(parent, child)]
        path.append(action)

    path.reverse()
    return path


def uniformCostSearch(problem):
    Q = PriorityQueue()
    costs = {}  # (node):cost
    parents = {}  # (child):(parent)
    actions = {}  # (parent),(child):(action)
    visited = []
    discovered = []
    goal_state = []
    path = []
    init_state = problem.getStartState()
    discovered.append(init_state)
    costs[init_state] = 0
    Q.push(init_state, 0)

    while not Q.isEmpty():
        current_state = Q.pop()
        visited.append(current_state)
        discovered.remove(current_state)  # swaps from discovered to visited

        if problem.isGoalState(current_state):
            goal_state = current_state
            break

        successors = problem.getSuccessors(current_state)

        for n in successors:
            if n[0] not in visited and n[0] not in discovered:
                discovered.append(n[0])
                parents[n[0]] = current_state
                actions[(current_state, n[0])] = n[1]
                costs[n[0]] = n[2] + costs[current_state]
                Q.push(n[0], costs[n[0]])
            if n[0] in discovered:
                current_cost = costs[n[0]]
                new_cost = costs[current_state] + n[2]
                if new_cost < current_cost:
                    parents[n[0]] = current_state
                    actions[(current_state, n[0])] = n[1]
                    costs[n[0]] = new_cost

    parent = goal_state
    while parent is not init_state:
        child = parent
        parent = parents[child]
        action = actions[(parent, child)]
        path.append(action)

    path.reverse()
    return path


def nullHeuristic(state, problem=None):
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    Q = PriorityQueue()
    visited = []
    discovered = []
    goal_state = []
    path = []
    parents = {}
    actions = {}
    h_costs = {}
    g_costs = {}
    costs = {}
    init_state = problem.getStartState()
    h_costs[init_state] = heuristic(init_state, problem)
    g_costs[init_state] = 0
    costs[init_state] = 0
    Q.push(init_state, 0)
    discovered.append(init_state)

    if problem.isGoalState(init_state):
        return []

    while not Q.isEmpty():
        current_state = Q.pop()
        if current_state not in visited:
            visited.append(current_state)
            discovered.remove(current_state)

            if problem.isGoalState(current_state):
                goal_state = current_state
                break

            successors = problem.getSuccessors(current_state)

            for u in successors:
                if u[0] not in visited:
                    if u[0] not in discovered:
                        discovered.append(u[0])
                        h_costs[u[0]] = heuristic(u[0], problem)
                        g_costs[u[0]] = g_costs[current_state] + u[2]
                        costs[u[0]] = g_costs[u[0]] + h_costs[u[0]]
                        Q.push(u[0], costs[u[0]])
                        parents[u[0]] = current_state
                        actions[(current_state, u[0])] = u[1]
                    elif u[0] in discovered and heuristic(u[0], problem) + g_costs[current_state] + u[2] < costs[u[0]]:
                        h_costs[u[0]] = heuristic(u[0], problem)
                        g_costs[u[0]] = g_costs[current_state] + u[2]
                        costs[u[0]] = h_costs[u[0]] + g_costs[u[0]]
                        parents[u[0]] = current_state
                        actions[(current_state, u[0])] = u[1]
                        Q.push(u[0], costs[u[0]])

    parent = goal_state
    while parent is not init_state:
        child = parent
        parent = parents[child]
        action = actions[(parent, child)]
        path.append(action)

    path.reverse()
    return path


class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function.
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height - 2, self.walls.width - 2
        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        self.visitedCorners = (False, False, False, False)
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print 'Warning: no food in corner ' + str(corner)
        self._expanded = 0  # Number of search nodes expanded
        # Please add any code here which you would like to use
        # in initializing the problem

    def getStartState(self):
        "Returns the start state (in your state space, not the full Pacman state space)"
        start = self.startingPosition
        visited = self.visitedCorners
        state = (start, visited)
        return state

    def isGoalState(self, state):
        "Returns whether this search state is a goal state of the problem"
        check = list(state[1])

        for c in range(len(self.corners)):  # check all 4 corners
            if state[0] == self.corners[c]:
                check[c] = True
        self.visitedCorners = tuple(check)
        if all(self.visitedCorners):
            return True
        else:
            return False

    def getSuccessors(self, state):
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            # Add a successor state to the successor list if the action is legal
            # Here's a code snippet for figuring out whether a new position hits a wall:
            x, y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]
            if not hitsWall:
                successors.append((((nextx, nexty), self.visitedCorners), action, 1))

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem; i.e.
    it should be admissible (as well as consistent).
    """
    corners = problem.corners  # These are the corner coordinates
    walls = problem.walls  # These are the walls of the maze, as a Grid (game.py)
    pos = state[0]
    distances = []
    for corner in corners:
        manhatten = abs((pos[0] - corner[0]) + (pos[1] - corner[1]))
        distances.append(manhatten)

    h_value = min(distances)
    return h_value


class AStarCornersAgent(SearchAgent):
    """A SearchAgent for CornersProblem using A* and your cornersHeuristic
    No need to change anything here.
    """

    def __init__(self):
        self.searchFunction = lambda prob: aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem


class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """

    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0
        self.heuristicInfo = {}  # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append((((nextx, nexty), nextFood), direction, 1))
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x, y = self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost


class AStarFoodSearchAgent(SearchAgent):
    """A SearchAgent for FoodSearchProblem using A* and your foodHeuristic

    No need to change anything here.
    """

    def __init__(self):
        self.searchFunction = lambda prob: aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem



def realDist(point1, point2, gameState):
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.breadthFirstSearch(prob))

def foodHeuristic(state, problem):

    position, foodGrid = state
    foodCoordinates = foodGrid.asList()
    foodCosts = {}
    remainingFoodDists = []

    if len(foodCoordinates) == 0:   # trivial case
        return 0

    if 'h_costs' not in problem.heuristicInfo.keys():
        problem.heuristicInfo['h_costs'] = {}

    if position not in problem.heuristicInfo['h_costs'].keys():
        foodDistances = [realDist(position, food, problem.startingGameState) for food in foodCoordinates]
        for i in range(len(foodCoordinates)):
            foodCosts[foodCoordinates[i]] = foodDistances[i]
        problem.heuristicInfo['h_costs'][position] = foodCosts

    for i in problem.heuristicInfo['h_costs'][position].keys():
        if i in foodCoordinates:
            remainingFoodDists.append(problem.heuristicInfo['h_costs'][position][i])

    return max(remainingFoodDists)







class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches"
    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception, 'findPathToClosestDot returned an illegal move: %s!\n%s' % t
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print 'Path found with cost %d.' % len(self.actions)

    def findPathToClosestDot(self, gameState):
        "Returns a path (a list of actions) to the closest dot, starting from gameState"
        # Here are some useful elements of the startState
        problem = AnyFoodSearchProblem(gameState)
        return breadthFirstSearch(problem)

class AnyFoodSearchProblem(PositionSearchProblem):


    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test
        that will complete the problem definition.
        """
        if state in self.food.asList(): # pacman is on food position
            return True
        else:
            return False



def start_corner_problem_astar():
    tiny_corner_layout = layout.getLayout(
        'C:\Users\Bernhard\AppData\Local\Programs\Python\Python27\Lib\site-packages\pacman-0.1-py2.7.egg\pac\layouts\\tinyCorners')  # load the layout of the map
    medium_corner_layout = layout.getLayout(
        'C:\Users\Bernhard\AppData\Local\Programs\Python\Python27\Lib\site-packages\pacman-0.1-py2.7.egg\pac\layouts\mediumCorners')  # load the layout of the map
    gameState = pacman.GameState()
    gameState.initialize(medium_corner_layout, 0)

    problem = CornersProblem(gameState)

    rules = pac.pacman.ClassicGameRules(0)
    sa = AStarCornersAgent()
    gameDisplay = graphicsDisplay.PacmanGraphics(frameTime=0.1)  # visualization
    game = rules.newGame(medium_corner_layout, sa, [], gameDisplay, False, False)
    game.run()

def start_corner_problem():
    tiny_corner_layout = layout.getLayout(
        'C:\Users\Bernhard\AppData\Local\Programs\Python\Python27\Lib\site-packages\pacman-0.1-py2.7.egg\pac\layouts\\tinyCorners')  # load the layout of the map
    medium_corner_layout = layout.getLayout(
        'C:\Users\Bernhard\AppData\Local\Programs\Python\Python27\Lib\site-packages\pacman-0.1-py2.7.egg\pac\layouts\mediumCorners')  # load the layout of the map
    rules = pac.pacman.ClassicGameRules(0)
    sa = SearchAgent(fn=breadthFirstSearch, prob=CornersProblem)
    gameDisplay = graphicsDisplay.PacmanGraphics(frameTime=0.1)  # visualization
    game = rules.newGame(medium_corner_layout, sa, [], gameDisplay, False, False)
    game.run()


def start_game():
    mr_pacman = SearchAgent(fn=aStarSearch, prob=PositionSearchProblem)
    ghosts = [RandomGhost(1), RandomGhost(2)]  # controls the behavior of two ghosts
    gameDisplay = graphicsDisplay.PacmanGraphics(frameTime=0.1)  # initialize the display of the playing field
    lay = layout.getLayout(
        'C:\Users\Bernhard\AppData\Local\Programs\Python\Python27\Lib\site-packages\pacman-0.1-py2.7.egg\pac\layouts\mediumMaze')  # load the layout of the map

    game = rules.newGame(lay, mr_pacman, ghosts, gameDisplay, False, False)  # instantiate a Game instance, see below
    game.run()  # run the game, until Pacman is caught by a ghost or there is no food left


def start_eating_dots():
    rules = pac.pacman.ClassicGameRules(0)
    sa = AStarFoodSearchAgent()
    gameDisplay = graphicsDisplay.PacmanGraphics(frameTime=0.1)  # visualization
    game = rules.newGame(layout.getLayout(
        'C:\Users\Bernhard\AppData\Local\Programs\Python\Python27\Lib\site-packages\pacman-0.1-py2.7.egg\pac\layouts\\trickySearch'),
                         sa, [], gameDisplay, False, False)
    game.run()

def start_eating_closest_dot():

    rules = pac.pacman.ClassicGameRules(0)
    sa = ClosestDotSearchAgent()
    gameDisplay = graphicsDisplay.PacmanGraphics(frameTime = 0.1)  # visualization
    game = rules.newGame(layout.getLayout('C:\Users\Bernhard\AppData\Local\Programs\Python\Python27\Lib\site-packages\pacman-0.1-py2.7.egg\pac\layouts\\bigSearch'),
                         sa, [], gameDisplay, False, False)
    game.run()

start_eating_closest_dot()
