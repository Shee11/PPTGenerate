"""Theme protocol for presentation styling configuration."""
from typing import Protocol


class Theme(Protocol):
    """Protocol for theme implementations.
    
    Themes define global styling for presentations including:
    - Color palette
    - Typography system
    - Layout spacing (margins, gutters)
    - Header/footer configuration
    - Multi-slide sequence patterns
    
    Note: Implementations may have additional methods for format conversion
    (e.g., to_css_vars() for HTML rendering), but those are not required
    by the protocol since they are renderer-specific.
    """
    
    # Color properties
    primary_color: str
    secondary_color: str
    accent_color: str
    background_color: str
    text_color: str
    
    # Font properties
    font_family: str
    
    # Layout spacing
    margin_x: str
    margin_y: str
    gutter: str
    
    def get_slide_background(self, slide_index: int) -> str:
        """Get background for a specific slide based on sequence pattern.
        
        Args:
            slide_index: Zero-based slide index
            
        Returns:
            Background value (color or image path)
        """
        ...
