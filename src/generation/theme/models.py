"""Theme models for structured theme representation."""
from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class TypographyStyle(BaseModel):
    """Typography style for a specific text level."""
    size: int = Field(..., ge=10, le=200, description="Font size in pixels")
    weight: Literal["light", "regular", "medium", "semibold", "bold", "black"] = Field(
        default="regular", description="Font weight"
    )
    line_height: float = Field(default=1.4, ge=0.8, le=3.0, description="Line height multiplier")


class ThemeTypography(BaseModel):
    """Typography settings for all text levels."""
    h1: TypographyStyle = Field(default_factory=lambda: TypographyStyle(size=60, weight="bold", line_height=1.1))
    h2: TypographyStyle = Field(default_factory=lambda: TypographyStyle(size=40, weight="medium", line_height=1.2))
    h3: TypographyStyle = Field(default_factory=lambda: TypographyStyle(size=28, weight="medium", line_height=1.3))
    body: TypographyStyle = Field(default_factory=lambda: TypographyStyle(size=18, weight="regular", line_height=1.5))
    caption: TypographyStyle = Field(default_factory=lambda: TypographyStyle(size=14, weight="regular", line_height=1.4))


class ThemeHeaderFooter(BaseModel):
    """Header and footer positioning settings."""
    header_height: str = Field(default="15%", description="Header height as percentage")
    footer_height: str = Field(default="10%", description="Footer height as percentage")
    header_position: Literal["fixed_top_left", "fixed_top_right", "centered", "none"] = Field(
        default="fixed_top_left", description="Header position"
    )
    footer_position: Literal["fixed_bottom_left", "fixed_bottom_right", "centered", "none"] = Field(
        default="fixed_bottom_left", description="Footer position"
    )
    header_decoration: Literal["underline_accent", "overline_accent", "box", "none"] = Field(
        default="none", description="Header decoration style"
    )
    footer_decoration: Literal["underline_accent", "overline_accent", "box", "none"] = Field(
        default="none", description="Footer decoration style"
    )


class Theme(BaseModel):
    """Complete theme definition for presentations.
    
    A theme defines the visual appearance of slides including:
    - Colors (primary, secondary, accent, background, text)
    - Typography (sizes, weights for h1, h2, h3, body, caption)
    - Spacing (margins, gutters)
    - Header/footer styling
    
    Built-in themes:
    - corp_modern_v1: Professional corporate with blue accent
    - minimal_dark_v1: Clean dark theme with cyan accent
    - cyber_neon_v1: Vibrant neon on dark background
    - forest_nature_v1: Green nature-inspired theme
    - ocean_deep_v1: Deep blue oceanic theme
    - royal_purple_v1: Elegant purple theme
    - slate_professional_v1: Neutral slate professional
    - warm_sunset_v1: Warm orange/red sunset colors
    """
    
    # Identity
    id: str = Field(..., description="Unique theme identifier (e.g., 'my_theme_v1')")
    
    # Spacing
    margin_x: str = Field(default="40px", description="Horizontal margin")
    margin_y: str = Field(default="30px", description="Vertical margin")
    gutter: str = Field(default="20px", description="Gap between elements")
    
    # Header/Footer
    header_footer: ThemeHeaderFooter = Field(default_factory=ThemeHeaderFooter)
    
    # Sequence pattern
    sequence_pattern: Literal["alternating_background", "section_break", "progressive", "uniform"] = Field(
        default="alternating_background",
        description="How slide backgrounds vary through the deck"
    )
    
    # Typography
    typography: ThemeTypography = Field(default_factory=ThemeTypography)
    
    # Colors - the core visual identity
    primary_color: str = Field(default="#2563eb", description="Primary brand color (buttons, links)")
    secondary_color: str = Field(default="#64748b", description="Secondary muted color")
    accent_color: str = Field(default="#f59e0b", description="Accent highlight color")
    background_color: str = Field(default="#ffffff", description="Main background color")
    text_color: str = Field(default="#1e293b", description="Main text color")
    primary_background: str = Field(default="#f8fafc", description="Primary slide background")
    secondary_background: str = Field(default="#ffffff", description="Secondary/alternate background")
    
    # Fonts
    font_family: str = Field(default="Inter, system-ui, sans-serif", description="Body font family")
    heading_font: str = Field(default="Inter, system-ui, sans-serif", description="Heading font family")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Theme":
        """Create Theme from dictionary."""
        return cls(**data)
    
    def is_dark(self) -> bool:
        """Check if this is a dark theme based on background color."""
        # Simple heuristic: if background is dark, text should be light
        bg = self.background_color.lower()
        # Dark colors typically have low RGB values
        if bg.startswith("#"):
            try:
                r = int(bg[1:3], 16)
                g = int(bg[3:5], 16)
                b = int(bg[5:7], 16)
                return (r + g + b) / 3 < 128
            except (ValueError, IndexError):
                pass
        return False


# Reference schema for LLM - shows all available keys
THEME_SCHEMA_REFERENCE = """
Theme JSON Schema:
{
  "id": "string (required) - Unique identifier like 'my_theme_v1'",
  
  "margin_x": "string - Horizontal margin e.g. '40px', '60px'",
  "margin_y": "string - Vertical margin e.g. '30px', '40px'",
  "gutter": "string - Gap between elements e.g. '20px', '24px'",
  
  "header_footer": {
    "header_height": "string - e.g. '15%', '20%'",
    "footer_height": "string - e.g. '10%'",
    "header_position": "fixed_top_left | fixed_top_right | centered | none",
    "footer_position": "fixed_bottom_left | fixed_bottom_right | centered | none",
    "header_decoration": "underline_accent | overline_accent | box | none",
    "footer_decoration": "underline_accent | overline_accent | box | none"
  },
  
  "sequence_pattern": "alternating_background | section_break | progressive | uniform",
  
  "typography": {
    "h1": {"size": 60, "weight": "bold", "line_height": 1.1},
    "h2": {"size": 40, "weight": "medium", "line_height": 1.2},
    "h3": {"size": 28, "weight": "medium", "line_height": 1.3},
    "body": {"size": 18, "weight": "regular", "line_height": 1.5},
    "caption": {"size": 14, "weight": "regular", "line_height": 1.4}
  },
  
  "primary_color": "#hex - Primary brand color (buttons, links, accents)",
  "secondary_color": "#hex - Secondary muted color (subtitles, metadata)",
  "accent_color": "#hex - Highlight color for emphasis",
  "background_color": "#hex - Main background",
  "text_color": "#hex - Main text color",
  "primary_background": "#hex - Primary slide background",
  "secondary_background": "#hex - Alternate/secondary background",
  
  "font_family": "string - Body font e.g. 'Inter, system-ui, sans-serif'",
  "heading_font": "string - Heading font e.g. 'Playfair Display, serif'"
}

Weight options: light | regular | medium | semibold | bold | black
"""
