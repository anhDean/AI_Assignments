import pac

from pac import util
from pac import search
from pac import layout
from pac import pacman
from pac.pacmanAgents import GreedyAgent
from pac.ghostAgents import RandomGhost
from pac.searchAgents import SearchAgent
from pac.searchAgents import PositionSearchProblem
from pac.game import Actions, Directions
from pac.pacman_utils import NotebookGraphics
rules = pacman.ClassicGameRules(timeout=0)
from pac.util import Queue, Stack, PriorityQueue
from pac import graphicsDisplay

rules = pacman.ClassicGameRules(0)

def depthFirstSearch(problem):

    Q = Stack()

    actions = {}        # (parent)(child):(action)
    parents = {}        # (child):(parent)
    visited = []        # states visited
    discovered = []     # states discovered
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
            if u[0] in discovered and u[0] not in visited:          #parent update
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

    actions = {}        # (parent)(child):(action)
    parents = {}        # (child):(parent)
    visited = []        # states visited
    discovered = []     # states discovered
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
    costs = {}      #(node):cost
    parents = {}    #(child):(parent)
    actions = {}    #(parent),(child):(action)
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
        discovered.remove(current_state) #swaps from discovered to visited

        if problem.isGoalState(current_state):
            goal_state = current_state
            break

        successors = problem.getSuccessors(current_state)

        for n in successors:
            if n[0] not in visited and n[0] not in discovered:
                discovered.append(n[0])
                parents[n[0]] = current_state
                actions[(current_state,n[0])] = n[1]
                costs[n[0]] = n[2] + costs[current_state]
                Q.push(n[0], costs[n[0]])
            if n[0] in discovered:
                current_cost = costs[n[0]]
                new_cost = costs[current_state]+n[2]
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
                        h_costs[u[0]] = heuristic(u[0],problem)
                        g_costs[u[0]] = g_costs[current_state] + u[2]
                        costs[u[0]] = g_costs[u[0]] + h_costs[u[0]]
                        Q.push(u[0], costs[u[0]])
                        parents[u[0]] = current_state
                        actions[(current_state,u[0])] = u[1]
                    elif u[0] in discovered and heuristic(u[0],problem) + g_costs[current_state] + u[2] < costs[u[0]]:
                        h_costs[u[0]] = heuristic(u[0],problem)
                        g_costs[u[0]] = g_costs[current_state]+u[2]
                        costs[u[0]] = h_costs[u[0]] + g_costs[u[0]]
                        parents[u[0]] = current_state
                        actions[(current_state,u[0])] = u[1]
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
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        self.visitedCorners = (False, False, False, False)
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print 'Warning: no food in corner ' + str(corner)
        self._expanded = 0 # Number of search nodes expanded
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

        for c in range(len(self.corners)):   # check all 4 corners
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
        x,y= self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)



def start_corner_problem():
    tiny_corner_layout = layout.getLayout('C:\Users\Bernhard\AppData\Local\Programs\Python\Python27\Lib\site-packages\pacman-0.1-py2.7.egg\pac\layouts\\tinyCorners')  # load the layout of the map
    medium_corner_layout = layout.getLayout('C:\Users\Bernhard\AppData\Local\Programs\Python\Python27\Lib\site-packages\pacman-0.1-py2.7.egg\pac\layouts\mediumCorners')  # load the layout of the map
    rules = pac.pacman.ClassicGameRules(0)
    sa = SearchAgent(fn=breadthFirstSearch, prob=CornersProblem)
    gameDisplay = graphicsDisplay.PacmanGraphics(frameTime = 0.1)  # visualization
    game = rules.newGame(tiny_corner_layout, sa, [], gameDisplay, False, False)
    game.run()



def start_game():

    mr_pacman = SearchAgent(fn=aStarSearch, prob=PositionSearchProblem)
    ghosts = [RandomGhost(1), RandomGhost(2)]  # controls the behavior of two ghosts
    gameDisplay = graphicsDisplay.PacmanGraphics(frameTime = 0.1) # initialize the display of the playing field
    lay = layout.getLayout('C:\Users\Bernhard\AppData\Local\Programs\Python\Python27\Lib\site-packages\pacman-0.1-py2.7.egg\pac\layouts\\tinyCorners')  # load the layout of the map

    game = rules.newGame(lay, mr_pacman, ghosts, gameDisplay, False, False)  # instantiate a Game instance, see below
    game.run()  # run the game, until Pacman is caught by a ghost or there is no food left

start_corner_problem()