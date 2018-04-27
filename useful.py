import pickle
from time import strftime, time
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
    t0 = time()
    with open('{}.sim'.format(name), 'rb') as f:
        p = pickle.load(f)
        print("Loading simulation complete in {:f}s".format(time() - t0))
        return p
