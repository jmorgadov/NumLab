"""
This module contains the basic structures for parsing.
"""

from __future__ import annotations

from typing import List, Set

from grammar import Grammar, Terminal
from tokenizer import Token, Tokenizer


def _flatten(nested_list: list) -> list:
    """Flats a nested list into a single list.

    Parameters
    ----------
    nested_list : list
        Nested list.

    Returns
    -------
    list
        Resulting flatten list.

    Examples
    --------

        >>> _flatten([1, 2, 3])
        [1,2,3]
        >>> _flatten([1, [2, 3]])
        [1,2,3]
        >>> _flatten([1, [[[2]]], 3])
        [1,2,3]
        >>> _flatten([[[1, [[2]]]], 3])
        [1,2,3]
    """
    flatten_list = []
    for item in nested_list:
        if isinstance(item, list):
            flatten_list += _flatten(item)
        else:
            flatten_list.append(item)
    return flatten_list


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


class Parser:
    """Structure used for parsing a text given a grammar and a tokenizer.

    Parameters
    ----------
    grammar : Grammar
        Grammar that will be use for parsing.
    tokenizer : Tokenizer
        Tokenizer that will be use for tokenize a given txt.
    """

    def __init__(self, grammar: Grammar, tokenizer: Tokenizer = None):
        self.grammar = grammar
        self.tokenizer = tokenizer
        self._first = None
        self._prod_first = None
        self._follow = None
        self._ll_one_table = None

    def _calcule_first_and_follow(self):
        """Recalculates the `first` and `follow` sets of the grammar."""
        self.calculate_follow()

    def _build_ll_one_table(self):
        """Builds the LL(1) table."""
        table = self._ll_one_table = {}

        all_terminals = self.grammar.all_terminals()
        all_terminals.add(Terminal("$"))
        for expr, prod in self.grammar.all_productions():
            if prod.is_eps:
                continue
            for terminal in all_terminals:
                if terminal == "EPS":
                    continue
                if terminal in self._prod_first[prod]:
                    if (expr, terminal) in table and table[expr, terminal] is not None:
                        raise ValueError(
                            f"Ambiguity in the LL(1) table: \n"
                            f"{expr} {prod}\n"
                            f"{expr} {table[expr, terminal]}"
                        )
                    table[expr, terminal] = prod
                elif "EPS" in self._first[expr] and terminal.name in self._follow[expr]:
                    table[expr, terminal] = "EPS"
                elif (expr, terminal) not in table:
                    table[expr, terminal] = None

    def parse_file(self, file_path: str):
        """Opens a file and parses it contents.

        Parameters
        ----------
        file_path : str
            File path.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        self.parse(text)

    def parse(self, text: str):
        """Parses a text.

        Parameters
        ----------
        text : str
            Text to be parsed.
        """
        tokens = self.tokenizer.tokenize(text)
        self.parse_tokens(tokens)

    def parse_tokens(self, tokens: List[Token]):
        """Parses a list of tokens.

        Parameters
        ----------
        tokens : List[Token]
            List of tokens to be parsed.
        """
        pass

    def calculate_first(self):
        """Calculates the `first` set of the grammar."""

        self._first = {expr: TerminalSet() for expr in self.grammar.exprs}
        self._prod_first = {
            prod: TerminalSet() for _, prod in self.grammar.all_productions()
        }

        change = True

        while change:
            change = False
            for expr, prod in self.grammar.all_productions():
                for item in prod.items:
                    if item.is_terminal:
                        change |= self._first[expr].add(item)
                        self._prod_first[prod].add(item)
                        break
                    if item != expr:
                        change |= self._first[expr].update(self._first[item])
                        self._prod_first[prod].update(self._first[item])
                        if "EPS" not in self._first[item].terminals:
                            break

    def calculate_follow(self):
        """Calculates `follow` set of the grammar."""

        # First is needed to calculate follow
        self.calculate_first()

        follow = {expr: TerminalSet() for expr in self.grammar.exprs}
        follow[self.grammar.start_expr].add(Terminal("$"))

        change = True

        while change:
            change = False
            for expr, prod in self.grammar.all_productions():
                for i, item in enumerate(prod.items):
                    next_item = prod.items[i + 1] if i + 1 < len(prod.items) else None
                    if item.is_terminal:
                        continue
                    if next_item is None:
                        change |= follow[item].update(follow[expr] - "EPS")
                    elif next_item.is_terminal:
                        change |= follow[item].add(next_item)
                    else:
                        change |= follow[item].update(self._first[next_item] - "EPS")
                        if "EPS" not in self._first[next_item].terminals:
                            break
        self._follow = follow
