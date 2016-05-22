import pac

from pac import util
from pac import search
from pac import layout
from pac import pacman
from math import fabs

from pac.searchAgents import SearchAgent
from pac.searchAgents import PositionSearchProblem
from pac.searchAgents import mazeDistance

from pac.game import Actions, Directions
from pac.pacman_utils import NotebookGraphics
from pac.util import Queue, Stack, PriorityQueue

from pac import graphicsDisplay


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())  # delete this later, otherwise the start state
                                                                                 # will count as expanded twice!
    print 'problem', problem


    from pac.game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [e, e, w, s, w, w, s, w]




def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    stack = Stack()

    visited = []
    parent_dict = dict()
    start_state = problem.getStartState()
    stack.push(start_state)
    current_path = []
    actions_dict = dict()
    final_actions = []
    flag = False

    if problem.isGoalState(problem.getStartState()):
        return []

    while not stack.isEmpty():
        current_state = stack.pop()
        current_path.append(current_state)
        visited.append(current_state)

        if problem.isGoalState(current_state):
            break

        successors = problem.getSuccessors(current_state)

        for s in successors:
            flag = False
            if s[0] not in visited:
                stack.push(s[0])
                parent_dict[s[0]] = current_state
                actions_dict[(current_state, s[0])] = s[1]
                flag = True



        if not successors and not stack.isEmpty() or flag is False:
            current_state = stack.pop()
            while current_path[-1] != parent_dict[current_state]:
                current_path.pop()
            stack.push(current_state)

    for i in range(len(current_path)-1):
       final_actions.append(actions_dict[current_path[i],current_path[i+1]])


    return final_actions

def start_game():
    rules = pacman.ClassicGameRules(timeout=0)
    rules = pac.pacman.ClassicGameRules(0)

    from pac.pacmanAgents import GreedyAgent
    mr_pacman = SearchAgent(fn=breadthFirstSearch, prob=PositionSearchProblem)


    from pac.ghostAgents import RandomGhost
    ghosts = [RandomGhost(1), RandomGhost(2)]  # controls the behavior of two ghosts

    #gameDisplay = NotebookGraphics(sleep_time = 0.2)  # initialize the display of the playing field
    gameDisplay =  graphicsDisplay.PacmanGraphics(frameTime = 0.1)

    lay = layout.getLayout('tinyMaze')

    game = rules.newGame(lay, mr_pacman, ghosts, gameDisplay, False, False)  # instantiate a Game instance, see below
    game.run()  # run the game, until Pacman is caught by a ghost or there is no food left



def breadthFirstSearch(problem):
    """
        Search the deepest nodes in the search tree first

        Your search algorithm needs to return a list of actions that reaches
        the goal.  Make sure to implement a graph search algorithm.

        To get started, you might want to try some of these simple commands to
        understand the search problem that is being passed in:
        """
    stack = Queue()

    visited = []
    parent_dict = dict()
    start_state = problem.getStartState()
    stack.push(start_state)
    actions_dict = dict()
    final_actions = []
    discovered = [problem.getStartState]

    if problem.isGoalState(problem.getStartState()):
        return []

    while not stack.isEmpty():
        current_state = stack.pop()
        visited.append(current_state)

        if problem.isGoalState(current_state):
            break

        successors = problem.getSuccessors(current_state)
        for s in successors:
            if s[0] not in visited and s[0] not in discovered:
                stack.push(s[0])
                parent_dict[s[0]] = current_state
                actions_dict[(current_state, s[0])] = s[1]
                discovered.append(s[0])

    while current_state is not start_state:
        parent = parent_dict[current_state]
        final_actions.append(actions_dict[parent, current_state])
        current_state = parent

    final_actions.reverse()
    return final_actions

def uniformCostSearch(problem):
        """
            Search the deepest nodes in the search tree first

            Your search algorithm needs to return a list of actions that reaches
            the goal.  Make sure to implement a graph search algorithm.

            To get started, you might want to try some of these simple commands to
            understand the search problem that is being passed in:
            """
        stack = PriorityQueue()

        visited = []
        parent_dict = dict()
        start_state = problem.getStartState()
        stack.push(start_state, 0)
        actions_dict = dict()
        final_actions = []
        discovered = [problem.getStartState]
        cost_dict = dict()
        cost_dict[start_state] = 0
        parent_dict[start_state] = (420,420)
        cost_dict[(420,420)] = 0

        if problem.isGoalState(problem.getStartState()):
            return []

        while not stack.isEmpty():
            current_state = stack.pop()

            if current_state not in visited:

                visited.append(current_state)

                if problem.isGoalState(current_state):
                    break
                successors = problem.getSuccessors(current_state)
                for s in successors:
                    if s[0] not in visited:
                        if s[0] not in cost_dict:
                            cost_dict[s[0]] = cost_dict[current_state] + s[2]
                            stack.push(s[0], cost_dict[s[0]]+1)
                            parent_dict[s[0]] = current_state
                            actions_dict[(current_state, s[0])] = s[1]
                            discovered.append(s[0])
                        elif cost_dict[current_state] + s[2] < cost_dict[s[0]]:
                            cost_dict[s[0]] = cost_dict[current_state] + s[2]
                            parent_dict[s[0]] = current_state
                            parent_dict[s[0]] = current_state
                            actions_dict[(current_state, s[0])] = s[1]

        while current_state is not start_state:
            parent = parent_dict[current_state]
            final_actions.append(actions_dict[parent, current_state])
            current_state = parent
        final_actions.reverse()

        return final_actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
        Search the deepest nodes in the search tree first

        Your search algorithm needs to return a list of actions that reaches
        the goal.  Make sure to implement a graph search algorithm.

        To get started, you might want to try some of these simple commands to
        understand the search problem that is being passed in:
        """
    stack = PriorityQueue()

    visited = []
    parent_dict = dict()
    start_state = problem.getStartState()
    stack.push(start_state, 0)
    actions_dict = dict()
    final_actions = []
    discovered = [problem.getStartState]
    cost_dict = dict()
    h_dict = dict()
    g_dict = dict()

    h_dict[start_state] = heuristic(start_state, problem)
    g_dict[start_state] = 0
    cost_dict[start_state] = 0
    parent_dict[start_state] = (420, 420)
    cost_dict[(420, 420)] = 0

    if problem.isGoalState(problem.getStartState()):
        return []

    while not stack.isEmpty():
        current_state = stack.pop()

        if current_state not in visited:

            visited.append(current_state)

            if problem.isGoalState(current_state):
                break
            successors = problem.getSuccessors(current_state)
            for s in successors:
                if s[0] not in visited:
                    if s[0] not in cost_dict:
                        h_dict[s[0]] = heuristic(s[0], problem)
                        g_dict[s[0]] = g_dict[current_state] + s[2]
                        cost_dict[s[0]] = g_dict[s[0]] + h_dict[s[0]]
                        stack.push(s[0], cost_dict[s[0]])
                        parent_dict[s[0]] = current_state
                        actions_dict[(current_state, s[0])] = s[1]
                        discovered.append(s[0])
                    elif heuristic(s[0],problem) + g_dict[current_state] + s[2] < cost_dict[s[0]]:
                        h_dict[s[0]] = heuristic(s[0], problem)
                        g_dict[s[0]] = g_dict[current_state] + s[2]
                        cost_dict[s[0]] = g_dict[s[0]] + h_dict[s[0]]
                        stack.push(s[0], cost_dict[s[0]])
                        parent_dict[s[0]] = current_state
                        actions_dict[(current_state, s[0])] = s[1]

    while current_state is not start_state:
        parent = parent_dict[current_state]
        final_actions.append(actions_dict[parent, current_state])
        current_state = parent

    final_actions.reverse()
    return final_actions

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
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print 'Warning: no food in corner ' + str(corner)
        self._expanded = 0 # Number of search nodes expanded
        self.visited_corner = (False, False, False, False)

        # Please add any code here which you would like to use
        # in initializing the problem

    def getStartState(self):
        "Returns the start state (in your state space, not the full Pacman state space)"
        tmp = (self.startingPosition, self.visited_corner)
        return tmp

    def isGoalState(self, state):
        tmp = list(state[1])

        for i in range(len(self.corners)):
            if state[0] == self.corners[i]:
                tmp[i] = True
        self.visited_corner = (tmp[0], tmp[1], tmp[2], tmp[3])
        return self.visited_corner == (True, True, True, True)

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            # Add a successor state to the successor list if the action is legal
            # Here's a code snippet for figuring out whether a new position hits a wall:
             x, y = state[0]
             dx, dy = Actions.directionToVector(action)
             nextx, nexty = int(x + dx), int(y + dy)
             hitsWall = self.walls[nextx][nexty]

             if not hitsWall:
                successors.append((((nextx,nexty), self.visited_corner), action, 1))
                "*** YOUR CODE HERE ***"

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x,y= self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)

def start_corner_problem():
    tiny_corner_layout = layout.getLayout('tinyCorners')
    medium_corner_layout = layout.getLayout('mediumCorners')
    rules = pac.pacman.ClassicGameRules(0)
    sa = SearchAgent(fn=breadthFirstSearch, prob=CornersProblem)
    gameDisplay = graphicsDisplay.PacmanGraphics(frameTime = 0.1)  # visualization
    game = rules.newGame(tiny_corner_layout, sa, [], gameDisplay, False, False)
    game.run()

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
    corners = problem.corners # These are the corner coordinates
    walls = problem.walls # These are the walls of the maze, as a Grid (game.py)
    distance = []
    for i in range(len(corners)):
        distance.append(fabs((corners[i][0] - state[0][0]) + (corners[i][1] - state[0][1])))
    "*** YOUR CODE HERE ***"
    return min(distance)  # Default to trivial solution

class AStarCornersAgent(SearchAgent):
    """A SearchAgent for CornersProblem using A* and your cornersHeuristic

    No need to change anything here.
    """
    def __init__(self):
        self.searchFunction = lambda prob: aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem


def start_corner_problem_astar():
    tiny_corner_layout = layout.getLayout('tinyCorners')
    medium_corner_layout = layout.getLayout('mediumCorners')
    big_corner_layout = layout.getLayout('bigCorners')

    gameState = pacman.GameState()
    gameState.initialize(medium_corner_layout, 0)

    problem = CornersProblem(gameState)

    rules = pac.pacman.ClassicGameRules(0)
    sa = AStarCornersAgent()
    gameDisplay = graphicsDisplay.PacmanGraphics(frameTime = 0.1)  # visualization
    game = rules.newGame(layout.getLayout('mediumCorners'), sa, [], gameDisplay, False, False)
    game.run()



def createHGrid(state, problem):
    position, foodGrid = state
    food_list = foodGrid.asList()
    wall_list = problem.walls.asList()
    q = Queue()
    parent_dict = dict()
    h_dict = dict()


    for food in food_list:
        q.push(food)
        visited = []
        h_dict[food] = dict()
        h_dict[food][food] = 0
        visited.append(food)
        parent_dict.clear()
        parent_dict[food] = 420
        h_dict[food][420] = 0

        while not q.isEmpty():
            s = q.pop()
            cost = h_dict[food][s] + 1
            x = s[0]
            y = s[1]
            for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:

                dx, dy = Actions.directionToVector(action)
                nextx, nexty = int(x + dx), int(y + dy)

                if not ((nextx, nexty) in wall_list) and not ((nextx, nexty) in visited):
                    visited.append((nextx, nexty))
                    h_dict[food][(nextx, nexty)] = cost
                    q.push((nextx, nexty))
                    parent_dict[(nextx, nexty)] = s

    return h_dict



def foodHeuristic(state, problem):


    position, foodGrid = state
    "*** YOUR CODE HERE ***"
    food_list = foodGrid.asList()
    wall_list = problem.walls.asList()

    if not problem._expanded:
        problem.heuristicInfo['HGrid'] = createHGrid(state, problem)



    cost_list = []

    for food in food_list:
        cost_list.append(problem.heuristicInfo['HGrid'][food][state[0]])

    if not cost_list:
        return 0

    return max(cost_list)  # Default to trivial solution

"""
def foodHeuristic(state, problem):


    position, foodGrid = state
    "*** YOUR CODE HERE ***"
    food_list = foodGrid.asList()
    wall_list = problem.walls.asList()

    distance = []
    for i in range(len(food_list)):
        distance.append(fabs((food_list[i][0] - state[0][0]) + (food_list[i][1] - state[0][1])))
    "*** YOUR CODE HERE ***"
    if not len(distance):
        return 0
    return max(distance)  # Default to trivial solution


"""
"""
def foodHeuristic(state, problem):

    position, foodGrid = state


    food_list = foodGrid.asList()


    cost = 0
    for food in food_list:
        cost = max(cost, fabs(position[0] - food[0]) + fabs(position[1] - food[1]))

    return cost  # Default to trivial solution
"""

class AStarFoodSearchAgent(SearchAgent):
    """A SearchAgent for FoodSearchProblem using A* and your foodHeuristic

    No need to change anything here.
    """
    def __init__(self):
        self.searchFunction = lambda prob: aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem

class FoodSearchProblem:
    """
    A search problem associated with finding a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see pac.game module) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost


def start_eating_dots():


    rules = pac.pacman.ClassicGameRules(0)
    sa = AStarFoodSearchAgent()
    gameDisplay = graphicsDisplay.PacmanGraphics(frameTime = 0.1)  # visualization
    game = rules.newGame(layout.getLayout('trickySearch'), sa, [], gameDisplay, False, False)
    game.run()

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
        # type: (object) -> object
        "Returns a path (a list of actions) to the closest dot, starting from gameState"
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        food_list = food.asList()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)
        return breadthFirstSearch(problem)


class AnyFoodSearchProblem(PositionSearchProblem):
    """
      A search problem for finding a path to any food.

      This search problem is just like the PositionSearchProblem, but
      has a different goal test, which you need to fill in below.  The
      state space and successor function do not need to be changed.

      The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
      inherits the methods of the PositionSearchProblem.

      You can use this search problem to help you fill in
      the findPathToClosestDot method.
    """

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
        x, y = state
        if state in self.food.asList():
            return True



def start_eating_closest_dot():


    rules = pac.pacman.ClassicGameRules(0)
    sa = ClosestDotSearchAgent()
    gameDisplay = graphicsDisplay.PacmanGraphics(frameTime = 0.1)  # visualization
    game = rules.newGame(layout.getLayout('bigSearch'), sa, [], gameDisplay, False, False)
    game.run()

start_eating_closest_dot()