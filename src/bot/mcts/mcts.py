import logging
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

    def get_next_move(self):
        if self._limit == 'budget':
            start_time = time.time()
            elapsed_time = 0
            num_iter = 0
            while elapsed_time < self._time_budget:
                self._run_iteration()
                elapsed_time = time.time() - start_time
                num_iter += 1
            logging.info(f'Ran {num_iter} iterations in {elapsed_time} s')
        else:
            for _ in range(self._iterations):
                self._run_iteration()

        best_action = self._root.get_best_action()

        if self._root.n != 0:
            logging.info(
                f'Best action: {best_action} | Win rate: {self._root.v / self._root.n * 100:.3f}%'
            )
        else:
            logging.info(f'Best action: {best_action} | Win rate: Not available')

        return self._root.get_best_action()

    def _run_iteration(self):
        selected_node = self._select()
        if selected_node.n != 0 and not selected_node.is_terminal():
            selected_node.expand()
            selected_node = selected_node.get_first_child()
        rollout_value = selected_node.rollout()
        selected_node.backprop(rollout_value)

    def _select(self) -> Node:
        current = self._root
        while not current.is_leaf():
            current = current.get_child_with_highest_UCB(self._C)
        return current
