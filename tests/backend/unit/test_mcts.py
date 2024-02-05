from unittest.mock import Mock

import pytest

from src.bot.mcts.mcts import MCTS
from src.bot.mcts.node import Node


def test_create_root_node():
    game = Mock()
    mcts = MCTS(game)

    assert mcts._root._game == game
    assert mcts._root.n == 0
    assert mcts._root.v == 0


def test_select_root_node():
    game = Mock()
    mcts = MCTS(game)

    assert mcts.select() == mcts._root


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
def test_select_child_node_with_higher_UCB(children_n_v, select_child, C):
    some_game_state = Mock()
    root = Node(some_game_state)
    children = []
    for n, v in children_n_v:
        child = Node(some_game_state)
        child.n = n
        child.v = v
        children.append(child)
    root.add_children(children)
    root.n = len(children) - 1

    mcts = MCTS(some_game_state, C=C)
    mcts._root = root

    assert mcts.select() == children[select_child]

def test_expand_node():
    game = Mock()
    mcts = MCTS(game)
    node = Mock()
    mcts._root = node

    mcts.expand(node)
    
    node.expand.assert_called_once()
    
def test_rollout():
    game = Mock()
    mcts = MCTS(game)
    node = Mock()
    node.rollout.return_value = 10
    mcts._root = node
    
    assert mcts.rollout(mcts._root) == 10