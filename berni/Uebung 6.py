import itertools
import numpy as np
from numpy import array


class Mrf(object):

    def __init__(self, domain, cliques):
        ''' Domain: Values that the variables can take
            Cliques: List of tuples (variables,potential_matrix) '''
        self.domain = domain
        self.cliques = cliques
        self.variables = set()
        for vs, matrix in cliques:
            self.variables.update(vs)

    def get_potential(self, configuration):
        ''' Return the potential (unnormalized) of the given variable configuration)'''
        p = 1.0
        for var, pot in self.cliques:
            if 0 < len(var) < 2:        # unary potential
                p *= pot[configuration[var[0]]]
            else:                       # pairwise potential
                p *= pot[(configuration[var[0]]), (configuration[var[1]])]

        return p    # all multiplied together

    def get_configurations(self):
        ''' Returns a list of dicts with all possible variable configurations '''
        configurations = []
        for values in itertools.product(self.domain, repeat=len(self.variables)):
            configurations.append(dict(zip(self.variables, values)))

        return configurations

    def compute_Z(self):
        ''' Return the normalization constant'''
        z = 0.0
        for conf in self.get_configurations():
            pot = self.get_potential(conf)
            z += pot
        return z

    def argmax(self):
        '''Return a dict with a most likely configuration and its unnormalized potential'''
        configurations = self.get_configurations()
        pots = [self.get_potential(i) for i in configurations]  # calc potentials of cliques
        maxPot = max(pots)      # get max potential
        ind = pots.index(maxPot)    # get index of configuration that generates max potential
        return configurations[ind], maxPot

# Example with only two unary potentials and one pairwise potential (in practice you will have many)
domain = [0, 1]

# Unary potential on v1
variables_unary_v1 = array((1, ))
potential_unary_v1 = array((0.1, 0.8))  # the state 0 has a potential of 0.1, state 1 has a potential of 0.8
variables_unary_v2 = array((2, ))
potential_unary_v2 = array((0.3, 0.6))  # the state 0 has a potential of 0.3, state 1 has a potential of 0.6

# Pairwise potential
variables_pairwise = array([1, 2])  # A potential over variables 1 and 2
potential_pairwise = array([[1, 0],
                            [0, 1]])  # States where v1 and v2 are equal have a potential of 1, else 0

# Create the Mrf
my_mrf = Mrf(domain, [(variables_unary_v1, potential_unary_v1),
                      (variables_unary_v2, potential_unary_v2),
                      (variables_pairwise, potential_pairwise)])

# Notice that we used numpy arrays to create the potentials, this allows us to use easy indexing with tuples
matrix_position = (0, 1)
#print potential_pairwise[matrix_position]

my_configuration = {1: 1, 2: 1, 3: 1, 4: 0}  # Assuming we have 4 variables
potential = my_mrf.get_potential(my_configuration)
z = my_mrf.compute_Z()
configuration, value = my_mrf.argmax()


def build_line_scan_mrf(row, unary_on, unary_off, pairwise):
    '''Returns and MRF for the described model and the observed row of pixels'''
    unaries = []
    pairwise_cliques = []

    for i, val in enumerate(row):
        variables_unary_tmp = array((i,))

        if val is 1:
            unaries.append((variables_unary_tmp,unary_on))
        if val is 0:
            unaries.append((variables_unary_tmp,unary_off))
        if i is not 0:
            variables_pairwise = array([i-1, i])
            pairwise_cliques.append((variables_pairwise,pairwise))
    return Mrf([0, 1], pairwise_cliques + unaries)


row = [0,0,0,0,0,1,0,0,0,0,0]

unary_on = array([1,3])
unary_off = array([2,1])
pairwise=array([[1,1],[1,1]])

mrf = build_line_scan_mrf(row, unary_on, unary_off, pairwise)