from data_plot import Plotter
from simulation_generator import Generator

if __name__ == '__main__':
    # # === Types === #
    # a = Type('A', 10, 1.0, 0.7)
    # b = Type('B', 0, 1.0, 0.5)
    # c = Type('C', 0, 1.0, 0.3)
    #
    # # === Mutations === #
    # a.add_mutation(a, 0.999)
    # a.add_mutation(b, 0.001)
    #
    # b.add_mutation(b, 0.999)
    # b.add_mutation(c, 0.001)
    #
    # c.add_mutation(c, 1.0)
    #
    # # === Simulation === #
    # sim = Simulation(a, b, c, max=200)

    Mutation = Generator.Mutation

    rates = {('a', 'b'): (1.0, 0.6), ('A', 'b'): (1.0, 0.5), ('a', 'B'): (1.0, 0.5), ('A', 'B'): (1.0, 0.2)}

    mutation_rates = {
        Mutation(('a', 'b'), ('a', 'b')): 0.998,

        Mutation(('a', 'B'), ('A', 'B')): 0.01,
        Mutation(('a', 'B'), ('a', 'b')): 0.,

        Mutation(('A', 'b'), ('a', 'b')): 0.,
        Mutation(('A', 'b'), ('A', 'B')): 0.01,

        Mutation(('A', 'B'), ('a', 'B')): 0.,
        Mutation(('A', 'B'), ('A', 'b')): 0.,
        Mutation(('A', 'B'), ('A', 'B')): 1.0,
    }

    sim = Generator.parameters(('a', 'b'), ('A', 'B'), rates=rates, mutation_rates=mutation_rates)

    for t in sim.get_types:
        print('{}, {}'.format(str(t), list(map(lambda x: '{}: {}'.format(str(x[0]), x[1]), t.mutations))))

    sim.run(100.0)

    plt = Plotter()

    plt.plot(sim.get_types, sim.get_tmax)
