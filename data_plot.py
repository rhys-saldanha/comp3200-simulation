from typing import List

import matplotlib.pyplot as plt
import seaborn as sns
from deprecated import deprecated

from type import Type


class LinePlot:
    @deprecated
    def plot(self, types: List[Type], tmax: int, size_max: int):
        """
        Types do not have a statistics history anymore.
        This kind of statistics graph was not useful for analysis.

        :param int tmax: maximum time of simulation
        :param List[Type] types: list of types to plot
        """
        plt.title("Plot of type size over time")
        plt.xlabel("time")
        plt.ylabel("Number of type")

        legend_list = []
        for e in types:
            v, t = list(zip(*e.history))
            plt.scatter(t, v, marker='.')
            legend_list.append("{}: size".format(e.full_name))
        plt.legend(legend_list, loc='upper left')
        plt.ylim((0, size_max))
        plt.xlim((0, tmax))

        plt.show()


class StackedPlot:
    def plot(self, types: List[Type], tmax: int, size_max: int):
        plt.xlabel("time")
        plt.ylabel("Number of type")

        times = types[0].get_times
        histories = list(map(lambda t: t.get_sizes, types))
        labels = list(map(str, types))

        plt.stackplot(times, histories, labels=labels)
        plt.legend(loc='lower right')
        plt.ylim((0, size_max))
        plt.xlim((0, tmax))

        plt.show()
