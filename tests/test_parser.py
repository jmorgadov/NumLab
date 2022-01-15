import logging
import sys
from pathlib import Path
from typing import List

import pytest
from numlab.compiler import (AST, Grammar, LR1Parser, ParserManager, Symbol,
                             Tokenizer)
from numlab.exceptions import ParsingError


# Math ast
class Expr(AST):
    def __init__(self, term: AST, expr: AST = None):
        self.expr = expr
        self.term = term

    def eval(self):
        if self.expr is None:
            return self.term.eval()
        else:
            return self.expr.eval() + self.term.eval()


class Term(AST):
    def __init__(self, factor: AST, term: AST = None):
        self.term = term
        self.factor = factor

    def eval(self):
        if self.term is None:
            return self.factor.eval()
        else:
            return self.term.eval() * self.factor.eval()


class Factor(AST):
    def __init__(self, value: int = None, expr: AST = None):
        self.value = value
        self.expr = expr

    def eval(self):
        if self.expr is None:
            return self.value
        else:
            return self.expr.eval()


builders = {
    "F -> i": lambda x: Factor(value=int(x.value)),
    "F -> ( E )": lambda p1, x, p2: Factor(expr=x),
    "T -> F": lambda x: Term(factor=x),
    "T -> T * F": lambda x, t, y: Term(term=x, factor=y),
    "E -> T": lambda x: Expr(term=x),
    "E -> E + T": lambda x, p, y: Expr(expr=x, term=y),
}


@pytest.fixture
def grammar():
    gm = Grammar.open("./tests/grammars/math_expr_lr.gm")
    gm.assign_builders(builders)
    return gm


@pytest.fixture
def tokenizer():
    tokenizer = Tokenizer()
    tokenizer.add_pattern("NEWLINE", r"( |\n)*\n\n*( |\n)*", lambda l: None)
    tokenizer.add_pattern("SPACE", r"( |\t)( \t)*", lambda t: None)
    tokenizer.add_pattern("i", r"\d\d*")
    tokenizer.add_pattern("+", r"+")
    tokenizer.add_pattern("*", r"\*")
    tokenizer.add_pattern("(", r"\(")
    tokenizer.add_pattern(")", r"\)")
    return tokenizer


@pytest.fixture
def parser(grammar, tokenizer):
    return ParserManager(grammar, tokenizer)


# Test parsing
def test_parse(parser: ParserManager):
    ast = parser.parse("(1+2)*3")
    assert ast.eval() == 9

    ast = parser.parse("(1+2)*(3+4)")
    assert ast.eval() == 21

    with pytest.raises(ParsingError):
        parser.parse("1+2+")

    with pytest.raises(ParsingError):
        parser.parse("1+2)")

    with pytest.raises(ParsingError):
        parser.parse("(")

    with pytest.raises(ParsingError):
        parser.parse("")


def test_parse_file(parser: ParserManager):
    ast = parser.parse_file("./tests/grammars/math_file")
    assert ast.eval() == 54


def test_save_and_load_lrtable(grammar, tokenizer):
    table_file = Path("./tests/grammars/math_expr_lr_table")

    if table_file.exists():
        table_file.unlink()

    parser = LR1Parser(grammar, str(table_file))

    assert table_file.exists()
    assert parser.lr1_table._first is not None

    parser = LR1Parser(grammar, str(table_file))

    assert parser.lr1_table._first is None

    parser_man = ParserManager(grammar, tokenizer, parser)

    assert parser_man.parse("1 + 2").eval() == 3

    table_file.unlink()
