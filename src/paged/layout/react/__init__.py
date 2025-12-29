"""React MDX layout engine for semantic component-based presentations."""

from .layout_engine import ReactLayoutEngine
from .layout_validator import (
    validate_widget_in_slot,
    validate_slide_layout,
    suggest_better_layout,
    get_layout_guidance_prompt,
)

__all__ = [
    "ReactLayoutEngine",
    "validate_widget_in_slot",
    "validate_slide_layout",
    "suggest_better_layout",
    "get_layout_guidance_prompt",
]
