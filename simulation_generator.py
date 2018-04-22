import itertools
from collections import namedtuple
from functools import reduce
from typing import List, Set, Tuple, Dict

import matplotlib.pyplot as plt
import networkx as nx

from data_plot import network
from simulation import Simulation
from type import Type


class ParameterError(Exception):
    def __init__(self, s):
        self.message = s

    def __str__(self):
        return 'Parameter error: ' + self.message


class Generator:
    Mutation = namedtuple('Mutation', ['source', 'target'])

    @staticmethod
    def config_file(filename: str):
        # TODO generate Types and Simulation from file
        print('Not implemented')
        pass

    @staticmethod
    def parameters(wildtype: Tuple, *mutated: Tuple,
                   rates: Dict[Tuple[str, str], Tuple[float, float]] = False,
                   default_rate: Tuple[float, float] = (0.0, 1.0),
                   mutation_rates: Dict[Mutation, float] = False, default_mutation_rate: float = 0.001,
                   wildtype_size: int = 200, size: int = 200) -> Simulation:
        for m in mutated:
            if len(wildtype) != len(m):
                raise ParameterError('wildtype and mutated must have the same number of genes')
        if not rates:
            rates = dict()
        if not mutation_rates:
            mutation_rates = dict()

        all_seq = Generator.all_seq(wildtype, *mutated)

        types: Dict[Tuple, Type] = dict()

        types[wildtype] = Type(''.join(wildtype), wildtype_size, *rates.get(wildtype, default_rate))

        for seq in all_seq:
            types[seq] = Type(''.join(seq), wildtype_size if seq == wildtype else 0,
                              *rates.get(seq, default_rate))

        sources = {wildtype}
        used_sources = set()
        finals = []
        for i in range(0, len(wildtype) + 1):
            finals = sources
            for s, source in enumerate(sources):
                types[source].pos = (i, s / len(sources))

                targets = Generator.partial_match(wildtype, source, all_seq, i + 1) - used_sources

                for target in targets:
                    types[source].add_mutation(types[target], mutation_rates.get(Generator.Mutation(source, target),
                                                                                 default_mutation_rate))

                    types[source].add_child(types[target])
                    types[target].add_parent(types[source])

                    types[target].add_mutation(types[source], mutation_rates.get(Generator.Mutation(target, source),
                                                                                 default_mutation_rate))

            used_sources |= sources
            sources = Generator.partial_match_list(wildtype, sources, all_seq, i + 1) - used_sources

        return Simulation(*types.values(), max=size, wildtype=types[wildtype],
                          finals=[types[t] for t in finals])

    @staticmethod
    def all_seq(wildtype, *mutated) -> List:
        # Given the wildtype and fully mutated strains as lists,
        # create all intermediate stages
        return Generator.f7(itertools.product(*zip(wildtype, *mutated)))

    @staticmethod
    def partial_match_list(wildtype, sources, all_seq, l) -> Set:
        # partial match for every source, chain together results, remove repeats
        return set(
            itertools.chain.from_iterable(map(lambda x: Generator.partial_match(wildtype, x, all_seq, l), sources)))

    @staticmethod
    def partial_match(wildtype, source, all_seq, l) -> Set:
        return set([target for target in all_seq if
                    # reduce(lambda x, y: x + 1 if y[0] != y[1] else x, zip(wildtype, target), 0) == l and
                    reduce(lambda x, y: x + 1 if y[0] != y[1] else x, zip(source, target), 0) == 1])

    @staticmethod
    def f7(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]


if __name__ == '__main__':
    sim = Generator.parameters(('0', '0', '0', '0', '0', '0'), ('1', '1', '1', '1', '1', '1'),
                               ('1', '1', '1', '1', '2', '1'))

    # sim = Generator.parameters(('a', 'b', 'c', 'd', 'e', 'f'), ('A', 'B', 'C', 'D', 'E1', 'F'),
    #                            ('A', 'B', 'C', 'D', 'E2', 'F'))

    # for t in sim.get_types:
    #     print('{}, {}'.format(str(t), list(map(lambda x: '{}: {}'.format(str(x[0]), x[1]), t.mutations))))

    # for t in sim.get_types:
    #     print('{}, {}'.format(t, list(map(str, t.children))))
    #     print('{}, {}'.format(t, list(map(str, t.parents))))
    #     print('-----')

    print('number of types: {}'.format(len(sim.get_types)))

    network(sim, nx)
    plt.show()
