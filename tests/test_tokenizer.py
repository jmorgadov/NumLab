import re

import pytest
from tokenizer import Tokenizer


@pytest.fixture
def tokenizer():
    return Tokenizer()


def test_add_pattern(tokenizer: Tokenizer):
    ttype = "TOKEN_TYPE"
    patt = r"[a+]"

    tokenizer.add_pattern(ttype, patt)

    assert ttype in tokenizer._token_patterns
    assert tokenizer._token_patterns[ttype] == re.compile(patt)


def test_add_existent_token_type(tokenizer: Tokenizer):
    ttype = "AB"
    patt = r"[ab]+"

    with pytest.raises(ValueError):
        tokenizer.add_pattern(ttype, patt)
        tokenizer.add_pattern(ttype, patt)


def test_tokenizer(tokenizer: Tokenizer):
    patterns = {
        "AB": r"[ab]+",
        "ABC": r"[abc]+",
        "ABCD": r"[abcd]+",
        "SPACE": r"[ \t]"
    }

    for token_type, patt in patterns.items():
        tokenizer.add_pattern(token_type, patt)

    text = "ab cdaba"
    tokens = tokenizer.tokenize(text)

    types = ["AB", "SPACE", "ABC", "ABCD"]

    assert len(tokens) == len(types)
    for token, ttype in zip(tokens, types):
        assert token.token_type == ttype


def test_wrong_pattern_order(tokenizer: Tokenizer):
    ttype_1 = "ABC"
    patt_1 = r"[abc]+"

    ttype_2 = "AB"
    patt_2 = r"[ab]+"

    tokenizer.add_pattern(ttype_1, patt_1)
    tokenizer.add_pattern(ttype_2, patt_2)

    text = "ababbbb"
    tokens = tokenizer.tokenize(text)

    assert tokens[0].token_type != ttype_2
