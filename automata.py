"""
This module contains the structs necessary to represent an automata.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple, Union

_ATMT_COUNT = 0


class State:
    """
    A state of an automata.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.transitions: List[Transition] = []

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return str(self)


class Transition:
    def __init__(
        self, from_state: State, to_state: State, condition: Any = None, action: int = 1
    ) -> None:
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition
        self.action = action

    @property
    def is_epsilon(self) -> bool:
        return self.condition is None

    def __str__(self) -> str:
        return f"{self.from_state} - ({self.condition}) -> {self.to_state}"


class Automata:
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
        self._stack: List[Tuple[State, int]] = []

    def __getattr__(self, item: str) -> Any:
        if item in self.states:
            return self.states[item]
        raise AttributeError(f"No attribute {item}")

    def add_state(
        self, state: Union[str, State], start: bool = False, end: bool = False
    ) -> State:
        if isinstance(state, str):
            if state in self.states:
                raise ValueError(f"State {state} already exists.")
            state = State(state)
        self.states[state.name] = state
        if start:
            self.start_states.append(state)
        if end:
            self.end_states.append(state)
        return state

    def add_transition(
        self,
        from_state: Union[str, State],
        to_state: Union[str, State],
        condition: Any = None,
        action: int = None,
    ) -> None:
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
        if len(self.start_states) == 1:
            return self.start_states[0]
        start_st = self.add_state(f"_start_{self.name}")
        for state in self.start_states:
            self.add_transition(start_st, state)
        self.start_states = [start_st]
        return start_st

    def set_single_end(self) -> State:
        if len(self.end_states) == 1:
            return self.end_states[0]
        end_st = self.add_state(f"_end_{self.name}")
        for state in self.end_states:
            self.add_transition(state, end_st)
        self.end_states = [end_st]
        return end_st

    def set_single_start_end(self) -> Tuple[State, State]:
        start_st = self.set_single_start()
        end_st = self.set_single_end()
        return start_st, end_st

    def run(
        self,
        input_: Iterable,
        stop_at_end: bool = False,
        success_at_full_input: bool = False,
    ) -> bool:
        if not self.start_states:
            raise ValueError("No start states defined.")
        self._pos = 0
        self._input = input_
        self._stack = [(st, self._pos) for st in self.start_states]
        while self._stack:
            if self._step():
                break
            if self._current_state in self.end_states and stop_at_end:
                return True
        return success_at_full_input or self._current_state in self.end_states

    def _step(self):
        print(self._stack)
        self._current_state, self._pos = self._stack.pop()
        for transition in self._current_state.transitions:
            if transition.is_epsilon or (
                0 <= self._pos < len(self._input)
                and self._input[self._pos] == transition.condition
            ):
                run_state = (transition.to_state, self._pos + transition.action)
                self._stack.append(run_state)
        if self._pos >= len(self._input) or self._pos < 0:
            return self._current_state in self.end_states
        return False
