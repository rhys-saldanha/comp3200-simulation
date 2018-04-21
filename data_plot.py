from typing import List

import matplotlib.pyplot as plt
import seaborn as sns
from deprecated import deprecated

from type import Type

resolution = 1000


def line_plot(types: List[Type], tmax: int, size_max: int):
    """
    Types do not have a statistics history anymore.
    This kind of statistics graph was not useful for analysis.

    :param int tmax: maximum time of simulation
    :param List[Type] types: list of types to plot
    """
    plt.title("Plot of type size over time")
    plt.xlabel("time")
    plt.ylabel("Number of type")

    num_points = len(types[0].history)
    reduce = int(num_points / resolution)

    legend_list = []
    for e in types:
        v, t = list(zip(*e.history[::reduce]))
        plt.scatter(t, v, marker='.')
        legend_list.append("{}".format(e.full_name))
    plt.legend(legend_list, loc='upper left')
    plt.ylim((0, size_max))
    plt.xlim((0, tmax))

    plt.show()


def stacked_plot(types: List[Type], tmax: int, size_max: int):
    plt.xlabel("time")
    plt.ylabel("Number of type")

    num_points = len(types[0].history)
    reduce = int(num_points / resolution)

    times = types[0].get_times[::reduce]
    histories = list(map(lambda t: t.get_sizes[::reduce], types))
    labels = list(map(str, types))

    plt.stackplot(times, histories, labels=labels)
    plt.legend(loc='lower right')
    plt.ylim((0, size_max))
    plt.xlim((0, tmax))

    plt.show()
