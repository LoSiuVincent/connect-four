from selenium import webdriver
import pytest

@pytest.fixture
def browser():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()

def test_launch_website(browser):
    browser.get('http://localhost:8000')
    
    assert 'Connect 4' in browser.title