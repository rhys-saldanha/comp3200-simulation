import itertools
from typing import List, Tuple, Set

import matplotlib.pyplot as plt
import networkx as nx

from simulation import Simulation
from type import Type

resolution = 1000

default_edge_colour = 'gray'
default_node_colour = 'gray'

dominant_node_colour = 'red'
dominant_edge_arrow_colour = 'white'
dominant_edge_bar_colour = 'red'


def line_plot(sim: Simulation, plt=plt, do_reduce=True):
    reduce = __plot_setup(sim, plt, do_reduce)

    legend_list = []
    for e in sim.get_types():
        v, t = list(zip(*sim.get_history(e)[::reduce]))
        plt.plot(t, v)
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


def network(sim: Simulation, nx=nx, plt=plt) -> nx.Graph:
    return network_with_percentages(sim, [], percentages=False, nx=nx, plt=plt)


def network_with_dominant(sim: Simulation, path: List[Type], nx=nx, plt=plt) -> nx.Graph:
    return network_with_percentages(sim, [path], percentages=False, nx=nx, plt=plt)


def network_with_percentages(sim: Simulation, paths: List[List[Type]], percentages=True, nx=nx, plt=plt) -> nx.Graph:
    G = nx.DiGraph()
    G.add_nodes_from([t for t in sim.get_types()])
    G.add_edges_from(list(itertools.chain(*[[(t, c) for c in t.children] for t in sim.get_types()])))
    G.add_edges_from(list(itertools.chain(*[[(t, p) for p in t.parents] for t in sim.get_types()])))

    num_paths = len(paths)
    max_width = 10.0

    dominant_nodes: Set[Type] = set()
    dominant_arcs: Set[Tuple[Type, Type]] = set()

    for p in paths:
        for i, t in enumerate(p[:-1]):
            t_next = p[i + 1]
            if 'weight' in G[t][t_next]:
                G[t_next][t]['weight'] += 1
            else:
                G[t_next][t]['weight'] = 1
            dominant_arcs.add((t_next, t))
        for t in p:
            dominant_nodes.add(t)

    pos = {}
    for t in sim.get_types():
        pos[t] = t.pos

    weights = [G[u][v].get('weight', 0) for u, v in dominant_arcs]

    edge_labels = {}
    if percentages:
        for u, v in dominant_arcs:
            weight = G[u][v].get('weight', 0)
            if weight != 0:
                edge_labels[(u, v)] = '{0:.2f}%'.format((weight * 100) / num_paths)
    for i in range(len(weights)):
        weights[i] = (weights[i] / num_paths) * max_width if weights[i] != 0 else 1

    # Draw base graph with no arrows and labels
    nx.draw(G, pos, node_color=default_edge_colour, edge_color=default_edge_colour, with_labels=True, arrows=False)
    # Draw dominant nodes with correct colour and slightly bigger
    nx.draw_networkx_nodes(G, pos, nodelist=dominant_nodes, node_color=dominant_node_colour, node_size=500)
    # Draw dominant arrow edges without weight change
    nx.draw_networkx_edges(G, pos, edgelist=dominant_arcs,
                           edge_color=dominant_edge_arrow_colour,
                           arrowstyle='-|>', node_size=500)
    # Draw background for dominant edges with weights to show percentages
    nx.draw_networkx_edges(G, pos, edgelist=dominant_arcs, edge_color=dominant_edge_bar_colour, width=weights,
                           arrows=False, node_size=500)
    # Draw edge labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # Draw nodes with default colour to form highlight rings
    nx.draw_networkx_nodes(G, pos, node_color=default_node_colour, with_labels=True)

    # Turn off axises and remove borders
    plt.axis('off')
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                        hspace=0, wspace=0)

    return G
