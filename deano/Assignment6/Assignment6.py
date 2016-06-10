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
        # calculate unary potentials
        p_unary = 1.0;
        p_pairwise = 1.0;
        for rv, pot in self.cliques:
            if len(rv) > 1:
                p_pairwise *= pot[(configuration[rv[0]], configuration[rv[1]])]
            else:
                p_unary *= pot[configuration[rv[0]]]         
        return p_unary * p_pairwise


    def get_configurations(self):
        ''' Returns a list of dicts with all possible variable configurations '''
        configurations = []
        for values in itertools.product(self.domain, repeat=len(self.variables)):
            configurations.append(dict(zip(self.variables, values)))

        return configurations

    def compute_Z(self):
        ''' Return the normalization constant'''
        return sum([self.get_potential(config) for config in self.get_configurations()])

    def argmax(self):
        '''Return a dict with a most likely configuration and its unnormalized potential'''
        configs = self.get_configurations()
        potentials = [self.get_potential(config) for config in configs]
        maxPotential = max(potentials)
        return configs[potentials.index(maxPotential)], maxPotential

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
matrix_position = (1, 1)
print potential_pairwise[matrix_position]
print my_mrf.cliques
print my_mrf.variables


# uncomment this code when you have implemented the method

my_configuration = {1: 1, 2: 1, 3: 1, 4: 0}  # Assuming we have 4 variables
potential = my_mrf.get_potential(my_configuration)
print potential

# uncomment this code when you have implemented the method

configuration, value = my_mrf.argmax()
print configuration, value


# uncomment this code when you have implemented the method

Z = my_mrf.compute_Z()
print Z

def build_line_scan_mrf(row, unary_on, unary_off, pairwise):
    '''Returns and MRF for the described model and the observed row of pixels'''
    unaries = []
    pairwise_cliques = []
    for i,x in enumerate(row):
        if x:
            unaries.append((array((i, )), unary_on ))
        else:
            unaries.append((array((i, )), unary_off ))

        if i < len(row) - 1: 
            pairwise_cliques.append((array([i, i+1]), pairwise))
    return Mrf([0, 1], unaries + pairwise_cliques )


from matplotlib import pyplot as plt


def view_row(row):
    ''' Displays the row. If called multiple calls in a single cell it only displays last call'''
    img = array([row])
    plt.imshow(img, interpolation='nearest', cmap='hot', vmin=0, vmax=1)


def configuration2row(configuration):
    ''' Convert from a configuration in the mrf to the image row'''
    row = [0] * len(configuration.items())
    for pos, value in configuration.items():
        row[pos] = value

    return row

# Change this code as you wish

row = [0,0,1,0,1,0,1,1,1,0,1]

unary_on = array([0.1,2])
unary_off = array([2,0.1])
pairwise=array([[1,0.1],[0.1,1]])

mrf = build_line_scan_mrf(row, unary_on, unary_off, pairwise)
am, value = mrf.argmax()
print am, value
view_row(configuration2row(am))
plt.show()
