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



def start_game():

    mr_pacman = SearchAgent(fn=uniformCostSearch, prob=PositionSearchProblem)
    ghosts = [RandomGhost(1), RandomGhost(2)]  # controls the behavior of two ghosts
    gameDisplay = graphicsDisplay.PacmanGraphics(frameTime = 0.1) # initialize the display of the playing field
    lay = layout.getLayout('C:\Users\Bernhard\AppData\Local\Programs\Python\Python27\Lib\site-packages\pacman-0.1-py2.7.egg\pac\layouts\\tinyMaze')  # load the layout of the map

    game = rules.newGame(lay, mr_pacman, ghosts, gameDisplay, False, False)  # instantiate a Game instance, see below
    game.run()  # run the game, until Pacman is caught by a ghost or there is no food left

start_game()