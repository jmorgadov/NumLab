import logging
from typing import Any


class Transition:
    """
    A transition between two states.

    Parameters
    ----------
    from_state : State
        The state from which the transition starts.
    to_state : State
        The state to which the transition goes.
    condition : Any
        The condition under which the transition is taken.
    action : int
        The action to perform when the transition is taken.

    Attributes
    ----------
    from_state : State
        The state from which the transition starts.
    to_state : State
        The state to which the transition goes.
    condition : Any
        The condition under which the transition is taken.
    action : int
        The action to perform when the transition is taken.
    """

    def __init__(
        self,
        from_state: "State",
        to_state: "State",
        condition: Any = None,
        action: int = 1,
        negated: bool = False,
    ) -> None:
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition
        self.action = action
        self.negated = negated

    def check_condition(self, value: Any) -> bool:
        """
        Check if the transition is taken.

        Parameters
        ----------
        value : Any
            The value to check.

        Returns
        -------
        bool
            True if the transition is taken, False otherwise.
        """

        if self.condition is None:
            return True
        if isinstance(self.condition, list):
            ret_val = value in self.condition
        else:
            ret_val = value == self.condition
        ret_val = not ret_val if self.negated else ret_val
        neg = "^" if self.negated else ""
        logging.debug(
            f"Checking condition {neg}{self.str_cond} against {value} ({ret_val})"
        )
        return ret_val

    @property
    def is_epsilon(self) -> bool:
        """Returns True if the transition is an epsilon transition."""
        return self.condition is None

    def __str__(self) -> str:
        return f"{self.from_state} - ({self.condition}) -> {self.to_state}"

    @property
    def str_cond(self) -> str:
        """
        Get the string representation of the condition.

        Returns
        -------
        str
            The string representation of the condition.
        """

        if self.condition is None:
            return "ε"
        if isinstance(self.condition, list):
            cond = self.condition
            return (
                cond.__repr__()
                if len(cond) <= 10
                else (f"[{cond[0].__repr__()}, ..., {cond[-1].__repr__()}]")
            )
        return self.condition.__repr__()
