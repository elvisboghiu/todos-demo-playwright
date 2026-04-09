"""Test data generators for TodoMVC tests."""

from typing import List


def generate_english_text(text: str = None) -> str:
    """Generate or return English text for todo items.
    
    Args:
        text: Optional specific text to return. If None, returns a default.
        
    Returns:
        English text string
    """
    if text is not None:
        return text
    return "Buy groceries"


def generate_english_texts() -> List[str]:
    """Generate a list of English text examples.
    
    Returns:
        List of English text strings
    """
    return [
        "Buy groceries",
        "Write report",
        "Call dentist",
        "Complete project",
        "Review code",
    ]


def generate_non_english_text(language: str = "chinese") -> str:
    """Generate non-English text for todo items.
    
    Args:
        language: Type of non-English text ('chinese', 'arabic', 'emoji')
        
    Returns:
        Non-English text string
    """
    texts = {
        "chinese": "买菜",
        "arabic": "اشتري الحليب",
        "emoji": "🎯 Complete project",
    }
    return texts.get(language, texts["chinese"])


def generate_non_english_texts() -> List[str]:
    """Generate a list of non-English text examples.
    
    Returns:
        List of non-English text strings
    """
    return [
        "买菜",  # Chinese: Buy vegetables
        "اشتري الحليب",  # Arabic: Buy milk
        "🎯 Complete project",  # Emoji
        "日本語テスト",  # Japanese
        "🚀 Launch feature",  # Emoji with text
    ]


def generate_numeric_text(text: str = None) -> str:
    """Generate or return numeric text for todo items.
    
    Args:
        text: Optional specific text to return. If None, returns a default.
        
    Returns:
        Numeric text string
    """
    if text is not None:
        return text
    return "Task 123"


def generate_numeric_texts() -> List[str]:
    """Generate a list of numeric text examples.
    
    Returns:
        List of numeric text strings
    """
    return [
        "Task 123",
        "Buy 5 apples",
        "2024-01-15",
        "Meeting at 3pm",
        "Buy 2 kg flour",
    ]


def generate_mixed_text(text: str = None) -> str:
    """Generate or return mixed text (text with numbers and special chars).
    
    Args:
        text: Optional specific text to return. If None, returns a default.
        
    Returns:
        Mixed text string
    """
    if text is not None:
        return text
    return "Meeting at 3pm"


def generate_mixed_texts() -> List[str]:
    """Generate a list of mixed text examples.
    
    Returns:
        List of mixed text strings
    """
    return [
        "Meeting at 3pm",
        "Buy 2 kg flour",
        "Task #42 - Review",
        "Call 555-1234",
        "Email: test@example.com",
    ]
