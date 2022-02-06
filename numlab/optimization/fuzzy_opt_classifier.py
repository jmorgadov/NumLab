import math
from typing import Callable


class FuzzyRule:
    def __init__(self, name: str, functions: list, rule: Callable):
        self.name = name
        self.functions = functions
        self.rule = rule

    def apply(self, *input_values: tuple):
        if len(input_values) != len(self.functions):
            raise ValueError(
                "The number of input values does not match the number of functions"
            )
        results = [self.functions[i](val) for i, val in enumerate(input_values)]
        return self.rule(*results)


class FuzzyOptClassifier:
    def __init__(self):
        self.max_loop_depth = 0
        self.changes = []
        self.rules = [
            FuzzyRule(
                name="Poor change",
                functions=[
                    lambda x: self._norm_bell_curve(0, 0.2, x),
                    lambda x: self._norm_bell_curve(0, 1, x),
                ],
                rule=max,
            ),
            FuzzyRule(
                name="Acceptable change",
                functions=[
                    lambda x: self._norm_bell_curve(0.5, 0.2, x),
                    lambda x: self._norm_bell_curve(0.5, 1, x),
                ],
                rule=max,
            ),
            FuzzyRule(
                name="Good change",
                functions=[
                    lambda x: self._norm_bell_curve(1, 0.2, x),
                    lambda x: self._norm_bell_curve(1, 1, x),
                ],
                rule=max,
            ),
        ]
        self.membership_val_centers = [0.1, 0.5, 1]

    def add_change(self, category: float, loop_depth: float):
        self.max_loop_depth = max(self.max_loop_depth, loop_depth)
        self.changes.append((category, loop_depth))

    def _loop_depth_val(self, loop_depth):
        return min(3, loop_depth)

    def _defuzzify(self, *values):
        return sum(
            [self.membership_val_centers[i] * values[i] for i in range(len(values))]
        ) / sum(values)

    def _classify_single_change(self, category: float, loop_depth: float):
        vals = [
            self.rules[i].apply(category, self._loop_depth_val(loop_depth))
            for i in range(len(self.rules))
        ]
        return self._defuzzify(*vals)

    def classify_changes(self):
        if len(self.changes) == 0:
            raise ValueError("No changes have been added")
        return [self._classify_single_change(*vals) for vals in self.changes]

    def classify_optimization_quality(self):
        if len(self.changes) == 0:
            raise ValueError("No changes have been added")
        vals = self.classify_changes()
        return max(vals)

    def _bell_curve(self, mean: float, std: float, x: float):
        return (1 / (std * math.sqrt(2 * math.pi))) * math.exp(
            -((x - mean) ** 2) / (2 * std ** 2)
        )

    def _norm_bell_curve(self, mean: float, std: float, x: float):
        return self._bell_curve(mean, std, x) / self._bell_curve(mean, std, mean)
