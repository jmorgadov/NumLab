"""
This module contains the structs necessary to represent an automata.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple, Union

_ATMT_COUNT = 0


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

    def __init__(self, name: str) -> None:
        self.name = name
        self.transitions: List[Transition] = []
        self.automata = None

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

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return str(self)


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
        self, from_state: State, to_state: State, condition: Any = None, action: int = 1
    ) -> None:
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition
        self.action = action

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
            return value in self.condition
        if callable(self.condition):
            return self.condition(value)
        return value == self.condition

    @property
    def is_epsilon(self) -> bool:
        """Returns True if the transition is an epsilon transition."""
        return self.condition is None

    def __str__(self) -> str:
        return f"{self.from_state} - ({self.condition}) -> {self.to_state}"


class Automata:
    """
    An automata.

    Parameters
    ----------
    name : str
        The name of the automata.

    Attributes
    ----------
    name : str
        The name of the automata.
    states : Dict[str, State]
        The states of the automata.
    start_states : List[State]
        The start states of the automata.
    end_states : List[State]
        The end states of the automata.
    """

    def __init__(self, name: str = None) -> None:
        if name is None:
            global _ATMT_COUNT
            name = f"atmt_{_ATMT_COUNT}"
            _ATMT_COUNT += 1
        self.name = name
        self.states: Dict[str, State] = {}
        self.start_states: List[State] = []
        self.end_states: List[State] = []

        self._pos = 0
        self._input = None
        self._current_state: State = None
        self._processes: List[Tuple[State, int]] = []
        self._processes_idx: int = 0

    def __getattr__(self, item: str) -> Any:
        if item in self.states:
            return self.states[item]
        raise AttributeError(f"No attribute {item}")

    def concatenate(self, other: Automata, set_single: bool = False) -> Automata:
        """
        Concatenate the automata with another one.

        Parameters
        ----------
        other : Automata
            The other automata.
        set_single : bool, optional
            Whether to set the automata to have a single start and end state
            when needed, by default False.

        Returns
        -------
        Automata
            The concatenated automata.

        Raises
        ------
        ValueError
            If the current automata has multiple end states and ``set_single`` is
            False.
        ValueError
            If the other automata has multiple start states and ``set_single`` is
            False.
        """

        if len(self.end_states) != 1:
            if set_single:
                self.set_single_end()
            else:
                raise ValueError(f"Automata {self.name} has multiple end states.")
        if len(other.start_states) != 1:
            if set_single:
                other.set_single_start()
            else:
                raise ValueError(f"Automata {other.name} has multiple start states.")
        self.end_state.substitute(other.start_state)
        self.end_states = other.end_states
        return self

    @property
    def start_state(self) -> State:
        """Get the start state of the automata."""
        if len(self.start_states) == 1:
            return self.start_states[0]
        raise ValueError("The automata has multiple start states.")

    @property
    def end_state(self) -> State:
        """Get the end state of the automata."""
        if len(self.end_states) == 1:
            return self.end_states[0]
        raise ValueError("The automata has multiple end states.")

    def add_state(
        self, state: Union[str, State] = None, start: bool = False, end: bool = False
    ) -> State:
        """
        Add a state to the automata.

        Parameters
        ----------
        state : Union[str, State]
            The name of the state to add or the state itself.
        start : bool
            Whether the state is a start state.
        end : bool
            Whether the state is an end state.

        Returns
        -------
        State
            The added state.
        """

        if state is None:
            state = State(f"q{len(self.states)}")
        if isinstance(state, str):
            if state in self.states:
                raise ValueError(f"State {state} already exists.")
            state = State(state)
        self.states[state.name] = state
        if start:
            self.start_states.append(state)
        if end:
            self.end_states.append(state)
        state.automata = self
        return state

    def add_transition(
        self,
        from_state: Union[str, State],
        to_state: Union[str, State],
        condition: Any = None,
        action: int = None,
    ) -> None:
        """
        Add a transition to the automata.

        Parameters
        ----------
        from_state : Union[str, State]
            The state from which the transition starts.
        to_state : Union[str, State]
            The state to which the transition goes.
        condition : Any
            The condition under which the transition is taken.
        action : int
            The action to perform when the transition is taken.

        Raises
        ------
        ValueError
            If any of the states does not exist.
        """

        if isinstance(from_state, str):
            from_state = self.states.get(from_state, None)
            if from_state is None:
                raise ValueError(f"No state {from_state} defined.")
        if isinstance(to_state, str):
            to_state = self.states.get(to_state, None)
            if to_state is None:
                raise ValueError(f"No state {to_state} defined.")
        if action is None:
            action = 0 if condition is None else 1
        transition = Transition(from_state, to_state, condition, action)
        from_state.transitions.append(transition)
        return transition

    def set_single_start(self) -> State:
        """
        Set the automata to have a single start state.

        Returns
        -------
        State
            The start state.
        """

        if len(self.start_states) == 1:
            return self.start_states[0]
        start_st = self.add_state(f"_start_{self.name}")
        for state in self.start_states:
            self.add_transition(start_st, state)
        self.start_states = [start_st]
        return start_st

    def set_single_end(self) -> State:
        """
        Set the automata to have a single end state.

        Returns
        -------
        State
            The end state.
        """

        if len(self.end_states) == 1:
            return self.end_states[0]
        end_st = self.add_state(f"_end_{self.name}")
        for state in self.end_states:
            self.add_transition(state, end_st)
        self.end_states = [end_st]
        return end_st

    def set_single_start_end(self) -> Tuple[State, State]:
        """
        Set the automata to have a single start and end state.

        Returns
        -------
        Tuple[State, State]
            The start and end state.
        """

        start_st = self.set_single_start()
        end_st = self.set_single_end()
        return start_st, end_st

    def run(
        self,
        input_: Iterable,
        stop_at_end: bool = False,
        success_at_full_input: bool = False,
    ) -> bool:
        """
        Run the automata on the given input.

        Parameters
        ----------
        input_ : Iterable
            The input to run the automata on.
        stop_at_end : bool
            Whether to stop the automata at the first end state encountered.
        success_at_full_input : bool
            Whether to consider the automata successful if the input is fully
            consumed.

        Returns
        -------
        bool
            Whether the automata succeeded.

        Raises
        ------
        ValueError
            If the automata has no start state.
        """

        if not self.start_states:
            raise ValueError("No start states defined.")
        self._pos = 0
        self._input = input_
        self._processes = [(st, self._pos) for st in self.start_states]
        while self._processes:
            if self._step():
                break
            if self._current_state in self.end_states and stop_at_end:
                return True
        return success_at_full_input or self._current_state in self.end_states

    def _step(self):
        self._current_state, self._pos = self._processes[self._processes_idx]
        last_process_count = len(self._processes)
        new_processes = 0

        for transition in self._current_state.transitions:
            if transition.is_epsilon or (
                0 <= self._pos < len(self._input)
                and transition.check_condition(self._input[self._pos])
            ):
                run_state = (transition.to_state, self._pos + transition.action)
                if new_processes == 0:
                    self._processes[self._processes_idx] = run_state
                else:
                    self._processes.append(run_state)
                new_processes += 1

        if not new_processes:
            self._processes.pop(self._processes_idx)
        self._processes_idx = (
            0
            if last_process_count != len(self._processes)
            else (self._processes_idx + 1) % len(self._processes)
        )

        if self._pos >= len(self._input) or self._pos < 0:
            return self._current_state in self.end_states
        return False
