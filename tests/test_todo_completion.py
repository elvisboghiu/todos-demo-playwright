"""Tests for todo completion functionality."""

import pytest
from pages.todo_page import TodoPage
from utils.test_data import generate_english_texts


class TestTodoCompletion:
    """Test suite for todo completion functionality."""

    def test_mark_todo_complete(self, todo_page: TodoPage) -> None:
        """Verify checkbox marks item complete.
        
        Requirements: 4.1
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)
        
        # Mark it as complete
        todo_page.mark_todo_complete(0)
        
        # Verify the checkbox is checked
        assert todo_page.is_todo_completed(0) is True

    def test_completed_item_appears_in_completed_view(self, todo_page: TodoPage) -> None:
        """Verify item in Completed filter.
        
        Requirements: 4.2
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)
        
        # Mark it as complete
        todo_page.mark_todo_complete(0)
        
        # Switch to Completed filter
        completed_todos = todo_page.get_completed_todos()
        
        # Verify the todo appears in the Completed view
        assert len(completed_todos) == 1
        assert completed_todos[0] == todo_text

    def test_completed_todo_has_visual_styling(self, todo_page: TodoPage) -> None:
        """Verify visual completion indicator.

        Requirements: 4.3, 4.4
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)

        # Get the todo item element before completion
        todo_items = todo_page.page.locator(todo_page.TODO_ITEMS)
        todo_item = todo_items.nth(0)

        # Mark it as complete
        todo_page.mark_todo_complete(0)

        # Verify the todo item has the 'completed' class
        class_list = todo_item.get_attribute("class")
        assert "completed" in class_list

    def test_completed_item_has_visual_styling_in_completed_filter(self, todo_page: TodoPage) -> None:
        """Verify completed item shows visual styling in Completed filter view.

        Requirements: 4.4
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)

        # Mark it as complete
        todo_page.mark_todo_complete(0)

        # Verify the checkbox is checked
        assert todo_page.is_todo_completed(0) is True

        # Switch to Completed filter
        todo_page.click_completed_filter()

        # Wait for filter to apply
        try:
            todo_page.page.locator(todo_page.TODO_LIST).wait_for(state="visible", timeout=2000)
        except:
            pass

        # Get the todo item element in the completed view
        todo_items = todo_page.page.locator(todo_page.TODO_ITEMS)
        assert todo_items.count() == 1, "Should have exactly one item in Completed filter"

        todo_item = todo_items.nth(0)

        # Verify the todo item has the 'completed' class in Completed filter view
        class_list = todo_item.get_attribute("class")
        assert "completed" in class_list, f"Completed item should have 'completed' class, got: {class_list}"


from hypothesis import given, strategies as st, settings, HealthCheck


class TestTodoCompletionProperties:
    """Property-based tests for todo completion functionality."""

    @given(todo_text=st.text(min_size=1, max_size=50).filter(lambda x: x.strip() and '\n' not in x and '\r' not in x and '\t' not in x))
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        deadline=None,
        max_examples=10
    )
    def test_property_completed_items_appear_in_completed_view(
        self, todo_page: TodoPage, todo_text: str
    ) -> None:
        """Property test: Completed items appear in Completed view and not in Active view.
        
        **Feature: todomvc-playwright-tests, Property 3: Completed Items Appear in Completed View**
        **Validates: Requirements 4.2, 7.1, 7.3**
        
        For any todo item that is marked as completed, that item SHALL appear in the 
        "Completed" filter view and SHALL NOT appear in the "Active" filter view.
        """
        # Navigate to ensure clean state
        todo_page.navigate()
        todo_page.page.wait_for_timeout(500)
        
        # Add the todo
        todo_page.add_todo(todo_text)
        todo_page.page.wait_for_timeout(500)
        
        # Mark it as complete
        todo_page.mark_todo_complete(0)
        todo_page.page.wait_for_timeout(500)

        # Verify the checkbox is actually checked
        assert todo_page.is_todo_completed(0) is True, "Checkbox should be checked after marking todo complete"
        
        # Verify the todo appears in the Completed view
        completed_todos = todo_page.get_completed_todos()
        assert todo_text in completed_todos, f"Todo '{todo_text}' should appear in Completed view"
        
        # Verify the todo does NOT appear in the Active view
        active_todos = todo_page.get_active_todos()
        assert todo_text not in active_todos, f"Todo '{todo_text}' should NOT appear in Active view but found it there"
