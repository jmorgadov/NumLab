import pytest
import re

from automata import Automata, FOWARD, BACKWARD, STAY

def test_add_state():
    a = Automata()

    a.add_state('q0', initial=True)
    assert 'q0' in a.state_ids
    assert a.initial_state == a.state_ids['q0']

    a.add_state('q1')
    assert 'q1' in a.state_ids
    assert a.initial_state != a.state_ids['q1']

    a.add_state('q2', final=True)
    assert 'q2' in a.state_ids
    assert a.final_states == [a.state_ids['q2']]

    a.add_state('q3', final=True)
    assert 'q3' in a.state_ids
    assert a.state_ids['q3'] in a.final_states


def test_add_transition():
    a = Automata()

    a.add_state('q0', initial=True)
    a.add_state('q1')
    a.add_state('q2', final=True)

    a.add_transition('q0', 'a', 'q1')
    assert a.q0 in a.transitions
    assert a.transitions[a.q0][0].value == 'a'
    assert a.transitions[a.q0][0].to_state == a.q1
    assert a.transitions[a.q0][0].action == FOWARD
    assert a.transitions[a.q0][0].regex == False

    a.add_transition('q1', 'b', 'q2', BACKWARD, regex=True)
    assert a.q1 in a.transitions
    assert a.transitions[a.q1][0].value == re.compile('b')
    assert a.transitions[a.q1][0].to_state == a.q2
    assert a.transitions[a.q1][0].action == BACKWARD
    assert a.transitions[a.q1][0].regex == True

    a.add_transition('q1', 'c', 'q2', STAY)
    assert a.q1 in a.transitions
    assert a.transitions[a.q1][1].value == 'c'
    assert a.transitions[a.q1][1].to_state == a.q2
    assert a.transitions[a.q1][1].action == STAY
    assert a.transitions[a.q1][1].regex == False

@pytest.fixture
def pair_ones_automata():
    a = Automata()
    a.add_state('q0', initial=True, final=True)
    a.add_state('q1')
    a.add_transition('q0', '1', 'q1')
    a.add_transition('q1', '1', 'q0')
    a.add_transition('q0', '0', 'q0')
    a.add_transition('q1', '0', 'q1')
    return a

@pytest.fixture
def alpha_automata():
    a = Automata()
    a.add_state('q0', initial=True)
    a.add_state('q1', final=True)
    a.add_transition('q0', r'[a-z]', 'q0', regex=True)
    a.add_transition('q0', r'[^a-z]', 'q1', regex=True)
    return a

def test_run(pair_ones_automata, alpha_automata):
    assert pair_ones_automata.run('11')
    assert pair_ones_automata.run('00')
    assert pair_ones_automata.run('01') == False
    assert pair_ones_automata.run('1000101') == False

    assert alpha_automata.run('abc$')
    assert alpha_automata.run('abc') == False
    assert alpha_automata.run('abc', success_at_full_input=True)
    
    input_ = "sometext123"
    alpha_automata.run(input_, stop_when_final=True)
    final_pos = alpha_automata._pos - 1
    assert input_[:final_pos] == 'sometext'
