from time import time
from typing import List

import numpy as np

from type import Type


class Simulation:
    """
    This class simulates the concurrent increase and decrease in type
    population sizes, taking into account their respective birth and death rates.
    """

    def __init__(self, *types: Type, **kwargs):
        """
        Given a list of `Type`s, this object will run a simulation for a
        given amount of time

        :param Type types: list of Types to simulate
        :param kwargs: Can give a max size different to the sum of the size of all types
        """
        self.__types: List[Type] = types
        self.__time = 0
        self.__update_values()
        # Set population maximum equal to initial population
        self.__pop_max: int = kwargs.get('max', self.size)
        self.__tmax = 0

    def run(self, t: float) -> None:
        """
        Runs the simulation.

        Will run till the simulation time passes the given time.

        :param t: when to run the simulation till
        """
        self.__tmax = t
        print("Running till time {}".format(t))
        maximum_percentage = -1
        t0 = time()
        while self.__time < t:
            percentage_completed = int((self.__time * 100) / t)
            if percentage_completed > maximum_percentage:
                maximum_percentage = percentage_completed
                if maximum_percentage % 10 == 0:
                    print("{}%\t{:f}s".format(maximum_percentage, time() - t0))
            self.__cycle()
        print("Simulation complete in {:f}s".format(time() - t0))

    def __cycle(self):
        # Move time forwards
        self.__time += self.__time_nothing
        # Find type with operation event
        t, op = self.__choose_event_any()

        # If birth and we are over the max pop, we need a death
        if op == 1 and self.size >= self.__pop_max:
            d = self.__choose_event('death')
            # Only update with death if types are different, otherwise they cancel
            if d != t:
                d.update(-1, self.__time)
            else:
                # Update with nothing to prevent birth
                d.update(0, self.__time)

        # # If birth and we are over the max pop, do nothing
        # if op == 1 and self.size >= self.pop_max:
        #     t.update(0, self.time)

        # Check we have a type to update
        # as all types may have died out
        if t is not None:
            # Update initial type choice with operation
            # May result in mutation and operation to different type
            t.update(op, self.__time)
        for t in self.__types:
            t.update(0, self.__time)

        self.__update_values()

    @property
    def __time_nothing(self) -> float:
        return -1.0 * np.log(np.random.uniform()) / self.probability_total

    def __update_values(self):
        # Reduce the number of computations to only when values have been changed
        self.probability = {'birth': sum(map(lambda t: t.probability('birth'), self.__types)),
                            'death': sum(map(lambda t: t.probability('death'), self.__types))}
        self.probability_total = sum(self.probability.values())
        self.size = sum(map(lambda t: t.size, self.__types))

    def __choose_event_any(self) -> (Type, int):
        if self.probability_total == 0:
            # All types have died out
            return None, 0
        n = np.random.uniform(high=self.probability_total)

        if n > self.probability['birth']:
            return self.__choose_event('death', n - self.probability['birth']), -1
        return self.__choose_event('birth', n), +1

    def __choose_event(self, s: str, n: float = None) -> Type:
        if n is None:
            n = np.random.uniform(high=self.probability[s])

        t = 0.0
        # Loop through types
        for e in self.__types:
            t += e.probability(s)
            # If argument is within the new total, we've found the operation it applies to
            if n < t:
                return e
        # Argument was outside of possible values
        # raise ValueError

    @property
    def get_types(self):
        # internal list cannot be changed from outside
        return self.__types[:]

    @property
    def get_tmax(self):
        return self.__tmax
