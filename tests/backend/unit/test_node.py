import pytest
from unittest.mock import Mock

from src.bot.mcts.node import Node


def test_is_leaf_node_returns_true():
    node = Node()

    assert node.is_leaf()


def test_is_leaf_node_returns_false():
    node = Node()
    children = [Node() for _ in range(7)]
    node.add_children(children)

    assert not node.is_leaf()


def test_child_get_parent_node():
    parent = Node()
    child = Node()
    parent.add_children([child])

    assert child.get_parent() == parent


def test_root_get_parent_node():
    root = Node()

    assert root.get_parent() == root

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

def test_expand_node():
    game = Mock()
    game.get_available_actions.return_value = [0, 1, 2]
    game.step.return_value = Mock()
    node = Node(game)
    assert len(node.get_children()) == 0

    node.expand()

    assert len(node.get_children()) == 3


def test_rollout_node():
    actual_game = Mock()
    actual_game.get_available_actions.return_value = [0, 1]
    actual_game.is_terminal.side_effect = [False, False, True]
    actual_game.get_value.return_value = 10
    node = Node(actual_game)

    rollout_value = node.rollout()

    actual_game.is_terminal.assert_not_called()
    assert rollout_value == 10
