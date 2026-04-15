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


