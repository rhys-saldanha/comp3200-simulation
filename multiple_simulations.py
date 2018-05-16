import argparse
import functools
import os
import pickle
import sys
import time
from multiprocessing import Pool, cpu_count
from os import listdir
from os.path import isfile, join
from typing import List

from simulation import Simulation
from simulation_generator import Generator
from type import Type

parser = argparse.ArgumentParser('multiple_simulations')
parser.add_argument('-c', nargs='+', help='config file(s) for simulation in JSON format', default=None)
parser.add_argument('-d', help='directory of config file(s) for simulation in JSON format', type=str, default=None)
parser.add_argument('-n', help='number of simulations to run', type=int, default=1)
parser.add_argument('-t', help='time input for Simulation.run()', type=float, default=0.0)
parser.add_argument('-v', help='verbose mode, prints a lot more but will get messy', type=bool, default=False)
args = parser.parse_args()

CONFIG_FILES: List[str] = args.c
DIRECTORY: str = args.d
SIM_NUM: int = args.n
TIME: float = args.t
PRINT: bool = args.v

CONFIG = 'config/'
DATA = 'data/'


def dominant_path(sim: Simulation, name: str) -> List[Type]:
    sim = sim.clone()
    # print('Running {}'.format(name))
    sim.run(TIME)
    if PRINT:
        print('Finished {}'.format(name))
    return sim.get_dominant_path()


def run_multiple_simulations(config: str, output_folder: str):
    g = Generator(prints=PRINT)
    if PRINT:
        print(config)
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

    with Pool(maxtasksperchild=1) as pool:
        simulations = [config + '_{}'.format(i) for i in range(SIM_NUM)]

        f = functools.partial(dominant_path, s)

        result = pool.map(f, simulations)

    print('Finished simulations at {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    print('Took {}s'.format(time.time() - t0))

    filename = os.path.basename(os.path.splitext(config)[0])

    filename = join(output_folder, '{}.sim'.format(filename))

    with open(filename, 'wb') as f_sim:
        pickle.dump(result, f_sim, -1)


if __name__ == '__main__':
    if 'config' not in listdir('.'):
        print('Could not find \'config\' folder', file=sys.__stderr__)
        sys.exit()

    print('Found {} CPUs'.format(cpu_count()))
    print('------------------')

    # Make folder for data if it doesn't exist
    os.makedirs(DATA, exist_ok=True)

    if CONFIG_FILES:
        for c in CONFIG_FILES:
            data_dir = os.path.dirname(join(DATA, c))
            os.makedirs(data_dir, exist_ok=True)
            run_multiple_simulations(join(CONFIG, c), data_dir)
    elif DIRECTORY:
        config_directory = join(CONFIG, DIRECTORY)
        data_directory = join(DATA, DIRECTORY)
        # Make data directory
        os.makedirs(data_directory, exist_ok=True)
        # Find all config files in config directory
        files = [f for f in listdir(config_directory) if isfile(join(config_directory, f)) and '.json' in f]
        for c in files:
            run_multiple_simulations(join(config_directory, c), data_directory)
            print('------------------')
    else:
        print('No config files or folder specified, exiting')

# python multiple_simulations.py -c abc_ABC_D.json -t 1.0 -v true
