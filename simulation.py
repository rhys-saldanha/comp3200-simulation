from time import time
from typing import List

import numpy as np

from type import Type


class Simulation:
    def __init__(self, *types: Type, **kwargs):
        self.types: List[Type] = types
        self.time = 0
        self._update_values()
        # Set population maximum equal to initial population
        self.pop_max: int = kwargs.get('max', self.size)
        self.tmax = 0

    def run(self, t: float) -> None:
        self.tmax = t
        print("Running till time {}".format(t))
        maximum_percentage = -1
        t0 = time()
        while self.time < t:
            percentage_completed = int((self.time * 100) / t)
            if percentage_completed > maximum_percentage:
                maximum_percentage = percentage_completed
                if maximum_percentage % 10 == 0:
                    print("{}%\t{:f}s".format(maximum_percentage, time() - t0))
            self._cycle()
        print("Simulation complete in {:f}s".format(time() - t0))

    def _cycle(self):
        # Move time forwards
        self.time += self._time_nothing
        # Find type with operation event
        t, op = self._choose_event_any()

        # If birth and we are over the max pop, we need a death
        if op == 1 and self.size >= self.pop_max:
            d = self._choose_event('death')
            # Only update with death if types are different, otherwise they cancel
            if d != t:
                d.update(-1, self.time)
            else:
                # Update with nothing to prevent birth
                d.update(0, self.time)

        # # If birth and we are over the max pop, do nothing
        # if op == 1 and self.size >= self.pop_max:
        #     t.update(0, self.time)

        # Check we have a type to update
        # as all types may have died out
        if t is not None:
            # Update initial type choice with operation
            # May result in mutation and operation to different type
            t.update(op, self.time)
        for t in self.types:
            t.update(0, self.time)

        self._update_values()

    @property
    def _time_nothing(self) -> float:
        return -1.0 * np.log(np.random.uniform()) / self.probability_total

    def _update_values(self):
        # Reduce the number of computations to only when values have been changed
        self.probability = {'birth': sum(map(lambda t: t.probability('birth'), self.types)),
                            'death': sum(map(lambda t: t.probability('death'), self.types))}
        self.probability_total = sum(self.probability.values())
        self.size = sum(map(lambda t: t.size, self.types))

    def _choose_event_any(self) -> (Type, int):
        if self.probability_total == 0:
            # All types have died out
            return None, 0
        n = np.random.uniform(high=self.probability_total)

        if n > self.probability['birth']:
            return self._choose_event('death', n - self.probability['birth']), -1
        return self._choose_event('birth', n), +1

    def _choose_event(self, s: str, n: float = None) -> Type:
        if n is None:
            n = np.random.uniform(high=self.probability[s])

        t = 0.0
        # Loop through types
        for e in self.types:
            t += e.probability(s)
            # If argument is within the new total, we've found the operation it applies to
            if n < t:
                return e
        # Argument was outside of possible values
        # raise ValueError
