import pytest
from tokenizer import Tokenizer
import re

@pytest.fixture
def tokenizer():
    return Tokenizer()

def test_add_pattern(tokenizer: Tokenizer):
    ttype = "TOKEN_TYPE"
    patt = r"[a+]"

    tokenizer.add_pattern(ttype, patt)

    assert ttype in tokenizer._token_patterns
    assert tokenizer._token_patterns[ttype] == re.compile(patt)

def test_add_existent_pattern(tokenizer: Tokenizer):
    ttype = "AB"
    patt = r"[ab]+"
    patt_2 = r"[c]+"

    tokenizer.add_pattern(ttype, patt)
    tokenizer.add_pattern(ttype, patt)
    tokenizer.add_pattern(ttype, patt_2)

    r = 0
    for item in tokenizer._token_patterns:
        if item == ttype: r += 1
    
    assert r == 1
    assert tokenizer._token_patterns[ttype] == re.compile(patt_2)

def test_tokenizer(tokenizer: Tokenizer):
    patterns = {"AB": r"[ab]+", "ABC": r"[abc]+", "ABCD": r"[abcd]+", "SPACE": r"[ \t]"}

    for item in patterns:
        tokenizer.add_pattern(item, patterns[item])
    
    text = "ab cdaba"
    tokens = tokenizer.tokenize(text)

    types = ["AB", "SPACE", "ABC", "ABCD"]

    assert len(tokens) == len(types)
    for i in range(len(types)):
        assert tokens[i].token_type == types[i]

def test_wrong_pattern_order(tokenizer: Tokenizer):
    ttype_1 = "ABC"
    patt_1 = r"[abc]+"

    ttype_2 = "AB"
    patt_2 = r"[ab]+"

    tokenizer.add_pattern(ttype_1, patt_1)
    tokenizer.add_pattern(ttype_2, patt_2)

    text = "ababbbb"
    tokens = tokenizer.tokenize(text)

    with pytest.raises(AssertionError):
        assert tokens[0].token_type == ttype_2