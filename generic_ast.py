"""
This module contains the AST structure for the compiler.
"""

from __future__ import annotations

from typing import List, Optional

from grammar import Item


class AST:
    """Abstract syntax tree.

    Parameters
    ----------
    item : Item
        Item to derive.
    parent : Optional[AST]
        Parent of the derivation, by default None.

    Attributes
    ----------
    parent : Optional[AST]
        Parent of the derivation.
    item : Item
        Item to derive.
    value : object
        Value of the derivation.
    children : List[AST]
        List of children.
    """

    def __init__(self, item: Item, parent: Optional[AST] = None):
        self.parent = parent
        self.item = item
        self.value = None
        self.children: List[AST] = []

    def is_terminal(self) -> bool:
        """Checks if the derivation is a terminal.

        Returns
        -------
        bool
            True if the derivation is a terminal, False otherwise.
        """
        return self.item.is_terminal()

    def print_tree(self, level: int = 0):
        """Prints the derivation tree.

        Parameters
        ----------
        level : int
            level of the derivation.
        """
        val = self.item.__str__()
        if self.item.is_terminal:
            val += f" -> {self.value}"
        print(f"{'  ' * level}{val}")
        if self.children is not None:
            for child in self.children:
                child.print_tree(level + 1)
