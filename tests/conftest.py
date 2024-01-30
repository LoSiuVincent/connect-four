import pytest
from selenium import webdriver


@pytest.fixture
def browser():
    driver = webdriver.Firefox()
    driver.get("http://localhost:8000")
    yield driver
    driver.quit()
