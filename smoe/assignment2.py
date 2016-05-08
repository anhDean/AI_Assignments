import pprint
import collections

def show_state(state, ghost_pos=None):
    """Show the state graphically, and the position of the ghost, if it is known"""
    chars = {'C': 'C',
             '-C': '0',
             'NV': '.'}

    ss = [range(4) for _ in range(4)]
    for s in state:
        c, i, j = s.split('_')
        ss[int(i)][int(j)] = chars[c]
    if ghost_pos:
        ss[ghost_pos[0]][ghost_pos[1]] = 'G'

    pprint.pprint(ss)

def is_1_2_safe(state):
    """a function that determines in a propositional way if it safe to move to the (1, 2) square."""
    chars = {'C': 'C',
             '-C': '0',
             'NV': '.'}

    ss = [range(4) for _ in range(4)]
    for s in state:
        c, i, j = s.split('_')
        ss[int(i)][int(j)] = chars[c]


    neighbour_state =( ss[1][1], ss[1][3], ss[0][2], ss[2][2])
    nei_counter =  collections.Counter(neighbour_state)
    c_counter = sum(x.count('C') for x in ss)

    if ss[1][1] == 'C' and ss[1][0] == '0' and ss[0][1] == '0' and ss[2][1] == '0':
        return 'Ghost_1_2'
    if ss[1][3] == 'C' and ss[0][3] == '0' and ss[2][3] == '0':
        return 'Ghost_1_2'
    if ss[0][2] == 'C' and ss[0][1] == '0' and ss[0][3] == '0':
        return 'Ghost_1_2'
    if ss[2][2] == 'C' and ss[2][1] == '0' and ss[2][3] == '0' and ss[3][2] == '0':
        return 'Ghost_1_2'

    if nei_counter['C'] > 2:
        return 'Ghost_1_2'
    elif (nei_counter['C'] == 0 and nei_counter['-C'] == 4 )or (nei_counter['C']-c_counter < 0) or (nei_counter['0']  != 0):
        return 'Safe_1_2'
    else:
        return 'Unsafe_1_2'

state = (['NV_0_0', 'NV_0_1', 'NV_0_2', 'NV_0_3', 'NV_1_0', 'C_1_1', 'NV_1_2', 'NV_1_3', 'NV_2_0', 'NV_2_1', 'C_2_2', 'NV_2_3', 'NV_3_0', 'NV_3_1', 'NV_3_2', 'NV_3_3'],
 ['NV_0_0', 'NV_0_1', 'NV_0_2', 'NV_0_3', 'NV_1_0', 'NV_1_1', 'NV_1_2', 'NV_1_3', 'NV_2_1', 'NV_2_0', 'NV_2_2', 'NV_2_3', 'NV_3_0', 'NV_3_2', 'NV_3_1', 'NV_3_3'],
  ['C_0_0', 'NV_0_1', 'NV_0_2', 'NV_0_3', 'NV_1_0', 'NV_1_1', 'NV_1_2', 'NV_1_3', 'NV_2_1', 'NV_2_0', 'NV_2_2', 'NV_2_3', 'NV_3_0', 'NV_3_2', 'NV_3_1', 'NV_3_3'],
  ['-C_0_0', 'NV_0_1', 'NV_0_2', 'NV_0_3', 'NV_1_0', 'NV_1_1', 'NV_1_2', 'C_1_3', 'NV_2_1', 'NV_2_0', 'NV_2_2', 'NV_2_3', 'NV_3_0', 'NV_3_2', 'NV_3_1', 'NV_3_3'],
  ['NV_0_0', '-C_0_1', 'NV_0_2', 'NV_0_3', '-C_1_0', 'C_1_1', 'NV_1_2', 'NV_1_3', '-C_2_1', 'NV_2_0', 'NV_2_2', 'NV_2_3', 'NV_3_0', 'NV_3_2', 'NV_3_1', '-C_3_3'],
  ['-C_0_0', '-C_0_1', '-C_0_2', '-C_0_3', 'NV_1_0', 'NV_1_1', '-C_1_2', '-C_1_3', '-C_2_0', 'C_2_1', 'NV_2_2', '-C_2_3', 'C_3_0', 'NV_3_1', 'C_3_2', 'NV_3_3'],
  ['-C_0_0', '-C_0_1', '-C_0_2', '-C_0_3', '-C_1_0', 'NV_1_1', '-C_1_2', 'NV_1_3', 'NV_2_0', '-C_2_1', 'NV_2_2', 'NV_2_3', '-C_3_0', '-C_3_1', 'NV_3_2', 'C_3_3'],
  ['-C_0_0', '-C_0_1', 'NV_0_2', '-C_0_3', '-C_1_0', '-C_1_1', 'NV_1_2', 'C_1_3', '-C_2_0', '-C_2_1', 'NV_2_2', 'NV_2_3', '-C_3_0', 'NV_3_1', '-C_3_2', 'NV_3_3'],
  ['-C_0_0', '-C_0_1', 'C_0_2', 'NV_0_3', '-C_1_0', '-C_1_1', '-C_1_2', 'C_1_3', '-C_2_0', '-C_2_1', '-C_2_2', '-C_2_3', 'NV_3_0', '-C_3_1', 'NV_3_2', 'NV_3_3'],
  ['-C_0_0', '-C_0_1', '-C_0_2', 'NV_0_3', 'NV_1_0', '-C_1_1', 'C_1_2', '-C_1_3', '-C_2_0', 'C_2_1', 'NV_2_2', 'NV_2_3', '-C_3_0', '-C_3_1', 'C_3_2', 'NV_3_3'],
  ['NV_0_0', 'NV_0_1', 'C_0_2', '-C_0_3', 'NV_1_0', 'C_1_1', 'NV_1_2', 'C_1_3', '-C_2_0', '-C_2_1', 'NV_2_2', '-C_2_3', '-C_3_0', '-C_3_1', 'NV_3_2', '-C_3_3'])

for s in state:
    show_state(s)
    print is_1_2_safe(s)
