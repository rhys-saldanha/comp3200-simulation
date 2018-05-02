import random
from enum import Enum
from typing import List, Tuple

import numpy as np
from deprecated import deprecated


class Event(Enum):
    NOTHING = 0
    BIRTH = 1
    DEATH = -1


class Type:
    mutations: List[Tuple['Type', float]]
    pos: Tuple[int, int]
    name = 'default'

    def __init__(self, name: str, initial_size: int, birth_rate: float = 1.0, death_rate: float = 1.0):
        if initial_size < 0:
            raise ValueError('Initial size must be positive')
        if birth_rate < 0:
            raise ValueError('Birth rate must be positive')
        if death_rate < 0:
            raise ValueError('Death rate must be positive')
        if death_rate == 0:
            raise ValueError('Death rate must be non-zero')

        self.name = name
        self.rates = {Event.BIRTH: birth_rate, Event.DEATH: death_rate}
        self.full_name = "{}({},{})".format(self.name, *self.rates.values())

        self.time = -1.0
        # self.history = list()
        self.size = self.max_size = self.initial_size = initial_size

        self.stats_history = list()
        self.sum = 0.0
        self.sumsq = 0.0
        self.mean = 0.0
        self.var = 0.0
        self.n = 0

        self.mutations = list()
        self.mutation_total = 0.0
        # Initialise with no mutation options except self
        # self.add_mutation(self, 1.0)

        self.children: List['Type'] = list()
        self.parents: List['Type'] = list()

        self.update(Event.NOTHING, 0.0, False)

    def sim_init(self):
        # Things to do once the type object is passed to the Simulation
        mutations = set([m for m, _ in self.mutations if m != self])
        relations = set(self.parents + self.children)
        all_types = mutations | relations
        if len(mutations) < len(all_types):
            raise Exception('A parent or child isn\'t mentioned in the mutations')
        if len(relations) < len(all_types):
            raise Exception('A mutation isn\'t mentioned in the parents or children')
        self.add_self_mutation()

    def update(self, op: Event, time: float, mutate: bool = True) -> int:
        # Check that you haven't already been updated for this time
        if self.time != time:
            # Check that you're allowed to mutate and you're a birth update
            if mutate and op == Event.BIRTH:
                return self.find_mutation(time)
            else:
                # Otherwise update your own values
                self.size += op.value
                self.max_size = max(self.size, self.max_size)
                self.time = time
                # self.history.append((self.size, self.time))
                # self.record_stats()

        return self.size

    def record_stats(self):
        self.n += 1
        self.mean, self.sum = self._calc_mean(self.sum, self.size, self.n)
        self.var, self.sumsq = self._calc_var(self.sumsq, self.mean, self.size, self.n)
        self.stats_history.append((self.mean, self.var, self.time))

    def probability(self, s: Event) -> float:
        return self.rates[s] * self.size

    @deprecated
    def add_mutations(self, no_mutation: float, *args: Tuple['Type', float]):
        """
        Add mutation targets to a type of individual with probabilities. If the sum of probabilities
        is greater than 1 it will be normalised.

        :param no_mutation: probability of no mutation
        :param args: tuples of a Type and its mutation probability
        """
        s = sum([x[1] for x in args]) + no_mutation
        no_mutation = no_mutation / s
        self.mutations: List[Tuple['Type', float]] = [(x[0], x[1] / s) for x in args]
        self.mutations.append((self, no_mutation))

    def add_mutation(self, target, probability):
        if len(self.mutations) == 0 or target not in list(zip(*self.mutations))[0]:
            self.mutations.append((target, probability))
        self.set_mutation_total()
        # if total != 1:
        #     # Normalise
        #     self.mutations = list(map(lambda x: (x[0], x[1] / total), self.mutations))

    def add_self_mutation(self):
        if self not in map(lambda m: m[0], self.mutations):
            self.mutations.append((self, 1.0 - sum([m[1] for m in self.mutations])))
            self.set_mutation_total()

    def set_mutation_total(self):
        self.mutation_total = sum([m[1] for m in self.mutations])

    def find_mutation(self, time: float) -> int:
        r = random.uniform(0., self.mutation_total)
        total = 0.
        # Loop through mutations
        for e, p in self.mutations:
            total += p
            # If argument is within the new total, we've found the mutation it applies to
            if r <= total:
                # A mutation event cannot itself mutate
                return e.update(Event.BIRTH, time, False)
        assert False, 'Shouldn\'t get here'

    # @property
    # def get_sizes(self) -> List[float]:
    #     return list(list(zip(*self.history))[0])
    #
    # @property
    # def get_times(self) -> List[float]:
    #     return list(list(zip(*self.history))[1])

    def __eq__(self, other):
        return type(other) is Type and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return '{}|{}'.format(self.name, self.rates[Event.DEATH], self.size)

    @staticmethod
    def _calc_mean(sum, size, n):
        sum += size
        return sum / n, sum

    @staticmethod
    def _calc_var(sumsq, mean, size, n):
        sumsq += np.square(size)
        return (sumsq / n) - np.square(mean), sumsq

    def add_child(self, c: 'Type'):
        self.children.append(c)

    def add_parent(self, p: 'Type'):
        self.parents.append(p)

    def clone(self) -> 'Type':
        t = Type(self.name, self.initial_size, self.rates[Event.BIRTH], self.rates[Event.DEATH])
        t.pos = self.pos
        return t
