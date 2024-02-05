import math
import random
from copy import deepcopy
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

    def get_game(self) -> Game:
        return self._game
    
    def get_available_actions(self) -> int:
        return self._game.get_available_actions()

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

    def get_best_child(self, C) -> 'Node':
        UCBs = [child._calculate_UCB(C) for child in self._children]
        max_UCB = max(UCBs)
        for idx, value in enumerate(UCBs):
            if value == max_UCB:
                return self._children[idx]

    def _calculate_UCB(self, C) -> float:
        if self.n == 0:
            return math.inf
        else:
            return self.v / self.n + C * math.sqrt(math.log(self._parent.n) / self.n)

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
            return current.get_best_child(self._C)

    def expand(self, node: Node) -> None:
        game = node.get_game()
        new_nodes = [Node(game.step(action)) for action in game.get_available_actions()]
        node.add_children(new_nodes)

    def rollout(self, node: Node) -> float:
        game_copy = deepcopy(node.get_game())
        while not game_copy.is_terminal():
            random_action = random.choice(node.get_available_actions())
            game_copy.step(random_action)
        return game_copy.get_value()
