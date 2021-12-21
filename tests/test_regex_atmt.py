import pytest
from automata import Automata
from regex_atmt import check, match, _get_basic_re_expr


def test_simple_check():
    assert check("a", "a")
    assert check("a", "b") == False
    assert check("a", "aa") == False
    assert check("ab", "ab")
    assert check("ab", "aab") == False


def test_star_op():
    assert check("a*", "")
    assert check("a*", "a")
    assert check("a*", "aa")
    assert check("a*b", "aaab")
    assert check("a*b", "aaa") == False


def test_or_op():
    assert check("a|b", "a")
    assert check("a|b", "b")
    assert check("a|b", "c") == False
    assert check("a|b|c", "c")


def test_escape_char():
    assert check(r"\(a", "a") == False
    assert check(r"\(a", "(a")
    assert check(r"a\*", "a*")
    assert check(r"a\*", "a") == False
    assert check(r"a\**", "a***")
    assert check(r"a\**", "a")
    assert check(r"a\\*", "a\\\\")


def test_special_chars():
    assert check(r"a..*b", "afoob")
    assert check(r"a.*b", "ab")
    assert check(r"a.*b", "afoob")
    assert check(r"a\sb", "a b")
    assert check(r"a\nb", "a\nb")
    assert check(r"a\tb", "a\tb")
    assert check(r"a\rb", "a\rb")
    assert check(r"a\a*b", "afoob")
    assert check(r"a\a*b", "aFoob") == False
    assert check(r"a\A*b", "aFOOb")
    assert check(r"a\A*b", "aFoob") == False
    assert check(r"a(\A|\a)*b", "aFoob")
    assert check(r"a\db", "a5b")
    assert check(r"a\d*b", "a5x4b") == False
    assert check(r"a\d*.\db", "a5x4b")


def test_combined_op():
    assert check("aa*|b*", "a")
    assert check("aa*|b*", "b")
    assert check("aa*|b*", "")
    assert check("aa*b*", "a")
    assert check("aa*b*", "b") == False
    assert check("aa*b*", "ab")
    assert check("aa*b*", "aab")
    assert check("(a|b)*", "aabbababa")


def test_negation():
    assert check(r"(^a)", "b")
    assert check(r"(^a)", "a") == False
    assert check(r"(^a)(^a)*", "bcdef")
    assert check(r"'((^')|(\\'))*(^\\)'", "'asfew'")
    assert check(r"'((^')|(\\'))*(^\\)'", "'ab\\'") == False
    assert check(r"'((^')|(\\'))*(^\\)'", "'asfew\\'a") == False
    assert check(r"'((^')|(\\'))*(^\\)'", "'asfew\\'a'")
    assert check(r"'((^')|(\\'))*(^\\)'", "'asfew' foo 'bar'") == False
    assert check(r"'((^')|(\\'))*(^\\)'", "'asfew\\' foo \\'bar'")


def test_match():
    assert match("a", "a")
    assert match("a", "b") is None

    re_match = match("a", "aaaa")
    assert re_match
    assert re_match.end == 1

    re_match = match(r"'((^')|(\\'))*(^\\)'", "'aaa'")
    assert re_match
    assert re_match.end == 5

    re_match = match(r"'((^')|(\\'))*(^\\)'", "'aaa' foo")
    assert re_match
    assert re_match.end == 5

    re_match = match(r"'((^')|(\\'))*(^\\)'", "'aaa' foo 'bar'")
    assert re_match
    assert re_match.end == 5

    re_match = match(r"'((^')|(\\'))*(^\\)'", "'aaa\\' foo \\'bar'")
    assert re_match
    assert re_match.end == 17


def test_advance_to_basic():
    patterns = {
        "a": "a",
        "a+": "aa*",
        "[0-9]": "(0|1|2|3|4|5|6|7|8|9)",
    }

    for adv, basic in patterns.items():
        assert _get_basic_re_expr(adv) == basic
