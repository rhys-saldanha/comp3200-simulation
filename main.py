from os import listdir
from os.path import join, isfile

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

import data_plot
import useful
from simulation import Simulation
from simulation_generator import Generator
from type import Type


def mutations_simulation():
    gen = Generator(prints=True, history=True)
    sim = gen.config_file('config/two_paths_ABC_D/0_00.json')

    data_plot.network(sim, nx)
    plt.show()

    # for t in sim.get_types():
    #     print('{}, {}'.format(str(t), list(map(lambda x: '{}: {}'.format(str(x[0]), x[1]), t.mutations))))

    # sim.run(10.)
    # data_plot.stacked_plot(sim, plt)
    # data_plot.network_with_dominant(sim, nx)
    # plt.show()


def display_simulation(sim: Simulation):
    # data_plot.stacked_plot(sim.get_types(), sim.get_tmax(), sim.get_pop_max(), plt)
    # plt.figure()
    # data_plot.line_plot(sim, plt)
    # plt.figure()
    data_plot.network_with_dominant(sim, sim.get_dominant_path(), nx)
    # data_plot.network(sim, nx)
    plt.show()


def one_type_exp():
    # === Types === #
    a = Type('A', 100, 10., 0.)

    # === Simulation === #
    sim = Simulation([a], max=10000, history=True)

    sim.run(1.)

    data_plot.line_plot(sim, plt, do_reduce=False)
    plt.show()


def two_type_competition():
    a = Type('A', 10000, 10., 8.0)
    b = Type('B', 100, 10., 5.0)

    sim = Simulation([a, b], max=10000, history=True, prints=True)

    sim.run(3.)

    data_plot.line_plot(sim, plt, do_reduce=False)
    plt.show()


def mutations_competition():
    a = Type('A', 10000, 10., 8.0)
    a.pos = (0, 0)
    b = Type('B', 0, 10., 5.0)
    b.pos = (1, 1)
    c = Type('C', 0, 10., 4.0)
    c.pos = (1, -1)

    a.add_mutation(b, 0.001)
    a.add_child(b)
    b.add_mutation(a, 0.001)
    b.add_parent(a)

    a.add_mutation(c, 0.001)
    a.add_child(c)
    c.add_mutation(a, 0.001)
    c.add_parent(a)

    sim = Simulation([a, b, c], max=10000, history=True, prints=True)

    sim.run(3.)

    data_plot.line_plot(sim, plt, do_reduce=False)
    plt.figure()
    data_plot.network(sim, nx=nx, plt=plt)
    plt.figure()
    data_plot.network_with_dominant(sim, sim.get_dominant_path(), nx=nx, plt=plt)
    plt.show()


def graph_multiple_sims(parameters: str, data: str):
    gen = Generator()

    # for f in files[:-1]:
    #     sim = gen.config_file(parameters)
    #     path = useful.load_paths('data/', f + '.sim')
    #     data_plot.network_with_percentages(sim, path, nx)
    #     plt.figure()
    #
    # f = files[-1]
    sim = gen.config_file(parameters)
    path = useful.load_paths_ambiguous(*data.split('/'))
    data_plot.network_with_dominant(sim, path[0], nx=nx, plt=plt)
    plt.show()

    # d = json_graph.node_link_data(G)
    # json.dump(d, open('force/force.json', 'w'))
    # http_server.load_url('force/force.html')


def graph_directory(directory: str):
    config_directory = join('config', directory)
    data_directory = join('data', directory)
    gen = Generator()

    files = [f for f in listdir(config_directory) if isfile(join(config_directory, f)) and '.json' in f]

    for p in files:
        plt.figure(p)
        sim = gen.config_file(join(config_directory, p))
        try:
            paths = useful.load_paths(join(data_directory, p[:-5] + '.sim'))
        except FileNotFoundError:
            continue
        # print(list(map(lambda x: list(map(str, x)), paths)))
        data_plot.network_with_percentages(sim, paths, nx=nx, plt=plt)

    plt.show()


def check_doubling_time():
    # divide and times sizes by 10 to show doubling time is consistent
    a = Type('A', 500, 4., 2.)
    b = Type('Food Source', 2000 - a.size, 1., 1.)
    # stop point reduction if small simulation
    s = Simulation([a, b], max=2000, history=True, prints=True)

    s.run(10.0)

    data_plot.line_plot(s, plt, title='')
    plt.figure()
    data_plot.stacked_plot(s, plt, title='')
    plt.show()


def plot_differences_data():
    ds = [-2.5, -2.0, -1.5, -1.25, -1., -0.75, -0.5, -0.25, 0., 0.25, 0.5, 0.75, 1., 1.25, 1.5, 2.0, 2.5, 3.0]
    Abc = [.68, .74, .63, .56, .66, .60, .52, .46, .58, .5, .47, .47, .39, .33, .33, .25, .21, .16]
    abD = list(map(lambda x: 1. - x, Abc))

    plt.scatter(ds, Abc, marker='x')
    plt.plot(ds, np.poly1d(np.polyfit(ds, Abc, 1))(ds), '--')
    plt.scatter(ds, abD, marker='x')
    plt.plot(ds, np.poly1d(np.polyfit(ds, abD, 1))(ds), '--')

    plt.xlabel('Difference in fitness')
    plt.xlim((min(ds), max(ds)))

    plt.ylabel('Percentage dominance')
    plt.ylim((0., 1.))

    plt.legend(['Abc', 'abD'], loc='upper right')

    plt.show()


def plot_differences_with_predicted():
    ds = [-2.5, -2.0, -1.5, -1.25, -1., -0.75, -0.5, -0.25, 0., 0.25, 0.5, 0.75, 1., 1.25, 1.5, 2.0, 2.5, 3.0]
    Abc = [.68, .74, .63, .56, .66, .60, .52, .46, .58, .5, .47, .47, .39, .33, .33, .25, .21, .16]
    abD = list(map(lambda x: 1. - x, Abc))

    Abc_fitness = 7.0
    abD_fitness = [Abc_fitness - d for d in ds]

    def f(a: float, b: float) -> float:
        x = np.log(a) - np.log(b)
        if x == 0:
            return 0.0
        y = np.divide(1.0 - np.exp(-x), 1.0 - np.exp(-10000.0 * x))
        return y

    predicted_abD = []
    predicted_Abc = []

    for s, d in zip(abD_fitness, ds):
        print(f(s, Abc_fitness))
        print(f(Abc_fitness, s))
        if d < 0:
            predicted_abD.append(0.5 - f(s, Abc_fitness))
            predicted_Abc.append(0.5 + f(s, Abc_fitness))
        else:
            predicted_abD.append(0.5 + f(Abc_fitness, s))
            predicted_Abc.append(0.5 - f(Abc_fitness, s))

    # predicted_abD = [0.5 - f(s, Abc_fitness) if d < 0 else 0.5 + f(Abc_fitness, s) for s, d in zip(abD_fitness, ds)]
    # predicted_Abc = [0.5 - f(Abc_fitness, s) if d > 0 else 0.5 + f(s, Abc_fitness) for s, d in zip(abD_fitness, ds)]

    plt.scatter(ds, Abc, marker='x')
    plt.plot(ds, predicted_Abc, '--')
    plt.scatter(ds, abD, marker='x')
    plt.plot(ds, predicted_abD, '--')

    plt.xlabel('Difference in fitness')
    plt.xlim((min(ds), max(ds)))

    plt.ylabel('Percentage dominance')
    plt.ylim((0., 1.))

    plt.legend(['Abc', 'abD'], loc='upper right')

    plt.show()


def plot_learned_parameters():
    cs = '10	6.31	3.981	2.512	1.585	1	0.631	0.3981	0.2512	0.1585	0'.split()
    data = '76.15033333	207.4646667	305.7595833	354.2038333	366.9398333	369.1825833	374.76425	370.315	364.0986667	345.0256667	327.93185'.split()
    mine = '122.0109489	176.0598416	244.3904636	323.6092782	406.8260287	485.6350523	553.2351778	606.5229868	645.7547661	673.2346661	726.063584'.split()

    cs = list(map(float, cs))
    data = list(map(float, data))
    mine = list(map(float, mine))

    plt.scatter(cs, data, marker='x')
    plt.scatter(cs, mine, marker='x')

    plt.xlabel('Concentration of antibiotic')
    plt.xlim(xmin=0)
    plt.ylabel('Growth descriptor')
    plt.ylim(ymin=0)

    plt.legend(['Provided data', 'Learned parameters'], loc='upper right')

    plt.show()


if __name__ == '__main__':
    # graph_directory('more_data')
    # graph_directory('.')
    # plot_differences_data()
    # plot_differences_with_predicted()
    # one_type_exp()
    # two_type_competition()
    # mutations_competition()
    mutations_simulation()