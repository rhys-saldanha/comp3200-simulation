import argparse
import functools
import os
import pickle
import time
from multiprocessing import Pool, cpu_count
from typing import List

from simulation import Simulation
from simulation_generator import Generator
from type import Type

parser = argparse.ArgumentParser('multiple_simulations')
parser.add_argument('-c', nargs='+', help='config file(s) for simulation in JSON format', required=True)
parser.add_argument('-n', help='number of simulations to run', type=int, default=100)
parser.add_argument('-t', help='time input for Simulation.run()', type=float, required=True)
parser.add_argument('-v', help='verbose mode, prints a lot more but will get messy', type=bool, default=False)
args = parser.parse_args()

PARAMETERS: List[str] = args.c
SIM_NUM: int = args.n
TIME: float = args.t
PRINT: bool = args.v


def dominant_path(sim: Simulation, name: str) -> List[Type]:
    sim = sim.clone()
    # print('Running {}'.format(name))
    sim.run(TIME)
    if PRINT:
        print('Finished {}'.format(name))
    return sim.get_dominant_path()


def run_multiple_simulations(config: str):
    g = Generator(prints=PRINT)
    s = g.config_file(config)

    # Showing graphs messes with threading, only use to test simulation config
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

    print('Simulating {} {} times for {} time'.format(config, SIM_NUM, TIME))
    print('Starting at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    t0 = time.time()

    with Pool() as pool:
        simulations = [config + '_{}'.format(i) for i in range(SIM_NUM)]

        f = functools.partial(dominant_path, s)

        result = pool.map(f, simulations)

    print('Finished simulations at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    print('Took {}s'.format(time.time() - t0))

    with open('data/{}.sim'.format(config.split('/')[-1]), 'wb') as f_sim:
        pickle.dump(result, f_sim, -1)


if __name__ == '__main__':
    print('Found {} CPUs'.format(cpu_count()))

    # Make folder for data if it doesn't exist
    os.makedirs('data/', exist_ok=True)

    [run_multiple_simulations(p) for p in PARAMETERS]

# python multiple_simulations.py -c config/abc_ABC_D.json -t 1.0 -v true
