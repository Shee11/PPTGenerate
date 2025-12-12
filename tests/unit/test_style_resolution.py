"""Unit tests for Theme/Style to CSS conversion."""
import pytest
from src.layout.theme import Theme
from src.layout.style import Style


class TestThemeToCSSConversion:
    """Test Theme.to_css_vars() method."""
    
    def test_default_theme_css_vars(self):
        """Default theme should produce correct CSS variables."""
        theme = Theme()
        css_vars = theme.to_css_vars()
        
        assert "--color-primary" in css_vars
        assert "--color-secondary" in css_vars
        assert "--color-accent" in css_vars
        assert "--color-background" in css_vars
        assert "--color-text" in css_vars
        assert "--font-family" in css_vars
        assert "--font-heading" in css_vars
        assert "--font-size-base" in css_vars
        assert "--line-height" in css_vars
    
    def test_custom_theme_css_vars(self):
        """Custom theme values should be reflected in CSS variables."""
        theme = Theme(
            primary_color="#2563eb",
            accent_color="#7c3aed",
            font_family="Inter, system-ui, sans-serif",
            base_font_size="18px",
            line_height="1.6"
        )
        
        css_vars = theme.to_css_vars()
        
        assert css_vars["--color-primary"] == "#2563eb"
        assert css_vars["--color-accent"] == "#7c3aed"
        assert css_vars["--font-family"] == "Inter, system-ui, sans-serif"
        assert css_vars["--font-size-base"] == "18px"
        assert css_vars["--line-height"] == "1.6"
    
    def test_heading_font_fallback(self):
        """When heading_font is None, should fall back to font_family."""
        theme = Theme(font_family="Arial, sans-serif")
        css_vars = theme.to_css_vars()
        
        assert css_vars["--font-heading"] == "Arial, sans-serif"
    
    def test_custom_heading_font(self):
        """Custom heading font should override fallback."""
        theme = Theme(
            font_family="Arial, sans-serif",
            heading_font="Georgia, serif"
        )
        css_vars = theme.to_css_vars()
        
        assert css_vars["--font-heading"] == "Georgia, serif"
        assert css_vars["--font-family"] == "Arial, sans-serif"


class TestStyleToCSSConversion:
    """Test Style.to_css_props() method."""
    
    def test_default_style_css_props(self):
        """Default style should produce correct CSS properties."""
        style = Style(theme_name="default")
        css_props = style.to_css_props()
        
        # Gap and padding now come from theme, not style
        assert "border-radius" in css_props
        assert css_props["border-radius"] == "8px"
    
    def test_custom_style_css_props(self):
        """Custom style values should be reflected in CSS properties."""
        style = Style(
            theme_name="custom",
            border_radius="12px",
            background="#f5f5f5"
        )
        
        css_props = style.to_css_props()
        
        # Gap and padding now come from theme, not style
        assert css_props["border-radius"] == "12px"
        assert css_props["background-color"] == "#f5f5f5"
    
    def test_background_optional(self):
        """Background should only be included if set."""
        style = Style(theme_name="default")
        css_props = style.to_css_props()
        
        assert "background-color" not in css_props
    
    def test_background_override(self):
        """Background override should be included when set."""
        style = Style(theme_name="default", background="#ffffff")
        css_props = style.to_css_props()
        
        assert css_props["background-color"] == "#ffffff"
