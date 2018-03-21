import matplotlib.pyplot as plt
import numpy as np
from deprecated import deprecated

from simulation import Simulation


class Plotter:
    @deprecated
    def plot(self, simulation: Simulation, data=True):
        """
        Types do not have a statistics history anymore.
        This kind of statistics graph was not useful for analysis.

        :param Simulation simulation: Simulation object for data
        :param bool data: If `True` will graph the population size of all types
        """
        stats = False

        if data:
            plt.title("Plot of type size over time")
            plt.xlabel("time")
            plt.ylabel("Number of type")
            legend_list = []
            for e in simulation.types:
                v, t = list(zip(*e.history))
                plt.scatter(t, v, marker='x')
                legend_list.append("{}: size".format(e.full_name))
            plt.legend(legend_list, loc='upper left')
            plt.xlim(xmin=0.0, xmax=simulation.tmax)
            plt.ylim(ymin=0)

        if data and stats:
            plt.figure()

        if stats:
            plt.title("Plot of type statistics over time")
            plt.xlabel("time")
            plt.ylabel("Number of type")
            legend_list = []
            cmap = plt.get_cmap('tab10')
            for i, e in enumerate(simulation.types):
                m, v, t = list(zip(*e.stats_history))
                v = list(map(lambda x: np.sqrt(x), v))
                plt.plot(t, m, linestyle="--", c=cmap(i))
                plt.plot(t, v, linestyle=":", c=cmap(i))
                legend_list.append("{}: mean".format(e.full_name))
                legend_list.append("{}: standard deviation".format(e.full_name))
            plt.legend(legend_list, loc='upper left')
            plt.xlim(xmin=0.0, xmax=simulation.tmax)
            plt.ylim(ymin=0)

        plt.show()
