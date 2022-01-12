import pytest
from numlab.automata import Automata
from numlab import nlre


def test_simple_check():
    assert nlre.check("a", "a")
    assert nlre.check("a", "b") == False
    assert nlre.check("a", "aa") == False
    assert nlre.check("ab", "ab")
    assert nlre.check("ab", "aab") == False


def test_star_op():
    assert nlre.check("a*", "")
    assert nlre.check("a*", "a")
    assert nlre.check("a*", "aa")
    assert nlre.check("a*b", "aaab")
    assert nlre.check("a*b", "aaa") == False


def test_or_op():
    assert nlre.check("a|b", "a")
    assert nlre.check("a|b", "b")
    assert nlre.check("a|b", "c") == False
    assert nlre.check("a|b|c", "c")


def test_escape_char():
    assert nlre.check(r"\(a", "a") == False
    assert nlre.check(r"\(a", "(a")
    assert nlre.check(r"a\*", "a*")
    assert nlre.check(r"a\*", "a") == False
    assert nlre.check(r"a\**", "a***")
    assert nlre.check(r"a\**", "a")
    assert nlre.check(r"a\\*", "a\\\\")


def test_special_chars():
    assert nlre.check(r"a..*b", "afoob")
    assert nlre.check(r"a.*b", "ab")
    assert nlre.check(r"a.*b", "afoob")
    assert nlre.check(r"a\sb", "a b")
    assert nlre.check(r"a\nb", "a\nb")
    assert nlre.check(r"a\tb", "a\tb")
    assert nlre.check(r"a\rb", "a\rb")
    assert nlre.check(r"a\a*b", "afoob")
    assert nlre.check(r"a\a*b", "aFoob") == False
    assert nlre.check(r"a\A*b", "aFOOb")
    assert nlre.check(r"a\A*b", "aFoob") == False
    assert nlre.check(r"a(\A|\a)*b", "aFoob")
    assert nlre.check(r"a\db", "a5b")
    assert nlre.check(r"a\d*b", "a5x4b") == False
    assert nlre.check(r"a\d*.\db", "a5x4b")


def test_combined_op():
    assert nlre.check("aa*|b*", "a")
    assert nlre.check("aa*|b*", "b")
    assert nlre.check("aa*|b*", "")
    assert nlre.check("aa*b*", "a")
    assert nlre.check("aa*b*", "b") == False
    assert nlre.check("aa*b*", "ab")
    assert nlre.check("aa*b*", "aab")
    assert nlre.check("(a|b)*", "aabbababa")


def test_negation():
    assert nlre.check(r"(^a)", "b")
    assert nlre.check(r"(^a)", "a") == False
    assert nlre.check(r"(^a)(^a)*", "bcdef")
    assert nlre.check(r"'((^')|(\\'))*(^\\)'", "'asfew'")
    assert nlre.check(r"'((^')|(\\'))*(^\\)'", "'ab\\'") == False
    assert nlre.check(r"'((^')|(\\'))*(^\\)'", "'asfew\\'a") == False
    assert nlre.check(r"'((^')|(\\'))*(^\\)'", "'asfew\\'a'")
    assert nlre.check(r"'((^')|(\\'))*(^\\)'", "'asfew' foo 'bar'") == False
    assert nlre.check(r"'((^')|(\\'))*(^\\)'", "'asfew\\' foo \\'bar'")


def test_match():
    assert nlre.match("a", "a")
    assert nlre.match("a", "b") is None

    re_match = nlre.match("a", "aaaa")
    assert re_match
    assert re_match.end == 1

    re_match = nlre.match(r"'((^')|(\\'))*(^\\)'", "'aaa'")
    assert re_match
    assert re_match.end == 5

    re_match = nlre.match(r"'((^')|(\\'))*(^\\)'", "'aaa' foo")
    assert re_match
    assert re_match.end == 5

    re_match = nlre.match(r"'((^')|(\\'))*(^\\)'", "'aaa' foo 'bar'")
    assert re_match
    assert re_match.end == 5

    re_match = nlre.match(r"'((^')|(\\'))*(^\\)'", "'aaa\\' foo \\'bar'")
    assert re_match
    assert re_match.end == 17
