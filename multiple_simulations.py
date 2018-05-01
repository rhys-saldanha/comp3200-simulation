import functools
import os
import pickle
from multiprocessing import Pool, cpu_count
from typing import List

from simulation import Simulation
from simulation_generator import Generator
from type import Type

PARAMETERS = 'two_paths'
SIM_NUM = 30
TIME = 10.0
PRINT = False


def dominant_path(sim: Simulation, name: str) -> List[Type]:
    sim = sim.clone()
    # print('Running {}'.format(name))
    sim.run(TIME)
    print('Finished {}'.format(name))
    return sim.get_dominant_path()


if __name__ == '__main__':
    print('Simulating {} {} times for {} time'.format(PARAMETERS, SIM_NUM, TIME))
    print('Found {} CPUs'.format(cpu_count()))

    # Make folder for data if it doesn't exist
    os.makedirs('data/', exist_ok=True)

    g = Generator(print=PRINT)

    simulation = g.config_file('parameters/' + PARAMETERS)

    # data_plot.network(s, nx)
    # plt.show()

    # Duplicate Simulation, save history, run and show graph just to check it's all good
    # s_dup = s.clone()
    # s_dup.set_history(True)
    # s_dup.run(TIME)
    # data_plot.line_plot(s_dup, plt)
    # plt.show()

    with Pool(processes=cpu_count() - 1) as pool:
        simulations = [PARAMETERS + '_{}'.format(i) for i in range(SIM_NUM)]

        f = functools.partial(dominant_path, simulation)

        result = pool.map(f, simulations)

    with open('data/{}.sim'.format(PARAMETERS), 'wb') as f_sim:
        pickle.dump(result, f_sim, -1)

    print('Finished!')
