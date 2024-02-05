import pytest

from src.bot import Bot


def test_getting_random_move():
    bot = Bot(strategy='random')

    prediction = bot.predict('PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')

    assert isinstance(prediction, int)


def test_getting_random_move_when_only_one_column_left():
    bot = Bot(strategy='random')

    prediction = bot.predict('PCPCPCE|PCPCPCE|PCPCPCE|PCPCPCE|PCPCPCE|PCPCPCE')

    assert prediction == 6


def test_getting_fixed_move():
    bot = Bot(strategy='fixed')

    prediction = bot.predict('PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')

    assert prediction == 1


def test_getting_fixed_move_when_column_full():
    bot = Bot(strategy='fixed')

    prediction = bot.predict('EPEEEEE|ECEEEEE|EPEEEEE|ECEEEEE|EPEEEEE|ECEEEEE')

    assert prediction == 0


@pytest.mark.parametrize(
    'board_str,prediction',
    [
        ('CCCEEEE|PPPEEEE|PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE', 3),  # Horizontal win
        ('CPEEEEE|CPEEEEE|CPEEEEE|CEEEEEE|EEPEEEE|EEEEEEE', 0),  # Vertical win
        ('CPCEEEE|PCCEEEE|EPPCEEE|EEECPEE|EEEEEEP|EEEEEEE', 0),  # Major diagonal win
        ('EEECPEE|EEEPCEP|EEECPPE|EEPPCEE|EPCPEEE|CPCEEEE', 3),  # Minor diagonal win
    ],
)
def test_getting_MCTS_move(board_str, prediction):
    bot = Bot(strategy='mcts')

    bot_prediction = bot.predict(board_str)

    assert bot_prediction == prediction
