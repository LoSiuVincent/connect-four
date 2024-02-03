from src.board import Board

class Bot:
    def __init__(self, strategy: str):
        self._strategy = strategy

    def predict(self, board_str: str):
        if self._strategy == 'fixed':
            board = Board.create(board_str)
            if not board.is_column_full(1):
                return 1
            else:
                return board.get_next_available_column()
