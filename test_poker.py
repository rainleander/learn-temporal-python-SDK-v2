import pytest
from workflow import PokerWorkflow


@pytest.fixture(scope="module")
def workflow():
    return PokerWorkflow()


def test_workflow_initial_state(workflow):
    state = workflow.execute_game()
    assert state["round"] == 1
    assert len(state["players"]) == 2
    assert all([p["hand"] for p in state["players"]])
    assert state["deck"]


def test_workflow_round_2(workflow):
    state = workflow.execute_game()
    state = workflow.execute_game()
    assert state["round"] == 2
    assert all([p["hand"] for p in state["players"]])
    assert state["deck"]


def test_workflow_round_3(workflow):
    state = workflow.execute_game()
    state = workflow.execute_game()
    state = workflow.execute_game()
    assert state["round"] == 3
    assert all([p["hand"] for p in state["players"]])
    assert state["deck"]


def test_workflow_round_4(workflow):
    state = workflow.execute_game()
    state = workflow.execute_game()
    state = workflow.execute_game()
    state = workflow.execute_game()
    assert state["round"] == 4
    assert all([p["hand"] for p in state["players"]])
    assert state["deck"]


def test_workflow_round_5(workflow):
    state = workflow.execute_game()
    state = workflow.execute_game()
    state = workflow.execute_game()
    state = workflow.execute_game()
    state = workflow.execute_game()
    assert state["round"] == 5
    assert all([p["hand"] for p in state["players"]])
    assert not state["deck"]
    assert any([p["hand_rank"] for p in state["players"]])
