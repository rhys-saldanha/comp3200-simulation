import itertools
from collections import namedtuple
from typing import List, Set, Tuple, Dict

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
    def parameters(wildtype: Tuple, mutated: Tuple,
                   rates: Dict[Tuple[str, str], Tuple[float, float]] = False, default_rate: float = (0.0, 1.0),
                   mutation_rates: Dict[Mutation, float] = False, default_mutation_rate: float = 0.001,
                   wildtype_size: int = 200, size: int = 200) -> Simulation:
        if len(wildtype) != len(mutated):
            raise ParameterError('wildtype and mutated must have the same number of genes')
        if not rates:
            rates = dict()
        if not mutation_rates:
            mutation_rates = dict()

        all_seq = Generator.__all_seq(wildtype, mutated)

        types: Dict[Tuple, Type] = dict()

        types[wildtype] = Type(''.join(wildtype), wildtype_size, *rates.get(wildtype, default_rate))

        for seq in all_seq:
            types[seq] = Type(''.join(seq), wildtype_size if seq == wildtype else 0,
                              *rates.get(seq, default_rate))

        sources = {wildtype}
        used_sources = set()
        for i in range(len(wildtype) + 1):
            for source in sources:
                source_type = types[source]
                # source_type.add_mutation(source_type, mutation_rates.get(Generator.Mutation(source, source),
                #                                                          1.0 - default_mutation_rate))

                targets = Generator.__partial_match(source, all_seq)

                for target in targets:
                    target_type = types[target]

                    # target_type.add_mutation(target_type, mutation_rates.get(Generator.Mutation(target, target),
                    #                                                          1.0 - default_mutation_rate))

                    source_type.add_mutation(target_type, mutation_rates.get(Generator.Mutation(source, target),
                                                                             default_mutation_rate))

                    target_type.add_mutation(source_type, mutation_rates.get(Generator.Mutation(target, source),
                                                                             default_mutation_rate))
            used_sources |= sources
            sources = Generator.__partial_match_list(sources, all_seq) - used_sources

        for t in types.values():
            t.add_self_mutation()

        print(list(map(lambda t: str(t), types.values())))
        print(list(map(lambda t: str(t.mutations), types.values())))

        return Simulation(*types.values(), max=size)

    @staticmethod
    def __all_seq(wildtype, mutated) -> List:
        return list(itertools.product(*zip(wildtype, mutated)))

    @staticmethod
    def __partial_match_list(sources, targets, d=1) -> Set:
        # partial match for every source, chain together results, remove repeats
        return set(itertools.chain.from_iterable(map(lambda x: Generator.__partial_match(x, targets, d), sources)))

    @staticmethod
    def __partial_match(source, targets, d=1) -> Set:
        # Uses set symmetric difference
        source = set(source)
        # 1 difference gives 2 options
        d *= 2
        return set(filter(lambda x: len(set(x) ^ source) == d, targets))
