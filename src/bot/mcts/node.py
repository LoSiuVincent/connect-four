import math
import random
from copy import deepcopy

from .game import Game


class Node:
    def __init__(self, game: Game = None, n: int = 0, v: float = 0):
        self._parent = self
        self._children = []
        self._game = game
        self.n = n
        self.v = v

    def get_available_actions(self) -> int:
        return self._game.get_available_actions()

    def is_root(self) -> bool:
        return self._parent == self

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

    def get_child_with_highest_UCB(self, C) -> 'Node':
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

    def expand(self) -> None:
        children = [Node(self._game.step(action)) for action in self._game.get_available_actions()]
        self.add_children(children)

    def rollout(self) -> float:
        game_copy = deepcopy(self._game)
        while not game_copy.is_terminal():
            random_action = random.choice(self._game.get_available_actions())
            game_copy.step(random_action)
        return game_copy.get_value()

    def backprop(self, value: float) -> None:
        self.n += 1
        self.v += value
        if not self.is_root():
            self._parent.backprop(value)

    def __repr__(self) -> str:
        return f'Node(n={self.n}, v={self.v})'
