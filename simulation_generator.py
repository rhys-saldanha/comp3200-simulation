import itertools
import json
from collections import namedtuple
from functools import reduce
from typing import List, Set, Tuple, Dict, Sequence

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

    def __init__(self, **kwargs):
        self.__save_history: bool = kwargs.get('history', False)
        self.__print: bool = kwargs.get('print', False)

    def config_file(self, filename: str):
        if '.json' != filename[-5:]:
            filename += '.json'
        with open(filename, 'r') as f:
            data = json.load(f)

        if type(data['wildtype']) is str:
            data['wildtype'] = tuple(data['wildtype'])
        for i, m in enumerate(data['mutated']):
            if type(m) is str:
                data['mutated'][i] = tuple(m)
        ks = list(data['rates'].keys())
        for k in ks:
            v = data['rates'][k]
            data['rates'][tuple(k)] = tuple(v)
            del data['rates'][k]
        data['default_rate'] = tuple(data['default_rate'])
        print(data['rates'])
        return self.parameters(**data)

    def parameters(self, wildtype: Tuple, mutated: List[Tuple],
                   rates: Dict[Sequence[str], Tuple[float, float]] = False,
                   default_rate: Tuple[float, float] = (0.0, 1.0),
                   mutation_rates: Dict[Mutation, float] = False, default_mutation_rate: float = 0.001,
                   wildtype_size: int = None, size: int = 200) -> Simulation:
        for m in mutated:
            if len(wildtype) != len(m):
                raise ParameterError('wildtype and mutated must have the same number of genes')
        if not rates:
            rates = dict()
        if not mutation_rates:
            mutation_rates = dict()
        if not wildtype_size:
            wildtype_size = size

        all_seq = self.all_seq(wildtype, *mutated)

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

                targets = self.partial_match(wildtype, source, all_seq, i + 1) - used_sources

                for target in targets:
                    types[source].add_mutation(types[target], mutation_rates.get(self.Mutation(source, target),
                                                                                 default_mutation_rate))

                    types[source].add_child(types[target])
                    types[target].add_parent(types[source])

                    types[target].add_mutation(types[source], mutation_rates.get(self.Mutation(target, source),
                                                                                 default_mutation_rate))

            used_sources |= sources
            sources = self.partial_match_list(wildtype, sources, all_seq, i + 1) - used_sources

        return Simulation(*types.values(), max=size, wildtype=types[wildtype],
                          finals=[types[t] for t in finals], history=self.__save_history, print=self.__print)

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
    # sim = Generator.parameters(('0', '0', '0', '0', '0', '0'), ('1', '1', '1', '1', '1', '1'),
    #                            ('1', '1', '1', '1', '2', '1'))

    # sim = Generator.parameters(tuple('abc'), tuple('ABC'), tuple('ABD'), size=10000, wildtype_size=10000,
    #                            default_rate=(10.0, 9.))

    # sim = Generator.parameters(('a', 'b', 'c', 'd', 'e', 'f'), ('A', 'B', 'C', 'D', 'E1', 'F'),
    #                            ('A', 'B', 'C', 'D', 'E2', 'F'))

    # for t in sim.get_types:
    #     print('{}, {}'.format(str(t), list(map(lambda x: '{}: {}'.format(str(x[0]), x[1]), t.mutations))))

    # for t in sim.get_types():
    #     print('children: {}, {}'.format(t, list(map(str, t.children))))
    #     print('parents: {}, {}'.format(t, list(map(str, t.parents))))
    #     print('-----')
    #
    # print('number of types: {}'.format(len(sim.get_types())))

    # network(sim, nx)
    # plt.show()

    gen = Generator()

    sim = gen.config_file('parameters/abc_ABC_D.json')
    # print([str(t) for t in sim.get_types()])
    network(sim, nx)
    plt.show()
