"""Tests for todo deletion functionality."""

import pytest
from pages.todo_page import TodoPage
from utils.test_data import generate_english_texts


class TestTodoDeletion:
    """Test suite for todo deletion functionality."""

    def test_delete_todo(self, todo_page: TodoPage) -> None:
        """Verify item is removed from list.
        
        Requirements: 5.1
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)
        
        # Verify it was added
        todos = todo_page.get_todo_items()
        assert len(todos) == 1
        assert todos[0] == todo_text
        
        # Delete the todo
        todo_page.delete_todo(0)
        
        # Verify it was deleted
        todos_after = todo_page.get_todo_items()
        assert len(todos_after) == 0

    def test_deleted_todo_not_in_active_view(self, todo_page: TodoPage) -> None:
        """Verify absence in Active filter.
        
        Requirements: 5.2
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)
        
        # Delete the todo
        todo_page.delete_todo(0)
        
        # Switch to Active filter
        active_todos = todo_page.get_active_todos()
        
        # Verify the deleted todo is not in the Active view
        assert len(active_todos) == 0
        assert todo_text not in active_todos

    def test_deleted_todo_not_in_completed_view(self, todo_page: TodoPage) -> None:
        """Verify absence in Completed filter.
        
        Requirements: 5.3
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)
        
        # Mark it as complete
        todo_page.mark_todo_complete(0)
        
        # Delete the todo
        todo_page.delete_todo(0)
        
        # Switch to Completed filter
        completed_todos = todo_page.get_completed_todos()
        
        # Verify the deleted todo is not in the Completed view
        assert len(completed_todos) == 0
        assert todo_text not in completed_todos

    def test_delete_todo_from_multiple_items(self, todo_page: TodoPage) -> None:
        """Verify deletion works correctly with multiple items.
        
        Requirements: 5.1, 5.4
        """
        # Add multiple todos
        test_todos = generate_english_texts()[:3]
        for todo_text in test_todos:
            todo_page.add_todo(todo_text)
        
        # Verify all were added
        todos = todo_page.get_todo_items()
        assert len(todos) == 3
        
        # Delete the middle item (index 1)
        todo_page.delete_todo(1)
        
        # Verify the correct item was deleted
        todos_after = todo_page.get_todo_items()
        assert len(todos_after) == 2
        assert test_todos[0] in todos_after
        assert test_todos[1] not in todos_after
        assert test_todos[2] in todos_after


from hypothesis import given, strategies as st, settings, HealthCheck


class TestTodoDeletionProperties:
    """Property-based tests for todo deletion functionality."""

    @given(
        todo_text=st.text(min_size=1, max_size=50).filter(lambda x: x.strip() and not any(c in x for c in '\r\n\t'))
    )
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        deadline=None,
        max_examples=3
    )
    def test_property_deleted_items_disappear_from_all_views(
        self, todo_page: TodoPage, todo_text: str
    ) -> None:
        """Property test: Deleted items disappear from all views.
        
        **Feature: todomvc-playwright-tests, Property 6: Deleted Items Disappear from All Views**
        **Validates: Requirements 5.2, 5.3, 5.4**
        
        For any deleted todo item, that item SHALL NOT appear in the "Active" view, 
        "Completed" view, or main list view.
        """
        # Reload page to ensure clean state for each example
        todo_page.page.reload()
        
        # Add the todo
        todo_page.add_todo(todo_text)
        
        # Delete the item
        todo_page.delete_todo(0)
        
        # Verify it's not in the main list
        all_todos = todo_page.get_todo_items()
        assert todo_text not in all_todos
        
        # Verify it's not in the Active view
        active_todos = todo_page.get_active_todos()
        assert todo_text not in active_todos
        
        # Verify it's not in the Completed view
        completed_todos = todo_page.get_completed_todos()
        assert todo_text not in completed_todos
