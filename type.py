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
        self.history = list()
        self.size = initial_size
        self.initial_size = initial_size

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

        self.update(Event.NOTHING, 0.0, False)

    def update(self, op: Event, time: float, mutate: bool = True):
        # Check that you haven't already been updated for this time
        if self.time != time:
            # Check that you're allowed to mutate and you're a birth update
            if mutate and op == Event.BIRTH:
                self.find_mutation(time)
            else:
                # Otherwise update your own values
                self.size += op.value
                self.time = time
                self.record()

                # self.record_stats()

    def record(self):
        self.n += 1
        self.mean, self.sum = self._calc_mean(self.sum, self.size, self.n)
        self.var, self.sumsq = self._calc_var(self.sumsq, self.mean, self.size, self.n)

        self.history.append((self.size, self.time))

    def record_stats(self):
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
        self.mutation_total = sum([x[1] for x in self.mutations])
        # if total != 1:
        #     # Normalise
        #     self.mutations = list(map(lambda x: (x[0], x[1] / total), self.mutations))

    def find_mutation(self, time: float):
        n = np.random.uniform(high=self.mutation_total)
        t = 0
        # Loop through mutations
        for e, r in self.mutations:
            t += r
            # If argument is within the new total, we've found the mutation it applies to
            if n < t:
                # A mutation event cannot itself mutate
                e.update(Event.BIRTH, time, False)
                break

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return '{} ({},{})'.format(self.name, *self.rates.values(), self.size)

    @staticmethod
    def _get_sizes(d: List[Tuple[float, float]]) -> List[float]:
        return list(list(zip(*d))[0])

    @staticmethod
    def _calc_mean(sum, size, n):
        sum += size
        return sum / n, sum

    @staticmethod
    def _calc_var(sumsq, mean, size, n):
        sumsq += np.square(size)
        return (sumsq / n) - np.square(mean), sumsq
