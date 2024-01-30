from selenium.webdriver.common.by import By
import pytest
import time
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format=r'[%(levelname)s] %(message)s')

BASELINE_IMG_DIR = Path(__file__).resolve().parent / 'baseline'
CURRENT_IMG_DIR = Path(__file__).resolve().parent / 'current'


@pytest.mark.visual
def test_coins_show_up_when_the_game_drops_the_coins(browser, image_diff):
    canvas = browser.find_element(By.TAG_NAME, 'canvas')
    time.sleep(0.5)

    browser.execute_script('game.dropCoin(0);')
    time.sleep(1)

    baseline_image_path = str(BASELINE_IMG_DIR / 'first_coin.png')
    current_image_path = str(CURRENT_IMG_DIR / 'first_coin.png')
    if int(os.environ.get('UPDATE_BASELINE', 0)) == 1:
        canvas.screenshot(baseline_image_path)
        logging.info(f'Captured image to {baseline_image_path}')
    else:
        canvas.screenshot(current_image_path)
        assert image_diff(baseline_image_path, current_image_path)
