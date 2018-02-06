from time import time

import numpy as np
import pylab as plt

from type import Type


class Simulation:
    def __init__(self, *types: Type):
        self.operations = (+1, -1)
        self.types = types
        self.time = 0

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
        self.time += self._time_nothing()
        e, op = self._find_n_rate(np.random.uniform(high=self._rates_total()))
        e.update(op, self.time)
        for e in self.types:
            e.update(0, self.time)

    def _time_nothing(self) -> int:
        r = np.random.uniform()
        return -1.0 * np.log(r) / self._rates_total()

    def _rates_total(self) -> float:
        return sum(map(lambda e: e.rates_total(), self.types))

    def _find_n_rate(self, n):
        t = 0
        # Loop through types
        for e in self.types:
            # Zip together birth/death rates with the operation they represent
            for r, op in zip(e.rates, self.operations):
                # Add to total
                t += r * e.size
                # If argument is within the new total, we've found the operation it applies to
                if n < t:
                    return e, op

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
