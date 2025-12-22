"""Comparison widget for side-by-side comparisons."""
from typing import Any, ClassVar
from pydantic import Field

from src.common.size_class import SizeClass
from src.paged.widgets.base import BaseWidget, WidgetRegistry


@WidgetRegistry.register
class ComparisonWidget(BaseWidget):
    """Widget for displaying side-by-side comparisons (Before/After, Old vs New).
    
    Renders two columns with headers, bullet lists, and optional bottom note.
    Perfect for Traditional vs LLM, Old Approach vs New Approach, etc.
    
    Minimum size: M (medium) - needs space for two columns
    
    Parameters:
        left_title: Title for left column (e.g., "Traditional AI")
        left_items: Bullet points for left column (list of strings)
        right_title: Title for right column (e.g., "LLM Era")
        right_items: Bullet points for right column (list of strings)
        left_color: Optional color for left title (CSS color, default red)
        right_color: Optional color for right title (CSS color, default green)
        bottom_note: Optional note displayed below both columns
    """
    
    widget_type: ClassVar[str] = "Type.Comparison"
    min_size: ClassVar[SizeClass] = SizeClass.M
    
    def validate_parameters(self) -> None:
        """Validate Comparison-specific parameters."""
        required_params = ["left_title", "left_items", "right_title", "right_items"]
        for param in required_params:
            if param not in self.parameters:
                from pydantic_core import ValidationError
                raise ValidationError(
                    f"Comparison widget requires '{param}' parameter"
                )
    
    @staticmethod
    def get_widget_type() -> str:
        """Return widget type identifier."""
        return "Type.Comparison"
    
    def measure(self, style: dict[str, Any], max_width: float = float('inf'), max_height: float = float('inf')):
        """Calculate widget content size for Comparison.
        
        Comparison widget has two columns side-by-side with headers and lists.
        """
        from src.common.measurement import MeasuredSize
        
        # Get parameters with defaults
        left_items = self.parameters.get("left_items", [])
        right_items = self.parameters.get("right_items", [])
        bottom_note = self.parameters.get("bottom_note")
        
        # Get font size from style (default to body text)
        font_size_str = style.get("font-size", "18px")
        font_size = float(font_size_str.replace("px", "")) if isinstance(font_size_str, str) else 18
        line_height = float(style.get("line-height", 1.5))
        
        # Calculate height needed:
        # - Title line for each column
        # - List items (max of left/right)
        # - Bottom note if present
        max_items = max(len(left_items), len(right_items))
        title_height = font_size * line_height * 1.5  # Slightly larger for titles
        items_height = max_items * font_size * line_height * 1.2  # Line spacing for lists
        note_height = font_size * line_height * 2 if bottom_note else 0
        padding = 60  # Generous padding for comparison layout
        
        total_height = title_height * 2 + items_height + note_height + padding
        
        return MeasuredSize(
            width=max_width,
            height=min(total_height, max_height)
        )
    
    def render_data(self) -> dict[str, Any]:
        """Return data for template rendering."""
        return {
            "left_title": self.parameters.get("left_title", "Left"),
            "left_items": self.parameters.get("left_items", []),
            "right_title": self.parameters.get("right_title", "Right"),
            "right_items": self.parameters.get("right_items", []),
            "left_color": self.parameters.get("left_color", "var(--color-error, #ef4444)"),
            "right_color": self.parameters.get("right_color", "var(--color-success, #22c55e)"),
            "bottom_note": self.parameters.get("bottom_note"),
        }

