
import pprint
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
    
    return ss





def is_1_2_safe(state):
    """a function that determines in a propositional way if it safe to move to the (1, 2) square."""
    
    ss = show_state(state)
    
    safe_exp = ss[1][1]=='0' or ss[2][2]=='0' or ss[1][3]=='0' or ss[0][2]=='0' or \
               ss[0][0]=='C' or ss[0][1]=='C' or ss[0][3]=='C' or ss[1][0]=='C' or \
               ss[2][0]=='C' or ss[2][1]=='C' or ss[2][3]=='C' or ss[3][0]=='C' or \
               ss[3][1]=='C' or ss[3][2]=='C' or ss[3][3]=='C'
    
    ghost_exp = ((ss[0][2]=='C' and ss[2][2]=='C')) or \
                ((ss[1][1]=='C' and ss[1][3]=='C')) or \
                (ss[1][1]=='C' and ss[0][2]=='C' and (ss[0][1]=='0' or ss[0][0]=='0')) or \
                (ss[1][1]=='C' and ss[2][2]=='C' and (ss[2][1]=='0' or ss[3][1]=='0' or ss[2][0]=='0')) or \
                (ss[1][3]=='C' and ss[2][2]=='C' and (ss[2][3]=='0' or ss[3][3]=='0')) or  \
                (ss[1][3]=='C' and ss[0][2]=='C' and ss[0][3]!= '.') or \
                (ss[0][2] == 'C' and ss[0][3] != '.' and ss[0][1] != '.' )or \
                (ss[1][3] == 'C' and ss[0][3] != '.' and ss[2][0] != '.' )or \
                (ss[2][2] == 'C' and ss[2][3] != '.' and ss[2][1] != '.' and ss[3][2] != '.' ) or \
                (ss[1][1] == 'C' and ss[1][0] != '.' and ss[0][1] != '.' and ss[2][1] != '.' )

    if safe_exp:
        return 'Safe_1_2'
    
    elif ghost_exp:
        
        return 'Ghost_1_2'
    else:
        return 'Unsafe_1_2'