"""
This module contains the structs necessary to represent an automata.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, List, Set, Tuple, Union

from numlab.automata.state import State
from numlab.automata.transition import Transition

_ATMT_COUNT = 0


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

    @property
    def alphabet(self) -> Set[Tuple[Any, bool]]:
        """
        Get the alphabet of the automata.

        Returns
        -------
        List[Any]
            The alphabet of the automata.
        """

        alphabet = set()
        for state in self.states.values():
            for transition in state.transitions:
                if transition.is_epsilon:
                    continue
                if isinstance(transition.condition, str):
                    alphabet.add(transition.condition)
                else:
                    alphabet.update(transition.condition)
        return alphabet

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
        other = other.flat()
        other_first_state = other.start_state
        other_last_state = other.end_state
        self.end_state.merge(other_first_state)
        if other_last_state == other_first_state:
            other_last_state = self.end_state
        for state in other.states.values():
            for trans in state.transitions:
                if trans.to_state is other_first_state:
                    trans.to_state = self.end_state
        self.end_states = [other_last_state]
        return self

    @property
    def pos(self) -> int:
        """Position of the automata on the input"""
        return self._pos

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
        self,
        state: Union[str, State] = None,
        start: bool = False,
        end: bool = False,
        name: str = None,
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
            state.automata = self
        name = name if name is not None else state.name
        self.states[name] = state
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
        negated: bool = False,
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
        transition = Transition(from_state, to_state, condition, action, negated)
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

    def flat(self) -> Automata:
        """
        Flatten the automata.

        Returns
        -------
        Automata
            The flattened automata.
        """

        flat = Automata(self.name)
        count = 0
        visited_states = []
        non_visited_states = self.start_states
        while non_visited_states:
            new_non_visited_states = []
            for state in non_visited_states:
                flat.add_state(
                    state,
                    state in self.start_states,
                    state in self.end_states,
                    name=f"q{count}",
                )
                state.name = f"q{count}"
                count += 1
                visited_states.append(state)
                for transition in state.transitions:
                    to_state = transition.to_state
                    if (
                        to_state not in visited_states
                        and to_state not in new_non_visited_states
                        and to_state not in non_visited_states
                    ):
                        new_non_visited_states.append(transition.to_state)

            non_visited_states = new_non_visited_states
        return flat

    def show(self) -> None:
        """
        Show the automata.
        """

        # Inverse name states dict
        inv_states = {v: k for k, v in self.states.items()}

        for name, state in self.states.items():
            print(name, f"Final: {state in self.end_states}")
            for transition in state.transitions:
                neg = "^" if transition.negated else ""
                print(
                    f"  ({neg}{transition.str_cond}) "
                    f"-> {inv_states[transition.to_state]}"
                )

    def _eps_closure_single(self, state: Union[str, State]) -> Set[State]:
        """
        Compute the epsilon closure of a single state.

        Parameters
        ----------
        state : Union[str, State]
            The state to compute the epsilon closure of.

        Returns
        -------
        Set[State]
            The epsilon closure of the state.

        Raises
        ------
        ValueError
            If the state does not exist.
        """

        if isinstance(state, str):
            if state not in self.states:
                raise ValueError(f"No state {state} defined.")
            state = self.states[state]
        visited = set()
        non_vsited = [state]
        while non_vsited:
            new_non_vsited = []
            for current_state in non_vsited:
                visited.add(current_state)
                for transition in current_state.transitions:
                    if transition.is_epsilon:
                        to_st = transition.to_state
                        if (
                            to_st not in visited
                            and to_st not in new_non_vsited
                            and to_st not in non_vsited
                        ):
                            new_non_vsited.append(to_st)
            non_vsited = new_non_vsited
        return visited

    def eps_closure(
        self, state: Union[str, State, Iterable[str], Iterable[State]]
    ) -> Set[State]:
        """
        Compute the epsilon closure of a state or a set of states.

        Parameters
        ----------
        state : Union[str, State, Iterable[str], Iterable[State]]
            The state or a list of states.

        Returns
        -------
        Set[State]
            The epsilon closure of the state or a set of states.

        Raises
        ------
        ValueError
            If any of the states does not exist.
        """

        if isinstance(state, (str, State)):
            return self._eps_closure_single(state)
        whole_closure = set()
        for current_state in state:
            whole_closure.update(self._eps_closure_single(current_state))
        return whole_closure

    def _goto_single(self, state: Union[str, State], symbol: str) -> Set[State]:
        """
        Compute the goto of a single state.

        Parameters
        ----------
        state : Union[str, State]
            The state to compute the goto of.
        symbol : str
            The symbol to compute the goto of.

        Returns
        -------
        Set[State]
            The goto of the state.

        Raises
        ------
        ValueError
            If the state does not exist.
        """

        if isinstance(state, str):
            if state not in self.states:
                raise ValueError(f"No state {state} defined.")
            state = self.states[state]
        answer = set()
        st_esp_closure = self.eps_closure(state)
        for current_state in st_esp_closure:
            for transition in current_state.transitions:
                if not transition.is_epsilon and transition.check_condition(symbol):
                    answer.add(transition.to_state)
        return answer

    def goto(
        self, state: Union[str, State, Iterable[str], Iterable[State]], symbol: str
    ) -> Set[State]:
        """
        Compute the goto of a state or a set of states.

        Parameters
        ----------
        state : Union[str, State, Iterable[str], Iterable[State]]
            The state or a list of states.
        symbol : str
            The symbol to compute the goto of.

        Returns
        -------
        Set[State]
            The goto of the state or a set of states.

        Raises
        ------
        ValueError
            If any of the states does not exist.
        """

        if isinstance(state, (str, State)):
            return self._goto_single(state, symbol)
        whole_goto = set()
        for current_state in state:
            whole_goto.update(self._goto_single(current_state, symbol))
        return whole_goto

    def to_dfa(self, dfa2nfa: bool = False) -> Union[Automata, Tuple[Automata, Dict]]:
        """
        Convert the automata to a DFA.

        Parameters
        ----------
        dfa2nfa : bool
            If True, the return value will be a tuple of the DFA and the dfa2nfa
            dictionary, otherwise only the DFA will be returned. By default, False.

        Returns
        -------
        Union[Automata, Tuple[Automata, Dict]]
            The DFA.
        """

        get_name = lambda states: "".join(sorted(x.name for x in states))
        alphabet = self.alphabet
        dfa = Automata(self.name)
        start_state = self.eps_closure(self.start_states)
        start_name = get_name(start_state)
        q_0 = dfa.add_state(start_name, start=True, end=start_state in self.end_states)
        dfa_to_nfa = {q_0: start_state}
        visited = set()
        non_visited = [q_0]
        while non_visited:
            new_non_visited = []
            for current_state in non_visited:
                if current_state in visited:
                    continue
                visited.add(current_state)
                for char in alphabet:
                    goto_states = self.goto(dfa_to_nfa[current_state], char)
                    if not goto_states:
                        continue
                    next_state = self.eps_closure(goto_states)
                    next_name = get_name(next_state)
                    if next_name not in dfa.states:
                        dfa_state = dfa.add_state(
                            next_name,
                            end=any(s in self.end_states for s in next_state),
                        )
                        dfa_to_nfa[dfa_state] = next_state
                        new_non_visited.append(dfa_state)
                    else:
                        dfa_state = dfa.states[next_name]
                    dfa.add_transition(current_state.name, next_name, char)
                    if next_state not in new_non_visited and next_state not in visited:
                        new_non_visited.append(dfa_state)
            non_visited = new_non_visited
        return dfa if not dfa2nfa else (dfa, dfa_to_nfa)

    def run(
        self,
        input_: Iterable,
        stop_at_end: bool = False,
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
        self._processes_idx = 0
        self._input = input_
        self._processes = [(st, self._pos) for st in self.start_states]
        while self._processes:
            stop = self._step()
            if self._current_state in self.end_states:
                if stop_at_end:
                    return True
            if stop:
                break
        else:
            return False
        logging.debug(f"Final {self._processes_idx} {self._processes}")
        return self._current_state in self.end_states

    def _step(self):
        self._current_state, self._pos = self._processes[self._processes_idx]
        self._current_state.visited()
        if self._pos > len(self._input):
            self._processes.pop(self._processes_idx)
            return False
        new_processes = 0
        logging.debug(f"{self._processes_idx} {self._processes}")

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

        if self._processes:
            self._processes_idx = (self._processes_idx + 1) % len(self._processes)

        if self._pos >= len(self._input) or self._pos < 0:
            return self._current_state in self.end_states
        return False
