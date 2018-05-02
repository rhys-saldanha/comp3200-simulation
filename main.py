import matplotlib.pyplot as plt
import networkx as nx

import data_plot
import useful
from simulation import Simulation
from simulation_generator import Generator
from type import Type


def mutations_simulation():
    gen = Generator(prints=True, history=True)
    sim = gen.config_file('parameters/two_paths_ABC_D_uneven.json')

    data_plot.network(sim, nx)
    plt.show()

    # for t in sim.get_types():
    #     print('{}, {}'.format(str(t), list(map(lambda x: '{}: {}'.format(str(x[0]), x[1]), t.mutations))))

    sim.run(10.)
    data_plot.stacked_plot(sim, plt)
    # data_plot.network_with_dominant(sim, nx)
    plt.show()


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


def graph_multiple_sims(*files: str):
    gen = Generator()

    for f in files[:-1]:
        sim = gen.config_file('parameters/{}'.format(f))
        path = useful.load_paths('data/', f + '.sim')
        data_plot.network_with_percentages(sim, path, nx)
        plt.figure()

    f = files[-1]
    sim = gen.config_file('parameters/{}'.format(f))
    path = useful.load_paths('data/', f + '.sim')
    data_plot.network_with_percentages(sim, path, nx)
    plt.show()

    # d = json_graph.node_link_data(G)
    # json.dump(d, open('force/force.json', 'w'))
    # http_server.load_url('force/force.html')


def check_doubling_time():
    # divide and times sizes by 10 to show doubling time is consistent
    a = Type('A', 500, 4., 2.)
    b = (Type('B', 2000 - a.size, 4., 3.))
    # stop point reduction if small simulation
    s = Simulation(a, b, max=2000, history=True, prints=True)

    s.run(10.0)

    data_plot.line_plot(s, plt)
    plt.figure()
    data_plot.stacked_plot(s, plt)
    plt.show()


if __name__ == '__main__':
    # graph_multiple_sims('two_paths_ABC', 'two_paths_ABC_D')
    mutations_simulation()
