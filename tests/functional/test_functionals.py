import time

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.functional.conftest import BROWSER_WIDTH
from tests.functional.visreg import web_element_regression


def find_canvas(browser):
    return browser.find_element(By.TAG_NAME, 'canvas')


def find_state_text(browser):
    return browser.find_element(By.ID, 'id-game-state-text')


def get_cell_length(browser):
    return browser.execute_script('return view.getCellLength();')


def wait_until_text_appear(browser, text: str, timeout=5):
    WebDriverWait(browser, timeout).until(
        EC.text_to_be_present_in_element((By.ID, 'id-game-state-text'), text)
    )


def wait_until_text_disappear(browser, text: str, timeout=5):
    WebDriverWait(browser, timeout).until_not(
        EC.text_to_be_present_in_element((By.ID, 'id-game-state-text'), text)
    )


def click_column(browser, column_index):
    canvas = find_canvas(browser)
    cell_width = get_cell_length(browser)
    click_x = column_index * cell_width + 0.5 * cell_width - canvas.size['width'] / 2
    click_y = 100 - canvas.size['height'] / 2

    action = webdriver.common.action_chains.ActionChains(browser)
    action.move_to_element_with_offset(canvas, click_x, click_y)
    action.click()
    action.perform()

    time.sleep(1)


def test_canvas_exists(browser):
    # He sees a canvas where he can play the game
    try:
        find_canvas(browser)
    except NoSuchElementException:
        pytest.fail('There is no canvas element')


def test_layout(browser):
    # He sees a canvas center on the website
    canvas = find_canvas(browser)
    canvas_center_x = canvas.location['x'] + canvas.size['width'] / 2
    assert canvas_center_x == BROWSER_WIDTH / 2


@pytest.mark.visual
def test_board_exists(browser):
    # John sees a board drawn on the page
    canvas = find_canvas(browser)

    web_element_regression(canvas, 'board', wait_time_before_capture=1)


@pytest.mark.visual
def test_play_with_the_computer(browser):
    # John sees the canvas for the game
    canvas = find_canvas(browser)
    assert canvas is not None

    state_text = find_state_text(browser)

    # He sees "Your turn" and he clicks the first column
    wait_until_text_appear(browser, 'Your turn')
    click_column(browser, 0)

    # He sees a coin has appear
    web_element_regression(canvas, 'player_first_move')

    # He sees the text changed and became "Thinking ..." afterward
    wait_until_text_disappear(browser, 'Your turn')
    assert state_text.text == 'Thinking ...'

    # He sees "Your turn" again after a while and the computer has made a move
    wait_until_text_appear(browser, 'Your turn')
    web_element_regression(canvas, 'computer_first_move')

    # He clicks another column
    click_column(browser, 3)

    # He sees a coin has appear
    web_element_regression(canvas, 'player_second_move')

    # He sees the text changed and became "Thinking ..." afterward
    wait_until_text_disappear(browser, 'Your turn')
    assert state_text.text == 'Thinking ...'

    # He sees "Your turn" again after a while and the computer has made a move
    wait_until_text_appear(browser, 'Your turn')
    web_element_regression(canvas, 'computer_second_move')

    # He clicks the first column again
    click_column(browser, 0)

    # He sees the coin is stacked above the first coin
    web_element_regression(canvas, 'player_third_move')

    # He sees the text changed and became "Thinking ..." afterward
    wait_until_text_disappear(browser, 'Your turn')
    assert state_text.text == 'Thinking ...'

    # He sees "Your turn" again after a while and the computer has made a move
    wait_until_text_appear(browser, 'Your turn')
    web_element_regression(canvas, 'computer_third_move')


def test_player_wins_game(browser):
    state_text = find_state_text(browser)

    # John plays three moves to set up three in a row
    for _ in range(3):
        wait_until_text_appear(browser, 'Your turn')
        click_column(browser, 0)
        wait_until_text_disappear(browser, 'Your turn')
        assert state_text.text == 'Thinking ...'
        wait_until_text_appear(browser, 'Your turn')

    # He makes the winning move by placing the fourth disc in the same column
    click_column(browser, 0)

    # He sees "You win!" in the state text
    wait_until_text_disappear(browser, 'Your turn')
    assert 'You win!' in state_text.text

    # He clicks the first column again and confirms that the game is ended
    click_column(browser, 0)
    canvas = find_canvas(browser)
    web_element_regression(canvas, 'game_end_after_winning')
    

def test_player_loses_game(browser):
    state_text = find_state_text(browser)

    # John plays three moves to set up three in a row
    for _ in range(3):
        wait_until_text_appear(browser, 'Your turn')
        click_column(browser, 0)
        wait_until_text_disappear(browser, 'Your turn')
        assert state_text.text == 'Thinking ...'
        wait_until_text_appear(browser, 'Your turn')

    # He makes the losing move by placing the fourth disc in new column
    click_column(browser, 3)

    # He waits for the computer to make a move
    wait_until_text_disappear(browser, 'Your turn')
    assert state_text.text == 'Thinking ...'

    # He sees "You lose, try again!" in the state text
    wait_until_text_disappear(browser, 'Thinking ...')
    assert 'You lose, try again!' in state_text.text
    
    # He clicks the first column again and confirms that the game is ended
    click_column(browser, 0)
    canvas = find_canvas(browser)
    web_element_regression(canvas, 'game_end_after_losing')