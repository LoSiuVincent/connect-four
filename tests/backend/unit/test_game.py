import pytest

from src.bot.board import Board
from src.bot.mcts.game import ConnectFour


def create_game_from_board_str(board_str: str):
    board = Board.create(board_str)
    return ConnectFour(board)


def test_get_available_actions_when_no_full_columns():
    game = create_game_from_board_str('CCCEEEE|PPPEEEE|PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')

    assert game.get_available_actions() == [i for i in range(7)]


def test_get_available_actions_when_one_full_columns():
    game = create_game_from_board_str('CEEEEEE|PEEEEEE|PEEEEEE|CEEEEEE|PEEEEEE|CEEEEEE')

    assert game.get_available_actions() == [i for i in range(1, 7)]


def test_terminal_state_of_nobody_wins():
    game = create_game_from_board_str('PPPEEEE|CCCEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')

    assert not game.is_terminal()


def test_terminal_state_of_player_wins():
    game = create_game_from_board_str('PPPPEEE|CCCEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')

    assert game.is_terminal()


def test_terminal_state_of_draws():
    game = create_game_from_board_str('CCPPCPC|CCPPCCP|PPCCPPC|CCPPPCP|PPPCPPP|CCCPCCC')

    assert game.is_terminal()


def test_terminal_state_of_computer_wins():
    game = create_game_from_board_str('CCCCEEE|PPPEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')

    assert game.is_terminal()


def test_value_of_player_wins():
    game = create_game_from_board_str('PPPPEEE|CCCEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')

    assert game.get_value() == -1


def test_value_of_computer_wins():
    game = create_game_from_board_str('CCCCEEE|PPPEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')

    assert game.get_value() == 1


def test_value_of_draw():
    game = create_game_from_board_str('CCPPCPC|CCPPCCP|PPCCPPC|CCPPPCP|PPPCPPP|CCCPCCC')

    assert game.is_terminal()
    assert game.get_value() == 0


def test_runtime_error_when_game_not_terminated():
    game = create_game_from_board_str('EEECEEE|EEEPEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')

    with pytest.raises(RuntimeError):
        game.get_value()


@pytest.mark.parametrize(
    'board_str',
    [
        'PPPEEEE|CCCEEEE|CEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE',
        'PPPEEEE|CCCEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE',
    ],
)
def test_step_makes_player_move(board_str):
    board = Board.create(board_str)
    game = ConnectFour(board, player_first=True)

    game.step(3)

    assert game.is_terminal()
    assert game.get_value() == -1


@pytest.mark.parametrize(
    'board_str',
    [
        'CCCEEEE|PPPEEEE|PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE',
        'CCCEEEE|PPPEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE',
    ],
)
def test_step_makes_computer_move(board_str):
    board = Board.create(board_str)
    game = ConnectFour(board, player_first=False)

    game.step(3)

    assert game.is_terminal()
    assert game.get_value() == 1
