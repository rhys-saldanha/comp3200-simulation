import pickle
from os import listdir
from os.path import isfile, join
from time import strftime
from typing import List

from simulation import Simulation
from type import Type


def save_path(sim: Simulation, name: str = None) -> None:
    if not name:
        name = strftime("%Y%m%d-%H%M%S")
    else:
        name.replace('[TIME]', strftime("%Y%m%d-%H%M%S"))

    with open('{}.sim'.format(name), 'wb') as f:
        pickle.dump(sim.get_dominant_path(), f, -1)


def load_path(name: str) -> List[Type]:
    # t0 = time()
    if '.sim' != name[-4:]:
        name += '.sim'

    with open(name, 'rb') as f:
        p = pickle.load(f)
        # print("Loading path complete in {:f}s".format(time() - t0))
        return p


def load_paths(directory: str, part_name: str) -> List[List[Type]]:
    files = [f for f in listdir(directory) if isfile(join(directory, f)) and part_name in f]

    if directory[-1] != '/':
        directory += '/'

    if len(files) > 1:
        print('Too many files found')
        return []

    print(directory + files[0])

    with open(directory + files[0], 'rb') as f:
        p = pickle.load(f)

    return p
