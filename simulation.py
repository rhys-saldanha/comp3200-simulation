import random
from time import time
from typing import List, Dict, Tuple

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
        self.__history = {t: [] for t in types}

        self.wildtype: Type = kwargs.get('wildtype', types[0])
        self.__save_history: bool = kwargs.get('history', False)
        self.__prints: bool = kwargs.get('prints', False)

        self.__size: int = 0
        self.init_types()

        self.__tmax: int = 0
        # Set population maximum equal to initial population
        self.__pop_max: int = kwargs.get('max', self.__size)

        self.probability: Dict[Event, float] = {Event.BIRTH: sum([t.probability(Event.BIRTH) for t in self.__types]),
                                                Event.DEATH: sum([t.probability(Event.DEATH) for t in self.__types])}
        self.probability_total = sum(self.probability.values())

    def init_types(self):
        for t in self.__types:
            t.sim_init()
            self.__size += t.size

    def run(self, t: float) -> None:
        """
        Runs the simulation.

        Will run till the simulation time passes the given time.

        :param t: when to run the simulation till
        """
        if self.__prints:
            self.__run_with_prints(t)
        else:
            self.__run_silent(t)

    def __run_silent(self, t: float) -> None:
        self.__tmax = t
        while self.__time < t:
            self.__cycle()

    def __run_with_prints(self, t: float) -> None:
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
        # Find type and event
        t, op = self.__choose_event_any()

        # If birth and we are over the max pop, we need a death
        if op == Event.BIRTH and self.__size >= self.__pop_max:
            d = self.__choose_event(Event.DEATH)
            # Only update with death if types are different, otherwise they cancel
            if d != t:
                d.update(Event.DEATH, self.__time)
                t.update(Event.BIRTH, self.__time)
            # Update with nothing happens in final for loop

        # Check we have a type to update
        # as all types may have died out
        elif t is not None:
            # Update initial type choice with operation
            # May result in mutation and operation to different type
            t.update(op, self.__time)

        s = 0.0
        p_birth = 0.0
        p_death = 0.0

        for t in self.__types:
            update = t.update(Event.NOTHING, self.__time)
            if self.__save_history:
                self.__history[t].append((update, self.__time))
            s += update
            p_birth += t.probability(Event.BIRTH)
            p_death += t.probability(Event.DEATH)

        self.__size = s
        self.probability[Event.BIRTH] = p_birth
        self.probability[Event.DEATH] = p_death
        self.probability_total = p_birth + p_death

    @property
    def __time_nothing(self) -> float:
        # return -1.0 * np.log(1.0 - np.random.uniform()) / self.probability_total
        return random.expovariate(self.probability_total)

    def __choose_event_any(self) -> (Type, Event):
        if self.probability_total == 0:
            # All types have died out
            return None, Event.NOTHING
        # n = np.random.uniform(high=self.probability_total)
        n = random.random() * self.probability_total

        if n < self.probability[Event.BIRTH]:
            return self.__choose_event(Event.BIRTH, n), Event.BIRTH
        return self.__choose_event(Event.DEATH, n - self.probability[Event.BIRTH]), Event.DEATH

    def __choose_event(self, s: Event, n: float = None) -> Type:
        if n is None:
            # n = np.random.uniform(high=self.probability[s])
            n = random.random() * self.probability[s]

        t = 0.0
        # Loop through types
        for e in self.__types:
            t += e.probability(s)
            # If argument is within the new total, we've found the operation it applies to
            if n < t:
                return e
        # Argument was outside of possible values
        # raise ValueError

    def get_types(self) -> List[Type]:
        # internal list cannot be changed from outside
        return self.__types[:]

    def get_tmax(self) -> float:
        return self.__tmax

    def get_pop_max(self) -> int:
        return self.__pop_max

    def get_dominant_path(self) -> List[Type]:
        path: List[Type] = []
        # Find largest type at end of simulation
        t = max(self.get_types(), key=lambda x: x.size)
        # Trace back to wildtype through largest parent
        while t != self.wildtype:
            path.append(t)
            t = max(t.parents, key=lambda x: x.max_size)
        # At wildtype, still need to add it to the path
        path.append(t)
        return path

    def set_history(self, b: bool):
        self.__save_history = b

    def get_history(self, t: Type) -> List[Tuple[int, float]]:
        return self.__history[t]

    def check_history(self) -> bool:
        return self.__save_history

    def clone(self) -> 'Simulation':
        cloned_types = [t.clone() for t in self.__types]

        for sim_type in self.__types:
            cloned_type = cloned_types[cloned_types.index(sim_type)]
            for mutant_type, p in sim_type.mutations:
                cloned_mutant = cloned_types[cloned_types.index(mutant_type)]
                cloned_type.add_mutation(cloned_mutant, p)
            for parent_type in sim_type.parents:
                cloned_type.add_parent(cloned_types[cloned_types.index(parent_type)])
            for child_type in sim_type.children:
                cloned_type.add_child(cloned_types[cloned_types.index(child_type)])

        cloned_wildtype = cloned_types[cloned_types.index(self.wildtype)]
        return Simulation(*cloned_types, max=self.__pop_max, wildtype=cloned_wildtype)
