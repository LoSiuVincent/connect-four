from src.bot import Bot


def test_getting_random_move():
    bot = Bot(strategy='random')

    prediction = bot.predict('PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')

    assert isinstance(prediction, int)


def test_getting_fixed_move():
    bot = Bot(strategy='fixed')

    prediction = bot.predict('PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE')

    assert prediction == 1


def test_getting_fixed_move_when_column_full():
    bot = Bot(strategy='fixed')

    prediction = bot.predict('EPEEEEE|ECEEEEE|EPEEEEE|ECEEEEE|EPEEEEE|ECEEEEE')

    assert prediction == 0
