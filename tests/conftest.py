import pytest
from selenium import webdriver

BROWSER_WIDTH = 1000
BROWSER_HEIGHT = 1200

@pytest.fixture
def browser():
    driver = webdriver.Firefox()
    driver.get("http://localhost:8000")
    driver.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)
    yield driver
    driver.quit()
