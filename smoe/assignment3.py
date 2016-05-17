import pac

from pac import util
from pac import search
from pac import layout
from pac import pacman

from pac.searchAgents import SearchAgent
from pac.searchAgents import PositionSearchProblem

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
    mr_pacman = SearchAgent(fn=aStarSearch, prob=PositionSearchProblem)


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
        print final_actions

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
                        cost_dict[s[0]] = (cost_dict[current_state] - heuristic(parent_dict[current_state],problem))+ s[2] + heuristic(s[0], problem)
                        stack.push(s[0], cost_dict[s[0]])
                        parent_dict[s[0]] = current_state
                        actions_dict[(current_state, s[0])] = s[1]
                        discovered.append(s[0])
                    elif (cost_dict[current_state] - heuristic(parent_dict[current_state],problem))+ s[2] + heuristic(s[0], problem) < cost_dict[s[0]]:
                        cost_dict[s[0]] = (cost_dict[current_state] - heuristic(parent_dict[current_state],problem))+ s[2] + heuristic(s[0], problem)
                        stack.push(s[0], cost_dict[s[0]])
                        parent_dict[s[0]] = current_state
                        actions_dict[(current_state, s[0])] = s[1]

    while current_state is not start_state:
        parent = parent_dict[current_state]
        final_actions.append(actions_dict[parent, current_state])
        current_state = parent

    final_actions.reverse()

    return final_actions

start_game()


