import data_plot
from simulation import Simulation
from simulation_generator import Generator
from type import Type


def mutations():
    rates = {('a', 'b'): (10.0, 9.), ('A', 'b'): (10.0, 7.), ('a', 'B'): (10.0, 8.), ('A', 'B'): (10.0, 5.)}

    sim = Generator.parameters(('a', 'b'), ('A', 'B'), rates=rates, size=10000, wildtype_size=10000)

    # for t in sim.get_types:
    #     print('{}, {}'.format(str(t), list(map(lambda x: '{}: {}'.format(str(x[0]), x[1]), t.mutations))))

    sim.run(5.)
    line = data_plot.LinePlot()
    stack = data_plot.StackedPlot()
    line.plot(sim.get_types, sim.get_tmax, sim.get_size_max)
    stack.plot(sim.get_types, sim.get_tmax, sim.get_size_max)


def one_type_exp():
    # === Types === #
    a = Type('A', 1000, 10., 0.001)

    # === Mutations === #
    a.add_self_mutation()

    # === Simulation === #
    sim = Simulation(a, max=10000)

    sim.run(.3)
    stack = data_plot.StackedPlot()

    stack.plot(sim.get_types, sim.get_tmax, sim.get_size_max)


if __name__ == '__main__':
    mutations()

    data_plot.show()

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
