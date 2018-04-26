import functools
import pickle
from multiprocessing import Pool, cpu_count

from simulation import Simulation
from simulation_generator import Generator

NAME = 'data/10.0_abc_ABC_D_{}'
PARAMETERS = 'parameters/abc_ABC_D.json'
SIM_NUM = 16
TIME = 10.0


def dominant_paths(sim: Simulation, name: str) -> int:
    sim = sim.clone()
    # print(sim.wildtype, name)
    sim.run(TIME)
    with open('{}.sim'.format(name), 'wb') as f:
        pickle.dump(sim.get_dominant_path(), f, -1)
    return 0


if __name__ == '__main__':
    sim = Generator.config_file(PARAMETERS)
    with Pool(processes=cpu_count()) as pool:
        simulations = [NAME.format(i) for i in range(SIM_NUM)]

        f = functools.partial(dominant_paths, sim)

        pool.map(f, simulations)
