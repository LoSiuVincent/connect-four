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

    def get_available_actions(self) -> list[int]:
        return self._board.get_available_columns()

    def is_terminal(self) -> bool:
        return super().is_terminal()
