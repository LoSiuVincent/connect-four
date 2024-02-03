from .board import Board
from .strategy import create_strategy


class Bot:
    def __init__(self, strategy: str):
        self._strategy = create_strategy(strategy)

    def predict(self, board_str: str):
        board = Board.create(board_str)
        return self._strategy.predict(board)
