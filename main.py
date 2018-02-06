from simulation import Simulation
from type import Type

if __name__ == "__main__":
    a = Type("A", 400.0, 1.0, 0.1)
    b = Type("B", 0, 1.0, 0.1)
    a.add_mutations(0.1, (b, 0.9))
    sim = Simulation(a, b)
    sim.run(20.0)
