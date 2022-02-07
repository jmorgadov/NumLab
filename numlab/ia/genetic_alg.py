import abc
from itertools import accumulate
from random import choices, random
from time import time
from typing import Any, Tuple


class Metaheuristic(metaclass=abc.ABCMeta):
    def __init__(self, max_iter: int = 1000, minimize=True) -> None:
        self.max_iter = max_iter
        self.minimize = minimize
        self.best_solution: Any = None

    @abc.abstractmethod
    def eval(self, solution) -> float:
        pass

    def get_best(self, sol1, sol2) -> Any:
        ev1, ev2 = self.eval(sol1), self.eval(sol2)
        if (self.minimize and ev1 <= ev2) or (not self.minimize and ev1 >= ev2):
            return sol1
        return sol2

    @abc.abstractmethod
    def iteration(self) -> None:
        pass

    def brake_condition(self) -> bool:
        return False

    def run(self):
        t_0 = time()
        i = 0
        while not self.brake_condition() and i < self.max_iter:
            print(f"Iteration {i + 1} of {self.max_iter}")
            self.iteration()
            i += 1
        t_1 = time()
        exec_time = t_1 - t_0
        return self.best_solution, self.eval(self.best_solution), exec_time


class GeneticAlg(Metaheuristic, metaclass=abc.ABCMeta):
    def __init__(
        self,
        max_iter: int = 20,
        minimize=True,
        population_size=100,
        mutation_prob=0.01,
        best_selection_count=10,
        generate_new_randoms=5,
    ):
        super().__init__(max_iter, minimize)
        self.new_best_found = True
        self.mutation_prob = mutation_prob
        self.population_size = population_size
        self.new_randoms = generate_new_randoms
        print(f"Generating population of {self.population_size}")
        self.population = [self.get_random_solution() for _ in range(population_size)]
        print(f"Evaluating population")
        self.population = [(p, self.eval(p)) for p in self.population]
        self.population.sort(key=lambda p: p[1], reverse=not self.minimize)
        self.best_selection_count = best_selection_count

    @abc.abstractmethod
    def get_random_solution(self):
        pass

    @abc.abstractmethod
    def crossover(self, sol1, sol2) -> Tuple[Any, Any]:
        pass

    @abc.abstractmethod
    def mutate(self, sol) -> Any:
        pass

    def iteration(self) -> None:
        # First selection (bests)
        new_candidates = self.population[: self.best_selection_count]

        new_rnds = [self.get_random_solution() for _ in range(self.new_randoms)]
        new_rnds = [(p, self.eval(p)) for p in new_rnds]
        new_candidates.extend(new_rnds)

        # Crossover
        total = sum([p[1] for p in self.population])
        cum_weigths = list(accumulate([p[1] / total for p in self.population]))

        while len(new_candidates) < self.population_size:
            c1, c2 = choices(self.population, cum_weights=cum_weigths, k=2)
            c1, c2 = c1[0], c2[0]
            new_c1, new_c2 = self.crossover(c1, c2)
            new_candidates.append((new_c1, self.eval(new_c1)))
            if len(new_candidates) < self.population_size:
                new_candidates.append((new_c2, self.eval(new_c2)))

        # Mutation
        crossed_start = self.best_selection_count + self.new_randoms
        for i in range(crossed_start, len(new_candidates)):
            rnd = random()
            if rnd < self.mutation_prob:
                candidate = new_candidates[i][0]
                mutaded = self.mutate(candidate)
                mutaded_val = self.eval(mutaded)
                new_candidates[i] = (mutaded, mutaded_val)

        self.population = new_candidates
        self.population.sort(key=lambda p: p[1], reverse=not self.minimize)
        self.best_solution = self.population[0][0]
        print(f"Best solution: {self.population[0]}")
        times = [p[1] for p in self.population]
        avg = sum(times) / len(times)

