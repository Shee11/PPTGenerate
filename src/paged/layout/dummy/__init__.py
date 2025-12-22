"""Dummy layout implementation - reference implementation."""
from src.paged.layout.dummy.layout_engine import LayoutEngine
from src.paged.layout.dummy.theme import Theme
from src.paged.layout.dummy.style import Style
from src.paged.layout.dummy.validation import LayoutValidator, LayoutIssue, format_issues_for_llm

__all__ = [
    "LayoutEngine",
    "Theme",
    "Style",
    "LayoutValidator",
    "LayoutIssue",
    "format_issues_for_llm",
]
