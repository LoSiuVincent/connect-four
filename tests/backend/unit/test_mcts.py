from collections import deque
from unittest.mock import Mock

import pytest

from src.bot.mcts.mcts import MCTS
from src.bot.mcts.node import Node


def create_tree_bfs(game_state, depth, branching_factor, n_v_list):
    if len(n_v_list) < sum(branching_factor**d for d in range(depth)):
        raise ValueError(
            "n_v_list does not contain enough (n, v) pairs for the specified tree structure."
        )

    root_n, root_v = n_v_list.pop(0)
    root = Node(game_state, root_n, root_v)

    queue = deque([(root, 0)])  # (node, current_depth)

    while queue:
        current_node, current_depth = queue.popleft()

        if current_depth < depth:
            for action in range(branching_factor):
                if n_v_list:
                    child_n, child_v = n_v_list.pop(0)
                    child = Node(game_state, n=child_n, v=child_v, action=action)
                    current_node.add_children([child])
                    queue.append((child, current_depth + 1))
                else:
                    break

    return root


def get_n_v_lists(root: Node):
    output = []

    queue = deque([root])

    while queue:
        current = queue.popleft()
        for child in current.get_children():
            queue.append(child)

        output.append((current.n, current.v))

    return output


@pytest.fixture
def game_mock():
    return Mock()


@pytest.fixture
def mcts(game_mock):
    return MCTS(game_mock)


def test_create_root_node(mcts, game_mock):
    assert mcts._root._game == game_mock
    assert mcts._root.n == 0
    assert mcts._root.v == 0


def test_select_root_node(mcts):
    assert mcts.select() == mcts._root


def test_select_node_with_depth_two():
    game = Mock()
    mcts = MCTS(game)
    mcts._root = create_tree_bfs(
        game_mock, depth=2, branching_factor=1, n_v_list=[(2, 2), (1, 2), (0, 2)]
    )

    selected_node = mcts.select()
    assert selected_node.n == 0
    assert selected_node.v == 2


@pytest.mark.parametrize(
    'children_n_v,select_child,C',
    [
        ([(1, 1), (2, 1)], 0, 1.4),
        ([(10, 5), (5, 5)], 1, 1.4),
        ([(1, 1), (5, 10)], 1, 0),
        ([(50, 10), (50, 10), (1, 5)], 2, 100.0),
        ([(1, 1), (1, 1)], 0, 1.4),  # When all nodes have the same n and v, select the first
    ],
)
def test_select_child_node_with_higher_UCB(mcts, children_n_v, select_child, C):
    n_v_list = [(1, 1)] + children_n_v

    root = create_tree_bfs(
        game_mock, depth=1, branching_factor=len(children_n_v), n_v_list=n_v_list
    )
    mcts._root = root
    mcts._C = C

    selected_node = mcts.select()

    assert selected_node == root.get_children()[select_child]


def test_run_four_times(game_mock):
    game_mock.get_available_actions.return_value = [0, 1]
    game_mock.get_value.return_value = 10
    game_mock.step.return_value = game_mock
    game_mock.is_terminal.return_value = True

    mcts = MCTS(game_mock)
    assert get_n_v_lists(mcts._root) == [(0, 0)]

    mcts.run_iteration()
    assert get_n_v_lists(mcts._root) == [(1, 10)]

    mcts.run_iteration()
    assert get_n_v_lists(mcts._root) == [(2, 20), (1, 10), (0, 0)]

    mcts.run_iteration()
    assert get_n_v_lists(mcts._root) == [(3, 30), (1, 10), (1, 10)]

    mcts.run_iteration()
    assert get_n_v_lists(mcts._root) == [(4, 40), (2, 20), (1, 10), (1, 10), (0, 0)]
