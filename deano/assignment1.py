import sys
from sympy import var
import random
import matplotlib.pyplot as plt

print(sys.version) # make sure you are on 2.7




def generate_random_problem(n_vars, n_clauses):
    problem = []
    for _ in range(n_clauses):
        tmp_var = set()
        tmp_nVar = set()
        while len(tmp_var) + len(tmp_nVar) != 3:

            if(random.randint(0,1)):
                tmp_nVar.add(random.randint(1,n_vars))
            else:
                tmp_var.add(random.randint(1,n_vars))
        problem.append((tmp_var, tmp_nVar))

    return problem



def simplify_three_cnf(problem):

    append_list = []
    for idx, _ in enumerate(problem):
        b = len([x for x in problem[idx][0] if (x in problem[idx][1])]) != 0 # clause contains negated and non negated version of same variable
        if not b:
            append_list.append(idx)

    simplified_problem = [problem[x] for x in append_list]
    return simplified_problem




def get_initial_state(n_vars, n_clauses):
    # ? why is n_clauses as argument required ?
    state = []
    
    while len(state) != n_vars:
        if(random.randint(0,1)):
            state.append(True)
        else:
            state.append(False)
    return state


def eval_clause(state, clause):
  
    try:
         state1 = [state[x] for x in clause[0]]
    except IndexError:
        state1 = []

    try:
         state2 = [not state[x] for x in clause[1]]
    except IndexError:
        state2 = []

    expressions = state1 + state2

    if any(expressions):
        return True
    else:
        return False

def eval_three_cnf(problem, state):
    clause_evaluation = []
    for clause in problem:
        clause_evaluation.append(eval_clause(state, clause))

    if all(clause_evaluation):
        return True
    else:
        return False


def am_i_done(problem, state):
    return eval_three_cnf(problem,state)




def run_gsat_chain(problem, state, max_iter):
    
    final_state = state
    max_clause = 0
    success = False


    for _ in xrange(max_iter):


        flip_list = []
        flip_count = []

        if am_i_done(problem, final_state):
            return final_state, True

        for idx, _ in enumerate(final_state):

            tmp = final_state
            tmp[idx] = not final_state[idx] # flip state in state list
            count = 0

            for clause in problem:     
             # evaluate over all clauses
                if(eval_clause(tmp, clause)):
                    count += 1

            if(count >= max_clause):
               final_state[idx] = not final_state[idx]
               max_clause = count


    return final_state, success



def run_gsat(problem, max_iter, n_vars, max_n_chains):

    max_count = 0
    best_state = []
    success = False


    for _ in range(max_n_chains):
        state = get_initial_state(n_vars, 0)
        satisfying_assignment , success = run_gsat_chain(problem, state, max_iter)

        if success:
            return success, satisfying_assignment
        else:
            # count max clauses
            count = 0
            for clause in problem:
                if eval_clause(satisfying_assignment, clause):
                    count +=1

            if count > max_count:
                max_count = count

    return success, satisfying_assignment