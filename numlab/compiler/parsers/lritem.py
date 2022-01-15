from numlab.compiler.grammar import NonTerminal, Production, Symbol


class LRItem:
    """
    This class represents a single item in the LR state machine.
    """

    def __init__(self, prod: Production, dot_pos: int, lookahead: str = None):
        """
        Initializes a new LRItem.

        Parameters
        ----------
        production : Production
            Production that will be used.
        dot_pos : int
            Position of the dot in the production.
        """
        self.prod = prod
        self.lah = lookahead
        self.dot_pos = dot_pos
        self._repr = None

    @property
    def at_symbol(self) -> Symbol:
        """
        Returns the symbol at the dot.

        Returns
        -------
        Symbol
            Symbol at the dot.
        """
        if self.dot_pos < len(self.prod.symbols):
            return self.prod.symbols[self.dot_pos]
        return None

    @property
    def at_non_terminal(self) -> NonTerminal:
        """
        Returns the non-terminal at the dot.

        Returns
        -------
        NonTerminal
            Non-terminal at the dot.
        """
        at_symbol = self.at_symbol
        if at_symbol is None or at_symbol.is_terminal:
            return None
        return at_symbol

    def __repr__(self):
        """
        Returns a string representation of the item.

        Returns
        -------
        str
            String representation of the item.
        """

        if self._repr is not None:
            return self._repr
        head = f"{self.prod.head} -> "
        body_before_dot = " ".join(str(i) for i in self.prod.symbols[: self.dot_pos])
        body_after_dot = " ".join(str(i) for i in self.prod.symbols[self.dot_pos :])
        body = f"{body_before_dot} . {body_after_dot}"
        if self.lah is not None:
            text = f"{head}{body} [{self.lah}]"
        else:
            text = f"{head}{body}"
        self._repr = f"LRItem({text})"
        return self._repr

    def __eq__(self, other):
        if isinstance(other, tuple):
            prod, dot, lah = other
        elif isinstance(other, LRItem):
            prod, dot, lah = other.prod, other.dot_pos, other.lah
        else:
            return False
        same_prod = self.prod == prod
        same_dot = self.dot_pos == dot
        same_lah = self.lah == lah
        return same_prod and same_dot and same_lah

    def __hash__(self):
        return hash(self.__repr__())

    def __lt__(self, other):
        return str(self.prod) < str(other.prod)
