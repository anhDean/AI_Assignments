import sys
from sympy import var
import random
import matplotlib.pyplot as plt

print(sys.version) # make sure you are on 2.7

def generate_random_problem(n_vars, n_clauses):
    problem = []

    for i in range(n_clauses):
        posClause = set()
        negClause = set()
        while len(posClause) + len(negClause) != 3:
            vars = random.randint(0,n_vars-1)

            if random.randint(0, 1):
                posClause.add(vars)
            else:
                negClause.add(vars)

        problem.append((posClause, negClause))
    return problem

def simplify_three_cnf(problem):
    simplified_problem = []

    for i in problem:
        sameValues = set(i[0]) & set(i[1])
        print len(sameValues)
        if (len(sameValues)) == 0:
            simplified_problem.append(i)


    return simplified_problem

def get_initial_state(n_vars, n_clauses):
    state = []
    for i in range (0,n_vars):
        state.append(random.randint(0,1))
    return state

def eval_clause(state, clause):
    response = 0
    for i in clause[0]:
        response = response or state[i]
    for i in clause[1]:
        response = response or not state[i]

    return response


def eval_three_cnf(problem, state):
    response = 1
    for i in problem:
        response = response and eval_clause(state, i)

    return response

def run_gsat_chain(problem, state, max_iter):
    count = 0
    final_state = state
    tmp_state = state
    for clause in problem:
        if eval_clause(state, clause):
            count += 1
            
    maxCounter = count
    
    if am_i_done(problem, final_state):
        return final_state, True

    for _ in xrange(max_iter):
        count = 0

        tmp_state[random.randint(0, len(state)-1)] = not tmp_state[random.randint(0, len(state)-1)]

        for clause in problem:
            if eval_clause(state, clause):
                count += 1
        if count > maxCounter:
            maxCounter = count
            final_state = tmp_state

        tmp_state = final_state

    if am_i_done(problem, final_state):
        return final_state, True


    return final_state, False


def run_gsat(problem, max_iter, n_vars, max_n_chains):
    max_count = 0
    success = False

    for i in range(max_n_chains):
        state = get_initial_state(n_vars, 0)
        tmp_assignment, success = run_gsat_chain(problem, state, max_iter)

        if success:
            return success, tmp_assignment
        else:
            count = 0
            for clause in problem:
                if eval_clause(tmp_assignment, clause):
                    count +=1

            if count > max_count:
                satisfying_assignment = tmp_assignment
                max_count = count

    return success, satisfying_assignment