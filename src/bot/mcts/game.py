from typing import Protocol


class Game(Protocol):
    def step(self, action) -> None: ...

    def get_available_actions(self) -> list[int]: ...
