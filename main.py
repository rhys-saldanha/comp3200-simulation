from simulation import Simulation
from type import Type
from data_plot import Plotter

if __name__ == '__main__':
    # === Types === #
    a = Type('A', 10, 1.0, 0.7)
    b = Type('B', 0, 1.0, 0.5)
    c = Type('C', 0, 1.0, 0.3)

    # === Mutations === #
    a.add_mutation(a, 0.999)
    a.add_mutation(b, 0.001)

    b.add_mutation(b, 0.999)
    b.add_mutation(c, 0.001)

    c.add_mutation(c, 1.0)

    # === Simulation === #
    sim = Simulation(a, b, c, max=200)

    sim.run(100.0)

    plt = Plotter()

    plt.plot(sim)
