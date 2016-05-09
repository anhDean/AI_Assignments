import sys
import pprint

print(sys.version) # make sure you are on 2.7

def show_state(state, ghost_pos=None):
    """Show the state graphically, and the position of the ghost, if it is known"""
    chars = {'C': 'C',
             '-C': '0',
             'NV': '.'}

    ss = [list(range(4)) for _ in range(4)]
    for s in state:
        c, i, j = s.split('_')
        ss[int(i)][int(j)] = chars[c]
    if ghost_pos:
        ss[ghost_pos[0]][ghost_pos[1]] = 'G'
    pprint.pprint(ss)
    return ss


def is_1_2_safe(state):
    """a function that determines in a propositional way if it safe to move to the (1, 2) square."""
    ss = show_state(state)
    nNoChill = len([elements for rows in ss for elements in rows if elements is '0'])
    nChill = len([elements for rows in ss for elements in rows if elements is 'C'])
    nGhost = len([elements for rows in ss for elements in rows if elements is 'G'])
    nUnknown = len([elements for rows in ss for elements in rows if elements is '.'])


    #1_2 is safe
    if ss[1][2] is '0' or ss[1][2] is 'C':
        return 'Safe_1_2'
    elif ss[2][2] is '0' or ss[1][1] is '0' or ss[0][2] is '0' or ss[1][3]is '0':
        return 'Safe_1_2'

    #1_2 is ghost
    if ss[1][2] is 'G':
        return 'Ghost_1_2'
    elif ss[1][1] is 'C' and ss[2][2] is 'C' and ss[3][1] is 'C' and ss[0][2] is 'C':   # 4 Chills
        return 'Ghost_1_2'
    elif ss[1][1] is 'C' and ss[2][2] is 'C' and ss[3][1] is 'C':    # 3 Chills
        return 'Ghost_1_2'
    elif ss[2][2] is 'C' and ss[3][1] is 'C' and ss[0][2] is 'C':
        return 'Ghost_1_2'
    elif ss[3][1] is 'C' and ss[0][2] is 'C' and ss[1][1] is 'C':
        return 'Ghost_1_2'
    elif ss[0][2] is 'C' and ss[1][1] is 'C' and ss[2][2] is 'C':
        return 'Ghost_1_2'
    elif ss[0][2] is 'C' and ss[1][3] is 'C' and ss[0][3] is '0':    # Edges with 2 Chills
        return 'Ghost_1_2'
    elif ss[0][2] is 'C' and ss[1][1] is 'C' and ss[0][1] is '0':
        return 'Ghost_1_2'
    elif ss[1][1] is 'C' and ss[2][2] is 'C' and ss[2][1] is '0':
        return 'Ghost_1_2'
    elif ss[1][3] is 'C' and ss[2][2] is 'C' and ss[2][3] is '0':
        return 'Ghost_1_2'
    elif ss[0][2] is 'C' and ss[0][1] is '0' and ss[0][3] is '0':    # 1 Chill
        return 'Ghost_1_2'
    elif ss[1][3] is 'C' and ss[0][3] is '0' and ss[2][3] is '0':
        return 'Ghost_1_2'
    elif ss[1][1] is 'C' and ss[0][1] is '0' and ss[1][0] is '0' and ss[2][1] is '0':
        return 'Ghost_1_2'
    elif ss[2][2] is 'C' and ss[2][1] is '0' and ss[2][3] is '0' and ss[3][2] is '0':
        return 'Ghost_1_2'
    elif ss[0][0] == '0' and ss[0][1] == '0' and ss[0][3] == '0':  # 0 Chills
        if ss[1][0] == '0':
            if ss[2][0] == '0' and ss[2][1] == '0' and ss[2][3] == '0':
                if ss[3][0] == '0' and ss[3][1] == '0' and ss[3][2] == '0' and ss[3][3] == '0':
                    return 'Ghost_1_2'

    return 'Unsafe_1_2'









state = ['-C_0_0',
 'NV_0_1',
 'NV_0_2',
 '-C_0_3',
 'NV_1_0',
 'C_1_1',
 'NV_1_2',
 'C_1_3',
 '-C_2_0',
 'NV_2_1',
 'C_2_2',
 '-C_2_3',
 '-C_3_0',
 'NV_3_1',
 'NV_3_2',
 '-C_3_3']

ss = show_state(state)
result = is_1_2_safe(state)

nNoChill = len([elements for rows in ss for elements in rows if elements is '0'])
nChill = len([elements for rows in ss for elements in rows if elements is 'C'])
nGhost = len([elements for rows in ss for elements in rows if elements is 'G'])
nUnknown = len([elements for rows in ss for elements in rows if elements is '.'])
print([nNoChill,nChill,nGhost,nUnknown])


print(result)
