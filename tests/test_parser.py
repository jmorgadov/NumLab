from parser import Parser

import pytest
from grammar import Grammar


@pytest.fixture
def parser():
    gm = Grammar.open("./tests/grammars/math_expr.gm")
    return Parser(gm)


# Test first set calculation
def test_calculate_first_set(parser: Parser):
    parser.calculate_first()

    correct_first = {
        "Expr": ["'('", "i"],
        "Expr_X": ["'+'", "EPS"],
        "Term": ["'('", "i"],
        "Term_Y": ["'*'", "EPS"],
        "Factor": ["'('", "i"],
    }

    for expr, first_list in correct_first.items():
        for item in first_list:
            assert item in parser._first[expr]


# Test follow set calculation
def test_calculate_follow_set(parser: Parser):
    parser.calculate_follow()

    correct_follow = {
        "Expr": ["')'", "$"],
        "Expr_X": ["')'", "$"],
        "Term": ["'+'", "')'", "$"],
        "Term_Y": ["'+'", "')'", "$"],
        "Factor": ["'+'", "')'", "'*'", "$"],
    }

    for expr, follow_list in correct_follow.items():
        assert len(follow_list) == len(parser._follow[expr])
        for item in follow_list:
            assert item in parser._follow[expr]


# Test LL(1) table calculation
def test_calculate_ll_one_table(parser: Parser):
    parser.calculate_follow()
    parser._build_ll_one_table()

    correct_ll_one_table = {
        ("Expr", "$"): None,
        ("Expr", "')'"): None,
        ("Expr", "i"): parser.grammar.Expr.prod_0,
        ("Expr", "'+'"): None,
        ("Expr", "'('"): parser.grammar.Expr.prod_0,
        ("Expr", "'*'"): None,
        ("Expr_X", "$"): "EPS",
        ("Expr_X", "')'"): "EPS",
        ("Expr_X", "i"): None,
        ("Expr_X", "'+'"): parser.grammar.Expr_X.prod_0,
        ("Expr_X", "'('"): None,
        ("Expr_X", "'*'"): None,
        ("Term", "$"): None,
        ("Term", "')'"): None,
        ("Term", "i"): parser.grammar.Term.prod_0,
        ("Term", "'+'"): None,
        ("Term", "'('"): parser.grammar.Term.prod_0,
        ("Term", "'*'"): None,
        ("Term_Y", "$"): "EPS",
        ("Term_Y", "')'"): "EPS",
        ("Term_Y", "i"): None,
        ("Term_Y", "'+'"): "EPS",
        ("Term_Y", "'('"): None,
        ("Term_Y", "'*'"): parser.grammar.Term_Y.prod_0,
        ("Factor", "$"): None,
        ("Factor", "')'"): None,
        ("Factor", "i"): parser.grammar.Factor.prod_1,
        ("Factor", "'+'"): None,
        ("Factor", "'('"): parser.grammar.Factor.prod_0,
        ("Factor", "'*'"): None,
    }

    for key, value in correct_ll_one_table.items():
        assert parser._ll_one_table[key] == value
