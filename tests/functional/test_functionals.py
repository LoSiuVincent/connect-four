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
def test_player_wins_game(browser):
    state_text = browser.find_state_text()

    # John plays three moves to set up three in a row
    for _ in range(3):
        browser.click_column(0)
        browser.wait_until_computer_turn_done()

    # He makes the winning move by placing the fourth disc in the same column
    browser.click_column(0)

    # He sees "You win!" in the state text
    browser.wait_until_computer_turn_done()
    assert 'You win!' in state_text.text

    # He clicks the first column again and confirms that the game is ended
    browser.click_column(0, wait_before_player_turn_start=False)
    canvas = browser.find_canvas()
    web_element_regression(canvas, 'game_end_after_winning')


@pytest.mark.visual
def test_player_loses_game(browser):
    state_text = browser.find_state_text()

    # John plays three moves to set up three in a row
    for _ in range(3):
        browser.click_column(0)
        browser.wait_until_computer_turn_done()

    # He makes the losing move by placing the fourth disc in new column
    browser.click_column(3)

    # He sees "You lose, try again!" in the state text after the computer has made a move
    browser.wait_until_computer_turn_done()
    assert 'You lose, try again!' in state_text.text

    # He clicks the first column again and confirms that the game is ended
    browser.click_column(0, wait_before_player_turn_start=False)
    canvas = browser.find_canvas()
    web_element_regression(canvas, 'game_end_after_losing')
