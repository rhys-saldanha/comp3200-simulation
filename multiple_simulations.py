import functools
import os
import pickle
import time
from multiprocessing import Pool, cpu_count
from typing import List, Union

import matplotlib.pyplot as plt
import networkx as nx

import data_plot
from simulation import Simulation
from simulation_generator import Generator
from type import Type

PARAMETERS: List[str] = ['two_paths_ABC_D_more_separate_skewed_1_5']
SIM_NUM = 100
TIME = 10.0
PRINT = False


def dominant_path(sim: Simulation, name: str) -> List[Type]:
    sim = sim.clone()
    # print('Running {}'.format(name))
    sim.run(TIME)
    print('Finished {}'.format(name))
    return sim.get_dominant_path()


def run_multiple_simulations(parameters: str):
    g = Generator(prints=PRINT)
    s = g.config_file('parameters/' + parameters)

    # Showing graphs messes with threading, only use to test simulation parameters
    # data_plot.network(s, nx)
    # plt.show()
    # return

    # Duplicate Simulation, save history, run and show graph just to check it's all good
    # s_dup = s.clone()
    # s_dup.set_history(True)
    # s_dup.set_print(True)
    # s_dup.run(TIME)
    # data_plot.line_plot(s_dup, plt)
    # plt.show()

    print('Starting at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    t0 = time.time()

    with Pool(maxtasksperchild=2) as pool:
        simulations = [parameters + '_{}'.format(i) for i in range(SIM_NUM)]

        f = functools.partial(dominant_path, s)

        result = pool.map(f, simulations)

    print('Finished simulations at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    print('Took {}s'.format(time.time() - t0))

    with open('data/{}.sim'.format(parameters), 'wb') as f_sim:
        pickle.dump(result, f_sim, -1)
    print('Finished!')


if __name__ == '__main__':
    print('Simulating {} {} times for {} time'.format(PARAMETERS, SIM_NUM, TIME))
    print('Found {} CPUs'.format(cpu_count()))

    # Make folder for data if it doesn't exist
    os.makedirs('data/', exist_ok=True)

    [run_multiple_simulations(p) for p in PARAMETERS]
