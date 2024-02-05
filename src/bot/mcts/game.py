from typing import Protocol

from src.bot.board import Board


class Game(Protocol):
    def step(self, action: int) -> None: ...

    def get_available_actions(self) -> list[int]: ...

    def is_terminal(self) -> bool: ...

    def get_value(self) -> float: ...


class ConnectFour(Game):
    def __init__(self, board_str: str, player_first=True):
        self._board = Board.create(board_str)
        self._player_first = player_first

    def step(self, action: int) -> None:
        whose_move = self._get_whose_move()
        self._board.drop_coin(action, whose_move)

    def get_available_actions(self) -> list[int]:
        return self._board.get_available_columns()

    def is_terminal(self) -> bool:
        winner = self._board.get_winner()
        if len(self.get_available_actions()) == 0 and winner is None:
            return True
        else:
            return winner in ['player', 'computer']

    def get_value(self) -> float:
        if not self.is_terminal():
            raise RuntimeError('Game is not in terminal state')

        winner = self._board.get_winner()
        if winner == 'player':
            return -1
        elif winner == 'computer':
            return 1
        else:
            return 0

    def _get_whose_move(self) -> str:
        num_computer_moves = self._board.get_num_computer_moves()
        num_player_moves = self._board.get_num_player_moves()
        if num_computer_moves < num_player_moves:
            return 'computer'
        elif num_computer_moves > num_player_moves:
            return 'player'
        else:
            return 'player' if self._player_first else 'computer'
