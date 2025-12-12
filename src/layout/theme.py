"""Comprehensive theme model for multi-slide presentations."""
from typing import Literal, Optional

from pydantic import BaseModel, Field


class HeaderFooterStrategy(BaseModel):
    """Header and footer positioning strategy.
    
    Defines reserved areas at top/bottom that widgets must avoid during auto-layout.
    """
    
    header_height: str = Field(default="15%", description="Header area height (reserved at top)")
    footer_height: str = Field(default="10%", description="Footer area height (reserved at bottom)")
    header_position: Literal["fixed_top_left", "centered", "floating"] = Field(
        default="fixed_top_left",
        description="Header positioning strategy"
    )
    footer_position: Literal["fixed_bottom_left", "centered", "floating"] = Field(
        default="fixed_bottom_left",
        description="Footer positioning strategy"
    )
    header_decoration: Literal["none", "underline_accent", "border_bottom", "background_block"] = Field(
        default="underline_accent",
        description="Header decoration style"
    )
    footer_decoration: Literal["none", "border_top", "background_block"] = Field(
        default="none",
        description="Footer decoration style"
    )


class TypographyToken(BaseModel):
    """Typography token for a specific text style."""
    
    size: int = Field(..., description="Font size in pixels")
    weight: Literal["thin", "light", "regular", "medium", "semibold", "bold", "black"] = Field(
        default="regular",
        description="Font weight"
    )
    line_height: Optional[float] = Field(default=None, description="Line height multiplier")


class Typography(BaseModel):
    """Typography system with semantic tokens."""
    
    h1: TypographyToken = Field(
        default=TypographyToken(size=60, weight="bold", line_height=1.1),
        description="Primary heading style"
    )
    h2: TypographyToken = Field(
        default=TypographyToken(size=40, weight="medium", line_height=1.2),
        description="Secondary heading style"
    )
    h3: TypographyToken = Field(
        default=TypographyToken(size=28, weight="medium", line_height=1.3),
        description="Tertiary heading style"
    )
    body: TypographyToken = Field(
        default=TypographyToken(size=18, weight="regular", line_height=1.5),
        description="Body text style"
    )
    caption: TypographyToken = Field(
        default=TypographyToken(size=14, weight="regular", line_height=1.4),
        description="Caption/small text style"
    )


class Theme(BaseModel):
    """Comprehensive theme configuration for multi-slide presentations.
    
    Defines global styling that applies across multiple slides including:
    - Layout spacing (margins and gutters)
    - Header/footer positioning and reserved areas
    - Sequence patterns for slide backgrounds
    - Typography tokens
    - Color palette
    """

    # Theme metadata
    id: str = Field(default="default_theme", description="Unique theme identifier")
    
    # Layout spacing (replaces grid system)
    margin_x: str = Field(default="40px", description="Horizontal page margin")
    margin_y: str = Field(default="30px", description="Vertical page margin")
    gutter: str = Field(default="20px", description="Spacing between widgets/slots")
    
    # Header/footer strategy (key requirement)
    header_footer: HeaderFooterStrategy = Field(default_factory=HeaderFooterStrategy)
    
    # Sequence rhythm across slides (key requirement)
    sequence_pattern: Literal["uniform", "alternating_background", "section_break"] = Field(
        default="uniform",
        description="How slides alternate/transition visually"
    )
    
    # Typography system
    typography: Typography = Field(default_factory=Typography)
    
    # Color palette
    primary_color: str = Field(default="#000000", description="Primary brand color")
    secondary_color: str = Field(default="#666666", description="Secondary brand color")
    accent_color: str = Field(default="#0066cc", description="Accent/highlight color")
    background_color: str = Field(default="#ffffff", description="Default background color")
    text_color: str = Field(default="#000000", description="Default text color")
    
    # Background slots for sequence patterns
    primary_background: Optional[str] = Field(
        default=None,
        description="Primary background (image path or color) for alternating pattern"
    )
    secondary_background: Optional[str] = Field(
        default=None,
        description="Secondary background (image path or color) for alternating pattern"
    )
    
    # Typography attributes
    font_family: str = Field(default="sans-serif", description="Primary font family")
    heading_font: Optional[str] = Field(default=None, description="Font for headings (if different)")
    
    # Backward compatibility fields
    base_font_size: str = Field(default="16px", description="Base font size (deprecated - use typography.body.size)")
    line_height: str = Field(default="1.5", description="Base line height (deprecated - use typography.body.line_height)")

    def to_css_vars(self) -> dict[str, str]:
        """Convert theme to CSS custom properties.
        
        Returns:
            Dictionary mapping CSS variable names to values
        """
        vars_dict = {
            "--color-primary": self.primary_color,
            "--color-secondary": self.secondary_color,
            "--color-accent": self.accent_color,
            "--color-background": self.background_color,
            "--color-text": self.text_color,
            "--font-family": self.font_family,
            "--font-heading": self.heading_font or self.font_family,
            
            # Backward compatibility
            "--font-size-base": self.base_font_size,
            "--line-height": self.line_height,
            
            # Layout spacing
            "--margin-x": self.margin_x,
            "--margin-y": self.margin_y,
            "--gutter": self.gutter,
            
            # Header/footer strategy
            "--header-height": self.header_footer.header_height,
            "--footer-height": self.header_footer.footer_height,
            
            # Typography tokens
            "--font-h1-size": f"{self.typography.h1.size}px",
            "--font-h1-weight": self.typography.h1.weight,
            "--font-h1-line-height": str(self.typography.h1.line_height or 1.1),
            
            "--font-h2-size": f"{self.typography.h2.size}px",
            "--font-h2-weight": self.typography.h2.weight,
            "--font-h2-line-height": str(self.typography.h2.line_height or 1.2),
            
            "--font-h3-size": f"{self.typography.h3.size}px",
            "--font-h3-weight": self.typography.h3.weight,
            "--font-h3-line-height": str(self.typography.h3.line_height or 1.3),
            
            "--font-body-size": f"{self.typography.body.size}px",
            "--font-body-weight": self.typography.body.weight,
            "--font-body-line-height": str(self.typography.body.line_height or 1.5),
            
            "--font-caption-size": f"{self.typography.caption.size}px",
            "--font-caption-weight": self.typography.caption.weight,
            "--font-caption-line-height": str(self.typography.caption.line_height or 1.4),
        }
        
        # Add background images/colors if defined
        if self.primary_background:
            vars_dict["--background-primary"] = self.primary_background
        if self.secondary_background:
            vars_dict["--background-secondary"] = self.secondary_background
            
        return vars_dict
    
    def get_slide_background(self, slide_index: int) -> str:
        """Get background for a specific slide based on sequence pattern.
        
        Args:
            slide_index: Zero-based slide index
            
        Returns:
            Background value (color or image path)
        """
        if self.sequence_pattern == "uniform":
            return self.background_color
        
        elif self.sequence_pattern == "alternating_background":
            if slide_index % 2 == 0:
                return self.primary_background or self.background_color
            else:
                return self.secondary_background or self.background_color
        
        elif self.sequence_pattern == "section_break":
            # Every 3rd slide uses primary background as section break
            if slide_index % 3 == 0:
                return self.primary_background or self.background_color
            else:
                return self.background_color
        
        return self.background_color
