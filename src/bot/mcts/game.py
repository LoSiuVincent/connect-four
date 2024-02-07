from enum import Enum
from typing import Literal, Protocol

from src.bot.board import Board


class GameState(Enum):
    PLAYER_WIN = 0
    COMPUTER_WIN = 1
    DRAW = 2
    NORMAL = 3


class Game(Protocol):
    def step(self, action: int, whose_move: Literal['player', 'computer']) -> None: ...

    def get_available_actions(self) -> list[int]: ...

    def is_terminal(self) -> bool: ...

    def get_state(self) -> float: ...


class ConnectFour(Game):
    def __init__(self, board: Board):
        self._board = board

    def step(self, action: int, whose_move: Literal['player', 'computer']) -> None:
        self._board.drop_coin(action, whose_move)

    def get_available_actions(self) -> list[int]:
        return self._board.get_available_columns()

    def is_terminal(self) -> bool:
        winner = self._board.get_winner()
        if len(self.get_available_actions()) == 0 and winner is None:
            return True
        else:
            return winner in ['player', 'computer']

    def get_state(self) -> float:
        if not self.is_terminal():
            return GameState.NORMAL

        winner = self._board.get_winner()
        if winner == 'player':
            return GameState.PLAYER_WIN
        elif winner == 'computer':
            return GameState.COMPUTER_WIN
        else:
            return GameState.DRAW
