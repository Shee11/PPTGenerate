"""Style model for layout styling configuration."""
from typing import Optional

from pydantic import BaseModel, Field


class Style(BaseModel):
    """Style configuration for layout geometry and spacing.
    
    References typography tokens from theme and adds geometric properties
    specific to a particular layout instance. Style should NOT override
    theme spacing (gap, padding) - those come from theme's margin/gutter.
    
    Typography tokens from the theme are always used.
    """

    theme_name: str = Field(..., description="Name of the theme to apply")
    background: Optional[str] = Field(default=None, description="Override background color")
    border_radius: str = Field(default="8px", description="Corner radius for widgets")

    def to_css_props(self) -> dict[str, str]:
        """Convert style to CSS properties.
        
        Note: gap and padding are now controlled by theme (gutter and margin_x/margin_y),
        not by style configuration. This ensures consistency across layouts.
        
        Returns:
            Dictionary mapping CSS property names to values
        """
        props = {
            "border-radius": self.border_radius,
        }

        if self.background:
            props["background-color"] = self.background

        return props
