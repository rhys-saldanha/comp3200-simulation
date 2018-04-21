from time import time
from typing import List

import numpy as np

from type import Type, Event


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
        # self.__history = list()
        self.__update_values()
        # Set population maximum equal to initial population
        self.__pop_max: int = kwargs.get('max', self.__size)
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
        if op == Event.BIRTH and self.__size >= self.__pop_max:
            d = self.__choose_event(Event.DEATH)
            # Only update with death if types are different, otherwise they cancel
            if d != t:
                d.update(Event.DEATH, self.__time)
            else:
                # Update with nothing to prevent birth
                d.update(Event.NOTHING, self.__time)

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
            t.update(Event.NOTHING, self.__time)

        self.__update_values()

    @property
    def __time_nothing(self) -> float:
        return -1.0 * np.log(np.random.uniform()) / self.probability_total

    def __update_values(self):
        # Reduce the number of computations to only when values have been changed
        self.probability = {Event.BIRTH: sum(map(lambda t: t.probability(Event.BIRTH), self.__types)),
                            Event.DEATH: sum(map(lambda t: t.probability(Event.DEATH), self.__types))}
        self.probability_total = sum(self.probability.values())
        self.__size = sum(map(lambda t: t.size, self.__types))
        # self.__history.append((self.__time, self.__size))

    def __choose_event_any(self) -> (Type, Event):
        if self.probability_total == 0:
            # All types have died out
            return None, Event.NOTHING
        n = np.random.uniform(high=self.probability_total)

        if n < self.probability[Event.BIRTH]:
            return self.__choose_event(Event.BIRTH, n), Event.BIRTH
        return self.__choose_event(Event.DEATH, n - self.probability[Event.BIRTH]), Event.DEATH

    def __choose_event(self, s: Event, n: float = None) -> Type:
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

    @property
    def get_pop_max(self):
        return self.__pop_max

    def clone(self):
        cloned_types = [t.clone() for t in self.__types]
        return Simulation(*cloned_types, max=self.__pop_max)