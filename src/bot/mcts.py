import math


class Node:
    def __init__(self, state):
        self._parent = self
        self._children = []
        self._state = state
        self.n = 0
        self.v = 0

    def is_leaf(self):
        return len(self._children) == 0

    def add_children(self, children: list['Node']):
        for child in children:
            child._parent = self
        self._children.extend(children)

    def get_children(self):
        return self._children

    def get_parent(self):
        return self._parent

    def __repr__(self):
        return f'Node(n={self.n}, v={self.v})'


class MCTS:
    def __init__(self, game_state, C=1):
        self._root = Node(game_state)
        self._C = C

    def select(self):
        current = self._root
        if current.is_leaf():
            return current
        else:
            return self._get_best_child(current)

    def _get_best_child(self, parent):
        UCBs = [self._calculate_UCB(child) for child in parent.get_children()]
        max_UCB = max(UCBs)
        for idx, value in enumerate(UCBs):
            if value == max_UCB:
                return parent.get_children()[idx]

    def _calculate_UCB(self, node):
        if node.n == 0:
            return math.inf
        else:
            return node.v / node.n + self._C * math.sqrt(math.log(node.get_parent().n) / node.n)
