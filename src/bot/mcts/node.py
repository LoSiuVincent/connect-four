import math
import random
from copy import deepcopy
from typing import Literal

from .game import Game, GameState


def _argmax(list_: list):
    max_value = max(list_)
    for idx, value in enumerate(list_):
        if value == max_value:
            return idx


class Node:
    def __init__(
        self,
        game: Game = None,
        action: int = -1,
        n: int = 0,
        v: float = 0,
        whose_turn: Literal['player', 'computer'] = 'computer',
    ):
        self._parent = self
        self._children = []
        self._game = game
        self._action = action
        self._whose_turn = whose_turn
        self.n = n
        self.v = v

    def is_terminal(self) -> bool:
        return self._game.is_terminal()

    def is_leaf(self) -> bool:
        return len(self._children) == 0

    def get_first_child(self) -> 'Node':
        return self._children[0]

    def get_child_with_highest_UCB(self, C) -> 'Node':
        UCBs = [child._calculate_UCB(C) for child in self._children]
        return self._children[_argmax(UCBs)]

    def get_best_action(self) -> int:
        return self.get_child_with_best_action()._action
    
    def get_child_with_best_action(self) -> 'Node':
        best_child_idx = _argmax([child.n for child in self._children])
        best_child = self._children[best_child_idx]
        return best_child

    def expand(self) -> None:
        children = []
        for action in self._game.get_available_actions():
            game_copy = deepcopy(self._game)
            game_copy.step(action, self._whose_turn)
            child_node = Node(
                game_copy,
                action=action,
                whose_turn='player' if self._whose_turn == 'computer' else 'computer',
            )
            children.append(child_node)
        self._add_children(children)

    def rollout(self) -> Literal['player', 'computer', 'draw']:
        game_copy = deepcopy(self._game)
        current_turn = self._whose_turn
        while not game_copy.is_terminal():
            random_action = random.choice(self._game.get_available_actions())
            game_copy.step(random_action, current_turn)
            current_turn = 'player' if current_turn == 'computer' else 'computer'

        terminal_state = game_copy.get_state()
        if terminal_state == GameState.DRAW:
            return 'draw'
        elif terminal_state == GameState.PLAYER_WIN:
            return 'player'
        elif terminal_state == GameState.COMPUTER_WIN:
            return 'computer'

    def backprop(self, rollout: str) -> None:
        self.n += 1
        if rollout == 'computer':
            value = 1 if self._whose_turn == 'player' else 0
        elif rollout == 'player':
            value = 1 if self._whose_turn == 'computer' else 0
        elif rollout == 'draw':
            value = 0.5
        self.v += value
        if not self._is_root():
            self._parent.backprop(rollout)

    def _get_children(self) -> list['Node']:
        return self._children

    def _add_children(self, children: list['Node']) -> None:
        for child in children:
            child._parent = self
        self._children.extend(children)

    def _is_root(self) -> bool:
        return self._parent == self

    def _calculate_UCB(self, C) -> float:
        if self.n == 0:
            return math.inf
        else:
            return self.v / self.n + C * math.sqrt(math.log(self._parent.n) / self.n)

    def __repr__(self) -> str:
        return f'Node(n={self.n}, v={self.v})'
