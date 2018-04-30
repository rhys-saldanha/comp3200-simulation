import functools
import os
import pickle
from multiprocessing import Pool, cpu_count

from simulation import Simulation
from simulation_generator import Generator

PARAMETERS = 'two_paths'
SIM_NUM = 30
TIME = 10.0
PRINT = False


def dominant_paths(sim: Simulation, name: str) -> int:
    sim = sim.clone()
    print('Running {}'.format(name))
    sim.run(TIME)
    with open('{}.sim'.format(name), 'wb') as f_sim:
        pickle.dump(sim.get_dominant_path(), f_sim, -1)
    return 0


if __name__ == '__main__':
    print('Simulating {} {} times for {} time'.format(PARAMETERS, SIM_NUM, TIME))
    print('Found {} CPUs'.format(cpu_count()))

    # Make folder for data if it doesn't exist
    os.makedirs('data/', exist_ok=True)

    g = Generator(print=PRINT)

    s = g.config_file('parameters/' + PARAMETERS)
    with Pool(processes=cpu_count() - 1) as pool:
        simulations = ['data/' + PARAMETERS + '_{}'.format(i) for i in range(SIM_NUM)]

        f = functools.partial(dominant_paths, s)

        pool.map(f, simulations)

    print('Finished!')
