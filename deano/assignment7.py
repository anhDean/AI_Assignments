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

print final_arr
print rewards
print map_arr



actions = OrderedDict({'u': {(-1, 0): .8, (0, -1): .1, (0, 1): .1},
                       'l': {(0, -1): .8, (1, 0): .1, (-1, 0): .1},
                       'd': {(1, 0): .8, (0, -1): .1, (0, 1): .1},
                       'r': {(0, 1): .8, (1, 0): .1, (-1, 0): .1}})
print actions
print actions.keys()
print actions.values()
print actions.itervalues()

def in_bounds(state, map_shape):
    """utility function to determine if `state` is inside the map."""
    return 0 <= state[0] < map_shape[0] and 0 <= state[1] < map_shape[1]


gamma = 1

def init_utils(map_shape, rewards):
    """initialize all utilities to zero, or to the rewards for final states"""
    utilities = np.zeros(map_shape)
    utilities[final_arr] = rewards[final_arr]

    return utilities
print init_utils(map_shape, rewards)


def get_q_val(state, chosen_action, actions):
    # state: tuple of y,x coordinates (y,x)
    q_state = 0.0
    for t, prob in actions[chosen_action].iteritems():   
        new_state = tuple(map(lambda a,b : a + b, state, t))
        if in_bounds(new_state, map_shape):
            q_state +=  prob * utilities[new_state]
        else:
            q_state +=  prob * utilities[state]
            
    return q_state



def update_utils(utilities, map_shape, map_arr, rewards, final_arr, actions, gamma):
    """run one single step of value iteration"""
    new_utilities = np.zeros(map_shape)
    new_utilities[final_arr] = rewards[final_arr]
    
    # for each state compute utility
    Y, X = map_shape
    for y in range(Y):
        for x in range(X):
            state = (y,x)
            new_utilities[state] = rewards[state]                 
            if not final_arr[state] and map_arr[state]:
                utils = []
                # expected for single action
                for act, transitions in actions.iteritems():                            
                    utils.append(get_q_val(state, act, actions))
                new_utilities[state] += max(utils)
                
            elif not map_arr[state]:
                new_utilities[state] = 0
                       
    utilities[:] = new_utilities.copy()
                        
                


utilities = init_utils(map_shape, rewards)
update_utils(utilities, map_shape, map_arr, rewards, final_arr, actions, gamma)
update_utils(utilities, map_shape, map_arr, rewards, final_arr, actions, gamma)


plt.imshow(utilities, interpolation='nearest')
#plt.show()


def min_num_iterations():
    """
    returns the minimum number of iterations of value iteration
    so that the Euclidean distance between utility estimates is
    smaller than 10**-4
    """
    err = 1e6
    count = 0
    
    while (err > 1e-4):
        bkp_utils = utilities.copy()
        update_utils(utilities, map_shape, map_arr, rewards, final_arr, actions, gamma)
        d = bkp_utils.flatten() - utilities.flatten()
        err= np.sqrt(np.dot(d,d))
        count += 1
    return count


def get_strategy(utilities, map_shape, map_arr, final_arr, actions):
    strategy = np.zeros(map_shape, dtype=np.character)
    
    Y, X = map_shape
    for y in range(Y):
        for x in range(X):
            state = (y,x)
            if not final_arr[state] and map_arr[state]:
                q_vals = [get_q_val(state, act, actions) for act in actions.keys()]
                strategy[state] = actions.keys()[q_vals.index(max(q_vals))]
            else:
                strategy[state] = 'x'
                

    return strategy
                    
                    
print utilities.flatten()
print min_num_iterations()
print utilities

    
strategy = get_strategy(utilities, map_shape, map_arr, final_arr, actions)
print strategy






