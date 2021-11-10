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

