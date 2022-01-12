from __future__ import annotations

from typing import Any, Callable, List

from numlab.automata.transition import Transition


class State:
    """
    A state of an automata.

    Attributes
    ----------
    name : str
        The name of the state.
    transitions : List[Transition]
        The transitions of the state.
    """

    def __init__(self, name: str, on_visited: Callable = None) -> None:
        self.name = name
        self.transitions: List[Transition] = []
        self.automata = None
        self.on_visited = on_visited

    def visited(self):
        """
        Calls the ``on_visited`` callback if it is defined.
        """
        if self.on_visited:
            self.on_visited()

    def substitute(self, other_state: State) -> State:
        """
        Substitute the state with another one.

        Parameters
        ----------
        other_state : State
            The other state.

        Returns
        -------
        State
            The substituted state.
        """

        self.name = other_state.name
        self.transitions = other_state.transitions
        return self

    def merge(self, other_state: State) -> State:
        """
        Merge the state with another one.

        Parameters
        ----------
        other_state : State
            The other state.

        Returns
        -------
        State
            The merged state.
        """

        for trans in other_state.transitions:
            to_state = self if trans.to_state is other_state else trans.to_state
            new_t = Transition(
                self,
                to_state,
                trans.condition,
                trans.action,
                trans.negated,
            )
            self.transitions.append(new_t)
        return self

    def next_state(self, cond: Any):
        """
        Get the next state given a condition.

        Parameters
        ----------
        cond : Any
            The condition.

        Returns
        -------
        State
            The next state.
        """

        for trans in self.transitions:
            if trans.check_condition(cond):
                return trans.to_state
        return None

    def show(self) -> None:
        """
        Show the state.
        """

        print(self)
        for trans in self.transitions:
            print(f"  {trans}")

    def copy(self) -> State:
        """
        Copy the state.

        Returns
        -------
        State
            The copied state.
        """

        new_state = State(self.name)
        new_state.transitions = self.transitions
        return new_state

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return str(self)
