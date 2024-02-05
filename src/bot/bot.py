import random

from .board import Board
from .mcts import MCTS, ConnectFour


def create_strategy(strategy: str):
    if strategy == 'fixed':
        return FixedStrategy()
    elif strategy == 'random':
        return RandomStrategy()
    elif strategy == 'mcts':
        return MCTSStrategy()


class FixedStrategy:
    def predict(self, board: Board):
        if not board.is_column_full(1):
            return 1
        else:
            return board.get_next_available_column()


class RandomStrategy:
    def predict(self, board: Board):
        return random.choice(board.get_available_columns())


class MCTSStrategy:
    def predict(self, board: Board):
        game = ConnectFour(board)
        mcts = MCTS(game, limit='budget', time_budget=2)
        return mcts.get_next_move()


class Bot:
    def __init__(self, strategy: str):
        self._strategy = create_strategy(strategy)

    def predict(self, board_str: str):
        board = Board.create(board_str)
        return self._strategy.predict(board)
