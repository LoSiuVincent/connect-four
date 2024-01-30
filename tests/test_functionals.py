import time

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from tests.visreg import web_element_image_regression


def test_canvas_exists(browser):
    # He sees a canvas where he can play the game
    try:
        browser.find_element(By.TAG_NAME, "canvas")
    except NoSuchElementException:
        pytest.fail("There is no canvas element")


def test_layout(browser):
    browser.set_window_size(1600, 1000)

    # He sees a canvas center on the website
    canvas = browser.find_element(By.TAG_NAME, "canvas")
    canvas_center_x = canvas.location["x"] + canvas.size["width"] / 2
    canvas_center_y = canvas.location["y"] + canvas.size["height"] / 2
    assert canvas_center_x == 800
    assert abs(canvas_center_y - 500) < 100


def test_correct_canvas_size(browser):
    # John sees the canvas has 8 cells height and 7 cells width
    canvas = browser.find_element(By.TAG_NAME, "canvas")

    cell_length = browser.execute_script("return view.getCellLength();")
    assert 8 * cell_length == canvas.size["height"]
    assert 7 * cell_length == canvas.size["width"]


@pytest.mark.visual
def test_board_exists(browser):
    # John sees a board drawn on the page
    canvas = browser.find_element(By.TAG_NAME, "canvas")
    time.sleep(1)

    web_element_image_regression(canvas, "board")


@pytest.mark.visual
def test_drop_coins_to_board(browser):
    # John sees the canvas for the game
    canvas = browser.find_element(By.TAG_NAME, "canvas")
    assert canvas is not None

    def click_column(column_index):
        cell_width = browser.execute_script("return view.getCellLength();")

        click_x = column_index * cell_width + 0.5 * cell_width
        click_y = 10

        action = webdriver.common.action_chains.ActionChains(browser)
        action.move_to_element_with_offset(canvas, click_x, click_y)
        action.click()
        action.perform()

        time.sleep(1)

    # He clicks in the first column
    click_column(0)

    web_element_image_regression(canvas, "functional_first_coin")

    # He clicks another column
    click_column(3)

    web_element_image_regression(canvas, "functional_second_coin")

    # He tries to drop a coin in the first column again
    click_column(0)

    web_element_image_regression(canvas, "functional_third_coin")
