from simulation import Simulation
from type import Type

if __name__ == "__main__":
    a = Type("A", 100.0, 1.0, 0.0)
    b = Type("B", 200.0, 0.0, 0.0)
    a.add_mutations(0.0, (b, 1.0))
    sim = Simulation(a, b)
    sim.run(3.0)
