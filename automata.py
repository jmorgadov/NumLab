"""
This module contains the structs necessary to represent an automata.
"""
from __future__ import annotations

import logging
import re
from typing import Any, Dict, Iterable, List, Union

STAY = 0
FOWARD = 1
BACKWARD = -1


class Transition:
    """
    Represents a transition in the automata.

    Parameters
    ----------
    from_state : int
        The id of the state from which the transition starts.
    value : Any
        The value of the transition.
    to_state : int
        The id of the state to which the transition ends.
    action : int, optional
        The action to perform.
    regex : bool, optional
        Whether the value is a regular expression.

    Attributes
    ----------
    from_state : int
        The id of the state from which the transition starts.
    value : Any
        The value of the transition.
    to_state : int
        The id of the state to which the transition ends.
    action : int, optional
        The action to perform.
    regex : bool, optional
        Whether the value is a regular expression.
    """

    def __init__(
        self,
        from_state: int,
        value: Any,
        to_state: int,
        action: int = FOWARD,
        regex: bool = False,
    ):
        self.from_state = from_state
        self.value = value
        self.to_state = to_state
        self.action = action
        self.regex = regex


class Automata:
    """
    Automata

    Attributes
    ----------
    initial_state : int
        The id of the initial state.
    final_states : List[int]
        The ids of the final states.
    state_ids : Dict[str, int]
        The mapping from state names to ids.
    state_names : Dict[int, str]
        The mapping from state ids to names.
    current_state : int
        The id of the current state.
    transitions : Dict[int, List[Transition]]
        The transitions from each state.
    """

    def __init__(self):
        self.initial_state: int = None
        self.final_states: List[int] = []
        self.state_names: Dict[int, str] = {}
        self.state_ids: Dict[str, int] = {}
        self.current_state: int = None
        self.transitions: Dict[int, List[Transition]] = {}
        self.last_pos = 0

        self._logs = False
        self._step_count = 0
        self._counter = 0
        self._atmt_counter = 0
        self._pos = 0
        self._input = None

    def __getattr__(self, item: str) -> Any:
        if item in self.state_ids:
            return self.state_ids[item]
        if item in self.state_names:
            return self.state_names[item]
        raise AttributeError(f"No attribute {item}")

    def add_state(
        self, name: str = None, initial: bool = False, final: bool = False
    ) -> int:
        """
        Add a state to the automata.

        Parameters
        ----------
        name : str, optional
            The name of the state.
        initial : bool, optional
            Whether the state is an initial state.
        final : bool, optional
            Whether the state is a final state.

        Returns
        -------
        int
            The id of the state.
        """

        if name is None:
            name = f"q{self._counter}"
            self._counter += 1

        if name in self.state_ids:
            raise ValueError("State already exists")
        state_id = self._counter
        self._counter += 1
        self.state_names[state_id] = name
        self.state_ids[name] = state_id
        self.transitions[state_id] = []
        if initial:
            self.initial_state = state_id
        if final:
            self.final_states.append(state_id)
        return state_id

    def add_transition(
        self,
        from_state: Union[str, int],
        value: Any,
        to_state: Union[str, int, Automata],
        action: int = FOWARD,
        regex: bool = False,
    ) -> None:
        """
        Add a transition to the automata.

        Parameters
        ----------
        from_state : Union[str, int]
            The id or name of the state from which the transition starts.
        value : Any
            The value of the transition.
        to_state : Union[str, int, Automata]
            The id or name of the state to which the transition ends.

            In case ``to_state`` is an automata, the transition will be added
            to the automata and the automata will be inserted into the
            current automata.
        action : int, optional
            The action to perform.
        regex : bool, optional
            Whether the value is a regular expression.
        """

        if isinstance(from_state, str):
            from_state = self.state_ids[from_state]
        if isinstance(to_state, str):
            to_state = self.state_ids[to_state]
        if isinstance(value, str) and regex:
            value = re.compile(value)

        # In case the transition is made to another automata
        if isinstance(to_state, Automata):
            to_atmt = to_state
            to_state = to_state.initial_state

            # Add all states and transitions from the sub-automata
            for state_transitions in to_atmt.transitions.values():
                for transition in state_transitions:
                    # Add the initial state of the transition to the automata
                    # if it does not exist yet
                    t_from_name = to_atmt.state_names[transition.from_state]
                    t_from_new_name = f"{self._atmt_counter}_{t_from_name}"
                    if t_from_new_name not in self.state_ids:
                        self.add_state(
                            t_from_new_name,
                            final=to_atmt.state_ids[t_from_name] in to_atmt.final_states,
                        )
                    # Add the final state of the transition to the automata
                    # if it does not exist yet
                    t_to_name = to_atmt.state_names[transition.to_state]
                    t_to_new_name = f"{self._atmt_counter}_{t_to_name}"
                    if t_to_new_name not in self.state_ids:
                        self.add_state(
                            t_to_new_name,
                            final=to_atmt.state_ids[t_to_name] in to_atmt.final_states,
                        )
                    # Add the transition to the automata
                    self.transitions[self.state_ids[t_from_new_name]].append(
                        Transition(
                            self.state_ids[t_from_new_name],
                            transition.value,
                            self.state_ids[t_to_new_name],
                            transition.action,
                            transition.regex,
                        )
                    )

            # Add the transition to the initial state of the sub-automata
            sub_atmt_init_name = (
                f"{self._atmt_counter}_{to_atmt.state_names[to_atmt.initial_state]}"
            )
            sub_atmt_init = self.state_ids[sub_atmt_init_name]
            self.transitions[from_state].append(
                Transition(from_state, value, sub_atmt_init, action, regex)
            )
            self._atmt_counter += 1
            return

        self.transitions[from_state].append(
            Transition(from_state, value, to_state, action, regex)
        )

    def run(
        self,
        input_: Iterable[Any],
        stop_when_final: bool = False,
        success_at_full_input: bool = False,
        logs: bool = False,
    ) -> bool:
        """
        Run the automata on the given input.

        Parameters
        ----------
        input_ : Iterable[Any]
            The input to run the automata on.
        stop_when_final : bool, optional
            Whether to stop the automata when it reaches a final state.
        success_at_full_input : bool, optional
            Whether to return True when the automata when the input is fully
            consumed even if it is not in a final state.
        """

        self._logs = logs
        if self.initial_state is None:
            raise ValueError("No initial state")
        self.current_state = self.initial_state
        self._pos = 0
        self._step_count = 0
        self.last_pos = 0
        self._input = input_
        while self._pos < len(input_):
            self._step()
            if self.current_state in self.final_states and stop_when_final:
                return True
        return success_at_full_input or self.current_state in self.final_states

    def _step(self) -> None:
        """
        Run the automata for one step.
        """

        for transition in self.transitions[self.current_state]:
            if transition.value is None:
                self.current_state = transition.to_state
                self.last_pos = self._pos
                return
            valid_value = transition.value == self._input[self._pos]
            if transition.regex:
                valid_value = transition.value.match(self._input[self._pos])
            if valid_value:
                logging.info(
                    f"{self._step_count}: Read: {self._input[self._pos]} "
                    f"Moving from {self.state_names[self.current_state]} "
                    f"to {self.state_names[transition.to_state]}"
                )
                self.current_state = transition.to_state
                self.last_pos = self._pos
                self._pos += transition.action
                return
        raise ValueError("Invalid input")
