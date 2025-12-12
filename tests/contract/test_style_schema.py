"""Contract tests for Theme and Style JSON schemas."""
import pytest
from pydantic import ValidationError
from src.layout.theme import Theme
from src.layout.style import Style


class TestThemeSchema:
    """Test Theme model schema and validation."""
    
    def test_theme_with_defaults(self) -> None:
        """Test that Theme can be created with default values."""
        theme = Theme()
        
        assert theme.primary_color == "#000000"
        assert theme.secondary_color == "#666666"
        assert theme.accent_color == "#0066cc"
        assert theme.background_color == "#ffffff"
        assert theme.text_color == "#000000"
        assert theme.font_family == "sans-serif"
        assert theme.heading_font is None
        assert theme.base_font_size == "16px"
        assert theme.line_height == "1.5"
    
    def test_theme_with_custom_colors(self) -> None:
        """Test Theme with custom color values."""
        theme = Theme(
            primary_color="#FF0000",
            secondary_color="#00FF00",
            accent_color="#0000FF",
        )
        
        assert theme.primary_color == "#FF0000"
        assert theme.secondary_color == "#00FF00"
        assert theme.accent_color == "#0000FF"
    
    def test_theme_to_css_vars(self) -> None:
        """Test conversion of Theme to CSS variables."""
        theme = Theme(
            primary_color="#FF0000",
            font_family="Arial",
        )
        
        css_vars = theme.to_css_vars()
        
        assert css_vars["--color-primary"] == "#FF0000"
        assert css_vars["--font-family"] == "Arial"
        assert "--color-secondary" in css_vars
        assert "--line-height" in css_vars
    
    def test_theme_with_heading_font(self) -> None:
        """Test Theme with separate heading font."""
        theme = Theme(
            font_family="Arial",
            heading_font="Georgia",
        )
        
        css_vars = theme.to_css_vars()
        assert css_vars["--font-heading"] == "Georgia"
    
    def test_theme_without_heading_font_uses_default(self) -> None:
        """Test that heading font defaults to main font."""
        theme = Theme(font_family="Verdana")
        
        css_vars = theme.to_css_vars()
        assert css_vars["--font-heading"] == "Verdana"


class TestStyleSchema:
    """Test Style model schema and validation."""
    
    def test_style_with_theme_name(self) -> None:
        """Test that Style requires theme_name."""
        style = Style(theme_name="default")
        
        assert style.theme_name == "default"
        assert style.border_radius == "8px"
        assert style.background is None
    
    def test_style_with_custom_spacing(self) -> None:
        """Test Style with border radius."""
        style = Style(
            theme_name="default",
            border_radius="12px",
        )
        
        assert style.border_radius == "12px"
    
    def test_style_with_background_override(self) -> None:
        """Test Style with background color override."""
        style = Style(
            theme_name="default",
            background="#F5F5F5",
        )
        
        assert style.background == "#F5F5F5"
    
    def test_style_to_css_props(self) -> None:
        """Test conversion of Style to CSS properties."""
        style = Style(
            theme_name="default",
            border_radius="12px",
        )
        
        css_props = style.to_css_props()
        
        assert css_props["border-radius"] == "12px"
        # Note: gap and padding now come from theme, not style
    
    def test_style_to_css_props_with_background(self) -> None:
        """Test CSS properties include background when set."""
        style = Style(
            theme_name="default",
            background="#EEEEEE",
        )
        
        css_props = style.to_css_props()
        assert css_props["background-color"] == "#EEEEEE"
    
    def test_style_to_css_props_without_background(self) -> None:
        """Test CSS properties exclude background when not set."""
        style = Style(theme_name="default")
        
        css_props = style.to_css_props()
        assert "background-color" not in css_props
    
    def test_style_requires_theme_name(self) -> None:
        """Test that theme_name is required."""
        with pytest.raises(ValidationError):
            Style()  # type: ignore
