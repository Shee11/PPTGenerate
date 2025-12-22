"""Text validation utilities for widget content.

This module provides validation for widget text content to ensure
it follows presentation best practices:
- Only inline markdown (bold, italic) is allowed
- No complex markdown structures (headings, horizontal rules, multiple paragraphs)
- No sequence-like concatenated sections
"""
import re
from typing import List, Tuple


# Patterns that indicate complex markdown structure (not allowed in widget text)
COMPLEX_MARKDOWN_PATTERNS = [
    # Markdown headings (# Header, ## Header, etc.)
    (r'^#{1,6}\s', "Markdown heading (# Header)"),
    (r'\n#{1,6}\s', "Markdown heading in text"),
    
    # Horizontal rules (---, ***, ___)
    (r'^-{3,}$', "Horizontal rule (---)"),
    (r'\n-{3,}\n', "Horizontal rule in text"),
    (r'^[*]{3,}$', "Horizontal rule (***)"),
    (r'\n[*]{3,}\n', "Horizontal rule in text"),
    (r'^_{3,}$', "Horizontal rule (___)"),
    (r'\n_{3,}\n', "Horizontal rule in text"),
    
    # Multiple paragraph breaks (double newlines creating sections)
    (r'\n\n\n', "Multiple paragraph breaks"),
    
    # Code blocks (triple backticks)
    (r'```', "Code block (use Media.Code widget instead)"),
]

# Allowed inline markdown patterns
ALLOWED_INLINE_PATTERNS = [
    r'\*\*[^*]+\*\*',   # Bold: **text**
    r'\*[^*]+\*',        # Italic: *text*
    r'__[^_]+__',        # Bold: __text__
    r'_[^_]+_',          # Italic: _text_
    r'`[^`]+`',          # Inline code: `code`
]


def validate_text_complexity(text: str, widget_type: str = "widget") -> Tuple[bool, List[str]]:
    """Validate that text doesn't contain complex markdown structures.
    
    Widget text should only contain:
    - Plain text
    - Inline markdown: **bold**, *italic*, `code`
    
    Widget text should NOT contain:
    - Markdown headings (# Header)
    - Horizontal rules (---)
    - Multiple paragraphs/sections
    - Code blocks (```)
    - Lists (use Type.List widget instead)
    
    Args:
        text: Text content to validate
        widget_type: Widget type name for error messages
        
    Returns:
        Tuple of (is_valid, list of error messages)
    """
    if not text:
        return True, []
    
    errors = []
    
    for pattern, description in COMPLEX_MARKDOWN_PATTERNS:
        if re.search(pattern, text, re.MULTILINE):
            errors.append(f"{widget_type} text contains {description}. Use separate widgets for structured content.")
    
    # Check for excessive length suggesting concatenated sections
    # A single widget text should be concise (roughly 200 chars max for most cases)
    # But we allow longer for quotes and body text
    if len(text) > 500:
        # If very long AND contains multiple newlines, likely concatenated content
        newline_count = text.count('\n')
        if newline_count > 5:
            errors.append(
                f"{widget_type} text appears to contain multiple sections ({newline_count} line breaks, {len(text)} chars). "
                "Split into separate widgets or slides."
            )
    
    return len(errors) == 0, errors


def sanitize_widget_text(text: str) -> str:
    """Sanitize widget text by removing complex markdown structures.
    
    This is a best-effort cleanup that:
    - Removes markdown headings (keeps the text)
    - Removes horizontal rules
    - Collapses multiple newlines
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text with complex structures removed
    """
    if not text:
        return text
    
    # Remove markdown headings but keep the text
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    
    # Remove horizontal rules
    text = re.sub(r'^-{3,}$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\*{3,}$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^_{3,}$', '', text, flags=re.MULTILINE)
    
    # Collapse multiple newlines to single newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def get_text_complexity_warning(text: str, widget_type: str = "widget") -> str | None:
    """Get a warning message if text has complexity issues.
    
    This is a non-blocking check that returns a warning string
    for logging/debugging purposes.
    
    Args:
        text: Text to check
        widget_type: Widget type for context
        
    Returns:
        Warning message string or None if text is valid
    """
    is_valid, errors = validate_text_complexity(text, widget_type)
    if not is_valid:
        return f"Text complexity warning in {widget_type}: " + "; ".join(errors)
    return None
