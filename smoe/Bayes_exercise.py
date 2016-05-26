import sys
import itertools
import networkx as nx
from networkx import DiGraph
from tabulate import tabulate
from bitstring import BitArray


class Cpt:

    def __init__(self, node, probabilities, parents=None):
        parents = parents or []
        self.node = node
        self.domain = [False, True]
        self.parents = parents
        self.probabilities = probabilities
        self.check_cpt()
        self.bitlen = len(self.parents)

    def complete_cpt(self):
        '''For binary variables, prepend P(false) given P(true)'''
        complete_probabilities = []
        for row in self.probabilities:
            ptrue = row[0]
            complete_probabilities.append([1 - ptrue, ptrue])
        self.probabilities = complete_probabilities

    def check_cpt(self):
        if 2 ** (len(self.parents)) != len(self.probabilities):
            raise ValueError(
                "{}: Number of parents incompatible with probability table")
        for row in self.probabilities:
            if len(row) != 2:
                raise ValueError(
                    "{}: Row does not have 2 values:{}".format(self.node, row))
            if not 0.99999 < sum(row) < 1.00001:
                raise ValueError(
                    "{}: Row is not normalized:{}".format(self.node, row))

    def get(self, configuration):
        conditional_row = self.conditioned(configuration)
        node_val = int(configuration[self.node])

        return conditional_row[node_val]

    def conditioned(self, conditioned):
        '''Returns the row of the Cpt specified by the truth value of the conditioned parents'''
        parent_config = []
        for parent in self.parents:
            try:
                parent_config.append(conditioned[parent])
            except KeyError:
                raise KeyError(
                    "The truth value of all parents must be given. Missing {}".format(parent))
        try:
            row = BitArray(parent_config or [0]).uint
        except:
            print "error: node:{} conditioned:{}, parent_config:{}".format(self.node, conditioned, parent_config)
            raise
        return self.probabilities[row]

    def conditioned_config(self, row):
        '''Returns the configuration of the conditioned variables for a given or row of the CPT'''
        number = row
        num_bits = len(self.parents)

        return [bool((number >> bit) & 1) for bit in range(num_bits - 1, -1, -1)]

    def formated(self, tablefmt="pipe"):
        '''tablefmt must be a format accepted by the tabular packagesee plain,simple,grid,pipe,orgtbl,rst,mediawiki,latex'''
        table = []
        for i, row in enumerate(self.probabilities):
            conditioned = [['False', 'True'][r]
                           for r in self.conditioned_config(i)]
            table.append([str(r) for r in conditioned + row])
        if tablefmt == 'html':
            import HTML
            fillers = [HTML.TableCell()] * len(self.parents)
            title = HTML.TableCell(
                self.node, style='font-weight:bold;', attribs={'colspan': 2})
            htmlcode = HTML.table([self.parents + ['False', "True"]] +
                                  table, header_row=fillers + [title], style='', border='')
            from IPython.display import display_html
            from IPython.display import HTML as IPHTML

            return IPHTML(htmlcode)
        else:
            return '\n' + '\t' * (len(self.parents) + 1) + '' + str(self.node) + '' + '\n' + tabulate(table, headers=self.parents + ['False', "True"], tablefmt=tablefmt) + '\n'

    def write_to_file(self, filename, tablefmt='pipe'):
        with open(filename, 'w') as f:
            f.write(self.formated(tablefmt=tablefmt))

    def __repr__(self):
        return self.formated()

