from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pytest


@pytest.fixture
def browser():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


def test_canvas_exists(browser):
    # John goes to the website
    browser.get('http://localhost:8000')

    # He sees a canvas where he can play the game
    try:
        browser.find_element(By.TAG_NAME, 'canvas')
    except NoSuchElementException:
        pytest.fail('There is no canvas element')


def test_layout(browser):
    # John goes to the website
    browser.get('http://localhost:8000')
    browser.set_window_size(1600, 1000)

    # He sees a canvas center on the website
    canvas = browser.find_element(By.TAG_NAME, 'canvas')
    canvas_center_x = canvas.location['x'] + canvas.size['width'] / 2
    canvas_center_y = canvas.location['y'] + canvas.size['height'] / 2
    assert canvas_center_x == 800
    assert abs(canvas_center_y - 500) < 100


def test_board_exists(browser):
    # John goes to the webiste
    browser.get('http://localhost:8000')

    # John sees the board shows up with 6 cells height and 7 cells width
    canvas = browser.find_element(By.TAG_NAME, 'canvas')

    cell_length = browser.execute_script('return game.getCellLength();')
    assert 8 * cell_length == canvas.size['height']
    assert 7 * cell_length == canvas.size['width']


def test_drop_coins_to_board(browser):
    # John goes to the website
    browser.get('http://localhost:8000')

    # John sees the canvas for the game
    canvas = browser.find_element(By.TAG_NAME, 'canvas')
    assert canvas is not None

    def click_column(column_index):
        cell_width = browser.execute_script('return game.getCellLength();')

        click_x = column_index * cell_width + 0.5 * cell_width
        click_y = 10

        action = webdriver.common.action_chains.ActionChains(browser)
        action.move_to_element_with_offset(canvas, click_x, click_y)
        action.click()
        action.perform()

        time.sleep(1)

    # He clicks on the first column
    click_column(0)

    first_column_bottom_cell_state = browser.execute_script("return game.getCellState(0, 0);")
    assert first_column_bottom_cell_state == 'player'

    # He clicks another column
    click_column(3)

    # Check the game state to ensure a coin has been added to the fourth column
    fourth_column_bottom_cell_state = browser.execute_script("return game.getCellState(3, 0);")
    assert fourth_column_bottom_cell_state == 'player'

    # He tries to drop a coin at the first column again
    click_column(0)

    # Check the game state to ensure another coin has been stacked in the first column
    first_column_second_last_bottom_cell_state = browser.execute_script(
        "return game.getCellState(0, 1);"
    )
    assert first_column_second_last_bottom_cell_state == 'player'
