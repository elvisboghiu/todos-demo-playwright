"""Page Object Model for TodoMVC application."""

from playwright.sync_api import Page, Locator
from typing import List


class TodoPage:
    """Page object for TodoMVC UI interactions."""

    # UI Element Selectors
    INPUT_FIELD = "input.new-todo"
    TODO_ITEMS = "ul.todo-list li"
    TODO_ITEM_LABEL = "ul.todo-list li label"
    TODO_CHECKBOX = "ul.todo-list li input[type='checkbox']"
    DELETE_BUTTON = "button.destroy"
    ACTIVE_FILTER = "a[href='#/active']"
    COMPLETED_FILTER = "a[href='#/completed']"
    ALL_FILTER = "a[href='#/']"
    TODO_LIST = "ul.todo-list"

    def __init__(self, page: Page):
        """Initialize TodoPage with a Playwright page instance.
        
        Args:
            page: Playwright page instance
        """
        self.page = page
        self.url = "https://demo.playwright.dev/todomvc/#/"

    def navigate(self) -> None:
        """Navigate to the TodoMVC application."""
        self.page.goto(self.url)
        # Clear local storage to ensure clean state
        self.page.context.clear_cookies()
        self.page.evaluate("""
            () => {
                localStorage.clear();
                sessionStorage.clear();
            }
        """)
        # Reload the page to apply the cleared storage
        self.page.reload()

    def add_todo(self, text: str) -> None:
        """Add a new todo item.
        
        Args:
            text: The todo item text to add
        """
        self.page.fill(self.INPUT_FIELD, text)
        self.page.press(self.INPUT_FIELD, "Enter")

    def mark_todo_complete(self, index: int) -> None:
        """Mark a todo item as complete by clicking its checkbox.
        
        Args:
            index: The index of the todo item (0-based)
        """
        checkboxes = self.page.locator(self.TODO_CHECKBOX)
        checkboxes.nth(index).click()

    def delete_todo(self, index: int) -> None:
        """Delete a todo item.

        Args:
            index: The index of the todo item to delete (0-based)
        """
        # Use JavaScript click to bypass hover visibility requirement
        self.page.evaluate(
            f"document.querySelectorAll('{self.DELETE_BUTTON}')[{index}].click()"
        )

    def click_active_filter(self) -> None:
        """Click the Active filter button."""
        try:
            self.page.click(self.ACTIVE_FILTER, timeout=5000)
        except:
            # Filter button might not be visible if no todos exist
            pass

    def click_completed_filter(self) -> None:
        """Click the Completed filter button."""
        try:
            self.page.click(self.COMPLETED_FILTER, timeout=5000)
        except:
            # Filter button might not be visible if no todos exist
            pass

    def click_all_filter(self) -> None:
        """Click the All filter button."""
        try:
            self.page.click(self.ALL_FILTER, timeout=5000)
        except:
            # Filter button might not be visible if no todos exist
            pass

    def get_todo_items(self) -> List[str]:
        """Get all visible todo item texts.
        
        Returns:
            List of todo item text strings
        """
        # Try to wait for the todo list to be visible, but don't fail if it's not
        try:
            self.page.locator(self.TODO_LIST).wait_for(state="visible", timeout=2000)
        except:
            # If the list is not visible, it might be empty, so just continue
            pass
        
        labels = self.page.locator(self.TODO_ITEM_LABEL)
        count = labels.count()
        return [labels.nth(i).text_content() for i in range(count)]

    def get_active_todos(self) -> List[str]:
        """Get all active (incomplete) todo items.

        Returns:
            List of active todo item text strings
        """
        # Click the active filter
        self.click_active_filter()

        # Wait for the filter to apply
        self.page.wait_for_timeout(500)

        return self.get_todo_items()

    def get_completed_todos(self) -> List[str]:
        """Get all completed todo items.

        Returns:
            List of completed todo item text strings
        """
        # Click the completed filter
        self.click_completed_filter()

        # Wait for the filter to apply
        self.page.wait_for_timeout(500)

        return self.get_todo_items()

    def is_todo_completed(self, index: int) -> bool:
        """Check if a todo item is marked as completed.
        
        Args:
            index: The index of the todo item (0-based)
            
        Returns:
            True if the todo is completed, False otherwise
        """
        checkboxes = self.page.locator(self.TODO_CHECKBOX)
        return checkboxes.nth(index).is_checked()
