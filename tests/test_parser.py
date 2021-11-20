from parser import Parser

import pytest
from tokenizer import Tokenizer
from grammar import Grammar
from exceptions import ParsingError



@pytest.fixture
def parser():
    gm = Grammar.open("./tests/grammars/math_expr.gm")

    tokenizer = Tokenizer()
    tokenizer.add_pattern("NEWLINE", r"[ \n]*\n+[ \n]*", lambda l: "NEWLINE")
    tokenizer.add_pattern("SPACE", r"[ \t]+", lambda t: None)
    tokenizer.add_pattern("i", r"\d+", int)
    tokenizer.add_pattern("PLUS", r"\+")
    tokenizer.add_pattern("TIMES", r"\*")
    tokenizer.add_pattern("LPAREN", r"\(")
    tokenizer.add_pattern("RPAREN", r"\)")
    return Parser(gm, tokenizer)


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
        ("Expr", "i"): parser.grammar.Expr.prod_0,
        ("Expr", "'('"): parser.grammar.Expr.prod_0,
        ("Expr_X", "$"): "EPS",
        ("Expr_X", "')'"): "EPS",
        ("Expr_X", "'+'"): parser.grammar.Expr_X.prod_0,
        ("Term", "i"): parser.grammar.Term.prod_0,
        ("Term", "'('"): parser.grammar.Term.prod_0,
        ("Term_Y", "$"): "EPS",
        ("Term_Y", "')'"): "EPS",
        ("Term_Y", "'+'"): "EPS",
        ("Term_Y", "'*'"): parser.grammar.Term_Y.prod_0,
        ("Factor", "i"): parser.grammar.Factor.prod_1,
        ("Factor", "'('"): parser.grammar.Factor.prod_0,
    }

    for key, value in parser._ll_one_table.items():
        if key in correct_ll_one_table:
            assert value == correct_ll_one_table[key]
        else:
            assert value is None

# Test parsing
def test_parse(parser: Parser):
    parser.parse("(1+2)*3")
    parser.parse("(1+2)*(3+4)")

    with pytest.raises(ParsingError):
        parser.parse("1+2+")

    with pytest.raises(ParsingError):
        parser.parse("1+2)")

    with pytest.raises(ParsingError):
        parser.parse("(")

    with pytest.raises(ParsingError):
        parser.parse("")
