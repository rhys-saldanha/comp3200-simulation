import itertools
from typing import List

import matplotlib.pyplot as plt
import networkx as nx

from simulation import Simulation
from type import Type

resolution = 1000


def line_plot(types: List[Type], tmax: float, size_max: int, plt=plt):
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
    # reduce = int(num_points / (resolution * tmax))
    reduce = int(num_points / (resolution))

    legend_list = []
    for e in types:
        v, t = list(zip(*e.history[::reduce]))
        plt.scatter(t, v, marker='.')
        legend_list.append('{}'.format(e.full_name))
    plt.legend(legend_list, loc='upper left')
    plt.ylim((0, size_max))
    plt.xlim((0, tmax))


def stacked_plot(types: List[Type], tmax: float, size_max: int, plt=plt):
    plt.xlabel("time")
    plt.ylabel("Number of type")

    num_points = len(types[0].history)
    # reduce = int(num_points / (resolution * tmax))
    reduce = int(num_points / (resolution))

    times = types[0].get_times[::reduce]
    histories = [t.get_sizes[::reduce] for t in types]
    labels = list(map(str, types))

    plt.stackplot(times, histories, labels=labels)
    plt.legend(loc='lower right')
    plt.ylim((0, size_max))
    plt.xlim((0, tmax))


def network_with_dominant(sim: Simulation, nx=nx) -> None:
    G = nx.Graph()
    G.add_nodes_from([t for t in sim.get_types()])
    G.add_edges_from(list(itertools.chain(*[[(t, c) for c in t.children] for t in sim.get_types()])))

    # Find largest type at end of simulation
    # t = sim.get_max_type()
    t = max(sim.get_types(), key=lambda t: t.size)
    # print('largest type at end: {}'.format(t))
    ts = t.parents
    # Trace back to wildtype (type with no parents) through largest parent Types
    # while t != sim.wildtype and len(t.parents) != 0:
    for i in range(5):
        if not (t != sim.wildtype and len(t.parents) != 0):
            break
        prev_t = t
        t = max(ts, key=lambda x: x.max_size)
        # print('parents: {}'.format([t.name for t in ts]))
        # print('largest parent: {}'.format(t))
        if prev_t and t:
            G[prev_t][t]['color'] = 'r'

        ts = t.parents

    pos = {}
    for t in sim.get_types():
        pos[t] = t.pos

    nx.draw(G, pos=pos, edge_color=[G[u][v].get('color', 'b') for u, v in G.edges()], with_labels=True)


def network(sim: Simulation, nx=nx):
    G = nx.Graph()
    G.add_nodes_from(sim.get_types())
    G.add_edges_from(list(itertools.chain(*[[(t, c) for c in t.children] for t in sim.get_types()])))

    pos = {}
    for t in sim.get_types():
        pos[t] = t.pos

    nx.draw(G, pos=pos, with_labels=True)


def network_with_percentages(sim: Simulation, paths: List[List[Type]], nx=nx):
    # TODO check simulations are all on the same types, just look at wildtype
    # TODO check simulations all ran for the same time?

    G = nx.Graph()
    G.add_nodes_from([t for t in sim.get_types()])
    G.add_edges_from(list(itertools.chain(*[[(t, c) for c in t.children] for t in sim.get_types()])))

    num_paths = len(paths)

    for p in paths:
        for i, t in enumerate(p[:-1]):
            t_next = p[i + 1]
            if 'weight' in G[t][t_next]:
                G[t][t_next]['weight'] += 1
            else:
                G[t][t_next]['weight'] = 1
            if 'colour' not in G[t][t_next]:
                G[t][t_next]['colour'] = 'r'

    pos = {}
    for t in sim.get_types():
        pos[t] = t.pos

    colours = [G[u][v].get('colour', 'b') for u, v in G.edges()]
    weights = [G[u][v].get('weight', 1) for u, v in G.edges()]
    edge_labels = {}
    for u, v in G.edges():
        weight = G[u][v].get('weight', 0)
        if weight != 0:
            edge_labels[(u, v)] = '{}%'.format((weight * 100) / num_paths)

    nx.draw(G, pos=pos, edge_color=colours, width=weights, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
