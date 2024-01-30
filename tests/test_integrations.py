from selenium.webdriver.common.by import By
import pytest
import time
import os
from pathlib import Path
import logging

from tests.visreg import web_element_image_regression


@pytest.mark.visual
def test_coins_show_up_when_the_game_drops_the_coins(browser, image_diff):
    canvas = browser.find_element(By.TAG_NAME, 'canvas')
    time.sleep(0.5)

    browser.execute_script('game.dropCoin(0);')
    time.sleep(1)

    web_element_image_regression(canvas, 'first_coin')
