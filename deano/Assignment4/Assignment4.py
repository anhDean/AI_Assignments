from Bayes_exercise import Cpt
# TODO: use for submission this line: from ai_algorithms.Bayes_exercise import Cpt



#Here we say that there is a 0.1 probability of raining if there are no clouds, and 0.8 if it is cloudy
rain = Cpt('Rain', [[0.9,0.1],
                    [0.2,0.8]], 
           ['Cloudy'])
print rain

# We decide that cloudy is not conditioned on any variable other variable, so we define a prior probability for it
cloudy = Cpt('Cloudy', [[0.6, 0.4]],[])
print cloudy

# Note that WetGrass is conditioned on two variables
wetgrass = Cpt('WetGrass', [[0.8,0.2],
                            [0.4,0.6],
                            [0.3,0.7],
                            [0.1,0.9]], ['Rain', 'Sprinkler'])
print wetgrass

sprinkler = Cpt('Sprinkler', [[0.2,0.8],                          
                              [0.7,0.3]], ['Cloudy'])
print sprinkler

wetgrass.conditioned(dict(Rain=True, Sprinkler=True))

import random



def sample_cpt(cpt, conditioned):
    '''Returns a sample (True/False) from the CPT, given the conditioned variables'''
    _, t= cpt.conditioned(conditioned)
    return (random.uniform(0,1) < t)


import itertools
import networkx as nx
from networkx import DiGraph
from tabulate import tabulate
from bitstring import BitArray
from IPython.display import Image, display_png

class BayesNet(DiGraph, nx.Graph):
    def __init__(self, cpts):
        DiGraph.__init__(self)
        self.cpts = cpts
        self.build_graph()

    def build_graph(self):
        for cpt in self.cpts:
            self.add_node(cpt.node, attr_dict=dict(cpt=cpt, texlbl=cpt.node))
            for parent in cpt.parents:
                self.add_edge(parent, cpt.node)

    def marginal_enumeration(self, query, conditioned):
        '''Returns the marginal probability P(query | conditioned) of 
        the query variable given the conditioned variables'''
        print "query: {}, conditioned: {}".format(query, conditioned)
        assert len(query.keys()) == 1, "Can only have one query variable"
        
        # get conditioned query node
        def getPermutations(n):
            # get all possible combinations of binary variable domain, size n^2
            combinations = []

            for i in range(2**n):
                config = bin(i)[2:].zfill(n) #binary representation of a number
                combinations.append([x == '1' for x in list(config)])
            return combinations

        nodes = self.nodes()
        hidden = [x for x in nodes if (x not in query.keys() and x not in conditioned.keys())]
        
        # get all possible combinations for hidden variable value assignment
        combinations = getPermutations(len(hidden))
        print combinations
        query_pb = []
        z = 0.0 # normalization constant

        # evaluate for both values of query variable
        for b in [True, False] :
            total_pb = 0.0 # intermediate variable to sum up probabilities for different hidden variable assignment
            for c in combinations:
                # for each combination sum up
                states = dict(zip(hidden,c))
                states.update({query.keys()[0]: b})
                states.update(conditioned)
                total_pb += self.probability_configuration(states)
            z += total_pb
            query_pb.insert(0, total_pb)
        query_pb = map(lambda x: x/z, query_pb)
        return query_pb[query[query.keys()[0]]]


    def probability_configuration(self,assignments):
        '''The probability of an assigment of all variables in 
        the Bayesian Network. '''   
        joint_p = 1.0
        for rv,val in assignments.iteritems():
            # for each node get corresponding line in table
            joint_p *= self.node[rv]['cpt'].conditioned(assignments)[val]
        return joint_p          

    def forward_sample(self):
        '''Computes a sample from the prior distribution. 
        Returns a dictionary with the state (True/False) of 
        each variable'''    
        sample = {}
        for n in nx.topological_sort(self): # n: node in ordered list
            # build conditioning for each node
            conditioning = {}
            for parent in self.predecessors(n):
                conditioning.update({parent : sample[parent]})
            sample.update({n:sample_cpt(self.node[n]['cpt'], conditioning)})

        return sample

    def __str__(self):
        return '<Bayes Net' + str(self.nodes())+'>'
        
    def __repr__(self):
        return self.__str__()
    '''
    def as_png(self):
        pd = nx.to_pydot(self)
        pd.write_png('/tmp/out.png')                
        return Image('/tmp/out.png')
    '''


bn = BayesNet([cloudy, rain, sprinkler, wetgrass])


print('Getting all nodes')
print(bn.nodes())
print "=="
print('Accessing the CPT associated to a node')
print(bn.node['Rain']['cpt'])
print "=="
print('Children of a node')
print(bn.successors('Cloudy'))
print "=="
print('Parents of a node')
print(bn.predecessors('Rain'))


def rejection_sampling(bn, query, conditioned, num_samples):    
    '''Computes an approximation to the probability for P(query | conditioned) '''
    count = 0
    hits = 0
    for _ in range(num_samples):
        sample = bn.forward_sample()   
        # check for consistency
        c_check = []
        for c_node, c_val in conditioned.iteritems():
            c_check.append(sample[c_node] == c_val)
        if all(c_check):
            count += 1.0

            q_check = []
            # check query variables
            for q_node, q_val in query.iteritems():
                q_check.append(sample[q_node] == q_val)

            if all(q_check):
                hits += 1.0

    return hits/count


