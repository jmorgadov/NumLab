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

from automata import Automata

SPECIAL_CHARS = ["(", ")", "|", "*", "+", "?"]


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
        return self.text[:self.end]


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
        self.atmt = _build_automata(re_expr)

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
    #                        .---- < ----.
    #                       /             \
    #  - - > (new_q0) --> (q0) -- .. --> (qf) --> ((new_qf))
    #              \                                /
    #               `------------- > --------------'
    #
    new_atmt = _apply_plus_op(atmt)
    new_atmt.add_transition("q0", "qf")
    return new_atmt


def _apply_plus_op(atmt: Automata) -> Automata:
    """
    Applies the plus operator to an automata.


    Parameters
    ----------
    atmt : Automata
        Automata.

    Returns
    -------
    Automata
        Automata after applying the plus operator.
    """
    #
    #                         .---- < ----.
    #                        /             \
    #   - - > (new_q0) --> (q0) -- .. --> (qf) --> ((new_qf))
    #
    new_atmt = Automata()
    new_atmt.add_state("q0", start=True)
    new_atmt.add_state("qf", end=True)
    new_atmt.add_transition(atmt.end_state, atmt.start_state)
    new_atmt.add_transition("q0", atmt.start_state)
    new_atmt.add_transition(atmt.end_state, "qf")
    return new_atmt


def _check_special_char(re_expr, index, atmt):
    if index < 0 or index >= len(re_expr) or re_expr[index] not in ["*", "+"]:
        return atmt, False
    if re_expr[index] == "*":
        atmt = _apply_star_op(atmt)
    elif re_expr[index] == "+":
        atmt = _apply_plus_op(atmt)
    return atmt, True


def _build_automata(re_expr: str, stack: list = None) -> Automata:
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

    if stack is None:
        stack = []

    if re_expr == "":
        if stack:
            return stack.pop()
        raise ValueError("Invalid regular expression.")

    # Parse a single character
    if re_expr[0] not in SPECIAL_CHARS or re_expr[0] == "\\":
        #
        # - - > (q0) -- a --> ((q1))
        #
        escaped = False
        if re_expr[0] == "\\":
            re_expr = re_expr[1:]
            escaped = True
        char = re_expr[0]

        if escaped:
            if char == "s":
                char = " "
            elif char == "n":
                char = "\n"
            elif char == "t":
                char = "\t"
            elif char == "r":
                char = "\r"
            elif char == "f":
                char = "\f"
        elif char == ".":
            char = None

        new_atmt = Automata()
        from_st = new_atmt.add_state("q0", start=True)
        to_st = new_atmt.add_state("q1", end=True)
        new_atmt.add_transition(from_st, to_st, char, action=1)
        new_atmt, changed = _check_special_char(re_expr, 1, new_atmt)

        if stack:
            atmt = stack.pop()
            atmt.concatenate(new_atmt)
            new_atmt = atmt

        stack.append(new_atmt)
        new_index = 2 if changed else 1
        return _build_automata(re_expr[new_index:], stack)

    # Parse a group
    if re_expr[0] == "(":
        close_paren_index = _find_matching_paren(re_expr)
        new_atmt = _build_automata(re_expr[1:close_paren_index])
        new_atmt, changed = _check_special_char(
            re_expr, close_paren_index + 1, new_atmt
        )
        if stack:
            atmt = stack.pop()
            atmt.concatenate(new_atmt)
            new_atmt = atmt
        stack.append(new_atmt)
        new_index = close_paren_index + 2 if changed else close_paren_index + 1
        return _build_automata(re_expr[new_index:], stack)

    # Parse an or operator
    if re_expr[0] == "|":
        #
        #              .-- > -- (a0) --..--> (af) -- > --.
        #             /                                   \
        # - - > (new_q0)                                  ((new_qf))
        #             \                                   /
        #              `-- > -- (b0) --..--> (bf) -- > --'
        #
        if not stack:
            raise ValueError("Invalid regular expression.")
        a_atmt = stack.pop()
        b_atmt = _build_automata(re_expr[1:])
        new_atmt = Automata()
        new_atmt.add_state("q0", start=True)
        new_atmt.add_state("qf", end=True)
        new_atmt.add_transition(new_atmt.start_state, a_atmt.start_state)
        new_atmt.add_transition(new_atmt.start_state, b_atmt.start_state)
        new_atmt.add_transition(a_atmt.end_state, new_atmt.end_state)
        new_atmt.add_transition(b_atmt.end_state, new_atmt.end_state)
        return new_atmt

    raise ValueError("Invalid regular expression {}".format(re_expr))


def compile_patt(re_expr: str) -> Automata:
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


def match(re_expr: str, text: str) -> bool:
    """
    Matches a regular expression against a text.

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
    re_patt = compile_patt(re_expr)
    return re_patt.match(text)
