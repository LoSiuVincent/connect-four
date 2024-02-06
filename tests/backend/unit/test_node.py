from unittest.mock import Mock

import pytest

from src.bot.mcts.node import Node


@pytest.fixture
def game_mock():
    return Mock()


def test_is_leaf_node_returns_true():
    node = Node()

    assert node.is_leaf()


def test_is_leaf_node_returns_false():
    node = Node()
    children = [Node() for _ in range(7)]
    node.add_children(children)

    assert not node.is_leaf()


@pytest.mark.parametrize(
    'children_n_v,select_child,C',
    [
        ([(1, 1), (2, 1)], 0, 1.4),
        ([(10, 5), (5, 5)], 1, 1.4),
        ([(1, 1), (5, 10)], 1, 0),
        ([(10, 50), (10, 50), (1, 5)], 2, 5.0),
        ([(0, 0), (0, 0)], 0, 1.4),  # When all nodes have the same n and v, select the first
    ],
)
def test_get_child_with_highest_UCB(children_n_v, select_child, C):
    some_game_state = Mock()
    node = Node(some_game_state)
    children = []
    for n, v in children_n_v:
        child = Node(some_game_state)
        child.n = n
        child.v = v
        children.append(child)
    node.add_children(children)
    node.n = len(children) - 1

    assert node.get_child_with_highest_UCB(C) == children[select_child]


@pytest.mark.parametrize(
    'children_n_v,best_action',
    [([(1, 1), (2, 1)], 0), ([(10, 5), (5, 5)], 1), ([(1, 1), (5, 10)], 1), ([(1, 1), (0, 0)], 0)],
)
def test_get_action_with_highest_average_value(children_n_v, best_action):
    some_game_state = Mock()
    root = Node(some_game_state)
    children = []
    for action, (n, v) in enumerate(children_n_v):
        child = Node(some_game_state, action=action)
        child.n = n
        child.v = v
        children.append(child)
    root.add_children(children)
    root.n = len(children) - 1

    assert root.get_best_action() == best_action


def test_expand():
    game = Mock()
    game.get_available_actions.return_value = [0, 1, 2]
    game.step.return_value = None
    node = Node(game)
    assert len(node.get_children()) == 0

    node.expand()

    assert len(node.get_children()) == 3
    for child in node.get_children():
        assert child._parent == node
        assert child._game is not None
        assert child._game is not game


def test_rollout():
    actual_game = Mock()
    actual_game.get_available_actions.return_value = [0, 1]
    actual_game.is_terminal.side_effect = [False, False, True]
    actual_game.get_value.return_value = 10
    node = Node(actual_game)

    rollout_value = node.rollout()

    actual_game.is_terminal.assert_not_called()
    assert rollout_value == 10


def test_backprop(game_mock):
    root = Node(game_mock, n=1, v=1)
    child = Node(game_mock, n=1, v=0)
    grandchild = Node(game_mock, n=0, v=0)
    root.add_children([child])
    child.add_children([grandchild])

    grandchild.backprop(10)

    assert grandchild.n == 1
    assert grandchild.v == 10

    assert child.n == 2
    assert child.v == 10

    assert root.n == 2
    assert root.v == 11
