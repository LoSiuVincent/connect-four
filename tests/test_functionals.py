from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pytest


@pytest.fixture
def browser():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


def test_launch_website(browser):
    browser.get('http://localhost:8000')

    assert 'Connect 4' in browser.title


def test_canvas_exists(browser):
    # John goes to the website
    browser.get('http://localhost:8000')

    # He sees a canvas where he can play the game
    try:
        browser.find_element(By.TAG_NAME, 'canvas')
    except NoSuchElementException:
        pytest.fail('There is no canvas element')
