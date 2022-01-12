"""
This module contains the TerminalSet structure.

This structure is used to calculate in an easy way the ``first`` and ``follow``
sets of a given grammar.
"""


from __future__ import annotations

from typing import Set

from numlab.compiler.grammar import Terminal
from numlab.compiler.tokenizer import Token


class TerminalSet:
    """Terminal set.

    Attributes
    ----------
    terminals : Set[Terminal]
        Set of terminals.
    """

    def __init__(self, terminals: Set[Terminal] = None):
        self.terminals = set() if terminals is None else terminals

    def __iter__(self):
        return iter(self.terminals)

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
        terminal_set : SymbolSet
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
            new_set = {symbol for symbol in self.terminals if symbol.name != other}
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
            new_set = {symbol for symbol in self.terminals if symbol.name == other}
            return TerminalSet(terminals=new_set)
        raise TypeError(
            f"unsupported operand type(s) for &: "
            f"'{type(self).__name__}' and '{type(other).__name__}'"
        )

    def has_token(self, token: Token):
        """Checks if the set contains a token.

        Parameters
        ----------
        token : str
            token to check.

        Returns
        -------
        bool
            ``True`` if the set contains the token, ``False`` otherwise.
        """
        return any(terminal.name == token.token_type for terminal in self.terminals)

    def __len__(self):
        return len(self.terminals)

    def __contains__(self, symbol: Terminal):
        return symbol in self.terminals

    def __getitem__(self, index):
        return list(self.terminals)[index]

    def __repr__(self):
        return list(self.terminals).__repr__()
