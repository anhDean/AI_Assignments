import sys
from random import randint

print(sys.version) # make sure you are on 2.7

def generate_random_problem_jojo(n_vars, n_clauses):
    problem = []

    for i in range(n_clauses):
        posClause = set()
        negClause = set()
        while len(posClause) + len(negClause) != 3:
            vars = randint(0,n_vars-1)

            if randint(0, 1):
                posClause.add(vars)
            else:
                negClause.add(vars)

        problem.append((posClause, negClause))
    return problem

def generate_random_problem(n_vars, n_clauses):
    problem = []
    for clause in range(n_clauses):
        pos = set([])
        neg = set([])
        # do until we found valid Clause with 3 different literals
        while(len(pos)+len(neg) != 3):
            var = randint(0,n_vars-1)
            posneg = randint(0,1)
            if posneg == 0 and var not in pos:
                pos.add(var)
            if posneg == 1 and var not in neg:
                neg.add(var)
        problem.append((pos,neg))
    return problem

def simplify_three_cnf(problem):
    simplified_problem = []
    for clause in problem:
        # same literal is not pos and neg in same clause
        # if liter would we pos and neg in same clause, clause is always 1 and can ge neglected
        if len(clause[0]&clause[1]) == 0:
            simplified_problem.append(clause)
    return simplified_problem

def get_initial_state(n_vars, n_clauses = 0):
    # no need for n_clauses
    state = []
    for i in range(n_vars):
        posneg = randint(0,1)
        if posneg == 1:
            state.append(True)
        else:
            state.append(False)
    return state

def eval_clause(state, clause):
    first = []
    second = []
    # evaluate pos literals
    try:
        for element in clause[0]:
            first.append(state[element])
    except IndexError:
        first = []
    # evaluate neg literals
    try:
        for element in clause[1]:
            second.append(not state[element])
    except IndexError:
        second = []

    if any(first) or any(second):
        return True
    else:
        return False

def eval_three_cnf(problem, state):
    eval_clauses = [eval_clause(state, clause) for clause in problem]
    if all(eval_clauses):
        return True
    else:
        return False

def am_i_done(problem, final_state):
    return eval_three_cnf(problem, final_state)

def run_gsat_chain(problem, state, max_iter):

    final_state = state
    gsat_state = state
    count = 0
    # no need to run chain if problem is already solved
    if am_i_done(problem, final_state):
        return final_state, True
    # evaluate number of positive clauses
    for clause in problem:
        if eval_clause(final_state, clause):
            count += 1
    maxTrue = count
    for i in range(max_iter):
        count = 0
        # flip random element of state vector
        index = randint(0,len(gsat_state) - 1)
        gsat_state[index] = not final_state[index]
        for clause in problem:
            if eval_clause(gsat_state,clause):
                count += 1

        if count > maxTrue:
            maxTrue = count
            final_state = gsat_state

        if am_i_done(problem,final_state):
            return final_state, True
    # no solution was found
    return final_state, False

def run_gsat(problem, max_iter, n_vars, max_n_chains):

    global badSolution
    maxTrue = 0
    success = False

    for _ in range(max_n_chains):
        # generate inital states and run gsat_chain
        state = get_initial_state(n_vars)
        tmp_assignment, success = run_gsat_chain(problem, state, max_iter)

        if success:
            return success, tmp_assignment
        else:
            count = len([eval_clause(present_solution, clause) for clause in problem if eval_clause(present_solution, clause)])
            if count > maxTrue:
                maxTrue = count
                satisfying_assignment = present_solution

    return success, satisfying_assignment

n = 10
m = 30
max_iter = 500
man_n_chains = 10
problem = generate_random_problem(n, m)
success, solution = run_gsat(problem, max_iter, n, man_n_chains)
print(success)
print(solution)