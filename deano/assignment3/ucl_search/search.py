# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import Stack, Queue, PriorityQueue

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):

    successor_idx = {'dir': 1, 'state': 0, 'cost': -1}

    MAX_ITER = int(20000)
    stateStack = Stack()
    visitedSet = set()
    actionList = [] # add actions to get to the state, use pop to remove last one
    successorDict = {}

    curState = problem.getStartState()
    stateStack.push(curState)
   
    for it in range(MAX_ITER):

        if problem.isGoalState(curState):
            return actionList

        if curState not in visitedSet:
            successors = problem.getSuccessors(curState)
            successorDict[curState] = successors

        visitedSet.add(curState)
        nStateTuple = filter(lambda x: x[0] not in visitedSet, successorDict[curState]) # get next state

        if len(nStateTuple) == 0:
            stateStack.pop()
            actionList.pop()
            curState = stateStack.list[-1]
        else:
            curState = nStateTuple[0][successor_idx['state']]
            stateStack.push(curState)
            actionList.append(nStateTuple[0][successor_idx['dir']])

    return []
    
def breadthFirstSearch(problem):
    successor_idx = {'dir': 1, 'state': 0, 'cost': -1}

    MAX_ITER = int(20000)
    stateQ = Queue()
    actQ = Queue() # queues action for backtracking
    visitedSet = set()

    curState = problem.getStartState()
    visitedSet.add(curState)

    actionList = [] # add actions to get to the state, use pop to remove last one

    for it in range(MAX_ITER):
        
        if problem.isGoalState(curState):
            return actionList
        
        successors = problem.getSuccessors(curState)

        for node in successors:
            if node[successor_idx['state']] not in visitedSet:
                stateQ.push(node[successor_idx['state']])
                actQ.push(actionList + [node[successor_idx['dir']]])
                visitedSet.add(node[successor_idx['state']])

        actionList = actQ.pop()
        curState = stateQ.pop()

    return []

def uniformCostSearch(problem):
    successor_idx = {'dir': 1, 'state': 0, 'cost': -1}

    MAX_ITER = int(2000)
    stateQ = PriorityQueue()
    visitedSet = set()
    successorDict = {}

    curState = problem.getStartState()
    actionList = [] # add actions to get to the state, use pop to remove last one
    currentCost = 0

    for it in range(MAX_ITER):

        if problem.isGoalState(curState):
            return actionList
        
        if curState not in visitedSet:
            successorDict[curState] = problem.getSuccessors(curState)
        visitedSet.add(curState)

        for node in successorDict[curState]:

            if node[successor_idx['state']] not in visitedSet:
                tmp_state = {'cost' : currentCost + node[successor_idx['cost']], 'action' : actionList + [node[successor_idx['dir']]], 'state': node[successor_idx['state']]}
                stateQ.push(tmp_state, tmp_state['cost'])
        # get next state to test
        nState = stateQ.pop()
        actionList = nState['action']
        curState = nState['state']
        currentCost = nState['cost']

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):

    successor_idx = {'dir': 1, 'state': 0, 'cost': -1}

    MAX_ITER = int(50000)
    stateQ = PriorityQueue()
    visitedSet = set()
    successorDict = {}

    curState = problem.getStartState()
    actionList = [] # add actions to get to the state, use pop to remove last one
    accGCost = 0

    for it in range(MAX_ITER):

        if problem.isGoalState(curState):
            return actionList
        
        if curState not in visitedSet:
            successorDict[curState] = problem.getSuccessors(curState)
        visitedSet.add(curState)

        for node in successorDict[curState]:

            if node[successor_idx['state']] not in visitedSet:
                tmp_state = node[successor_idx['state']]
                tmp_h_cost = heuristic(tmp_state, problem)
                tmp_g_cost = node[successor_idx['cost']] + accGCost
                tmp_action = actionList + [node[successor_idx['dir']]] 
                tmp_dict = {'action' : tmp_action, 'state': tmp_state, 'cost' : tmp_g_cost}
                stateQ.push(tmp_dict, tmp_h_cost + tmp_g_cost)
        # get next state to test
        nState = stateQ.pop()
        actionList = nState['action']
        curState = nState['state']
        accGCost = nState['cost']

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
