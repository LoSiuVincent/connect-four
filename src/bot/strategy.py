import random


def create_strategy(strategy: str):
    if strategy == 'fixed':
        return FixedStrategy()
    elif strategy == 'random':
        return RandomStrategy()


class FixedStrategy:
    def predict(self, board):
        if not board.is_column_full(1):
            return 1
        else:
            return board.get_next_available_column()


class RandomStrategy:
    def predict(self, board):
        return random.choice(board.get_available_columns())
