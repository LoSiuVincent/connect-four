import time
from typing import Literal

from .game import Game
from .node import Node


class MCTS:
    def __init__(
        self,
        game: Game,
        C: float = 1,
        limit: Literal['iter', 'budget'] = 'iter',
        time_budget: float = None,
        iterations: int = 1000,
    ):
        self._root = Node(game)
        self._C = C
        self._limit = limit
        self._time_budget = time_budget
        self._iterations = iterations

    def select(self) -> Node:
        current = self._root
        while not current.is_leaf():
            current = current.get_child_with_highest_UCB(self._C)
        return current

    def run_iteration(self):
        selected_node = self.select()
        if selected_node.n != 0:
            selected_node.expand()
            selected_node = selected_node.get_children()[0]
        rollout_value = selected_node.rollout()
        selected_node.backprop(rollout_value)

    def get_next_move(self):
        if self._limit == 'budget':
            start_time = time.time()
            elapsed_time = 0
            while elapsed_time < self._time_budget:
                self.run_iteration()
                elapsed_time = time.time() - start_time
        else:
            for _ in range(self._iterations):
                self.run_iteration()

        return self._root.get_best_action()
