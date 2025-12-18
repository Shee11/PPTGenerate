"""Style model for widget styling configuration."""
from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field, model_validator


class WidgetStyle(BaseModel):
    """Styling configuration for a specific widget type.
    
    All values reference theme tokens (e.g., 'body', 'primary_color', 'background_color').
    """
    
    font: Optional[str] = Field(
        default=None,
        description="Typography token from theme (h1, h2, h3, body, caption)"
    )
    align: Optional[Literal["left", "center", "right", "justify"]] = Field(
        default=None,
        description="Horizontal text alignment"
    )
    vertical_align: Optional[Literal["top", "center", "bottom"]] = Field(
        default=None,
        description="Vertical alignment within container"
    )
    foreground: Optional[str] = Field(
        default=None,
        description="Text color token from theme (primary_color, secondary_color, text_color, etc.)"
    )
    background: Optional[str] = Field(
        default=None,
        description="Background color token from theme (background_color, primary_background, etc.)"
    )
    border_radius: Optional[str] = Field(
        default=None,
        description="Border radius (e.g., '8px', '12px')"
    )


class Style(BaseModel):
    """Style configuration that defines how each widget type uses theme tokens.
    
    Each widget type should have an explicit style definition for proper rendering.
    """

    theme_name: str = Field(..., description="Name of the theme to apply")
    
    # Widget type styling rules - keys are widget types like "Type.Display", "Data.BigNum"
    widgets: Dict[str, WidgetStyle] = Field(
        default_factory=dict,
        description="Styling rules for each widget type, referencing theme tokens"
    )
    
    # Legacy/global properties
    border_radius: str = Field(default="8px", description="Default border radius for styled elements")
    background: Optional[str] = Field(default=None, description="Optional background color override")
    
    def get_widget_style(self, widget_type: str) -> Optional[WidgetStyle]:
        """Get styling for a specific widget type.
        
        Args:
            widget_type: Widget type identifier (e.g., "Type.Display")
            
        Returns:
            WidgetStyle if defined, None otherwise
        """
        return self.widgets.get(widget_type)
    
    def to_css_props(self) -> dict[str, str]:
        """Convert style properties to CSS properties.
        
        Returns:
            Dictionary of CSS property names to values
        """
        props = {
            "border-radius": self.border_radius,
        }
        
        if self.background:
            props["background-color"] = self.background
        
        return props
