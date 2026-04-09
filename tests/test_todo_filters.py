"""Tests for todo filter functionality."""

import pytest
from pages.todo_page import TodoPage
from utils.test_data import generate_english_texts


class TestActiveFilter:
    """Test suite for Active filter functionality."""

    def test_active_filter_shows_only_incomplete(self, todo_page: TodoPage) -> None:
        """Verify Active filter displays only incomplete items.
        
        Requirements: 6.1
        """
        # Add multiple todos
        test_todos = generate_english_texts()[:3]
        for todo_text in test_todos:
            todo_page.add_todo(todo_text)
        
        # Mark the first and third items as complete
        todo_page.mark_todo_complete(0)
        todo_page.mark_todo_complete(2)
        
        # Switch to Active filter
        active_todos = todo_page.get_active_todos()
        
        # Verify only the incomplete item is shown
        assert len(active_todos) == 1
        assert active_todos[0] == test_todos[1]

    def test_active_filter_hides_completed(self, todo_page: TodoPage) -> None:
        """Verify completed items hidden in Active view.
        
        Requirements: 6.2
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)
        
        # Mark it as complete
        todo_page.mark_todo_complete(0)
        
        # Switch to Active filter
        active_todos = todo_page.get_active_todos()
        
        # Verify the completed item is not shown
        assert len(active_todos) == 0
        assert todo_text not in active_todos

    def test_new_incomplete_item_appears_in_active(self, todo_page: TodoPage) -> None:
        """Verify new items in Active view.
        
        Requirements: 6.3
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)
        
        # Switch to Active filter
        active_todos = todo_page.get_active_todos()
        
        # Verify the new item appears in Active view
        assert len(active_todos) == 1
        assert active_todos[0] == todo_text

    def test_completed_item_removed_from_active(self, todo_page: TodoPage) -> None:
        """Verify completed items removed from Active.
        
        Requirements: 6.4
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)
        
        # Verify it's in Active view
        active_todos_before = todo_page.get_active_todos()
        assert len(active_todos_before) == 1
        assert active_todos_before[0] == todo_text
        
        # Mark it as complete
        todo_page.mark_todo_complete(0)
        
        # Switch to Active filter
        active_todos_after = todo_page.get_active_todos()
        
        # Verify the item is no longer in Active view
        assert len(active_todos_after) == 0
        assert todo_text not in active_todos_after


class TestCompletedFilter:
    """Test suite for Completed filter functionality."""

    def test_completed_filter_shows_only_completed(self, todo_page: TodoPage) -> None:
        """Verify Completed filter displays only completed items.
        
        Requirements: 7.1
        """
        # Add multiple todos
        test_todos = generate_english_texts()[:3]
        for todo_text in test_todos:
            todo_page.add_todo(todo_text)
        
        # Mark the first and third items as complete
        todo_page.mark_todo_complete(0)
        todo_page.mark_todo_complete(2)
        
        # Switch to Completed filter
        completed_todos = todo_page.get_completed_todos()
        
        # Verify only the completed items are shown
        assert len(completed_todos) == 2
        assert test_todos[0] in completed_todos
        assert test_todos[2] in completed_todos

    def test_completed_filter_hides_active(self, todo_page: TodoPage) -> None:
        """Verify active items hidden in Completed view.
        
        Requirements: 7.2
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)
        
        # Switch to Completed filter
        completed_todos = todo_page.get_completed_todos()
        
        # Verify the active item is not shown
        assert len(completed_todos) == 0
        assert todo_text not in completed_todos

    def test_completed_item_appears_in_completed_view(self, todo_page: TodoPage) -> None:
        """Verify completed items in Completed view.
        
        Requirements: 7.3
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)
        
        # Mark it as complete
        todo_page.mark_todo_complete(0)
        
        # Switch to Completed filter
        completed_todos = todo_page.get_completed_todos()
        
        # Verify the completed item appears in Completed view
        assert len(completed_todos) == 1
        assert completed_todos[0] == todo_text

    def test_deleted_completed_item_removed_from_view(self, todo_page: TodoPage) -> None:
        """Verify deleted items removed from Completed.
        
        Requirements: 7.4
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)
        
        # Mark it as complete
        todo_page.mark_todo_complete(0)
        
        # Verify it's in Completed view
        completed_todos_before = todo_page.get_completed_todos()
        assert len(completed_todos_before) == 1
        assert completed_todos_before[0] == todo_text
        
        # Delete the item
        todo_page.delete_todo(0)
        
        # Switch to Completed filter
        completed_todos_after = todo_page.get_completed_todos()
        
        # Verify the item is no longer in Completed view
        assert len(completed_todos_after) == 0
        assert todo_text not in completed_todos_after


from hypothesis import given, strategies as st, settings, HealthCheck


class TestFilterProperties:
    """Property-based tests for filter functionality."""

    @given(
        todo_texts=st.lists(
            st.text(min_size=1, max_size=30).filter(lambda x: x.strip() and not any(c in x for c in '\r\n\t')),
            min_size=1,
            max_size=3,
            unique=True
        ),
        completed_indices=st.lists(st.integers(min_value=0, max_value=2), max_size=3, unique=True)
    )
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        deadline=None,
        max_examples=5
    )
    def test_property_active_filter_shows_only_incomplete(
        self, todo_page: TodoPage, todo_texts: list, completed_indices: list
    ) -> None:
        """Property test: Active filter shows only incomplete items.
        
        **Feature: todomvc-playwright-tests, Property 4: Active Filter Shows Only Incomplete Items**
        **Validates: Requirements 6.1, 6.2**
        
        For any set of todo items with mixed completion states, the "Active" filter 
        SHALL display only items that are not completed.
        """
        # Navigate to fresh page to ensure clean state for each example
        todo_page.navigate()
        
        # Add all todos
        for todo_text in todo_texts:
            todo_page.add_todo(todo_text)
        
        # Mark specified items as complete (filter to valid indices)
        valid_completed_indices = [i for i in completed_indices if i < len(todo_texts)]
        for idx in valid_completed_indices:
            todo_page.mark_todo_complete(idx)
        
        # Get active todos
        active_todos = todo_page.get_active_todos()
        
        # Verify only incomplete items are shown
        expected_active = [
            todo_texts[i] for i in range(len(todo_texts)) 
            if i not in valid_completed_indices
        ]
        
        assert len(active_todos) == len(expected_active)
        # Compare stripped versions since TodoMVC may normalize whitespace
        for expected_todo in expected_active:
            assert any(expected_todo.strip() == active_todo.strip() for active_todo in active_todos)

    @given(
        todo_texts=st.lists(
            st.text(min_size=1, max_size=30).filter(lambda x: x.strip() and not any(c in x for c in '\r\n\t')),
            min_size=1,
            max_size=3,
            unique=True
        ),
        completed_indices=st.lists(st.integers(min_value=0, max_value=2), max_size=3, unique=True)
    )
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        deadline=None,
        max_examples=5
    )
    def test_property_completed_filter_shows_only_completed(
        self, todo_page: TodoPage, todo_texts: list, completed_indices: list
    ) -> None:
        """Property test: Completed filter shows only completed items.
        
        **Feature: todomvc-playwright-tests, Property 5: Completed Filter Shows Only Completed Items**
        **Validates: Requirements 7.1, 7.2**
        
        For any set of todo items with mixed completion states, the "Completed" filter 
        SHALL display only items that are marked as completed.
        """
        # Navigate to fresh page to ensure clean state for each example
        todo_page.navigate()
        
        # Add all todos
        for todo_text in todo_texts:
            todo_page.add_todo(todo_text)
        
        # Mark specified items as complete (filter to valid indices)
        valid_completed_indices = [i for i in completed_indices if i < len(todo_texts)]
        for idx in valid_completed_indices:
            todo_page.mark_todo_complete(idx)
        
        # Get completed todos
        completed_todos = todo_page.get_completed_todos()
        
        # Verify only completed items are shown
        expected_completed = [
            todo_texts[i] for i in valid_completed_indices
        ]
        
        assert len(completed_todos) == len(expected_completed)
        # Compare stripped versions since TodoMVC may normalize whitespace
        for expected_todo in expected_completed:
            assert any(expected_todo.strip() == completed_todo.strip() for completed_todo in completed_todos)
