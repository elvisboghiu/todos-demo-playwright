"""Tests for numeric text support in todo items."""

import pytest
from pages.todo_page import TodoPage
from utils.test_data import generate_numeric_texts, generate_mixed_texts


class TestNumericText:
    """Test suite for numeric text support."""

    def test_add_numeric_todo(self, todo_page: TodoPage) -> None:
        """Verify numbers in todo text.
        
        Requirements: 3.1, 3.2
        """
        # Add a numeric text todo
        todo_text = "Task 123"
        todo_page.add_todo(todo_text)
        
        # Verify the todo appears with correct numbers
        todos = todo_page.get_todo_items()
        assert len(todos) == 1
        assert todos[0] == todo_text

    def test_add_mixed_text_and_numbers_todo(self, todo_page: TodoPage) -> None:
        """Verify mixed content.
        
        Requirements: 3.1, 3.2, 3.3
        """
        # Add mixed text and numbers todos
        mixed_todos = generate_mixed_texts()[:3]
        for todo_text in mixed_todos:
            todo_page.add_todo(todo_text)
        
        # Verify all todos appear with correct mixed content
        todos = todo_page.get_todo_items()
        assert len(todos) == 3
        for i, expected_text in enumerate(mixed_todos):
            assert todos[i] == expected_text


from hypothesis import given, strategies as st, settings, HealthCheck


class TestNumericTextProperties:
    """Property-based tests for numeric text support."""

    @given(
        todo_text=st.one_of(
            st.text(
                alphabet=st.characters(
                    blacklist_categories=('Cc', 'Cs'),  # Exclude control chars and surrogates
                    blacklist_characters='\r\n\t'
                ),
                min_size=1,
                max_size=100
            ).filter(lambda x: x.strip() and any(c.isdigit() for c in x)),
            st.just("Task 123"),
            st.just("Buy 5 apples"),
            st.just("2024-01-15"),
            st.just("Meeting at 3pm"),
            st.just("Buy 2 kg flour"),
        )
    )
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        deadline=None,
        max_examples=100
    )
    def test_property_input_field_clears_after_addition(
        self, todo_page: TodoPage, todo_text: str
    ) -> None:
        """Property test: Input field clears after adding a todo.
        
        **Feature: todomvc-playwright-tests, Property 3: Input Field Clears After Addition**
        **Validates: Requirements 1.3**
        
        For any todo item that is successfully added, the input field SHALL be 
        empty after the addition.
        """
        # Clear localStorage and reload page for each example
        todo_page.page.evaluate("localStorage.clear()")
        todo_page.page.reload()
        
        # Add the todo
        todo_page.add_todo(todo_text)
        
        # Verify the input field is empty after addition
        input_value = todo_page.page.input_value(todo_page.INPUT_FIELD)
        assert input_value == "", f"Input field should be empty but contains: '{input_value}'"
