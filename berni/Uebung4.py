from Bayes_exercise import Cpt
import itertools
import networkx as nx
from networkx import DiGraph
from tabulate import tabulate
from bitstring import BitArray
from IPython.display import Image, display_png
import random

#Here we say that there is a 0.1 probability of raining if there are no clouds, and 0.8 if it is cloudy
rain = Cpt('Rain', [[0.9, 0.1],[0.2, 0.8]], ['Cloudy'])

cloudy = Cpt('Cloudy', [[0.6, 0.4]],[])

wetgrass = Cpt('WetGrass', [[0.8, 0.2],
                            [0.4, 0.6],
                            [0.3, 0.7],
                            [0.1, 0.9]], ['Rain', 'Sprinkler'])
sprinkler = Cpt('Sprinkler', [[0.2, 0.8],
                              [0.7, 0.3]], ['Cloudy'])


conditioned_state = dict(Rain=True, Sprinkler=False)
wetgrass.conditioned(conditioned_state)


def sample_cpt(cpt, conditioned):
    '''Returns a sample (True/False) from the CPT, given the conditioned variables'''
    [f, _ ] = cpt.conditioned(conditioned)
    r = random.random()
    if r <= f:
        return False
    else:
        return True

# This function is here for convenience and grading, there is no need to modify it.
def sample_cpt_multiple(cpt,conditioned,num_samples):
    '''Returns multiple samples from the the CPT'''
    return [sample_cpt(cpt, conditioned) for _ in range(num_samples)]



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

        Pcond = 0.0
        Pnorm = 0.0
        Nodes = self.nodes()
        hiddenNodes = [n for n in Nodes if (n not in query.keys()) and (n not in conditioned.keys())]
        D1 = list(itertools.product([False, True], repeat=len(hiddenNodes)))

        assignment = dict()
        assignment.update(query)
        assignment.update(conditioned)

        for assign in D1:   # calculate query likelyhood that is conditioned
            tmp_dict = dict(zip(hiddenNodes, assign))
            assignment.update(tmp_dict)
            Pcond = Pcond + self.probability_configuration(assignment)

        newassignemt = dict()
        newassignemt.update(conditioned)
        restNodes = [m for m in Nodes if (m not in conditioned.keys())]
        D2 = list(itertools.product([False, True], repeat=len(restNodes)))

        for assign in D2:   # calculate likelyhood of condition
            tmp_dict = dict(zip(restNodes, assign))
            newassignemt.update(tmp_dict)
            Pnorm = Pnorm + self.probability_configuration(newassignemt)

        return Pcond / Pnorm


    def probability_configuration(self,assignments):
        '''The probability of an assigment of all variables in
        the Bayesian Network. '''
        totalProb = 1.0
        Nodes = self.nodes()
        for n in Nodes:
            val = assignments[n]
            Probabilities = self.node[n]['cpt'].conditioned(assignments)
            totalProb = totalProb*Probabilities[val]
        return totalProb

    def forward_sample(self):
        '''Computes a sample from the prior distribution.
        Returns a dictionary with the state (True/False) of
        each variable'''

        nodeOrder = nx.topological_sort(self)
        T = [False for n in nodeOrder]
        assignment = dict(zip(nodeOrder,T))
        for n in nodeOrder:
            cpt = self.node[n]['cpt']
            assignment[n] = sample_cpt(cpt,assignment)

        return assignment


    def __str__(self):
        return '<Bayes Net' + str(self.nodes())+'>'

    def __repr__(self):
        return self.__str__()
    """
    def as_png(self):
    pd = nx.to_pydot(self)
    pd.write_png('/tmp/out.png')
    return Image('/tmp/out.png')
    """

def rejection_sampling(bn, query, conditioned, num_samples):
    '''Computes an approximation to the probability for P(query | conditioned) '''
    count = 0.0
    match = 0.0
    for _ in range(num_samples):
        sample = bn.forward_sample()
        c = [conditioned[item] == sample[item] for item in conditioned.keys()] # check sample for consistency
        if all(c):
            count += 1.0
            q = [sample[q] == query[q] for q in query.keys()] # check query
            if all(q):
                match += 1.0
    return match/count




bn = BayesNet([cloudy, rain, sprinkler, wetgrass])
assignments = dict(Sprinkler=True,WetGrass=False,Rain=True,Cloudy=True)
bn.probability_configuration(assignments)
bn.forward_sample()
#bn.marginal_enumeration(query=dict(Rain=True), conditioned=dict(WetGrass=False))
rejection_sampling(bn, dict(WetGrass=True, Rain=False), dict(Cloudy=True), 100)
"""
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
"""
