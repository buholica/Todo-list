import pytest
from playwright.sync_api import Playwright


@pytest.fixture(scope="session")
def set_up_context(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://todo-list-xjvc.onrender.com/")
    page.wait_for_load_state(state="networkidle")

    yield page

    browser.close()


@pytest.fixture(scope="session")
def set_up_page(set_up_context):
    return set_up_context