"""
This module contains the Visitor class.

The Visitor class contains a decorator ``visitor`` that is intended to be
used as a decorator for methods.

Example:
    >>> class TypeCollector:
    ...     visitor = Visitor().visitor
    ...
    ...     @visitor
    ...     def visit(self, node: Program):
    ...         # some code
    ...
    ...     @visitor
    ...     def visit(self, node: Function):
    ...         # some code
"""

from typing import Callable, Dict, Tuple, get_type_hints


class Visitor:
    """
    Visitor class.

    A visitor instance must be creater for each class that will decorate
    methods with the ``visitor`` decorator.
    """

    def __init__(self):
        self.cases: Dict[Tuple[type], Callable] = {}
        self.callbacks = []

    def visitor(self, func):
        """
        Decorator for methods.

        The decorator is intended to be used as a decorator for methods.
        The method will be registered in the ``cases`` dictionary.
        """
        case_key = tuple(get_type_hints(func).values())
        if case_key in self.cases:
            raise ValueError(f"Duplicate visitor: {case_key}")

        def wrapper(*args, **kwargs):
            case_key = tuple(type(arg) for arg in args[1:])
            if case_key not in self.cases:
                raise ValueError(f"No {type(args[0]).__name__} visitor for {case_key}")
            case_func = self.cases[case_key]
            for callback in self.callbacks:
                callback(*args, **kwargs)
            return case_func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        self.cases[case_key] = func
        return wrapper

    def callback(self, callback):
        """
        Add a callback to the visitor.

        The callback will be called for each node that is visited.
        """
        self.callbacks.append(callback)
        return callback
