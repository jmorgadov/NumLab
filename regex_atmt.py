"""
This module contains the necessary functions to build an automata
from a regular expression and match a text against it.

Exmaple:
    >>> from regex_atmt import match
    >>> match("a*b", "ab")
    RegexMatch(matched:'ab'; end=2)"
    >>> match("a+b", "b")
    >>> match("a*b", "abb")
    RegexMatch(matched:'abb'; end=3)"
    >>> match("a*b", "abbfoo")
    RegexMatch(matched:'abb'; end=3)"
"""

import logging

from automata import Automata

SPECIAL_CHARS = ["(", ")", "|", "*", "^"]
DIGITS = list("0123456789")
LOWER_CASE_CHARS = list("abcdefghijklmnopqrstuvwxyz")
UPPER_CASE_CHARS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


class RegexMatch:
    """
    Represents the result of a match.

    Parameters
    ----------
    re_expr : str
        The regular expression used to match the text.
    text : str
        The text to match against the regular expression.
    pos : int
        The position where the match ended.

    Attributes
    ----------
    re_expr : str
        The regular expression used to match the text.
    text : str
        The text that was matched against the regular expression.
    pos : int
        The position where the match ended.
    """

    def __init__(self, re_expr: str, text: str, end: int):
        self.re_expr = re_expr
        self.text = text
        self.end = end

    def __repr__(self):
        return f"RegexMatch(matched:{self.text[:self.end]}; end={self.end})"

    @property
    def matched_text(self) -> str:
        return self.text[: self.end]


class RegexPattern:
    """
    Regular expression compiled to an automata.

    Parameters
    ----------
    re_expr : str
        The regular expression to be converted.

    Attributes
    ----------
    re_expr : str
        The regular expression.
    atmt : Automata
        The automata representing the regular expression.

    Raises
    ------
    ValueError
        If the regular expression is not valid.
    """

    def __init__(self, re_expr: str):
        self.re_expr = re_expr
        self.atmt = _build_automata(self.re_expr).flat()

    def match(self, text: str) -> RegexMatch:
        """
        Match the text against the regular expression.

        Parameters
        ----------
        text : str
            The text to match against the regular expression.

        Returns
        -------
        RegexMatch
            The RegexMatch object containing the result of the match.
        """

        val = self.atmt.run(text)
        return RegexMatch(self.re_expr, text, self.atmt._pos) if val else None


def _find_matching_paren(text: str, start: int = 0) -> int:
    count = 0
    for i in range(start, len(text)):
        if text[i] == "(":
            count += 1
        elif text[i] == ")":
            count -= 1
        if count == 0:
            return i
    raise ValueError("Unmatched parenthesis.")


def _get_basic_re_expr(re_expr: str) -> str:
    """
    Converts a regular expression to a basic regular expression.

    Parameters
    ----------
    re_expr : str
        Regular expression.

    Returns
    -------
    str
        Basic regular expression.
    """
    return re_expr


def _apply_star_op(atmt: Automata) -> Automata:
    """
    Applies the star operator to an automata.

    Parameters
    ----------
    atmt : Automata
        Automata.

    Returns
    -------
    Automata
        Automata.
    """
    #
    #           .---- < ----.
    #          /             \
    #  - - > (q0) -- .. --> (qf) --> ((new_qf))
    #          \                      /
    #           `-------- > ---------'
    #

    flat_atmt = atmt.flat()
    q_0 = flat_atmt.start_state
    q_f = flat_atmt.end_state
    print(q_0, q_f)
    flat_atmt.states.pop(q_f.name)
    for state in list(flat_atmt.states.values()):
        for trans in state.transitions:
            print(f"Checking {trans}")
            if trans.to_state == q_f:
                trans.to_state = q_0
                print(f"Changing final transition to {trans.to_state}")
                print(trans)
    flat_atmt.end_states = [flat_atmt.start_state]
    return flat_atmt


def _check_special_char(re_expr, index, atmt):
    if index < 0 or index >= len(re_expr) or re_expr[index] != "*":
        return atmt, False
    atmt = _apply_star_op(atmt)
    return atmt, True


def _process_single_char(re_expr: str, negated: bool) -> Automata:
    """
    Processes a single character.

    Parameters
    ----------
    re_expr : str
        Regular expression.

    Returns
    -------
    Automata
        Automata.
    """
    #
    # - - > (q0) -- a --> ((q1))
    #
    escaped = False
    if re_expr[0] == "\\":
        re_expr = re_expr[1:]
        logging.debug("Escaped character")
        escaped = True
    cond = re_expr[0]
    logging.debug(f"Parsing {cond}")

    if escaped:
        if cond == "s":
            cond = " "
        elif cond == "n":
            cond = "\n"
        elif cond == "t":
            cond = "\t"
        elif cond == "r":
            cond = "\r"
        elif cond == "f":
            cond = "\f"
        elif cond =="v":
            cond = "\v"
        elif cond == "b":
            cond = "\b"
        elif cond == "d":
            cond = DIGITS
        elif cond == "a":
            cond = LOWER_CASE_CHARS
        elif cond == "A":
            cond = UPPER_CASE_CHARS
    elif cond == ".":
        cond = None

    new_atmt = Automata()
    from_st = new_atmt.add_state("q0", start=True)
    to_st = new_atmt.add_state("q1", end=True)
    new_atmt.add_transition(from_st, to_st, cond, negated=negated, action=1)
    logging.debug(f"Condition: {new_atmt.q0.transitions[0].str_cond}")
    new_atmt, changed = _check_special_char(re_expr, 1, new_atmt)
    logging.debug(f"Especial char found after {changed}")
    new_index = 2 if changed else 1
    new_index += 1 if escaped else 0
    return new_atmt, new_index


def _process_group(re_expr: str, negated: bool) -> Automata:
    """
    Processes a group.

    Parameters
    ----------
    re_expr : str
        Regular expression.

    Returns
    -------
    Automata
        Automata.
    """
    logging.debug("Parsing group")
    close_paren_index = _find_matching_paren(re_expr)
    negated = re_expr[1] == "^"
    start_index = 2 if negated else 1
    new_atmt = _build_automata(re_expr[start_index:close_paren_index], negated=negated)

    new_atmt, changed = _check_special_char(re_expr, close_paren_index + 1, new_atmt)

    logging.debug(f"Especial char found after group {changed}")
    new_index = close_paren_index + 2 if changed else close_paren_index + 1
    return new_atmt, new_index


def _process_or_operator(a_atmt: Automata, b_atmt: Automata) -> Automata:
    """
    Processes an or operator.

    Parameters
    ----------
    re_expr : str
        Regular expression.

    Returns
    -------
    Automata
        Automata.
    """
    #
    #              .-- > -- (a0) --..--> (af) -- > --.
    #             /                                   \
    # - - > (new_q0)                                  ((new_qf))
    #             \                                   /
    #              `-- > -- (b0) --..--> (bf) -- > --'
    #
    new_atmt = Automata()
    b_atmt = b_atmt.flat()
    q_0 = a_atmt.start_state.merge(b_atmt.start_state)
    for state in b_atmt.states.values():
        for trans in state.transitions:
            if trans.to_state == b_atmt.start_state:
                trans.to_state = q_0
    b_end_state = q_0 if b_atmt.end_state == b_atmt.start_state else b_atmt.end_state
    new_atmt.states["q0"] = q_0
    new_atmt.start_states = [q_0]
    new_atmt.add_state("qf", end=True)
    new_atmt.add_transition(a_atmt.end_state, new_atmt.end_state)
    new_atmt.add_transition(b_end_state, new_atmt.end_state)
    return new_atmt


def _build_automata(
    re_expr: str, last_atmt: Automata = None, negated: bool = False
) -> Automata:
    """
    Builds an automata from a regular expression using the Thompson
    construction algorithm.

    Parameters
    ----------
    re_expr : str
        Regular expression.

    Returns
    -------
    Automata
        Automata.
    """

    if re_expr == "":
        if last_atmt:
            return last_atmt
        raise ValueError("Invalid regular expression.")

    logging.debug(f"Building automata for {re_expr}")

    # Parse a single character
    if re_expr[0] not in SPECIAL_CHARS or re_expr[0] == "\\":
        new_atmt, new_index = _process_single_char(re_expr, negated)
        if last_atmt:
            new_atmt = last_atmt.concatenate(new_atmt)
        return _build_automata(re_expr[new_index:], new_atmt, negated)

    # Parse a group
    if re_expr[0] == "(":
        new_atmt, new_index = _process_group(re_expr, negated)
        if last_atmt:
            new_atmt = last_atmt.concatenate(new_atmt)
        return _build_automata(re_expr[new_index:], new_atmt, negated)

    # Parse an or operator
    if re_expr[0] == "|":
        logging.debug("Parsing or operator")
        if not last_atmt:
            raise ValueError("Invalid regular expression.")
        a_atmt = last_atmt
        b_atmt = _build_automata(re_expr[1:], None, negated)
        new_atmt = _process_or_operator(a_atmt, b_atmt)
        return new_atmt

    raise ValueError("Invalid regular expression {re_expr}")


def compile_patt(re_expr: str) -> RegexPattern:
    """
    Compiles a regular expression into an automata.

    Parameters
    ----------
    re_expr : str
        Regular expression.

    Returns
    -------
    Automata
        Automata.
    """
    return RegexPattern(re_expr)


def check(re_expr: str, text: str) -> bool:
    """
    Checks a regular expression against a text.

    Parameters
    ----------
    re_expr : str
        Regular expression.
    text : str
        Text.

    Returns
    -------
    bool
        True if the regular expression matches the text, False otherwise.
    """
    re_expr = _get_basic_re_expr(re_expr)
    re_patt = _build_automata(re_expr).flat()
    return re_patt.run(text)
