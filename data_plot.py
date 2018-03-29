from typing import List

import matplotlib.pyplot as plt
from deprecated import deprecated

from type import Type


class Plotter:
    @deprecated
    def plot(self, types: List[Type], tmax: int):
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
        plt.xlim(xmin=0.0, xmax=tmax)
        plt.ylim(ymin=0)

        # plt.title("Plot of type statistics over time")
        # plt.xlabel("time")
        # plt.ylabel("Number of type")
        # legend_list = []
        # cmap = plt.get_cmap('tab10')
        # for i, e in enumerate(simulation.__types):
        #     m, v, t = list(zip(*e.stats_history))
        #     v = list(map(lambda x: np.sqrt(x), v))
        #     plt.plot(t, m, linestyle="--", c=cmap(i))
        #     plt.plot(t, v, linestyle=":", c=cmap(i))
        #     legend_list.append("{}: mean".format(e.full_name))
        #     legend_list.append("{}: standard deviation".format(e.full_name))
        # plt.legend(legend_list, loc='upper left')
        # plt.xlim(xmin=0.0, xmax=simulation.__tmax)
        # plt.ylim(ymin=0)

        plt.show()
