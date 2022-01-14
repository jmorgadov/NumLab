"""
This module contains the structures for representing grammars.
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import (Any, Callable, Dict, Iterator, List, Optional, Set, Tuple,
                    Union)

from numlab.compiler.generic_ast import AST
from numlab.compiler.tokenizer import Token, Tokenizer

# Tokenizer for grammars
TKNZ = Tokenizer()
TKNZ.add_pattern("NEWLINE", r"( |\n)*\n\n*( |\n)*", lambda l: "NEWLINE")
TKNZ.add_pattern("SPACE", r"( |\t)( |\t)*", lambda t: None)
TKNZ.add_pattern("COMMENT", r"#(^\n)*\n", lambda t: None)
TKNZ.add_pattern("LITERAL", r"'((^')|(\\'))*(^\\)'", lambda l: l[1:-1])
TKNZ.add_pattern("SPECIAL", r"EPS")
TKNZ.add_pattern("ID", r"(\a|\A|_)(\a|\A|\d|_)*")
TKNZ.add_pattern("OP", r"\||:")


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
        if tok.NEWLINE and new_tokens and new_tokens[-1].NEWLINE:
            continue

        new_tokens.append(tok)
    return new_tokens


class Symbol(metaclass=ABCMeta):
    """Abstract class for representing either a Terminal or a NonTerminal.

    Parameters
    ----------
    name :
        Name of the grammar symbol.

    Attributes
    ----------
    name :
        Name of the grammar symbol.
    """

    def __init__(self, name):
        self.name = name
        self._ast = None

    @property
    def ast(self):
        """Return the abstract syntax tree of the grammar symbol.

        Returns
        -------
        AST
            Abstract syntax tree of the grammar symbol.
        """
        if self.is_terminal:
            return self
        return self._ast

    @property
    def is_terminal(self) -> bool:
        """Checks if the grammar symbol is a terminal or not.

        Returns
        -------
        bool
            True if the grammar symbol is a Terminal.
        """
        return isinstance(self, Terminal)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self is other

    @abstractmethod
    def copy(self) -> Symbol:
        """Creates a copy of the grammar symbol.

        Returns
        -------
        Symbol
            Copy of the grammar symbol.
        """
        pass

    def __hash__(self):
        return hash(self.name)


class Production:
    """Represents a grammar production.

    Parameters
    ----------
    symbols : List[Symbo]
        List of grammar symbols that compose the production.
    """

    def __init__(self, symbols: List[Symbol]):
        self.symbols = symbols
        self._head: NonTerminal = None
        self._builder: Callable = None

    def set_builder(self, func: Callable):
        """Sets the builder function for the production.

        Parameters
        ----------
        func : Callable
            Function that builds the AST.
        """
        self._builder = func

    @property
    def builder(self):
        """Returns the builder function for the production.

        Returns
        -------
        Callable
            Builder function.
        """
        if self._builder is None:
            raise ValueError("Builder function not set.")
        return self.set_builder

    @property
    def head(self):
        """Gets the head of the production.

        Returns
        -------
        NonTerminal
            Head of the production.
        """
        if self._head is None:
            raise ValueError("Production head missing.")
        return self._head

    @property
    def head_str(self) -> str:
        """Gets the head of the production as a string.

        Returns
        -------
        str
            Head of the production.
        """
        return f"{self.head.name} {str(self)}"

    @property
    def is_eps(self) -> bool:
        """Checks if the production is the empty production.

        Returns
        -------
        bool
            True if the production is the empty production.
        """
        return len(self.symbols) == 1 and self.symbols[0] == "EPS"

    def build_ast(self, symbols: List[Symbol]) -> AST:
        """Builds the AST for the production.

        Parameters
        ----------
        symbols : List[Symbol]
            List of grammar symbols that compose the production.

        Returns
        -------
        AST
            AST for the production.
        """
        if self._builder is None:
            raise ValueError(f"Builder function not set on production {self}.")
        return self._builder(*symbols)

    def __getitem__(self, index):
        return self.symbols[index]

    def __setitem__(self, index, item):
        self.symbols[index] = item

    def __repr__(self):
        prod_str = "-> " + " ".join(str(symbol) for symbol in self.symbols)
        return prod_str

    def __str__(self):
        return self.__repr__()


class NonTerminal(Symbol):
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
        for prod in self.prods:
            prod._head = self

    def set_ast(self, ast: AST):
        """Sets the abstract syntax tree for the expression.

        Parameters
        ----------
        ast : AST
            Abstract syntax tree for the expression.

        Returns
        -------
        None
        """
        self._ast = ast

    def copy(self):
        """Creates a copy of the non terminal.

        Returns
        -------
        NonTerminal
            Copy of the non terminal.
        """
        return NonTerminal(self.name, self.prods)

    def check_token(self, token: Token) -> bool:
        """Checks if the token matches the non terminal.

        Parameters
        ----------
        token : Token
            Token to be checked.

        Returns
        -------
        bool
            True if the token matches the non terminal.
        """
        return self.name == token.token_type

    def __getitem__(self, index):
        return self.prods[index]

    def __getattr__(self, item):
        if item.startswith("prod_"):
            return self.prods[int(item[5:])]
        raise AttributeError()

    def __repr__(self):
        return f"NT({self.name})"


class Terminal(Symbol):
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

    def __init__(self, name: str, value: Any = None):
        super().__init__(name)
        self.value = value

    def copy(self):
        """Creates a copy of the terminal.

        Returns
        -------
        Terminal
            Copy of the terminal.
        """
        return Terminal(self.name)

    def check_token(self, token: Token) -> bool:
        """Checks if the token matches the terminal.

        Parameters
        ----------
        token : Token
            Token to be checked.

        Returns
        -------
        bool
            True if the token matches the terminal.
        """
        return self.name == token.token_type

    def __repr__(self):
        return f"T({self.name})"


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
        self.start = None
        if exprs:
            self.start = exprs[0]
        self.exprs_dict = {exp.name: exp for exp in exprs}

    def __getattr__(self, item):
        if item in self.exprs_dict:
            return self.exprs_dict[item]
        raise AttributeError()

    @property
    def symbols(self) -> List[Symbol]:
        """Returns the list of symbols.

        Returns
        -------
        List[Symbol]
            List of symbols.
        """
        non_term = [expr for expr in self.exprs]
        term = list(self.all_terminals())
        return non_term + term

    def assign_builders(self, builders: Dict[str, Callable]) -> None:
        """Assigns the builders for the productions.

        Parameters
        ----------
        builders : Dict[str, Callable]
            Dictionary of builders.
        """
        for expr in self.exprs:
            for prod in expr.prods:
                builder_name = f"{expr.name} {prod}"
                prod.set_builder(builders[builder_name])

    def add_expr(self, expr: NonTerminal):
        """Adds a grammar expression to the grammar.

        Parameters
        ----------
        expr : NonTerminal
            Grammar expression to be added.
        """
        if expr.name in self.exprs_dict:
            raise ValueError(f"Grammar expression {expr.name} already exists.")
        self.exprs.append(expr)
        self.exprs_dict[expr.name] = expr

    @property
    def start_expr(self):
        """Gets the start expression of the grammar.

        Returns
        -------
        NonTerminal
            Start expression.
        """
        if self.start is None:
            raise ValueError("Grammar has no start expression.")
        return self.start

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
                for symbol in prod.symbols:
                    if isinstance(symbol, Terminal) and symbol.name not in [
                        "EPS",
                    ]:
                        terminals.append(symbol)
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

    @staticmethod
    def open(file_path: str) -> Grammar:
        """Reads and create a grammar from a `.gm` file.

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
                for i, symbol in enumerate(prod.symbols):
                    if symbol.name in exprs_dict:
                        prod[i] = exprs_dict[symbol.name]
                    elif symbol.name in terminals:
                        prod[i] = terminals[symbol.name]
                    else:
                        terminals[symbol.name] = symbol
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
        prod_symbols = self._parse_prod_symbols()
        return Production(prod_symbols)

    def _parse_prod_symbols(self) -> List[Symbol]:
        """Parses all the symbols of a production.

        Returns
        -------
        List[Symbol]
            Resulting symbols.
        """
        if self._ctoken.OP:
            return None
        if self._ctoken.NEWLINE:
            return None
        symbol = self._parse_symbol()
        prod_symbols = self._parse_prod_symbols()
        if prod_symbols is None:
            return [symbol]
        return [symbol] + prod_symbols

    def _parse_symbol(self) -> Symbol:
        """Parses a grammar symbol.

        Returns
        -------
        Symbol
            Resulting symbol.
        """
        self._check_token(["ID", "LITERAL", "SPECIAL"])
        name = self._ctoken.lexem

        # It always returns a Terminal but after parsing all terminals with
        # non terminal names will be replaced by the non terminal symbols.
        term = Terminal(name)
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
