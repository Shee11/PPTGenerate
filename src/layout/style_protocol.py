"""Style protocol for widget styling configuration."""
from typing import Protocol, Optional, Dict


class WidgetStyle(Protocol):
    """Protocol for widget-specific styling configuration.
    
    All values reference theme tokens (e.g., 'body', 'primary_color').
    """
    
    font: Optional[str]  # Typography token (h1, h2, body, caption)
    align: Optional[str]  # Horizontal alignment (left, center, right, justify)
    vertical_align: Optional[str]  # Vertical alignment (top, center, bottom)
    foreground: Optional[str]  # Text color token
    background: Optional[str]  # Background color token
    border_radius: Optional[str]  # Border radius (e.g., '8px')


class Style(Protocol):
    """Protocol for style implementations.
    
    Styles define how each widget type uses theme tokens.
    Maps widget types to their styling rules.
    
    Note: Implementations may have additional methods for format conversion
    (e.g., to_css_props() for HTML rendering), but those are not required
    by the protocol since they are renderer-specific.
    """
    
    theme_name: str  # Name of the theme to apply
    widgets: Dict[str, WidgetStyle]  # Styling rules per widget type
    border_radius: str  # Default border radius
    background: Optional[str]  # Optional background override
    
    def get_widget_style(self, widget_type: str) -> Optional[WidgetStyle]:
        """Get styling for a specific widget type.
        
        Args:
            widget_type: Widget type identifier (e.g., "Type.Display")
            
        Returns:
            WidgetStyle if defined, None otherwise
        """
        ...
