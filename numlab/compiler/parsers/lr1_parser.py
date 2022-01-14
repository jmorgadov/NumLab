import logging
from functools import lru_cache
from typing import Dict, List, Tuple

from numlab.compiler.generic_ast import AST
from numlab.compiler.grammar import (Grammar, NonTerminal, Production, Symbol,
                                     Terminal)
from numlab.compiler.grammar_ops import calculate_first, calculate_follow
from numlab.compiler.parsers.lritem import LRItem
from numlab.compiler.parsers.parser import Parser
from numlab.compiler.tokenizer import Token
from numlab.exceptions import ParsingError


class LR1Table:
    """
    This class represents the LR1 table.
    """

    def __init__(self, grammar: Grammar):
        """
        Initializes a new LR1 table.

        Parameters
        ----------
        grammar : Grammar
            Grammar that will be used.
        """
        self.grammar = grammar
        self._first = None
        self._follow = None

        # [state, symbol] -> [next_state, production]
        self._table: Dict[Tuple[int, Symbol], Tuple[int, Production]] = {}
        self._build_table()
        self._states_by_id: Dict[int, List[LRItem]] = None
        self._lr_items: Dict[Production, int, Terminal] = None
        self._item_prods: Dict[NonTerminal, Production] = None

    def _prepare_grammar(self):
        logging.info("Preparing grammar (adding S')")
        if "S`" not in self.grammar.exprs_dict:
            non_ter_prod = Production([self.grammar.start])
            non_ter = NonTerminal("S`", [non_ter_prod])
            self.grammar.add_expr(non_ter)
            self.grammar.start = non_ter
            self.grammar.start.prod_0.set_builder(lambda s: s.ast)

    def _extract_grammar_lr_items(self) -> List[LRItem]:
        """Extracts all LR items from the grammar."""

        logging.info("Extracting all LR items")
        lr_items = []
        self._item_prods = {}
        for _, prod in self.grammar.all_productions():
            for dot_pos in range(len(prod.symbols) + 1):
                item_prod = prod
                is_eps = prod.is_eps
                if is_eps:
                    item_prod = Production([])
                    item_prod._head = prod.head
                    item_prod._builder = prod._builder
                slr_item = LRItem(item_prod, dot_pos)
                lr_items.append(slr_item)
                if prod.head not in self._item_prods:
                    self._item_prods[prod.head] = []
                self._item_prods[prod.head.name].append(item_prod)
                if is_eps:
                    break
        logging.info(f"Found {len(lr_items)} LR items")
        logging.debug("Exacted items in the LR automata:")
        for lr_item in lr_items:
            logging.debug(f"  {lr_item}")
        return lr_items

    def _contained_in_first(self, terminal: Terminal, *symbols):
        """Checks if a terminal is contained in the first set of a set of symbols.

        Parameters
        ----------
        terminal : Terminal
            Terminal to be checked.
        symbols : Symbol
            Symbols to be checked.

        Returns
        -------
        bool
            True if the terminal is contained in the first set of the symbols.
        """
        for symbol in symbols:
            if isinstance(symbol, Symbol) and symbol.is_terminal:
                return symbol == terminal
            if terminal in self._first[symbol]:
                return True
            if "EPS" not in self._first[symbol]:
                break
        return False

    def _build_table(self):
        self._prepare_grammar()
        self._first = calculate_first(self.grammar)
        self._follow = calculate_follow(self.grammar, self._first)
        items = self._extract_grammar_lr_items()

        self._lr_items = {}
        for item in items:
            for follow in self._follow[item.prod.head]:
                new_lr_item = LRItem(item.prod, item.dot_pos, follow)
                self._lr_items[item.prod, item.dot_pos, follow] = new_lr_item

        init_state = self._closure(
            [
                self._lr_items[
                    self.grammar.start_expr.prod_0,
                    0,
                    self._follow[self.grammar.start_expr][0],
                ]
            ]
        )

        self._states_by_id = {0: init_state}

        logging.info("Building LR1 table")
        lr1_table: Dict[Tuple[int, str], Tuple[int, Production]] = {}
        current_state = 0
        while current_state < len(self._states_by_id):
            logging.debug(f"Building state {current_state}")
            state = self._states_by_id[current_state]
            for item in state:
                if item.at_symbol is None:
                    val = "OK" if item.prod.head.name == "S`" else item.prod
                    lr1_table[current_state, item.lah.name] = val
                else:
                    lr1_table[current_state, item.at_symbol.name] = self._goto(
                        current_state, item.at_symbol
                    )
            current_state += 1
        self._table = lr1_table
        logging.info("LR1 table built")

    def get_state_number(self, items: List[LRItem]) -> int:
        """Returns the state number for a list of LR items.

        Parameters
        ----------
        items : List[LRItem]
            List of LR items.

        Returns
        -------
        int
            State number.
        """
        for i, state in self._states_by_id.items():
            if state == items:
                return i
        i = len(self._states_by_id)
        self._states_by_id[i] = items
        return i

    def __getitem__(self, index):
        return self._table.get(index, None)

    @lru_cache(maxsize=None)
    def _goto(self, state: int, symbol: Symbol) -> int:
        """Returns the state number for a state and a symbol.

        Parameters
        ----------
        state : int
            State number.
        symbol : Symbol
            Symbol.

        Returns
        -------
        int
            State number.
        """
        state_items = self._states_by_id[state]
        filtered_items = [
            self._lr_items[item.prod, item.dot_pos + 1, item.lah]
            for item in state_items
            if item.at_symbol == symbol
        ]
        clausure = sorted(self._closure(filtered_items))
        return self.get_state_number(clausure)

    def _closure(self, items: List[LRItem]) -> List[LRItem]:
        """Returns the closure of a list of LR items.

        Parameters
        ----------
        items : List[LRItem]
            List of LR items.

        Returns
        -------
        List[LRItem]
            Closure of the list of LR items.
        """
        logging.debug(f"Calculating closure of {items}")
        closure = items
        change = True
        while change:
            change = False
            for item in closure:
                next_item = item.at_symbol
                if next_item is None or next_item.is_terminal:
                    continue
                lah = item.lah
                rest = item.prod.symbols[item.dot_pos + 1 :]
                rest.append(lah)
                for prod in self._item_prods[next_item.name]:
                    for fol in self._follow[next_item]:
                        if not self._contained_in_first(fol, *rest):
                            continue
                        lr_item = self._lr_items[prod, 0, fol]
                        if lr_item not in closure:
                            closure.append(lr_item)
                            change = True
        return closure


class LR1Parser(Parser):
    """LR1 Parser.

    Parameters
    ----------
    grammar : Grammar
        Grammar to be used.
    """

    def __init__(self, grammar: Grammar, lr1_table: LR1Table = None):
        super().__init__(grammar)
        self.lr1_table = LR1Table(grammar) if lr1_table is None else lr1_table

    def parse(self, tokens: List[Token]) -> AST:
        logging.debug(f"Parsing {len(tokens)} tokens (LR1)")
        table = self.lr1_table
        stack: List[Tuple[Symbol, int]] = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            logging.info(f"Parsing token {token}. Stack: {stack}")
            current_state = stack[-1][1] if stack else 0
            table_val = table[current_state, token.token_type]
            logging.info(
                f"Table value: {table_val} at ({current_state}, {token.token_type})"
            )
            if table_val == "OK":
                break
            if isinstance(table_val, int):
                logging.info(f"Making SHIFT action")
                term = Terminal(token.token_type, value=token.lexem)
                stack.append((term, table_val))
                i += 1
            elif isinstance(table_val, Production):
                logging.info(f"Making REDUCE action")
                reduce_prod = table_val
                # Pop from stack the necessary items
                items_needed = len(reduce_prod.symbols)
                items = []
                if items_needed != 0:
                    stack, items = stack[:-items_needed], stack[-items_needed:]
                items = [item[0].ast for item in items]

                # Apply reduction
                new_head = reduce_prod.head.copy()
                new_head.set_ast(reduce_prod.build_ast(items))
                logging.info(f"Reduced to {new_head}")
                logging.info(f"{new_head} AST = {new_head.ast}")

                # Check next state
                left_state = stack[-1][1] if stack else 0
                next_state = table[left_state, reduce_prod.head.name]
                logging.info(
                    f"Next state GOTO({left_state},{reduce_prod.head.name})"
                    f" is {next_state}"
                )
                # Push to stack the new item
                stack.append((new_head, next_state))
            elif table_val is None:
                raise ParsingError(f"Unexpected token", token)

        if len(stack) != 1:
            raise ValueError(f"Dirty stack at the end of the parsing. Stack: {stack}")
        return stack[-1][0].ast
