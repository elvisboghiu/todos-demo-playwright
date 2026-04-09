"""Pytest configuration and fixtures for TodoMVC tests."""

import pytest
from playwright.sync_api import sync_playwright, Browser, Page
from pages.todo_page import TodoPage


@pytest.fixture(scope="session")
def browser() -> Browser:
    """Provide a Playwright browser instance for the test session.
    
    Yields:
        Browser: Playwright browser instance
    """
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch()
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture
def page(browser: Browser) -> Page:
    """Provide a fresh Playwright page instance for each test.
    
    Args:
        browser: Browser fixture
        
    Yields:
        Page: Playwright page instance
    """
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture
def todo_page(page: Page) -> TodoPage:
    """Provide a TodoPage object instance for each test.
    
    Args:
        page: Page fixture
        
    Yields:
        TodoPage: TodoPage object initialized with the page
    """
    todo_page = TodoPage(page)
    todo_page.navigate()
    yield todo_page


@pytest.fixture
def cleanup(todo_page: TodoPage) -> None:
    """Clean up todos after each test by clearing the input field.
    
    Args:
        todo_page: TodoPage fixture
        
    Yields:
        None
    """
    yield
    # Clear any remaining todos by refreshing the page
    todo_page.page.reload()
