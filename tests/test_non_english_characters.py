"""Tests for non-English character support in todo items."""

import pytest
from pages.todo_page import TodoPage
from utils.test_data import generate_non_english_texts


class TestNonEnglishCharacters:
    """Test suite for non-English character support."""

    def test_add_chinese_characters_todo(self, todo_page: TodoPage) -> None:
        """Verify Chinese text preservation.
        
        Requirements: 2.1, 2.2
        """
        # Add a Chinese text todo
        todo_text = "买菜"  # Chinese: Buy vegetables
        todo_page.add_todo(todo_text)
        
        # Verify the todo appears with correct Chinese characters
        todos = todo_page.get_todo_items()
        assert len(todos) == 1
        assert todos[0] == todo_text

    def test_add_arabic_characters_todo(self, todo_page: TodoPage) -> None:
        """Verify Arabic text preservation.
        
        Requirements: 2.1, 2.2
        """
        # Add an Arabic text todo
        todo_text = "اشتري الحليب"  # Arabic: Buy milk
        todo_page.add_todo(todo_text)
        
        # Verify the todo appears with correct Arabic characters
        todos = todo_page.get_todo_items()
        assert len(todos) == 1
        assert todos[0] == todo_text

    def test_add_emoji_todo(self, todo_page: TodoPage) -> None:
        """Verify emoji preservation.
        
        Requirements: 2.1, 2.2
        """
        # Add an emoji todo
        todo_text = "🎯 Complete project"
        todo_page.add_todo(todo_text)
        
        # Verify the todo appears with correct emoji
        todos = todo_page.get_todo_items()
        assert len(todos) == 1
        assert todos[0] == todo_text


    def test_non_english_characters_preserved_in_views(self, todo_page: TodoPage) -> None:
        """Verify characters in all views.
        
        Requirements: 2.3
        """
        # Add non-English todos
        chinese_text = "买菜"
        arabic_text = "اشتري الحليب"
        emoji_text = "🎯 Complete project"
        
        todo_page.add_todo(chinese_text)
        todo_page.add_todo(arabic_text)
        todo_page.add_todo(emoji_text)
        
        # Verify all items appear in All view
        all_todos = todo_page.get_todo_items()
        assert len(all_todos) == 3
        assert chinese_text in all_todos
        assert arabic_text in all_todos
        assert emoji_text in all_todos
        
        # Mark first item as complete
        todo_page.mark_todo_complete(0)
        
        # Verify character preservation in Active view (should show 2 items)
        todo_page.click_active_filter()
        active_todos = todo_page.get_todo_items()
        assert len(active_todos) == 2
        assert arabic_text in active_todos
        assert emoji_text in active_todos
        assert chinese_text not in active_todos
        
        # Verify character preservation in Completed view (should show 1 item)
        todo_page.click_completed_filter()
        completed_todos = todo_page.get_todo_items()
        assert len(completed_todos) == 1
        assert chinese_text in completed_todos
        
        # Return to All view and verify all characters still preserved
        todo_page.click_all_filter()
        all_todos_final = todo_page.get_todo_items()
        assert len(all_todos_final) == 3
        assert chinese_text in all_todos_final
        assert arabic_text in all_todos_final
        assert emoji_text in all_todos_final



from hypothesis import given, strategies as st, settings, HealthCheck


class TestNonEnglishCharactersProperties:
    """Property-based tests for non-English character support."""

    @given(
        todo_text=st.one_of(
            st.text(
                alphabet=st.characters(
                    blacklist_categories=('Cc', 'Cs', 'Zs'),  # Exclude control chars, surrogates, and space separators
                    blacklist_characters='\r\n\t '
                ),
                min_size=1,
                max_size=100
            ).filter(lambda x: x.strip()),
            st.just("买菜"),
            st.just("اشتري الحليب"),
            st.just("🎯 Complete project"),
            st.just("日本語テスト"),
            st.just("🚀 Launch feature"),
        )
    )
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        deadline=None,
        max_examples=100
    )
    def test_property_character_preservation_in_display(
        self, todo_page: TodoPage, todo_text: str
    ) -> None:
        """Property test: Characters are preserved exactly as entered.
        
        **Feature: todomvc-playwright-tests, Property 7: Character Preservation in Display**
        **Validates: Requirements 2.2, 2.3, 3.2**
        
        For any todo item created with non-English characters or special characters,
        those characters SHALL be displayed exactly as entered without corruption 
        or modification.
        """
        # Clear localStorage and reload page for each example
        todo_page.page.evaluate("localStorage.clear()")
        todo_page.page.reload()
        
        # Add the todo with special characters
        todo_page.add_todo(todo_text)
        
        # Verify the todo appears with exact character preservation
        todos = todo_page.get_todo_items()
        assert len(todos) == 1
        assert todos[0] == todo_text, f"Expected '{todo_text}' but got '{todos[0]}'"
        
        # Mark as complete and verify characters preserved in Completed view
        todo_page.mark_todo_complete(0)
        completed_todos = todo_page.get_completed_todos()
        assert len(completed_todos) == 1
        assert completed_todos[0] == todo_text, f"Character corruption in Completed view: expected '{todo_text}' but got '{completed_todos[0]}'"
        
        # Return to All view and verify characters still preserved
        todo_page.click_all_filter()
        all_todos = todo_page.get_todo_items()
        assert len(all_todos) == 1
        assert all_todos[0] == todo_text, f"Character corruption in All view: expected '{todo_text}' but got '{all_todos[0]}'"
