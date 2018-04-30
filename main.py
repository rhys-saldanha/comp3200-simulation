from typing import List

import matplotlib.pyplot as plt
import networkx as nx

import data_plot
from simulation import Simulation
from simulation_generator import Generator
from type import Type
from useful import load_paths


def mutations_simulation() -> Simulation:
    gen = Generator()
    rates = {tuple('abc'): (10.0, 9.), tuple('Abc'): (10.0, 7.), tuple('ABc'): (10.0, 6.), tuple('ABC'): (10.0, 5.)}

    sim = gen.parameters(tuple('abc'), [tuple('ABC'), tuple('ABD')], rates=rates, size=10000, wildtype_size=10000,
                         default_rate=(10.0, 9.))

    # for t in sim.get_types:
    #     print('{}, {}'.format(str(t), list(map(lambda x: '{}: {}'.format(str(x[0]), x[1]), t.mutations))))

    sim.run(10.)

    return sim


def display_simulation(sim: Simulation):
    # data_plot.stacked_plot(sim.get_types(), sim.get_tmax(), sim.get_pop_max(), plt)
    # plt.figure()
    # data_plot.line_plot(sim.get_types(), sim.get_tmax(), sim.get_pop_max(), plt)
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


def graph_multiple_sims(paths: List[List[Type]]):
    gen = Generator()

    sim = gen.config_file('parameters/two_paths.json')
    # data_plot.network(sim)
    G = data_plot.network_with_percentages(sim, paths, nx)
    plt.show()

    # d = json_graph.node_link_data(G)
    # json.dump(d, open('force/force.json', 'w'))
    # http_server.load_url('force/force.html')


def check_doubling_time():
    a = Type('A', 1000, 4., 2.)
    s = Simulation(a, max=20000, history=True)

    s.run(3.0)

    data_plot.line_plot(s, plt)
    plt.show()


if __name__ == '__main__':
    paths = load_paths('data/', '10_0_abc_ABC_D_')
    print([str(t) for t in paths[0]])
    print(paths)
    graph_multiple_sims(paths)

# sim = mutations_simulation()
# save_simulation(sim, '10.0_ABC_D_3')

# sim = load_simulation('10.0_ABC_D_3')
# display_simulation(sim)

# mutation = Generator.Mutation
# mutation_rates = {
#     mutation(('a', 'b'), ('a', 'b')): 0.998,
#
#     mutation(('a', 'B'), ('A', 'B')): 0.01,
#     mutation(('a', 'B'), ('a', 'b')): 0.,
#
#     mutation(('A', 'b'), ('a', 'b')): 0.,
#     mutation(('A', 'b'), ('A', 'B')): 0.01,
#
#     mutation(('A', 'B'), ('a', 'B')): 0.,
#     mutation(('A', 'B'), ('A', 'b')): 0.,
#     mutation(('A', 'B'), ('A', 'B')): 1.0,
# }
# sim = Generator.parameters(('a', 'b'), ('A', 'B'), rates=rates, mutation_rates=mutation_rates)
