import time

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.conftest import BROWSER_WIDTH
from tests.visreg import web_element_regression


def test_canvas_exists(browser):
    # He sees a canvas where he can play the game
    try:
        browser.find_element(By.TAG_NAME, 'canvas')
    except NoSuchElementException:
        pytest.fail('There is no canvas element')


def test_layout(browser):
    # He sees a canvas center on the website
    canvas = browser.find_element(By.TAG_NAME, 'canvas')
    canvas_center_x = canvas.location['x'] + canvas.size['width'] / 2
    assert canvas_center_x == BROWSER_WIDTH / 2


def test_correct_canvas_size(browser):
    # John sees the canvas has 8 cells height and 7 cells width
    canvas = browser.find_element(By.TAG_NAME, 'canvas')

    cell_length = browser.execute_script('return view.getCellLength();')
    assert 8 * cell_length == canvas.size['height']
    assert 7 * cell_length == canvas.size['width']


@pytest.mark.visual
def test_board_exists(browser):
    # John sees a board drawn on the page
    canvas = browser.find_element(By.TAG_NAME, 'canvas')

    web_element_regression(canvas, 'board')


@pytest.mark.visual
def test_drop_coins_to_board(browser):
    # John sees the canvas for the game
    canvas = browser.find_element(By.TAG_NAME, 'canvas')
    assert canvas is not None

    def click_column(column_index):
        cell_width = browser.execute_script('return view.getCellLength();')

        click_x = column_index * cell_width + 0.5 * cell_width - canvas.size['width'] / 2
        click_y = 100 - canvas.size['height'] / 2

        action = webdriver.common.action_chains.ActionChains(browser)
        action.move_to_element_with_offset(canvas, click_x, click_y)
        action.click()
        action.perform()

        time.sleep(1)

    # He clicks in the first column
    click_column(0)
    web_element_regression(canvas, 'player_first_coin', wait_time_before_capture=1)

    # He waits for the computer move
    web_element_regression(canvas, 'computer_first_coin')

    # He clicks another column
    click_column(3)
    web_element_regression(canvas, 'player_second_coin', wait_time_before_capture=1)

    # He waits for the computer move again
    time.sleep(3)
    web_element_regression(canvas, 'computer_second_coin')

    # He tries to drop a coin in the first column again
    click_column(0)
    web_element_regression(canvas, 'player_third_coin', wait_time_before_capture=1)

    # He waits for the computer move again
    time.sleep(3)
    web_element_regression(canvas, 'computer_third_coin')
