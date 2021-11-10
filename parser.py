"""
This module contains the basic structures for parsing.
"""

from __future__ import annotations

from typing import List

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
        """__init__.

        """
        self.grammar = grammar
        self.tokenizer = tokenizer
        self._first_calculated = False
        self._follow_calculated = False

    def _calcule_first_and_follow(self):
        """Recalculates the `first` and `follow` sets of the grammar."""
        self._first_calculated = False
        self._follow_calculated = False
        self.calculate_first()
        self.calculate_follow()

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
        if self._first_calculated:
            return

        # Reset all expresion first
        for exp in self.grammar.exprs:
            exp.first_dict = None
            exp.first = []

        for exp in self.grammar.exprs:
            exp.calculate_first()
        self._first_calculated = True

    def calculate_follow(self):
        """Calculates `follow` set of the grammar."""
        if self._follow_calculated:
            return

        # First is needed to calculate follow
        self.calculate_first()

        # Reset all expression follows
        for exp in self.grammar.exprs:
            exp.follow = []

        # Add $ to Follow(S)
        self.grammar.start.follow.append(Terminal("END"))

        for expr, prod in self.grammar.all_productions():
            for i, item in enumerate(prod.items):
                if item.is_terminal:
                    continue
                # Check all next items while EPS is present
                for j in range(i + 1, len(prod.items)):
                    next_item = prod.items[j]
                    if next_item.is_terminal:
                        item.follow.append(next_item)
                        break
                    next_first = [fst for fst in next_item.first if fst.name != "EPS"]
                    item.follow.append(next_first)
                    if all(fst.name != "EPS" for fst in next_item.first):
                        break
                else:
                    # All next items contain EPS
                    if (
                        expr.follow not in item.follow
                        and item.follow not in expr.follow
                        and item != expr
                    ):
                        item.follow.append(expr.follow)
        for expr in self.grammar.exprs:
            expr.follow = list(set(_flatten(expr.follow)))
        self._follow_calculated = True
