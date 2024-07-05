# Test Suit 1: Checking if there are no tasks when a new user visits the page
from playwright.sync_api import expect
from datetime import datetime
import calendar
import pytest


def test_site_has_current_day(set_up_page):
    page = set_up_page
    main_title = page.get_by_role("heading")
    current_date = datetime.today()
    today = calendar.day_name[current_date.weekday()]
    expect(main_title).to_contain_text(f"Happy {today}")


def test_homepage(set_up_page):
    page = set_up_page
    paragraph = page.get_by_role("paragraph", name="Please, add a new task.")
    expect(paragraph).to_be_visible()


def test_active_tasks_page(set_up_page):
    page = set_up_page
    page.get_by_role("link", name="Active").click()
    paragraph = page.get_by_role("paragraph", name="There are no active tasks currently.")
    expect(paragraph).to_be_visible()


def test_completed_tasks_page(set_up_page):
    page = set_up_page
    page.get_by_role("link", name="Completed").click()
    paragraph = page.get_by_role("paragraph", name="There are no completed tasks currently.")
    expect(paragraph).to_be_visible()


def test_adding_new_empty_task(set_up_page):
    page = set_up_page
    page.get_by_role("button", name="Add").click()
    flash_message = page.get_by_role("paragraph", name="Please, type a new task.")
    page.wait_for_load_state(state="networkidle")
    expect(flash_message).to_be_visible()

    paragraph = page.get_by_role("paragraph", name="Please, add a new task.")
    expect(paragraph).to_be_visible()

    todo_item = page.get_by_locator("div.todo-item")
    expect(todo_item).to_be_hidden()


@pytest.mark.skip("To reduce the usage of API")
def test_adding_new_task(set_up_page):
    page = set_up_page
    text = "Create Test Plan"
    page.get_by_role("textbox", name="New Task").fill(text)
    page.get_by_role("button", name="Add").click()
    page.wait_for_selector("div.todo-item")
    added_text = page.get_by_text(text)
    expect(added_text).to_be_visible()
