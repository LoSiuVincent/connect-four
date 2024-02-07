from unittest.mock import Mock

import pytest

from src.bot.mcts.game import GameState
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
    node._add_children(children)

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
    node._add_children(children)
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
    root._add_children(children)
    root.n = len(children) - 1

    assert root.get_best_action() == best_action


@pytest.mark.parametrize(
    'whose_turn_of_root,whose_turn_of_children', [('player', 'computer'), ('computer', 'player')]
)
def test_expand(whose_turn_of_root, whose_turn_of_children):
    game = Mock()
    game.get_available_actions.return_value = [0, 1, 2]
    node = Node(game, whose_turn=whose_turn_of_root)
    assert len(node._get_children()) == 0

    node.expand()

    assert len(node._get_children()) == 3
    for child in node._get_children():
        assert child._parent == node
        assert child._game is not None
        assert child._whose_turn == whose_turn_of_children


@pytest.mark.parametrize(
    'whose_turn,last_state,rollout_value',
    [
        ('computer', GameState.PLAYER_WIN, 0),
        ('computer', GameState.COMPUTER_WIN, 1),
        ('computer', GameState.DRAW, 0.5),
        ('player', GameState.PLAYER_WIN, 1),
        ('player', GameState.COMPUTER_WIN, 0),
        ('player', GameState.DRAW, 0.5),
    ],
)
def test_rollout(whose_turn, last_state, rollout_value):
    game_mock = Mock()
    game_mock.get_available_actions.return_value = [0, 1]
    game_mock.is_terminal.side_effect = [False, False, True]
    game_mock.get_state.return_value = last_state
    node = Node(game_mock, whose_turn=whose_turn)

    assert node.rollout() == rollout_value


@pytest.mark.parametrize(
    'backprop_value,root_v,child_v,grandchild_v',
    [(1, 2, 0, 1), (0.5, 1.5, 0.5, 0.5), (0, 1, 1, 0)],
)
def test_backprop(game_mock, backprop_value, root_v, child_v, grandchild_v):
    root = Node(game_mock, n=2, v=1, whose_turn='computer')
    child = Node(game_mock, n=1, v=0, whose_turn='player')
    grandchild = Node(game_mock, n=0, v=0, whose_turn='computer')
    root._add_children([child])
    child._add_children([grandchild])

    grandchild.backprop(backprop_value)
    assert root.n == 3
    assert root.v == root_v

    assert child.n == 2
    assert child.v == child_v

    assert grandchild.n == 1
    assert grandchild.v == grandchild_v
