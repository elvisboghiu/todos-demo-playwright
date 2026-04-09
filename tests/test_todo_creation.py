"""Tests for todo creation functionality."""

import pytest
from pages.todo_page import TodoPage
from utils.test_data import generate_english_texts


class TestTodoCreation:
    """Test suite for todo creation functionality."""

    def test_add_english_todo(self, todo_page: TodoPage) -> None:
        """Verify English text todo creation.
        
        Requirements: 1.1, 1.2, 1.4
        """
        # Add a single English todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)
        
        # Verify the todo appears in the list
        todos = todo_page.get_todo_items()
        assert len(todos) == 1
        assert todos[0] == todo_text

    def test_add_multiple_english_todos(self, todo_page: TodoPage) -> None:
        """Verify multiple items display correctly.
        
        Requirements: 1.1, 1.2, 1.4
        """
        # Add multiple English todos
        test_todos = generate_english_texts()[:3]
        for todo_text in test_todos:
            todo_page.add_todo(todo_text)
        
        # Verify all todos appear in the list
        todos = todo_page.get_todo_items()
        assert len(todos) == 3
        for i, expected_text in enumerate(test_todos):
            assert todos[i] == expected_text

    def test_input_field_clears_after_addition(self, todo_page: TodoPage) -> None:
        """Verify input clears after adding a todo.
        
        Requirements: 1.3
        """
        # Add a todo
        todo_text = "Buy groceries"
        todo_page.add_todo(todo_text)
        
        # Verify the input field is empty
        input_value = todo_page.page.input_value(todo_page.INPUT_FIELD)
        assert input_value == ""



from hypothesis import given, strategies as st, settings, HealthCheck


class TestTodoCreationProperties:
    """Property-based tests for todo creation functionality."""

    @given(todo_text=st.text(min_size=1, max_size=100).filter(lambda x: x.strip() and not any(c in x for c in '\r\n\t')))
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        deadline=None,
        max_examples=10
    )
    def test_property_todo_creation_adds_item_to_list(
        self, todo_page: TodoPage, todo_text: str
    ) -> None:
        """Property test: Adding a todo item adds it to the list.
        
        **Feature: todomvc-playwright-tests, Property 1: Todo Creation Adds Item to List**
        **Validates: Requirements 1.1, 1.2, 2.1, 3.1**
        
        For any valid todo text (non-whitespace), adding a todo item SHALL result 
        in that item appearing in the todo list.
        """
        # Navigate to fresh page to ensure clean state for each example
        todo_page.navigate()
        
        # Add the todo
        todo_page.add_todo(todo_text)
        
        # Verify the todo was added
        todos_after = todo_page.get_todo_items()
        assert len(todos_after) == 1
        # Compare stripped versions since TodoMVC may normalize whitespace
        assert any(todo_text.strip() == todo.strip() for todo in todos_after)
