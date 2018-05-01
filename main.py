import matplotlib.pyplot as plt
import networkx as nx

import data_plot
import useful
from simulation import Simulation
from simulation_generator import Generator
from type import Type


def mutations_simulation():
    gen = Generator(prints=True)
    sim = gen.config_file('parameters/two_paths_ABC.json')

    # data_plot.network(sim, nx)
    # plt.show()

    # for t in sim.get_types():
    #     print('{}, {}'.format(str(t), list(map(lambda x: '{}: {}'.format(str(x[0]), x[1]), t.mutations))))

    sim.run(10.)

    ls = sim.wildtype.check_mutation.keys()

    print([str(t) for t in ls])
    print([sim.wildtype.check_mutation[t] for t in ls])
    #
    # data_plot.network_with_dominant(sim, nx)
    # plt.show()


def display_simulation(sim: Simulation):
    # data_plot.stacked_plot(sim.get_types(), sim.get_tmax(), sim.get_pop_max(), plt)
    # plt.figure()
    # data_plot.line_plot(sim, plt)
    # plt.figure()
    data_plot.network_with_dominant(sim, nx)
    # data_plot.network(sim, nx)
    plt.show()


def one_type_exp():
    # === Types === #
    a = Type('A', 1000, 10., 0.001)

    # === Mutations === #
    a.add_self_mutation()

    # === Simulation === #
    sim = Simulation(a, max=10000)

    sim.run(.3)

    data_plot.stacked_plot(sim.get_types(), sim.get_tmax(), sim.get_pop_max(), plt)
    plt.show()


def graph_multiple_sims():
    gen = Generator()
    sim = gen.config_file('parameters/two_paths_ABC_D.json')

    paths = useful.load_paths('data/', 'two_paths')

    # data_plot.network(sim)
    G = data_plot.network_with_percentages(sim, paths, nx)
    plt.show()

    # d = json_graph.node_link_data(G)
    # json.dump(d, open('force/force.json', 'w'))
    # http_server.load_url('force/force.html')


def check_doubling_time():
    # divide and times sizes by 10 to show doubling time is consistent
    a = Type('A', 1000, 4., 2.)
    # stop point reduction if small simulation
    s = Simulation(a, max=20000, history=True)

    s.run(3.0)

    data_plot.line_plot(s, plt)
    plt.show()


if __name__ == '__main__':
    mutations_simulation()
