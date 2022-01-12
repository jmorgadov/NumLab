import pytest
from numlab.automata import Automata


def test_add_state():
    """test_add_state.
    """
    a = Automata()

    q_0 = a.add_state("q0", start=True)
    assert "q0" in a.states
    assert a.start_states == [q_0]

    q_1 = a.add_state("q1")
    assert "q1" in a.states

    q_2 = a.add_state("q2", end=True)
    assert "q2" in a.states
    assert q_2 in a.end_states

    q_3 = a.add_state("q3", end=True)
    assert "q3" in a.states
    assert q_3 in a.end_states


def test_add_transition():
    a = Automata()

    q_0 = a.add_state("q0", start=True)
    q_1 = a.add_state("q1")
    q_2 = a.add_state("q2", end=True)

    a.add_transition("q0", "q1", "a")
    assert len(q_0.transitions) == 1
    assert q_0.transitions[0].condition == "a"
    assert q_0.transitions[0].from_state == q_0
    assert q_0.transitions[0].to_state == q_1
    assert q_0.transitions[0].is_epsilon == False

    a.add_transition("q1", "q2", "b")
    assert len(q_1.transitions) == 1
    assert q_1.transitions[0].condition == "b"
    assert q_1.transitions[0].from_state == q_1
    assert q_1.transitions[0].to_state == q_2
    assert q_1.transitions[0].is_epsilon == False

    a.add_transition(q_0, q_1)
    assert len(q_0.transitions) == 2
    assert q_0.transitions[1].condition == None
    assert q_0.transitions[1].from_state == q_0
    assert q_0.transitions[1].to_state == q_1
    assert q_0.transitions[1].is_epsilon == True


def test_run():
    a = Automata()
    a.add_state("q0", start=True, end=True)
    a.add_state("q1")
    a.add_transition("q0", "q1", "1")
    a.add_transition("q1", "q0", "1")
    a.add_transition("q0", "q0", "0")
    a.add_transition("q1", "q1", "0")

    assert a.run("11")
    assert a.run("00")
    assert a.run("01") == False
    assert a.run("1000101") == False


def test_non_deterministc():
    a = Automata()
    a.add_state("q0", start=True)
    a.add_state("q1")
    a.add_state("q2", end=True)
    a.add_transition("q0", "q0", "a")
    a.add_transition("q0", "q1", "a")
    a.add_transition("q1", "q2", "b")

    assert a.run("b") == False
    assert a.run("a") == False
    assert a.run("ab")
    assert a.run("aaaab")


def test_sub_automata():
    a = Automata()
    a_0 = a.add_state("q0a", start=True)
    a_1 = a.add_state("q1a", end=True)

    b = Automata()
    b_0 = b.add_state("q0b", start=True)
    b_1 = b.add_state("q1b", end=True)

    a.add_transition(a_0, b_0, "a")
    b.add_transition(b_0, b_1, "b")
    b.add_transition(b_1, a_1, "c")

    a.run("abc")


def test_multiple_starts_and_ends():
    a = Automata()
    a_0 = a.add_state("q0", start=True)
    a_1 = a.add_state("q1", start=True)
    a_2 = a.add_state("q2")
    a_3 = a.add_state("q3", end=True)
    a_4 = a.add_state("q4", end=True)

    a.add_transition(a_0, a_2, "a")
    a.add_transition(a_1, a_2, "b")
    a.add_transition(a_2, a_3, "c")
    a.add_transition(a_2, a_4, "d")

    assert a.run("ac")
    assert a.run("bc")
    assert a.run("ad")
    assert a.run("bd")
    assert a.run("abc") == False

    a.set_single_start_end()

    assert a.run("ac")
    assert a.run("bc")
    assert a.run("ad")
    assert a.run("bd")
    assert a.run("abc") == False


@pytest.fixture
def nfa():
    a = Automata()
    q_0 = a.add_state("q0", start=True)
    q_1 = a.add_state("q1")
    q_2 = a.add_state("q2")
    q_3 = a.add_state("q3", end=True)

    a.add_transition(q_0, q_0, "a")
    a.add_transition(q_0, q_0, "b")
    a.add_transition(q_0, q_1)
    a.add_transition(q_1, q_2, "a")
    a.add_transition(q_2, q_3, "a")
    a.add_transition(q_2, q_3, "b")
    return a


def test_epsilon_closure(nfa):
    assert nfa.eps_closure(nfa.q0) == {nfa.q0, nfa.q1}
    assert nfa.eps_closure({nfa.q0, nfa.q2}) == {nfa.q0, nfa.q1, nfa.q2}
    assert nfa.eps_closure({nfa.q0, nfa.q2, nfa.q3}) == {
        nfa.q0,
        nfa.q1,
        nfa.q2,
        nfa.q3,
    }

    nfa.add_transition(nfa.q1, nfa.q2)

    assert nfa.eps_closure(nfa.q0) == {nfa.q0, nfa.q1, nfa.q2}


def test_goto(nfa):
    assert nfa.goto(nfa.q0, "a") == {nfa.q0, nfa.q2}
    assert nfa.goto({nfa.q0, nfa.q1}, "a") == {nfa.q0, nfa.q2}
    assert nfa.goto(nfa.q0, "b") == {nfa.q0}
    assert nfa.goto({nfa.q0, nfa.q1}, "b") == {nfa.q0}


def test_to_dfa(nfa):
    dfa = nfa.to_dfa()
    assert len(dfa.states) == 4

    for state in dfa.states.values():
        conds = []
        for transition in state.transitions:
            assert transition.is_epsilon == False
            assert transition.condition not in conds
            conds.append(transition.condition)

