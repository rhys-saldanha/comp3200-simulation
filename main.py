import data_plot
import matplotlib.pyplot as plt
import networkx as nx
from simulation import Simulation
from simulation_generator import Generator
from type import Type


def mutations():
    rates = {tuple('abc'): (10.0, 9.), tuple('Abc'): (10.0, 7.), tuple('ABc'): (10.0, 6.), tuple('ABC'): (10.0, 5.)}

    sim = Generator.parameters(tuple('abc'), tuple('ABC'), tuple('ABD'), rates=rates, size=10000, wildtype_size=10000,
                               default_rate=(10.0, 9.))

    # for t in sim.get_types:
    #     print('{}, {}'.format(str(t), list(map(lambda x: '{}: {}'.format(str(x[0]), x[1]), t.mutations))))

    sim.run(3.)

    data_plot.network_with_dominant(sim, nx)
    plt.figure()
    data_plot.line_plot(sim.get_types, sim.get_tmax, sim.get_pop_max, plt)
    plt.figure()
    data_plot.stacked_plot(sim.get_types, sim.get_tmax, sim.get_pop_max, plt)
    plt.show()


def one_type_exp():
    # === Types === #
    a = Type('A', 1000, 10., 0.001)

    # === Mutations === #
    a.add_self_mutation()

    # === Simulation === #
    sim = Simulation(a, max=10000)

    sim.run(.3)

    data_plot.stacked_plot(sim.get_types, sim.get_tmax, sim.get_pop_max, plt)
    plt.show()


if __name__ == '__main__':
    mutations()

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
