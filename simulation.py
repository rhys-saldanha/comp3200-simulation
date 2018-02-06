from time import time
from typing import List

import numpy as np
import pylab as plt

from type import Type


class Simulation:
    def __init__(self, *types: Type):
        self.types: List[Type] = types
        self.time = 0
        self._update_values()
        # Set population maximum equal to initial population
        self.pop_max: int = self.size

    def run(self, t: float) -> None:
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
        self.plot(t)

    def _cycle(self):
        # Move time forwards
        self.time += self._time_nothing
        # Find type with operation event
        t, op = self._choose_event_any()

        # If birth and we are at our max pop, we need a death
        if op == 1 and self.size == self.pop_max:
            d = self._choose_event('death')
            # Only update with death if types are different, otherwise they cancel
            if d != t:
                d.update(-1, self.time)
            else:
                # Update with nothing to prevent birth
                d.update(0, self.time)

        # Update initial type choice with operation
        # May result in mutation and operation to different type
        t.update(op, self.time)
        for t in self.types:
            t.update(0, self.time)

        self._update_values()

    @property
    def _time_nothing(self) -> float:
        r = np.random.uniform()
        return -1.0 * np.log(r) / self.probability_total

    def _update_values(self):
        # Reduce the number of computations to only when values have been changed
        self.probability = {'birth': sum(map(lambda t: t.probability('birth'), self.types)),
                            'death': sum(map(lambda t: t.probability('death'), self.types))}
        self.probability_total = sum(self.probability.values())
        self.size = sum(map(lambda t: t.size, self.types))

    def _choose_event_any(self) -> (Type, int):
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

    def plot(self, tmax: float, data=True, stats=True):
        if data:
            plt.title("Plot of type size over time")
            plt.xlabel("time")
            plt.ylabel("Number of type")
            legend_list = []
            for e in self.types:
                v, t = list(zip(*e.history))
                plt.plot(t, v)
                legend_list.append("{}: size".format(e.full_name))
            plt.legend(legend_list, loc='upper left')
            plt.xlim(xmin=0.0, xmax=tmax)
            plt.ylim(ymin=0)
        if data and stats:
            plt.figure()
        if stats:
            plt.title("Plot of type statistics over time")
            plt.xlabel("time")
            plt.ylabel("Number of type")
            legend_list = []
            cmap = plt.get_cmap('tab10')
            for i, e in enumerate(self.types):
                m, v, t = list(zip(*e.stats_history))
                v = list(map(lambda x: np.sqrt(x), v))
                plt.plot(t, m, linestyle="--", c=cmap(i))
                plt.plot(t, v, linestyle=":", c=cmap(i))
                legend_list.append("{}: mean".format(e.full_name))
                legend_list.append("{}: standard deviation".format(e.full_name))
            plt.legend(legend_list, loc='upper left')
            plt.xlim(xmin=0.0, xmax=tmax)
            plt.ylim(ymin=0)
        plt.show()
