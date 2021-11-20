"""
This module contains the TerminalSet structure.

This structure is used to calculate in an easy way the ``first`` and ``follow``
sets of a given grammar.
"""


from __future__ import annotations

from typing import Set

from grammar import Terminal


class TerminalSet:
    """Terminal set.

    Attributes
    ----------
    terminals : Set[Terminal]
        Set of terminals.
    """

    def __init__(self, terminals: Set[Terminal] = None):
        self.terminals = set() if terminals is None else terminals

    def add(self, terminal: Terminal):
        """Adds a terminal to the set.

        Parameters
        ----------
        terminal : Terminal
            terminal to add.
        """
        last_len = len(self.terminals)
        self.terminals.add(terminal)
        return last_len != len(self.terminals)

    def update(self, terminal_set: TerminalSet):
        """Updates the set with another set.

        Parameters
        ----------
        terminal_set : ItemSet
            terminal set to update with.
        """
        last_len = len(self.terminals)
        self.terminals.update(terminal_set.terminals)
        return last_len != len(self.terminals)

    def __sub__(self, other):
        if isinstance(other, Terminal):
            return TerminalSet(terminals=self.terminals - {other})
        if isinstance(other, TerminalSet):
            return TerminalSet(terminals=self.terminals - other.terminals)
        if isinstance(other, set):
            return TerminalSet(terminals=self.terminals - other)
        if isinstance(other, str):
            new_set = {item for item in self.terminals if item.name != other}
            return TerminalSet(terminals=new_set)
        raise TypeError(
            f"unsupported operand type(s) for -: "
            f"'{type(self).__name__}' and '{type(other).__name__}'"
        )

    def __and__(self, other):
        if isinstance(other, Terminal):
            return TerminalSet(terminals=self.terminals & {other})
        if isinstance(other, TerminalSet):
            return TerminalSet(terminals=self.terminals & other.terminals)
        if isinstance(other, set):
            return TerminalSet(terminals=self.terminals & other)
        if isinstance(other, str):
            new_set = {item for item in self.terminals if item.name == other}
            return TerminalSet(terminals=new_set)
        raise TypeError(
            f"unsupported operand type(s) for &: "
            f"'{type(self).__name__}' and '{type(other).__name__}'"
        )

    def __len__(self):
        return len(self.terminals)

    def __contains__(self, item: Terminal):
        return item in self.terminals

    def __repr__(self):
        return list(self.terminals).__repr__()
