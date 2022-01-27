"""
This module contains the AST structure for the compiler.
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, List, Optional


DUMP_INDENT = 3

class AST(metaclass=ABCMeta):
    __slots__ = ()
    def dump(self, indent: int = 0) -> None:
        """
        Prints the AST in a human-readable format.
        """
        print(f"{' ' * indent}{self.__class__.__name__}:")
        for field in self.__slots__:
            value = getattr(self, field)
            if isinstance(value, list) and value:
                print(f"{' ' * (indent + DUMP_INDENT)}{field}: [")
                for item in value:
                    if isinstance(item, AST):
                        item.dump(indent + DUMP_INDENT*2)
                    else:
                        print(f"{' ' * (indent + DUMP_INDENT)}{item}")
                print(f"{' ' * (indent + DUMP_INDENT)}]")
            elif isinstance(value, AST):
                value.dump(indent + DUMP_INDENT)
            elif value:
                print(f"{' ' * (indent + DUMP_INDENT)}{field}: {value}")
