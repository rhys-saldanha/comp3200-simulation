import itertools
from typing import List

import networkx as nx
import matplotlib.pyplot as plt

from simulation import Simulation
from type import Type

resolution = 1000


def line_plot(types: List[Type], tmax: int, size_max: int, plt=plt):
    """
    Types do not have a statistics history anymore.
    This kind of statistics graph was not useful for analysis.

    :param plt:
    :param size_max:
    :param int tmax: maximum time of simulation
    :param List[Type] types: list of types to plot
    """
    plt.title("Plot of type size over time")
    plt.xlabel("time")
    plt.ylabel("Number of type")

    num_points = len(types[0].history)
    reduce = int(num_points / (resolution * tmax))

    legend_list = []
    for e in types:
        v, t = list(zip(*e.history[::reduce]))
        plt.scatter(t, v, marker='.')
        legend_list.append('{}'.format(e.full_name))
    plt.legend(legend_list, loc='upper left')
    plt.ylim((0, size_max))
    plt.xlim((0, tmax))


def stacked_plot(types: List[Type], tmax: int, size_max: int, plt=plt):
    plt.xlabel("time")
    plt.ylabel("Number of type")

    num_points = len(types[0].history)
    reduce = int(num_points / (resolution * tmax))

    times = types[0].get_times[::reduce]
    histories = [t.get_sizes[::reduce] for t in types]
    labels = list(map(str, types))

    plt.stackplot(times, histories, labels=labels)
    plt.legend(loc='lower right')
    plt.ylim((0, size_max))
    plt.xlim((0, tmax))


def network_with_dominant(sim: Simulation, nx=nx) -> None:
    G = nx.Graph()

    G.add_nodes_from(sim.get_types)

    G.add_edges_from(list(itertools.chain(*[[(t, c) for c in t.children] for t in sim.get_types])))

    pos = {}

    t = None
    ts = sim.finals
    while t != sim.wildtype:
        prev_t = t
        t = max(ts, key=lambda x: x.max_size)

        if prev_t and t:
            G[prev_t][t]['color'] = 'r'

        ts = t.parents

    for t in sim.get_types:
        pos[t] = t.pos

    nx.draw(G, pos=pos, edge_color=[G[u][v].get('color', 'b') for u, v in G.edges()], with_labels=True)


def network(sim: Simulation, nx=nx):
    G = nx.Graph()

    G.add_nodes_from(sim.get_types)

    G.add_edges_from(list(itertools.chain(*[[(t, c) for c in t.children] for t in sim.get_types])))

    pos = {}

    for t in sim.get_types:
        pos[t] = t.pos

    nx.draw(G, pos=pos, with_labels=True)


def network_with_percentages(sims: List[Simulation], nx=nx):
    pass