import random
import time
from unittest.mock import patch

import pytest

from src.bot.board import Board
from src.bot.mcts import MCTS, ConnectFour


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
    random.seed(10)
    board = Board.create(board_str)
    game = ConnectFour(board)
    mcts = MCTS(game)

    assert mcts.get_next_move() == prediction


def test_running_within_time_budget():
    random.seed(10)
    board = Board.create('EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')
    game = ConnectFour(board)
    mcts = MCTS(game, limit='budget', time_budget=1)

    start_time = time.time()
    mcts.get_next_move()
    end_time = time.time()

    assert end_time - start_time == pytest.approx(1, rel=0.1)


def test_run_with_fix_iteration():
    random.seed(10)
    board = Board.create('EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')
    game = ConnectFour(board)
    mcts = MCTS(game, limit='iter', iterations=500)

    with patch('src.bot.mcts.MCTS._run_iteration') as mock_run_iteration:
        with patch('src.bot.mcts.node.Node.get_best_action'):
            mcts.get_next_move()
            assert mock_run_iteration.call_count == 500


@pytest.mark.regression
def test_should_not_stop_player_when_column_full():
    random.seed(10)
    board = Board.create('EECPCEE|EEPCEEE|EECEEEE|EEPEEEE|EEPEEEE|EEPEEEE')
    game = ConnectFour(board)
    mcts = MCTS(game, limit='iter', iterations=2000)

    assert not mcts.get_next_move() == 2


@pytest.mark.regression
def test_list_index_out_of_range():
    random.seed(3)
    board = Board.create('EPCCPPE|EPCPCCE|EECPPCE|EEPPPCE|EEPCCPE|EEECEEE')
    game = ConnectFour(board)
    mcts = MCTS(game, limit='iter', iterations=20000)

    mcts.get_next_move()
