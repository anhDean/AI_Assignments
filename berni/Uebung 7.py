import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
from numpy import reshape

cmap = plt.get_cmap('hot')
map_shape = (3, 4)

map_arr = np.zeros(map_shape, dtype=np.bool)  # initialize an all-zero array
map_arr[:] = True  # This assigns a scalar value to all elements of the array, while keeping its shape.
map_arr[1, 1] = False


final_arr = np.zeros(map_shape, dtype=np.bool)
final_arr[:] = False
final_arr[0, 3] = True
final_arr[1, 3] = True




rewards = np.zeros(map_shape)
rewards[:] = -0.04
rewards[0, 3] = 1
rewards[1, 3] = -1

actions = OrderedDict({'u': {(-1, 0): .8, (0, -1): .1, (0, 1): .1},
                       'l': {(0, -1): .8, (1, 0): .1, (-1, 0): .1},
                       'd': {(1, 0): .8, (0, -1): .1, (0, 1): .1},
                       'r': {(0, 1): .8, (1, 0): .1, (-1, 0): .1}})
gamma = 1

def in_bounds(state, map_shape):
    """utility function to determine if `state` is inside the map."""
    return 0 <= state[0] < map_shape[0] and 0 <= state[1] < map_shape[1]

# initialize utilities
def init_utils(map_shape, rewards):
    """initialize all utilities to zero, or to the rewards for final states"""
    utilities = np.zeros(map_shape)
    utilities[final_arr] = rewards[final_arr]
    return utilities

def q_Val(node,selectedAction,actions,utilities,map_arr,gamma):
    # calculates the q value for a action in a node
    q = 0.0
    for action in actions[selectedAction]:
        prob = actions[selectedAction][action]
        newNode = (node[0]+action[0],node[1]+action[1])
        if in_bounds(newNode,map_shape) and map_arr[newNode]:    # legal action
            q += gamma*prob*utilities[newNode]
        else:   # not legal action stays in same state with updated utility
            q += gamma*prob*utilities[node]
    return q

def update_utils(utilities, map_shape, map_arr, rewards, final_arr, actions, gamma):
    """run one single step of value iteration"""
    new_utilities = np.zeros(map_shape)
    new_utilities[final_arr] = rewards[final_arr]
    rows, cols = map_shape
    for r in range(rows):
        for c in range(cols):
            node = (r, c)    # node we are in
            if map_arr[node] and not final_arr[node]:
                qVals = [q_Val(node,selectedAction,actions,utilities,map_arr,gamma) for selectedAction in actions.keys()]
                qVal = max(qVals)
                new_utilities[node] = rewards[node]
                new_utilities[node] += qVal
            if not map_arr[node]:   # non traversable areas have no utility
                new_utilities[node] = 0.0

    # This copies the values from new_utilities to utilities
    utilities[:] = new_utilities[:]

    # strictly, there is no return value needed, since `utilities` is
    # also updated in the calling function, but leave this in for
    # the grading to work!
    return utilities

utilities = init_utils(map_shape,rewards)

def min_num_iterations_():
    """
    returns the minimum number of iterations of value iteration
    so that the Euclidean distance between utility estimates is
    smaller than 10**-4
    """
    rows, cols = map_shape
    error = 1
    it = 0
    minErr = 1e-4
    while (error > minErr):
        bkp_utilities = utilities.copy()
        update_utils(utilities, map_shape, map_arr, rewards, final_arr, actions, gamma)
        diff = [(bkp_utilities[(r,c)] - utilities[(r,c)]) for r in range(rows) for c in range(cols)]
        error = np.sqrt(np.dot(diff, diff))
        it += 1
    return it



print min_num_iterations()


def get_strategy(utilities, map_shape, map_arr, final_arr, actions):
    strategy = np.zeros(map_shape, dtype=np.character)
    rows, cols = map_shape
    neigh = [(1,0),(0,1),(-1,0),(0,-1)]
    acts = ['d','r','u','l']

    for r in range(rows):
        for c in range(cols):
            node = (r,c)
            if map_arr[node] and not final_arr[node]:
                neighUtils = {}
                for action in neigh:
                    newNode = (node[0]+action[0],node[1]+action[1])
                    if in_bounds(newNode,map_shape) and map_arr[newNode]:
                        neighUtils[utilities[newNode]] = action
                bestAction = max(neighUtils.keys())
                strategy[node] = acts[neigh.index(neighUtils[bestAction])]
            else:
                strategy[node] = 'x'
    return strategy


strategy = get_strategy(utilities, map_shape, map_arr, final_arr, actions)
print utilities
print strategy