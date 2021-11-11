import os

import pytest
from grammar import Grammar


def test_grammar_parser():
    for file in os.listdir("./tests/grammars"):
        if file.endswith(".gm"):
            Grammar.open("./tests/grammars/" + file)


@pytest.fixture
def example_grm_4():
    return Grammar.open("./tests/grammars/example_4.gm")


def test_exprs_field(example_grm_4):
    exprs = example_grm_4.exprs
    assert len(exprs) == 3
    assert exprs[0].name == "expr1"
    assert exprs[1].name == "expr2"
    assert exprs[2].name == "expr3"


def test_all_terminals(example_grm_4):
    all_terms = example_grm_4.all_terminals()
    term_matches = {term.name: term.match for term in all_terms}

    terms = [
        ("'foo'", "foo"),
        ("'bar'", "bar"),
        ("int", None),
        ("str", None),
    ]

    for name, match in terms:
        assert name in term_matches
        assert term_matches[name] == match


def test_all_productions(example_grm_4):
    correct_prods = [
        ("expr1", ["'foo'", "expr2"]),
        ("expr2", ["'bar'"]),
        ("expr2", ["expr3"]),
        ("expr2", ["EPS"]),
        ("expr3", ["int", "str"]),
    ]

    for item1, item2 in zip(correct_prods, example_grm_4.all_productions()):
        c_expr_name, c_prod_items = item1
        expr, prod = item2
        expr_name, prod_items = expr.name, [item.name for item in prod.items]

        assert c_expr_name == expr_name
        assert all(x1 == x2 for x1, x2 in zip(c_prod_items, prod_items))


def test_assign_matches(example_grm_4):
    matches = {"int": r"\d+", "str": r"\w+"}
    example_grm_4.assign_term_matches(**matches)

    # check int match is correct according to matches dict
    int_term = example_grm_4.expr3.prod_0.items[0]
    assert int_term.match == matches["int"]

    # check str match is correct according to matches dict
    str_term = example_grm_4.expr3.prod_1.items[0]
    assert str_term.match == matches["str"]
