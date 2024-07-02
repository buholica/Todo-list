import pytest
from playwright.sync_api import Playwright


@pytest.fixture()
def set_up(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://todo-list-xjvc.onrender.com/")

    yield page

    context.close()
    browser.close()