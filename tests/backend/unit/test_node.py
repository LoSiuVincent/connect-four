from src.bot.mcts import Node


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
