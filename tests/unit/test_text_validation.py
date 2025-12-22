"""Tests for text validation utilities."""
import pytest

from src.utils.text_validation import (
    validate_text_complexity,
    sanitize_widget_text,
    get_text_complexity_warning,
)


class TestValidateTextComplexity:
    """Test validate_text_complexity function."""
    
    def test_valid_plain_text(self):
        """Plain text should pass validation."""
        is_valid, errors = validate_text_complexity("Hello World")
        assert is_valid
        assert len(errors) == 0
    
    def test_valid_inline_bold(self):
        """Inline bold markdown should pass validation."""
        is_valid, errors = validate_text_complexity("Scale to **1M requests/sec**")
        assert is_valid
        assert len(errors) == 0
    
    def test_valid_inline_italic(self):
        """Inline italic markdown should pass validation."""
        is_valid, errors = validate_text_complexity("*Lessons from the journey*")
        assert is_valid
        assert len(errors) == 0
    
    def test_valid_inline_code(self):
        """Inline code should pass validation."""
        is_valid, errors = validate_text_complexity("Use `docker run` command")
        assert is_valid
        assert len(errors) == 0
    
    def test_valid_mixed_inline(self):
        """Mixed inline markdown should pass validation."""
        is_valid, errors = validate_text_complexity("**Bold** and *italic* with `code`")
        assert is_valid
        assert len(errors) == 0
    
    def test_invalid_markdown_heading(self):
        """Markdown headings should fail validation."""
        is_valid, errors = validate_text_complexity("# This is a heading")
        assert not is_valid
        assert any("heading" in e.lower() for e in errors)
    
    def test_invalid_markdown_heading_level2(self):
        """Level 2 markdown headings should fail validation."""
        is_valid, errors = validate_text_complexity("## Subheading")
        assert not is_valid
        assert any("heading" in e.lower() for e in errors)
    
    def test_invalid_horizontal_rule_dashes(self):
        """Horizontal rule with dashes should fail validation."""
        is_valid, errors = validate_text_complexity("Title\n---\nContent")
        assert not is_valid
        assert any("horizontal rule" in e.lower() for e in errors)
    
    def test_invalid_horizontal_rule_asterisks(self):
        """Horizontal rule with asterisks should fail validation."""
        is_valid, errors = validate_text_complexity("Title\n***\nContent")
        assert not is_valid
        assert any("horizontal rule" in e.lower() for e in errors)
    
    def test_invalid_code_block(self):
        """Code blocks should fail validation."""
        is_valid, errors = validate_text_complexity("```python\ncode\n```")
        assert not is_valid
        assert any("code block" in e.lower() for e in errors)
    
    def test_invalid_multiple_paragraph_breaks(self):
        """Multiple paragraph breaks should fail validation."""
        is_valid, errors = validate_text_complexity("Para1\n\n\nPara2")
        assert not is_valid
        assert any("paragraph" in e.lower() for e in errors)
    
    def test_invalid_complex_example_from_issue(self):
        """The exact bad example from the issue should fail validation."""
        bad_text = "# Designing an AI Career That Evolves\n\n*Lessons from Chao Wang's journey*\n\n---\n**2011** · Face API beginnings \u2003→\u2003**2021** · Teams vision & AI"
        is_valid, errors = validate_text_complexity(bad_text)
        assert not is_valid
        # Should detect multiple issues
        assert len(errors) >= 2  # At least heading and horizontal rule
    
    def test_empty_text(self):
        """Empty text should pass validation."""
        is_valid, errors = validate_text_complexity("")
        assert is_valid
        assert len(errors) == 0
    
    def test_none_text(self):
        """None text should pass validation (handled gracefully)."""
        is_valid, errors = validate_text_complexity(None)
        assert is_valid
        assert len(errors) == 0
    
    def test_single_line_with_inline_heading(self):
        """Inline heading (not at start) should still be caught."""
        is_valid, errors = validate_text_complexity("Some text\n## Heading")
        assert not is_valid
    
    def test_short_text_with_many_newlines(self):
        """Short text should not trigger length warning."""
        text = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6"
        is_valid, errors = validate_text_complexity(text)
        assert is_valid  # Short enough, no complex markdown


class TestSanitizeWidgetText:
    """Test sanitize_widget_text function."""
    
    def test_removes_heading(self):
        """Should remove markdown heading markers."""
        result = sanitize_widget_text("# Heading Text")
        assert result == "Heading Text"
    
    def test_removes_level2_heading(self):
        """Should remove level 2 heading markers."""
        result = sanitize_widget_text("## Subheading")
        assert result == "Subheading"
    
    def test_removes_horizontal_rule(self):
        """Should remove horizontal rules."""
        result = sanitize_widget_text("Title\n---\nContent")
        assert "---" not in result
        assert "Title" in result
        assert "Content" in result
    
    def test_collapses_multiple_newlines(self):
        """Should collapse multiple newlines."""
        result = sanitize_widget_text("Para1\n\n\n\nPara2")
        assert "\n\n\n" not in result
    
    def test_preserves_inline_markdown(self):
        """Should preserve inline markdown."""
        result = sanitize_widget_text("**Bold** and *italic*")
        assert "**Bold**" in result
        assert "*italic*" in result
    
    def test_strips_whitespace(self):
        """Should strip leading/trailing whitespace."""
        result = sanitize_widget_text("  Text  ")
        assert result == "Text"
    
    def test_handles_empty_string(self):
        """Should handle empty string."""
        result = sanitize_widget_text("")
        assert result == ""
    
    def test_handles_none(self):
        """Should handle None gracefully."""
        result = sanitize_widget_text(None)
        assert result is None


class TestGetTextComplexityWarning:
    """Test get_text_complexity_warning function."""
    
    def test_no_warning_for_valid_text(self):
        """Should return None for valid text."""
        warning = get_text_complexity_warning("Valid **bold** text")
        assert warning is None
    
    def test_warning_for_invalid_text(self):
        """Should return warning string for invalid text."""
        warning = get_text_complexity_warning("# Heading\n---\nContent")
        assert warning is not None
        assert "warning" in warning.lower()
    
    def test_includes_widget_type_in_warning(self):
        """Should include widget type in warning message."""
        warning = get_text_complexity_warning("# Heading", widget_type="Type.Display")
        assert warning is not None
        assert "Type.Display" in warning


class TestIntegrationScenarios:
    """Integration tests for real-world scenarios."""
    
    def test_timeline_slide_bad_pattern(self):
        """Timeline content with multiple sections should fail."""
        # This pattern creates a long unstructured line
        bad_timeline = "**2011** · Face API\n\n---\n\n**2015** · Azure ML\n\n---\n\n**2021** · Teams AI"
        is_valid, errors = validate_text_complexity(bad_timeline)
        assert not is_valid
    
    def test_quote_with_attribution_good(self):
        """Quote with inline attribution should pass."""
        good_quote = "The best way to predict the future is to **invent it** — Alan Kay"
        is_valid, errors = validate_text_complexity(good_quote)
        assert is_valid
    
    def test_bullet_list_in_text_field(self):
        """Bullet list pattern should be detected as potential issue."""
        # Note: We don't block lists, but we want to encourage using Type.List widget
        list_text = "- Item 1\n- Item 2\n- Item 3"
        # This should pass (lists aren't blocked, just encouraged to use Type.List)
        is_valid, errors = validate_text_complexity(list_text)
        # Lists are not in COMPLEX_MARKDOWN_PATTERNS, so this passes
        # Users should be guided by prompt to use Type.List, but not blocked
        assert is_valid
    
    def test_simple_title_good(self):
        """Simple title text should pass."""
        good_title = "Designing an AI Career"
        is_valid, errors = validate_text_complexity(good_title)
        assert is_valid
    
    def test_subtitle_with_emphasis_good(self):
        """Subtitle with emphasis should pass."""
        good_subtitle = "*Lessons from a decade in ML*"
        is_valid, errors = validate_text_complexity(good_subtitle)
        assert is_valid
