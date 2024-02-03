import pytest
from selenium.common.exceptions import NoSuchElementException

from tests.functional.conftest import BROWSER_WIDTH
from tests.functional.visreg import web_element_regression


def test_canvas_exists(browser):
    # He sees a canvas where he can play the game
    try:
        browser.find_canvas()
    except NoSuchElementException:
        pytest.fail('There is no canvas element')


def test_layout(browser):
    # He sees a canvas center on the website
    canvas = browser.find_canvas()
    canvas_center_x = canvas.location['x'] + canvas.size['width'] / 2
    assert canvas_center_x == BROWSER_WIDTH / 2


@pytest.mark.visual
def test_board_exists(browser):
    # John sees a board drawn on the page
    canvas = browser.find_canvas()

    web_element_regression(canvas, 'board', wait_time_before_capture=1)


@pytest.mark.visual
def test_play_with_the_computer(browser):
    # John sees the canvas for the game
    canvas = browser.find_canvas()
    assert canvas is not None

    state_text = browser.find_state_text()

    # He sees "Your turn" and he clicks the first column
    browser.wait_until_text_appear('Your turn')
    browser.click_column(0)

    # He sees a coin has appear
    web_element_regression(canvas, 'player_first_move')

    # He sees the text changed and became "Thinking ..." afterward
    browser.wait_until_text_disappear('Your turn')
    assert state_text.text == 'Thinking ...'

    # He sees "Your turn" again after a while and the computer has made a move
    browser.wait_until_text_appear('Your turn')
    web_element_regression(canvas, 'computer_first_move')

    # He clicks another column
    browser.click_column(3)

    # He sees a coin has appear
    web_element_regression(canvas, 'player_second_move')

    # He sees the text changed and became "Thinking ..." afterward
    browser.wait_until_text_disappear('Your turn')
    assert state_text.text == 'Thinking ...'

    # He sees "Your turn" again after a while and the computer has made a move
    browser.wait_until_text_appear('Your turn')
    web_element_regression(canvas, 'computer_second_move')

    # He clicks the first column again
    browser.click_column(0)

    # He sees the coin is stacked above the first coin
    web_element_regression(canvas, 'player_third_move')

    # He sees the text changed and became "Thinking ..." afterward
    browser.wait_until_text_disappear('Your turn')
    assert state_text.text == 'Thinking ...'

    # He sees "Your turn" again after a while and the computer has made a move
    browser.wait_until_text_appear('Your turn')
    web_element_regression(canvas, 'computer_third_move')


@pytest.mark.visual
def test_player_wins_game(browser):
    state_text = browser.find_state_text()

    # John plays three moves to set up three in a row
    for _ in range(3):
        browser.wait_until_text_appear('Your turn')
        browser.click_column(0)
        browser.wait_until_text_disappear('Your turn')
        assert state_text.text == 'Thinking ...'
        browser.wait_until_text_appear('Your turn')

    # He makes the winning move by placing the fourth disc in the same column
    browser.click_column(0)

    # He sees "You win!" in the state text
    browser.wait_until_text_disappear('Your turn')
    assert 'You win!' in state_text.text

    # He clicks the first column again and confirms that the game is ended
    browser.click_column(0)
    canvas = browser.find_canvas()
    web_element_regression(canvas, 'game_end_after_winning')


@pytest.mark.visual
def test_player_loses_game(browser):
    state_text = browser.find_state_text()

    # John plays three moves to set up three in a row
    for _ in range(3):
        browser.wait_until_text_appear('Your turn')
        browser.click_column(0)
        browser.wait_until_text_disappear('Your turn')
        assert state_text.text == 'Thinking ...'
        browser.wait_until_text_appear('Your turn')

    # He makes the losing move by placing the fourth disc in new column
    browser.click_column(3)

    # He waits for the computer to make a move
    browser.wait_until_text_disappear('Your turn')
    assert state_text.text == 'Thinking ...'

    # He sees "You lose, try again!" in the state text
    browser.wait_until_text_disappear('Thinking ...')
    assert 'You lose, try again!' in state_text.text

    # He clicks the first column again and confirms that the game is ended
    browser.click_column(0)
    canvas = browser.find_canvas()
    web_element_regression(canvas, 'game_end_after_losing')
