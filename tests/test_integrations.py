import time

import pytest
from selenium.webdriver.common.by import By

from tests.visreg import web_element_regression


@pytest.mark.visual
def test_player_coins_show_up_when_the_game_drops_the_coins(browser):
    canvas = browser.find_element(By.TAG_NAME, "canvas")
    time.sleep(1)

    browser.execute_script("game.dropCoin(0);")
    web_element_regression(canvas, "player_coin")


@pytest.mark.visual
def test_computer_coins_show_up_when_the_game_drops_the_coins(browser):
    canvas = browser.find_element(By.TAG_NAME, "canvas")
    time.sleep(1)

    browser.execute_script("game.dropCoin(0, 'computer');")
    web_element_regression(canvas, "computer_coin")
