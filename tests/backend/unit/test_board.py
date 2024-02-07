import pytest

from src.bot.board import Board


def test_parse_board_str():
    board_str = 'CPEEEEE|ECEEEEE|EPEEEEE|ECEEEEE|EPEEEEE|ECEEEEE'

    expected_board = [
        ['computer', 'player', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'computer', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'player', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'computer', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'player', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'computer', 'empty', 'empty', 'empty', 'empty', 'empty'],
    ]

    assert Board._parse_board_str(board_str) == expected_board


def test_create_board_object():
    board = Board.create('CPEEEEE|ECEEEEE|EPEEEEE|ECEEEEE|EPEEEEE|ECEEEEE')

    assert isinstance(board, Board)

    expected_board = [
        ['computer', 'player', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'computer', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'player', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'computer', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'player', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'computer', 'empty', 'empty', 'empty', 'empty', 'empty'],
    ]
    assert board._board == expected_board


@pytest.mark.parametrize(
    'board_str,next_available_column',
    [
        ('CPEEEEE|ECEEEEE|EPEEEEE|ECEEEEE|EPEEEEE|ECEEEEE', 0),
        ('CPEEEEE|PCEEEEE|CPEEEEE|PCEEEEE|CPEEEEE|PCEEEEE', 2),
    ],
)
def test_get_next_available_column(board_str, next_available_column):
    board = Board.create(board_str)

    assert board.get_next_available_column() == next_available_column


def test_check_full_column():
    board = Board.create('CPEEEEE|PCEEEEE|CPEEEEE|PCEEEEE|CPEEEEE|PCEEEEE')

    assert board.is_column_full(0)
    assert board.is_column_full(1)
    assert not board.is_column_full(2)
    assert not board.is_column_full(3)
    assert not board.is_column_full(4)
    assert not board.is_column_full(5)
    assert not board.is_column_full(6)


def test_get_available_columns():
    board = Board.create('CPEEEEE|PCEEEEE|CPEEEEE|PCEEEEE|CPEEEEE|PCEEEEE')

    assert board.get_available_columns() == [2, 3, 4, 5, 6]


@pytest.mark.parametrize(
    "board_str,winner",
    [
        # Horizontal wins
        ('PPPPEEE|CCCEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE', 'player'),
        ('EEECCCC|EEEEPPP|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE', 'computer'),
        # Vertical wins
        ('PEEEEEE|PEEEEEE|PEEEEEE|PEECEEE|CEEEEEE|CEEEEEE', 'player'),
        ('CEEEEEE|CEEEEEE|CEEEEEE|CEEPEEE|PEEEEEE|PEEEEEE', 'computer'),
        # Diagonal descending wins (/)
        ('PCCCEEE|EPCCEEE|EEPCEEE|EEEPEEE|EEEEEEE|EEEEEEE', 'player'),
        ('CPPPEEE|ECPPEEE|EECPEEE|EEECEEE|EEEEEEE|EEEEEEE', 'computer'),
        # Diagonal ascending wins (\)
        ('CCCPEEE|CCPEEEE|CPEEEEE|PEEEEEE|EEEEEEE|EEEEEEE', 'player'),
        ('PPPCEEE|PPCEEEE|PCEEEEE|CEEEEEE|EEEEEEE|EEEEEEE', 'computer'),
        # No one wins
        ('EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE', None),
    ],
)
def test_win_conditions(board_str, winner):
    board = Board.create(board_str)

    assert board.get_winner() == winner


def test_drop_coins():
    board = Board.create('EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')

    board.drop_coin(0, 'computer')
    board.drop_coin(0, 'computer')
    board.drop_coin(0)
    board.drop_coin(0)
    board.drop_coin(0)
    board.drop_coin(0)

    assert board.get_available_columns() == [i for i in range(1, 7)]
    assert board.get_winner() == 'player'
