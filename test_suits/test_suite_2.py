# Testing the functionality
from playwright.sync_api import expect

TASK_1 = "Create Test Plan"
TASK_2 = "Cook dinner"


def test_adding_first_task(set_up_page):
    page = set_up_page
    page.get_by_role("textbox", name="New Task").fill(TASK_1)
    page.get_by_role("button", name="Add").click()
    page.wait_for_timeout(300)
    added_text = page.get_by_text(TASK_1)
    expect(added_text).to_be_visible()


def test_adding_second_task(set_up_page):
    page = set_up_page
    page.get_by_role("textbox", name="New Task").fill(TASK_2)
    page.get_by_role("button", name="Add").click()
    page.wait_for_timeout(300)
    added_text = page.get_by_text(TASK_2)
    expect(added_text).to_be_visible()


def test_completing_first_task(set_up_page):
    page = set_up_page
    page.locator("button.update-btn").first.click()
    completed_task = page.get_by_text(TASK_1, exact=True)
    page.wait_for_timeout(300)
    expect(completed_task).to_have_class("task-completed")


def test_completed_page_with_task(set_up_page):
    page = set_up_page
    page.get_by_role("link", name="Completed").click()
    page.wait_for_load_state(state="domcontentloaded")
    completed_task = page.get_by_text(TASK_1, exact=True)

    expect(completed_task).to_be_visible()
    expect(completed_task).to_have_class("task-completed")


def test_active_page_with_task(set_up_page):
    page = set_up_page
    page.get_by_role("link", name="Active").click()
    page.wait_for_load_state(state="domcontentloaded")
    active_task = page.get_by_text(TASK_2, exact=True)

    expect(active_task).to_be_visible()
    expect(active_task).to_have_class("task-active")


def test_removing_first_task(set_up_page):
    page = set_up_page
    page.get_by_role("link", name="All").click()
    completed_task = page.get_by_text(TASK_1, exact=True)
    page.locator("button.button-remove").nth(1).click()
    page.wait_for_load_state(state="domcontentloaded")

    expect(completed_task).to_be_hidden()