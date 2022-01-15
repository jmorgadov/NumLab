from typing import Dict, List

from numlab.compiler.grammar import Grammar, Terminal
from numlab.compiler.terminal_set import TerminalSet


def calculate_first(gm: Grammar) -> Dict[str, TerminalSet]:
    first = {expr.name: TerminalSet() for expr in gm.exprs}
    prod_first = {prod: TerminalSet() for _, prod in gm.all_productions()}

    change = True
    while change:
        change = False
        for expr, prod in gm.all_productions():
            for item in prod.symbols:
                if item.is_terminal:
                    change |= first[expr.name].add(item)
                    prod_first[prod].add(item)
                    break
                if item != expr:
                    change |= first[expr.name].update(first[item.name])
                    prod_first[prod].update(first[item.name])
                if "EPS" not in first[expr.name].terminals:
                    break
    return first


def calculate_follow(gm: Grammar, first: TerminalSet = None) -> Dict[str, TerminalSet]:
    """
    Calculate the follow sets for all non-terminals in the grammar.

    Parameters
    ----------
    gm : Grammar
        The grammar to calculate the follow sets for.
    first : TerminalSet, optional
        The first sets of the grammar. If not given, it will be calculated
        first.

    Returns
    -------
    Dict[str, TerminalSet]
        The follow sets for all non-terminals in the grammar.
    """

    # First is needed to calculate follow
    if first is None:
        first = calculate_first(gm)

    follow = {expr.name: TerminalSet() for expr in gm.exprs}
    follow[gm.start_expr.name].add(Terminal("$"))

    change = True
    while change:
        change = False
        for expr, prod in gm.all_productions():
            for i, item in enumerate(prod.symbols):
                next_item = prod.symbols[i + 1] if i + 1 < len(prod.symbols) else None
                if item.is_terminal:
                    continue
                if next_item is None:
                    change |= follow[item.name].update(follow[expr] - "EPS")
                elif next_item.is_terminal:
                    change |= follow[item.name].add(next_item)
                else:
                    change |= follow[item.name].update(first[next_item] - "EPS")
                    if "EPS" in first[next_item].terminals:
                        change |= follow[item.name].update(follow[expr] - "EPS")
    return follow
