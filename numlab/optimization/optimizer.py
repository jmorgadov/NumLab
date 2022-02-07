import random
from contextlib import redirect_stdout
from time import time

import numlab.nl_ast as ast
from numlab.ia.genetic_alg import GeneticAlg
from numlab.lang.context import Context
from numlab.visitors.eval_visitor import EvalVisitor
from numlab.visitors.opt_visitor import OptVisitor


class CodeOptimizer(GeneticAlg):
    """
    Genetic algorithm for optimizing the code
    """

    def __init__(
        self,
        ast: ast.AST,
        possible_changes: list,
        max_iter: int = 5,
        minimize=True,
        population_size=10,
        mutation_prob=0.1,
        best_selection_count=3,
        generate_new_randoms=2,
    ):
        self.ast = ast
        opt = OptVisitor()
        opt.check(self.ast)
        self.possible_changes = opt.changes
        self.last_vector = [0] * len(possible_changes)
        super().__init__(
            max_iter,
            minimize,
            population_size,
            mutation_prob,
            best_selection_count,
            generate_new_randoms,
        )

    def eval(self, solution) -> float:
        """
        Evaluate the fitness of the solution
        """
        for i, item in enumerate(solution):
            if self.last_vector[i] != item:
                node, change_func, revert_func = self.possible_changes[i]
                func = change_func if item else revert_func
                func(node)

        evaluator = EvalVisitor(Context())
        start = time()
        try:
            with open("logs.txt", "w+") as f:
                with redirect_stdout(f):
                    evaluator.eval(self.ast)
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise e
            self.last_vector = solution
            return float("inf") if self.minimize else 0
        end = time()
        self.last_vector = solution
        return end - start

    def get_random_solution(self):
        """
        Generate a random solution
        """
        vals = [random.randint(0, 1) for _ in range(len(self.possible_changes))]
        return vals

    def crossover(self, sol1, sol2):
        """
        Crossover two solutions
        """
        idx = random.randint(0, len(self.possible_changes) - 1)
        return sol1[:idx] + sol2[idx:], sol2[:idx] + sol1[idx:]

    def mutate(self, sol):
        """
        Mutate a solution
        """
        idx = random.randint(0, len(self.possible_changes) - 1)
        sol[idx] = 1 - sol[idx]
        return sol
