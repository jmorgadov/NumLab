"""
This module contains the structures for representing grammars.
"""

from __future__ import annotations

from abc import ABCMeta
from typing import Iterator, List, Optional, Set, Tuple, Union

from tokenizer import Token, Tokenizer

# Tokenizer for grammars
TKNZ = Tokenizer()
TKNZ.add_pattern("NEWLINE", r"[ \n]*\n+[ \n]*", lambda l: "NEWLINE")
TKNZ.add_pattern("SPACE", r"[ \t]+", lambda t: None)
TKNZ.add_pattern("LITERAL", r"'\.*[^\\]'", lambda l: l[1:-1])
TKNZ.add_pattern("SPECIAL", r"[A-Z_][A-Z0-9_]*")
TKNZ.add_pattern("ID", r"[a-zA-Z_][a-zA-Z0-9_]*")
TKNZ.add_pattern("OP", r"[|:]")


@TKNZ.process_tokens
def _process_tokens(tokens: List[Token]) -> List[Token]:
    """Process the tokens of a grammar file.

    This allows grammars to have productions on independent lines.

    Parameters
    ----------
    tokens : List[Token]
        Grammar tokens.

    Returns
    -------
    List[Token]
        Processed tokens.
    """
    new_tokens = []
    skip = 0
    for i, tok in enumerate(tokens):
        if skip:
            skip -= 1
            continue
        next_tok = tokens[i + 1] if i < len(tokens) - 1 else None
        last_tok = tokens[i - 1] if i > 0 else None
        if not new_tokens and tok.NEWLINE:
            continue
        if (
            tok.NEWLINE
            and next_tok is not None
            and last_tok is not None
            and last_tok.OP
            and last_tok.lexem == ":"
            and next_tok.OP
            and next_tok.lexem == "|"
        ):
            skip = 1
            continue
        if (
            tok.NEWLINE
            and next_tok is not None
            and next_tok.OP
            and next_tok.lexem == "|"
        ):
            continue
        new_tokens.append(tok)
    return new_tokens


class Item(metaclass=ABCMeta):
    """Abstract class for representing either a Terminal or a NonTerminal.

    Parameters
    ----------
    name :
        Name of the grammar item.

    Attributes
    ----------
    name :
        Name of the grammar item.
    """

    def __init__(self, name):
        self.name = name

    @property
    def is_terminal(self) -> bool:
        """Checks if the grammar item is a terminal or not.

        Returns
        -------
        bool
            True if the grammar item is a Terminal.
        """
        return isinstance(self, Terminal)

    def __str__(self):
        return self.name


class Production:
    """Represents a grammar production.

    Parameters
    ----------
    items : List[Item]
        List of grammar items that compose the production.
    """

    def __init__(self, items: List[Item]):
        self.items = items
        self.first = None

    def calculate_first(self, trace: List[NonTerminal] = []):
        """Calculates the `first` set of the production.

        Parameters
        ----------
        trace : List[NonTerminal]
            List of non terminals walked in the recursion.
        """
        if self.first is not None:
            return
        first = []
        for item in self.items:
            if item in trace:
                rec_eval = " -> ".join(it.name for it in trace)
                raise ValueError(
                    "Invalid grammar. Possible recursive evaluation:\n {rec_eval}"
                )
            item_first = item.calculate_first(trace + [item])
            first += item_first
            if not any(f.name == "EPS" for f in item_first):
                break
        self.first = first

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, item):
        self.items[index] = item

    def __repr__(self):
        s = "-> "
        for item in self.items:
            s += f"{item} "
        return s

    def __str__(self):
        s = "  | "
        for item in self.items:
            s += f"{item} "
        return s


class NonTerminal(Item):
    """Represents a non terminal (a grammar expression).

    Parameters
    ----------
    name : str
        Name of the expression.
    prods : List[Production]
        List of productions that compose the expression.
    """

    def __init__(self, name, prods: Optional[List[Production]] = None):
        super().__init__(name)
        self.prods = [] if prods is None else prods
        self.first_dict = None
        self.first = []
        self.follow = []

    def calculate_first(self, trace: List[NonTerminal] = None) -> List[Terminal]:
        """Calculates the `first` set of the expression.

        Parameters
        ----------
        trace : List[NonTerminal]
            List of non terminals walked in the recursion.

        Returns
        -------
        List[Terminal]
            List of the `first` set's items.
        """
        if self.first_dict is not None:
            return self.first_dict
        self.first_dict = {}
        if trace is None:
            trace = [self]
        for prod in self.prods:
            prod.calculate_first(trace)
            for fst in prod.first:
                if fst not in self.first_dict:
                    self.first_dict[fst] = []
                self.first_dict[fst].append(prod)
        self.first = list(self.first_dict.keys())
        return self.first

    def __getitem__(self, index):
        return self.prods[index]

    def __getattr__(self, item):
        if item.startswith("prod_"):
            return self.prods[int(item[5:])]
        raise AttributeError()

    def __repr__(self):
        return f"NT({self.name})"


class Terminal(Item):
    """Terminal.

    Parameters
    ----------
    name : str
        Name of the terminal.
    match :
        Regex pattern used to check if a token lexem match in parsing process.

    Attributes
    ----------
    name : str
        Name of the terminal.
    match : str
        Regex pattern used to check if a token lexem match in parsing process.
    """

    def __init__(self, name: str, match: str = None):
        super().__init__(name)
        self.match = match
        self.follow = self

    def __repr__(self):
        return f"T({self.name})"

    def calculate_first(self, trace: List[NonTerminal] = []) -> List[Terminal]:
        """Calculates the `first` set of this item. As it is a Terminal, the
        `first` se is itself.

        Parameters
        ----------
        trace : List[NonTerminal]
            List of non terminals walked in the recursion.

        Returns
        -------
        List[Terminal]
            List of the `first` set's items.
        """
        return [self]


class Grammar:
    """Represents a Grammar.

    Parameters
    ----------
    exprs : List[NonTerminal]
        Grammar expressions.

    Attributes
    ----------
    exprs : List[NonTerminal]
        Grammar expressions.
    """

    def __init__(self, exprs: List[NonTerminal] = None):
        self.exprs = [] if exprs is None else exprs
        if exprs:
            self.start = exprs[0]
        self.exprs_dict = {exp.name: exp for exp in exprs}

    def __getattr__(self, item):
        if item in self.exprs_dict:
            return self.exprs_dict[item]
        raise AttributeError()

    def all_terminals(self) -> Set[Terminal]:
        """Set of all the terminals in the grammar.

        Returns
        -------
        Set[Terminal]
            Terminals set.
        """
        terminals = []
        for exp in self.exprs_dict.values():
            for prod in exp.prods:
                for item in prod.items:
                    if isinstance(item, Terminal) and item.name not in [
                        "NEWLINE",
                        "EPS",
                    ]:
                        terminals.append(item)
        return set(terminals)

    def all_productions(self) -> Iterator[Tuple[NonTerminal, Production]]:
        """Production iterator.

        In each iteration a tuple is given where the first element is the
        expression and the second is the production.

        Returns
        -------
        Iterator[Tuple[NonTerminal, Production]]
            (Expression, Production) iterator.
        """
        for expr in self.exprs:
            for prod in expr.prods:
                yield (expr, prod)

    def assign_term_matches(self, **matches: str):
        """Assigns a set of matches for serveral terminals.

        Example:

        This assigns a match pattern for the terminal `i` on a grammar `grm`:

            >>> grm.assign_term_matches(i=r"[0-9]+")

        Parameters
        ----------
        matches : Dict[str, str]
            Kwargs containing the match patterns (values) for each terminal
            (keys).
        """
        for term in self.all_terminals():
            if term.name in matches:
                term.match = matches[term.name]
            elif term.match is None:
                print(f"[WARNING] Terminal {term.name} not found in match dictionary")

    @staticmethod
    def open(file_path: str) -> Grammar:
        """Reads and create a grammar from a `.grm` file.

        The `.grm` format can express a gramma as shown bellow.

        expression: production_1 | production_2 | ... | production_n

        Example:

        Expr: Term Expr_X
        Expr_X: '+' Expr | EPS
        Term: Factor Term_Y
        Term_Y: '*' Term | EPS
        Factor: '(' E ')' | i

        Productions also can be separated on independent lines. The follow
        grammar is the same as the show as a example:

        Expr: Term Expr_X

        Expr_X:
            | '+' Expr
            | EPS

        Term: Factor Term_Y

        Term_Y:
            | '*' Term
            | EPS

        Factor:
            | '(' E ')'
            | i

        Parameters
        ----------
        file_path : str
            Grammar file path.

        Returns
        -------
        Grammar
            Readed grammar.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        tokens = TKNZ.tokenize(text)
        grm_parser = _GrammarParser(tokens)
        grm = grm_parser.parse()
        return grm


class _GrammarParser:
    """Parser for grammars.

    Parameters
    ----------
    tokens : List[Token]
        Tokens to be parsed.
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self._cursor = 0

    def _check_token(
        self,
        expected_type: Union[str, List[str]],
        expected_value: str = None,
        pos: int = None,
        or_none: bool = False,
    ):
        """Check if the token in a given position match the expected type and
        value.

        Parameters
        ----------
        expected_type : Union[str, List[str]]
            Expected token type.
        expected_value : str, optional
            Expected value (lexem) of the token. If None then the value is not
            checked, by default None.
        pos : int, optional
            Position of the token to be checked. If None then `pos` is taken as
            the cursor prosition, by default None.
        or_none : bool, optional
            Do not raise exception if the position is invalid.

        Raises
        ------
        ValueError
            If the token does not match with the given restrictions.
        """
        if pos is None:
            pos = self._cursor
        if not isinstance(expected_type, list):
            expected_type = [expected_type]
        if pos >= len(self.tokens):
            if not or_none:
                raise ValueError("Expected token type: {expected_type}")
        if self.tokens[pos].token_type not in expected_type:
            raise ValueError(
                f"Error parsing token {self.tokens[pos]}. Expected "
                f"token type: {expected_type}."
            )
        if expected_value and self.tokens[pos].lexem != expected_value:
            raise ValueError(
                f"Error parsing token {self.tokens[pos]}. Expected "
                f"token value: {expected_value}"
            )

    @property
    def _ctoken(self) -> Token:
        """Token as cursos position (current token)self."""
        if self._cursor >= len(self.tokens):
            return None
        return self.tokens[self._cursor]

    def parse(self) -> Grammar:
        """Parses the tokens.

        Returns
        -------
        Grammar
            Resulting grammar.
        """
        self._cursor = 0
        return self._parse_grammar()

    def _parse_grammar(self) -> Grammar:
        """Parse a grammar.

        Returns
        -------
        Grammar
            Resulting grammar.
        """
        if self._cursor >= len(self.tokens):
            return None
        self._check_token("ID")
        exprs = self._parse_expr_list()
        exprs_dict = {exp.name: exp for exp in exprs}
        terminals = {}
        for exp in exprs:
            for prod in exp.prods:
                for i, item in enumerate(prod.items):
                    if item.name in exprs_dict:
                        prod[i] = exprs_dict[item.name]
                    elif item.name in terminals:
                        prod[i] = terminals[item.name]
                    else:
                        terminals[item.name] = item
        return Grammar(exprs)

    def _parse_expr_list(self) -> List[NonTerminal]:
        """Parses an expression list.

        Returns
        -------
        List[NonTerminal]
            Resulting expressions.
        """
        if self._ctoken is None:
            return None
        expr = self._parse_expr()
        expr_list = self._parse_expr_list()
        exprs = [expr]
        if expr_list is not None:
            exprs += expr_list
        return exprs

    def _parse_expr(self) -> NonTerminal:
        """Parses an expression.

        Returns
        -------
        NonTerminal
            Resulting expresson.
        """
        self._check_token("ID")
        expr_name = self._ctoken.lexem
        self._cursor += 1
        self._check_token("OP", ":")
        self._cursor += 1
        prod = self._parse_prod()
        prod_list = self._parse_prod_list()
        self._check_token("NEWLINE", or_none=True)
        self._cursor += 1
        prods = [prod]
        if prod_list is not None:
            prods += prod_list
        expr = NonTerminal(expr_name, prods)
        return expr

    def _parse_prod(self) -> Production:
        """Parses a production.

        Returns
        -------
        Production
            Resulting production.
        """
        prod_items = self._parse_prod_items()
        return Production(prod_items)

    def _parse_prod_items(self) -> List[Item]:
        """Parses all the items of a production.

        Returns
        -------
        List[Item]
            Resulting items.
        """
        if self._ctoken.OP:
            return None
        if self._ctoken.NEWLINE:
            return None
        item = self._parse_item()
        prod_items = self._parse_prod_items()
        if prod_items is None:
            return [item]
        return [item] + prod_items

    def _parse_item(self) -> Item:
        """Parses a grammar item.

        Returns
        -------
        Item
            Resulting item.
        """
        self._check_token(["ID", "LITERAL", "SPECIAL"])
        name = self._ctoken.lexem
        match = None
        if self._ctoken.LITERAL:
            match = name
            name = f"'{match}'"

        # It always returns a Terminal but after parsing all terminals with
        # non terminal names will be replaced by the non terminal item.
        term = Terminal(name, match)
        self._cursor += 1
        return term

    def _parse_prod_list(self) -> List[Production]:
        """Parses a production list.

        Returns
        -------
        List[Production]
            Resulting productions.
        """
        if self._cursor >= len(self.tokens):
            return None
        if self._ctoken.NEWLINE:
            return None
        self._check_token("OP", "|")
        self._cursor += 1
        prod = self._parse_prod()
        prod_list = self._parse_prod_list()
        if prod_list is None:
            return [prod]
        return [prod] + prod_list
