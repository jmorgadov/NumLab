import pytest
from automata import Automata
from regex_atmt import match


def test_simple_match():
    assert match("a", "a")
    assert match("a", "b") is None
    assert match("a", "aa")
    assert match("ab", "ab")
    re_m = match("ab", "abasdf")
    assert re_m
    assert re_m.matched_text == "ab"
    assert match("ab", "aab") is None


def test_star_op():
    assert match("a*", "")
    assert match("a*", "a")
    assert match("a*", "aa")
    assert match("a*b", "aaab")
    assert match("a*b", "aaa") is None


def test_or_op():
    assert match("a|b", "a")
    assert match("a|b", "b")
    assert match("a|b", "c") is None
    assert match("a|b|c", "c")


def test_plus_op():
    assert match("a+", "") is None
    assert match("a+", "a")
    assert match("a+b", "aab")
    assert match("a+b", "a") is None
    assert match("a+b", "b") is None
    assert match("a+b", "aa") is None


def test_escape_char():
    assert match(r"\(a", "a") is None
    assert match(r"\(a", "(a")
    assert match(r"a\*", "a*")
    assert match(r"a\*", "a") is None
    assert match(r"a\**", "a***")
    assert match(r"a\**", "a")
    assert match(r"a\\*", "a\\\\")


def test_special_chars():
    assert match(r"a.+b", "afoob")
    assert match(r"a.*b", "ab")
    assert match(r"a.*b", "afoob")
    assert match(r"a\sb", "a b")
    assert match(r"a\nb", "a\nb")
    assert match(r"a\tb", "a\tb")
    assert match(r"a\rb", "a\rb")
    assert match(r"a\fb", "a\fb")


def test_combined_op():
    assert match("a+|b*", "a")
    assert match("a+|b*", "b")
    assert match("a+|b*", "")
    assert match("a+b*", "a")
    assert match("a+b*", "b") is None
    assert match("a+b*", "ab")
    assert match("a+b*", "aab")
    assert match("(a|b)*", "aabbababa")
