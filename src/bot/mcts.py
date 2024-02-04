import math
from typing import Protocol


class Game(Protocol):
    pass


class Node:
    def __init__(self, game: Game = None):
        self._parent = self
        self._children = []
        self._game = game
        self.n = 0
        self.v = 0

    def is_leaf(self) -> bool:
        return len(self._children) == 0

    def add_children(self, children: list['Node']) -> None:
        for child in children:
            child._parent = self
        self._children.extend(children)

    def get_children(self) -> list['Node']:
        return self._children

    def get_parent(self) -> 'Node':
        return self._parent

    def __repr__(self) -> str:
        return f'Node(n={self.n}, v={self.v})'


class MCTS:
    def __init__(self, game: Game, C: float = 1):
        self._root = Node(game)
        self._C = C

    def select(self) -> Node:
        current = self._root
        if current.is_leaf():
            return current
        else:
            return self._get_best_child(current)

    def _get_best_child(self, parent: Node) -> Node:
        UCBs = [self._calculate_UCB(child) for child in parent.get_children()]
        max_UCB = max(UCBs)
        for idx, value in enumerate(UCBs):
            if value == max_UCB:
                return parent.get_children()[idx]

    def _calculate_UCB(self, node: Node) -> float:
        if node.n == 0:
            return math.inf
        else:
            return node.v / node.n + self._C * math.sqrt(math.log(node.get_parent().n) / node.n)
