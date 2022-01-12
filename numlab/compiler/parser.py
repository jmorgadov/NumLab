"""
This module contains the basic structures for parsing.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Dict, List, Tuple

from numlab.automata import Automata, State
from numlab.compiler.generic_ast import AST
from numlab.compiler.grammar import (Grammar, NonTerminal, Production, Symbol,
                                     Terminal)
from numlab.compiler.terminal_set import TerminalSet
from numlab.compiler.tokenizer import Token, Tokenizer
from numlab.exceptions import ParsingError

_REDUCE_ACTION = 0
_SHIFT_ACTION = 1


def calculate_first(gm: Grammar) -> TerminalSet:
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


def calculate_follow(gm: Grammar, first: TerminalSet = None) -> TerminalSet:
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
    TerminalSet
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
        head = f"{self.prod.head} -> "
        body_before_dot = " ".join(str(i) for i in self.prod.symbols[: self.dot_pos])
        body_after_dot = " ".join(str(i) for i in self.prod.symbols[self.dot_pos :])
        body = f"{body_before_dot} . {body_after_dot}"
        if self.lah is not None:
            text = f"{head}{body} [{self.lah}]"
        else:
            text = f"{head}{body}"
        return f"LRItem({text})"

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

    def __lt__(self, other):
        return str(self.prod) < str(other.prod)


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


class Parser:
    """Structure used for parsing a text given a grammar and a tokenizer.

    Parameters
    ----------
    grammar : Grammar
        Grammar that will be use for parsing.
    tokenizer : Tokenizer
        Tokenizer that will be use for tokenize a given txt.
    """

    def __init__(self, grammar: Grammar, tokenizer: Tokenizer = None):
        self.grammar = grammar
        self.tokenizer = tokenizer
        self._first = None
        self._prod_first = None
        self._follow = None
        self.token_to_term = {}
        self._slr_atmt_nfa = None
        self._stt2item = None

    def _calculate_first_and_follow(self):
        """Recalculates the `first` and `follow` sets of the grammar."""
        self._first = calculate_first(self.grammar)
        self._follow = calculate_follow(self.grammar, self._first)

    def _build_slr_atmt(self):
        if self._slr_atmt_nfa is not None and self._stt2item is not None:
            return self._slr_atmt_nfa, self._stt2item

        logging.debug("Building SLR automata")

        # Prepare grammar
        logging.debug("Preparing grammar (adding S')")
        if "S`" not in self.grammar.exprs_dict:
            non_ter_prod = Production([self.grammar.start])
            non_ter = NonTerminal("S`", [non_ter_prod])
            self.grammar.add_expr(non_ter)
            self.grammar.start = non_ter
            self.grammar.start.prod_0.set_builder(lambda s: s.ast)

        # Extract all slr items
        logging.debug("Extracting all SLR items")
        slr_items = []
        slr_item_dict = {}
        for _, prod in self.grammar.all_productions():
            for dot_pos in range(len(prod.symbols) + 1):
                slr_item = LRItem(prod, dot_pos)
                slr_items.append(slr_item)
                slr_item_dict[prod, dot_pos] = slr_item
        logging.debug(f"Found {len(slr_items)} SLR items")
        logging.debug("Exacted items in the SLR automata:")
        for slr_item in slr_items:
            logging.debug(f"  {slr_item}")

        # Build the SLR state machine
        logging.debug("Adding states to automata")
        stt2item, item2stt = {}, {}
        atmt = Automata()
        for i, slr_item in enumerate(slr_items):
            stt = atmt.add_state(
                f"q{i}",
                start=slr_item.prod.head.name == "S`" and slr_item.dot_pos == 0,
                end=True,
                name=str(slr_item),
            )
            stt2item[stt] = slr_item
            item2stt[slr_item] = stt

        logging.debug("Adding transitions to automata")
        for stt in atmt.states.values():
            slr_item = stt2item[stt]
            if slr_item.dot_pos == len(slr_item.prod.symbols):
                continue
            gm_item = slr_item.prod.symbols[slr_item.dot_pos]
            next_item = slr_item_dict[slr_item.prod, slr_item.dot_pos + 1]
            atmt.add_transition(stt, item2stt[next_item], gm_item.name)
            all_slr_items_head_gm = [
                slr_item_dict[p, 0]
                for _, p in self.grammar.all_productions()
                if p.head == gm_item
            ]
            for slr_item_gm in all_slr_items_head_gm:
                atmt.add_transition(stt, item2stt[slr_item_gm])

        self._slr_atmt_nfa = atmt
        self._stt2item = stt2item
        return atmt, stt2item

    def parse_file(self, file_path: str) -> AST:
        """Opens a file and parses it contents.

        Parameters
        ----------
        file_path : str
            File path.

        Returns
        -------
        AST
            AST generated by the parser.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        return self.parse(text)

    def parse(self, text: str) -> AST:
        """Parses a text.

        Parameters
        ----------
        text : str
            Text to be parsed.

        Returns
        -------
        AST
            AST generated by the parser.
        """
        tokens = self.tokenizer.tokenize(text)
        return self.parse_tokens(tokens)

    def parse_tokens(self, tokens: List[Token]) -> AST:
        """Parses a list of tokens.

        Parameters
        ----------
        tokens : List[Token]
            List of tokens to be parsed.
        method : str
            Method used for parsing.

        Returns
        -------
        AST
            AST generated by the parser.
        """
        tokens += [Token("$", "$")]
        return self._lr1_parse_tokens(tokens)

    def _lr1_parse_tokens(self, tokens: List[Token]) -> AST:
        """Parses a list of tokens using LR parsing.

        Parameters
        ----------
        tokens : List[Token]
            List of tokens to be parsed.

        Returns
        -------
        AST
            AST generated by the parser.
        """
        # Build LR1 parse table
        logging.debug(f"Parsing {len(tokens)} tokens (LR1)")
        table = LR1Table(self.grammar)
        stack: List[Tuple[Symbol, State]] = []
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

    def _slr_parse_tokens(self, tokens: List[Token]) -> AST:
        """Parses a list of tokens.

        Parameters
        ----------
        tokens : List[Token]
            List of tokens to be parsed.

        Returns
        -------
        AST
            AST generated by the parser.
        """
        logging.info("Parsing tokens using SLR method")

        # Build slr nfa automata
        slr_atmt_nfa, stt2item = self._build_slr_atmt()

        # Calculate first and follows
        self._calculate_first_and_follow()

        # Build slr dfa automata from slr nfa automata
        logging.info("Building SLR DFA automata")
        slr_atmt, dfa2nfa = slr_atmt_nfa.to_dfa(dfa2nfa=True)
        current_state = slr_atmt.start_state

        # State to SRL items dictionary
        logging.info("Building state to SRL items dictionary")
        state_items: Dict[State, List[LRItem]] = {}
        for state, old_states in dfa2nfa.items():
            state_items[state] = []
            for old_state in old_states:
                state_items[state].append(stt2item[old_state])

        # Initialize stack
        logging.info("Initializing stack")
        stack: List[Tuple[Symbol, State]] = []

        i = 0
        logging.info("Parsing tokens")
        while i < len(tokens):
            token = tokens[i]
            current_state = slr_atmt.start_state if not stack else stack[-1][1]
            action: int = None
            reduce_prod: Production = None

            # Decide between shift and reduce
            posible_items = state_items[current_state]
            for item in posible_items:
                if item.dot_pos == len(item.prod.symbols) and self._follow[
                    item.prod.head.name
                ].has_token(token):
                    if action is None or action == _REDUCE_ACTION:
                        action = _REDUCE_ACTION
                        reduce_prod = item.prod
                    else:
                        raise ParsingError("Ambiguity in the SLR", token)
                elif item.dot_pos < len(item.prod.symbols) and item.prod.symbols[
                    item.dot_pos
                ].check_token(token):
                    if action is None:
                        action = _SHIFT_ACTION
                    else:
                        raise ParsingError("Ambiguity in the SLR", token)

            if action == _REDUCE_ACTION:
                # Pop from stack the necessary items
                items_needed = len(reduce_prod.symbols)
                stack, items = stack[:-items_needed], stack[-items_needed:]
                items = [item[0] for item in items]

                # Apply reduction
                new_head = reduce_prod.head.copy()
                new_head.ast = reduce_prod.build_ast(items)

                # Check next state
                current_state = slr_atmt.start_state if not stack else stack[-1][1]
                next_state = current_state.next_state(new_head.name)

                # Push to stack the new item
                stack.append((new_head, next_state))
                if new_head.name == "S`":
                    break
            elif action == _SHIFT_ACTION:
                i += 1
                next_state = current_state.next_state(token.token_type)
                term = Terminal(token.token_type, value=token.lexem)
                if next_state is None:
                    raise ParsingError("Invalid token", token)
                stack.append((term, next_state))
            else:
                raise ParsingError("Invalid token", token)
        if len(stack) != 1:
            raise ParsingError("Invalid tokens", tokens[-1])
        return stack[0][0].ast
