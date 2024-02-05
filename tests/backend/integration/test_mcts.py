import pytest

from src.bot.board import Board
from src.bot.mcts.game import ConnectFour
from src.bot.mcts.mcts import MCTS


@pytest.mark.parametrize(
    'board_str,prediction',
    [
        ('CCCEEEE|PPPEEEE|PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE', 3),  # Horizontal win
        ('CPEEEEE|CPEEEEE|CPEEEEE|EEEEEEE|EEPEEEE|EEEEEEE', 0),  # Vertical win
        ('CPPPEEE|ECPPEEE|EECPEEE|EEEEEEE|EEEEEEE|EEEEEEE', 3),  # / diagonal win
        ('PPPCEEE|PPCEEEE|PCEEEEE|EEEEEEE|EEEEEEE|EEEEEEE', 0),  # \ diagonal win
    ],
)
def test_getting_winning_move(board_str, prediction):
    board = Board.create(board_str)
    game = ConnectFour(board)
    mcts = MCTS(game)

    assert mcts.get_next_move() == prediction
