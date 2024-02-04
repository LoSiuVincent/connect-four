from unittest.mock import Mock

import pytest

from src.bot.mcts import MCTS, Node


def test_create_root_node():
    game_state = Mock()
    mcts = MCTS(game_state)

    assert mcts._root._game == game_state
    assert mcts._root.n == 0
    assert mcts._root.v == 0


def test_select_root_node():
    game_state = Mock()
    mcts = MCTS(game_state)

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
