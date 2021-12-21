"""
This module contains the structures for text tokenization.

Example of use:

    from toknizer import Tokenizer

    tknz = Tokenizer()
    tknz.add_pattern("AB", r"[ab]+")
    tknz.add_pattern("Int", r"[0-9]+", lambda lex: int(lex))

    text = "aaaba23bba34"

    tokens = tknz.tokenize(text)
    print(tokens)

    > [Tok('aaaba'), Tok(23), Tok('bba'), Tok(34)]
"""

import logging
from typing import Any, Callable, Dict, List

from exceptions import TokenizationError
from regex_atmt import RegexPattern, check, compile_patt


class Token:
    """Represents a single token.

    Parameters
    ----------
    token_type : str
        Token type name.
    lexem : str
        Token lexem.
    line : int
        Line token position.
    col : int
        Column token position.

    Attributes
    ----------
    token_type : str
        Token type name.
    lexem : str
        Token lexem.
    line : int
        Line token position.
    col : int
        Column token position.
    """

    def __init__(self, token_type: str, lexem: str, line: int = 0, col: int = 0):
        self.token_type = token_type
        self.lexem = lexem
        self.line = line
        self.col = col

    def info(self) -> str:
        """Gives a detailed and formated info about the token.

        Returns
        -------
        str
            Token information.
        """
        line_col = f"(l:{self.line}, c:{self.col})"
        return f"{line_col:<16} {self.token_type:<25} {self.lexem}"

    def __getattr__(self, item):
        return self.token_type == item

    def __eq__(self, other):
        if not isinstance(other, Token):
            return self.lexem == other
        return super().__eq__(other)

    def __repr__(self):
        return f"Tok({self.lexem.__repr__()})"

    def __str__(self):
        return self.__repr__()


class Tokenizer:
    """Tokenizer"""

    def __init__(self):
        self.token_patterns: Dict[str, RegexPattern] = {}
        self._token_found_functions = {}
        self._process_tokens = lambda tk: tk

    def add_pattern(
        self, token_type: str, pattern: str, func: Callable[[str], Any] = None
    ):
        """Adds a pattern for recognizing tokens.

        Adding orden is very important as the patterns are checked in the same
        order they where added.

        Parameters
        ----------
        token_type : str
            Token type name for the pattern.
        pattern : str
            Regex pattern.
        func : Callable[[str], Any]
            When a match is found for a pattern and a token is created this
            function is applied to the token lexem. The token's new lexem will
            be the return value of `func`.
        """
        if token_type in self.token_patterns:
            raise TokenizationError(f"Token type {token_type} already exists.")
        self.token_patterns[token_type] = compile_patt(pattern)
        if func is None:
            func = lambda lex: lex
        self._token_found_functions[token_type] = func

    def add_patterns(self, **kwargs: str):
        """Adds a list of patterns for recognizing tokens

        The order of patterns is very important as the patterns are checked in the same
        order they where added.

        Parameters
        ----------
        **kwargs: str


        Example
        -------
        tknz.add_patterns(
            INT = r"\\d+",
            OPERATOR = r"[+\\-*/]"
            )

        """
        for token_type, patt in kwargs.items():
            self.add_pattern(token_type, patt)

    def process_tokens(self, func: Callable[[List[Token]], List[Token]]):
        """Decorator for processing the tokens after tokenization process.

        The decorated function will recieve the raw token list resulting after
        tokenization and it should return the processed token list.

        Parameters
        ----------
        func : Callable[[List[Token]], List[Token]]
            Function to be decorated.
        """
        self._process_tokens = func
        return func

    def token(
        self, token_type: str, patt: str
    ) -> Callable[[Callable[[str], Any]], Callable[[str], Any]]:
        """Generates a decorator that adds a token pattern and use the decorated
        function to process the token lexem.

        Example
        -------

        This:

            @my_tokenizer.token("tok_type", r"re_patt")
            def tok_type(lexem: str) -> str:
                return lexem.lower()

        Is the same as:

            my_tokenizer.add_pattern(
                "tok_type", r"re_patt", lambda lexem: lexem.lower()
            )

        Parameters
        ----------
        token_type : str
            Token type name for the pattern.
        patt : str
            Regex pattern.

        Returns
        -------
        Callable[[Callable[[str], Any]], Callable[[str], Any]]
            Generated decorator.
        """

        def token_deco(func: Callable[[str], Any]) -> Callable[[str], any]:
            """Decorator that adds a token pattern and use the decorated
            function to process the token lexem.

            Parameters
            ----------
            func : Callable[[str], Any]
                Function that process the token lexem once the token is created.

            Returns
            -------
            Callable[[str], any]
                Decorated function.
            """
            self.add_pattern(token_type, patt, func)
            return func

        return token_deco

    def tokenize(self, text: str) -> List[Token]:
        """Tokenize a text using the added token patterns.

        Parameters
        ----------
        text : str
            Text to be tokenized.
        """
        tokens = []
        line, col = 0, 0
        i = 0
        while i < len(text):
            for token_type, patt in self.token_patterns.items():
                print("matching", token_type, patt.re_expr)
                re_match = patt.match(text[i:])
                if re_match is not None:
                    print(re_match)
                    print(re_match.re_expr)
                    lexem = re_match.matched_text
                    print(lexem)
                    tok_lexem = self._token_found_functions[token_type](lexem)
                    if tok_lexem is not None:
                        tok = Token(token_type, tok_lexem, line, col)
                        print(tok)
                        tokens.append(tok)
                    i += len(lexem)
                    line_breaks = lexem.count("\n")
                    line += line_breaks
                    col += len(lexem)
                    if line_breaks:
                        col = len(lexem.split("\n")[-1])
                    break
            else:
                raise TokenizationError(
                    f"No match found. Line: {line}, Col: {col}.\n"
                    f"Text: {text[i:i+10]}..."
                )

        return self._process_tokens(tokens)
