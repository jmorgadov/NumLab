import re

import pytest
from exceptions import TokenizationError
from tokenizer import Tokenizer
import logging



@pytest.fixture
def tokenizer():
    return Tokenizer()


def test_add_pattern(tokenizer: Tokenizer):
    ttype = "TOKEN_TYPE"
    patt = r"aa*"

    tokenizer.add_pattern(ttype, patt)

    assert ttype in tokenizer.token_patterns
    assert tokenizer.token_patterns[ttype].re_expr == patt

def test_add_patterns(tokenizer: Tokenizer):
    patterns = {
        "AB": r"(a|b)(a|b)*",
        "ABC": r"(a|b|c)(a|b|c)*",
        "ABCD": r"(a|b|c|d)(a|b|c|d)*",
        "SPACE": r"( |\t)"
    }
    tokenizer.add_patterns(**patterns)
    for token_type, patt in patterns.items():
        assert token_type in tokenizer.token_patterns
        assert tokenizer.token_patterns[token_type].re_expr == patt


def test_add_existent_token_type(tokenizer: Tokenizer):
    ttype = "AB"
    patt = r"(a|b)(a|b)*"

    with pytest.raises(TokenizationError):
        tokenizer.add_pattern(ttype, patt)
        tokenizer.add_pattern(ttype, patt)


def test_tokenizer(tokenizer: Tokenizer):
    # logging.basicConfig(level=logging.DEBUG)
    patterns = {
        "AB": r"(a|b)(a|b)*",
        "ABC": r"(a|b|c)(a|b|c)*",
        "ABCD": r"(a|b|c|d)(a|b|c|d)*",
        "SPACE": r"( |\t)"
    }

    for token_type, patt in patterns.items():
        tokenizer.add_pattern(token_type, patt)

    text = "ab cdaba"
    tokens = tokenizer.tokenize(text)

    types = ["AB", "SPACE", "ABC", "ABCD"]

    assert len(tokens) == len(types)
    for token, ttype in zip(tokens, types):
        assert token.token_type == ttype

    # Test wrong text
    text = "123"
    with pytest.raises(TokenizationError):
        tokenizer.tokenize(text)


def test_wrong_pattern_order(tokenizer: Tokenizer):
    ttype_1 = "ABC"
    patt_1 = r"(a|b|c)(a|b|c)*"

    ttype_2 = "AB"
    patt_2 = r"(a|b)(a|b)*"

    tokenizer.add_pattern(ttype_1, patt_1)
    tokenizer.add_pattern(ttype_2, patt_2)

    text = "ababbbb"
    tokens = tokenizer.tokenize(text)

    assert tokens[0].token_type != ttype_2
