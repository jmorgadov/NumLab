from __future__ import annotations

from typing import List

from grammar import Grammar, Terminal
from tokenizer import Token, Tokenizer


def _flatten(nested_list: list) -> list:
    flatten_list = []
    for item in nested_list:
        if isinstance(item, list):
            flatten_list += _flatten(item)
        else:
            flatten_list.append(item)
    return flatten_list


class Parser:
    def __init__(self, grammar: Grammar, tokenizer: Tokenizer = None):
        self.grammar = grammar
        self.tokenizer = tokenizer
        self.first_calculated = False
        self.follow_calculated = False

    def _calcule_first_and_follow(self):
        self.first_calculated = False
        self.follow_calculated = False
        self.calculate_first()
        self.calculate_follow()

    def parse_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        self.parse(text)

    def parse(self, text):
        tokens = self.tokenizer.tokenize(text)
        self.parse_tokens(tokens)

    def parse_tokens(self, tokens: List[Token]):
        pass

    def calculate_first(self):
        if self.first_calculated:
            return

        # Reset all expresion first
        for exp in self.grammar.exprs:
            exp.first_dict = None
            exp.first = []

        for exp in self.grammar.exprs:
            exp.calculate_first()
        self.first_calculated = True

    def calculate_follow(self):
        if self.follow_calculated:
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
        self.follow_calculated = True
