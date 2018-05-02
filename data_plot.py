import itertools
from typing import List

import matplotlib.pyplot as plt
import networkx as nx

from simulation import Simulation
from type import Type

resolution = 1000
default_colour = 'gray'
dominant_colour = 'r'


def line_plot(sim: Simulation, plt=plt, do_reduce=True):
    reduce = __plot_setup(sim, plt, do_reduce)

    legend_list = []
    for e in sim.get_types():
        v, t = list(zip(*sim.get_history(e)[::reduce]))
        plt.scatter(t, v, marker='.')
        legend_list.append('{}'.format(e.full_name))
    plt.legend(legend_list, loc='upper left')


def stacked_plot(sim: Simulation, plt=plt, do_reduce=True):
    reduce = __plot_setup(sim, plt, do_reduce)

    times = sim.get_times(sim.wildtype)[::reduce]
    histories = [sim.get_sizes(t)[::reduce] for t in sim.get_types()]
    labels = list(map(str, sim.get_types()))

    plt.stackplot(times, histories, labels=labels)
    plt.legend(loc='lower right')


def __plot_setup(sim: Simulation, plt=plt, do_reduce=True):
    if not sim.check_history():
        raise Exception('This simulation has no history')

    plt.title("Plot of type size over time")
    plt.xlabel("time")
    plt.ylabel("Number of type")
    plt.ylim((0, sim.get_pop_max()))
    plt.xlim((0, sim.get_tmax()))
    num_points = len(sim.get_history(sim.get_types()[0]))
    return max(1, int(num_points / resolution)) if do_reduce else 1


def network(sim: Simulation, nx=nx) -> nx.Graph:
    return network_with_percentages(sim, [], percentages=False, nx=nx)


def network_with_dominant(sim: Simulation, nx=nx) -> nx.Graph:
    return network_with_percentages(sim, [sim.get_dominant_path()], percentages=False, nx=nx)


def network_with_percentages(sim: Simulation, paths: List[List[Type]], percentages=True, nx=nx) -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from([t for t in sim.get_types()])
    G.add_edges_from(list(itertools.chain(*[[(t, c) for c in t.children] for t in sim.get_types()])))

    num_paths = len(paths)
    node_colour = {}
    max_width = 10.0

    for p in paths:
        for i, t in enumerate(p[:-1]):
            t_next = p[i + 1]
            if 'weight' in G[t][t_next]:
                G[t][t_next]['weight'] += 1
            else:
                G[t][t_next]['weight'] = 1
            if 'colour' not in G[t][t_next]:
                G[t][t_next]['colour'] = dominant_colour
        for t in p:
            if t not in node_colour:
                node_colour[t] = dominant_colour

    pos = {}
    for t in sim.get_types():
        pos[t] = t.pos

    edge_colour = [G[u][v].get('colour', default_colour) for u, v in G.edges()]
    weights = [G[u][v].get('weight', 0) for u, v in G.edges()]
    node_colour = [node_colour.get(u, default_colour) for u in G]

    edge_labels = {}
    if percentages:
        for u, v in G.edges():
            weight = G[u][v].get('weight', 0)
            if weight != 0:
                edge_labels[(u, v)] = '{0:.2f}%'.format((weight * 100) / num_paths)
    for i in range(len(weights)):
        weights[i] = (weights[i] / num_paths) * max_width if weights[i] != 0 else 1

    nx.draw(G, pos=pos, node_color=node_colour, edge_color=edge_colour, width=weights, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    return G
