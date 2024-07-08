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


def test_homepage_empty(set_up_page):
    page = set_up_page
    paragraph = page.locator("p.message")
    message = "Please, add a new task."
    expect(paragraph).to_contain_text(message)


def test_active_page_empty(set_up_page):
    page = set_up_page
    page.get_by_role("link", name="Active").click()
    paragraph = page.locator("p.message")
    message = "There are no active tasks currently."
    expect(paragraph).to_contain_text(message)


def test_completed_page_empty(set_up_page):
    page = set_up_page
    page.get_by_role("link", name="Completed").click()
    paragraph = page.locator("p.message")
    message = "There are no completed tasks currently."
    expect(paragraph).to_contain_text(message)


def test_adding_new_empty_task(set_up_page):
    page = set_up_page
    page.get_by_role("button", name="Add").click()
    page.wait_for_load_state(state="networkidle")
    flash_paragraph = page.locator("p.flash")
    flash_message = "Please, type a new task."
    expect(flash_paragraph).to_contain_text(flash_message)

    paragraph = page.locator("p.message")
    message = "Please, add a new task."
    expect(paragraph).to_contain_text(message)

    todo_item = page.locator("div.todo-item")
    expect(todo_item).to_be_hidden()