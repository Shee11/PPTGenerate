"""Integration tests for style parameter application."""
import pytest
from src.layout.layout_engine import LayoutEngine
from src.layout.strategies.bento import BentoStandardStrategy
from src.layout.theme import Theme
from src.layout.style import Style
from src.widgets.typography import TypeDisplayWidget
from src.widgets.data import DataBigNumWidget
from src.render.html_renderer import HTMLRenderer
from src.common.renderable_layout import RenderableLayout, WidgetAssignment
from src.common.size_class import SizeClass


class TestStyleParameterApplication:
    """Test that style parameters are correctly applied to widgets in rendered HTML."""
    
    def test_theme_colors_applied(self):
        """Theme colors should be available as CSS variables."""
        theme = Theme(
            primary_color="#FF0000",
            accent_color="#00FF00",
            background_color="#FFFFFF"
        )
        
        css_vars = theme.to_css_vars()
        
        assert css_vars["--color-primary"] == "#FF0000"
        assert css_vars["--color-accent"] == "#00FF00"
        assert css_vars["--color-background"] == "#FFFFFF"
    
    def test_style_properties_applied(self):
        """Style properties should be available as CSS properties."""
        style = Style(
            theme_name="default",
            border_radius="12px"
        )
        
        css_props = style.to_css_props()
        
        # Gap and padding now come from theme, not style
        assert css_props["border-radius"] == "12px"
    
    def test_widget_parameter_color_applied(self):
        """Widget color parameters should be rendered in HTML."""
        widget = DataBigNumWidget(
            parameters={
                "color": "accent",
                "value": 12345,
                "label": "Revenue"
            }
        )
        
        data = widget.render_data()
        
        assert data["color"] == "accent"
    
    def test_widget_parameter_align_applied(self):
        """Widget alignment parameters should be rendered in HTML."""
        widget = TypeDisplayWidget(
            parameters={
                "align": "center",
                "text": "Centered Text"
            }
        )
        
        data = widget.render_data()
        
        assert data["align"] == "center"
    
    def test_widget_parameter_style_applied(self):
        """Widget style parameters (bold/italic) should be rendered in HTML."""
        widget = TypeDisplayWidget(
            parameters={
                "style": "bold",
                "text": "Bold Text"
            }
        )
        
        data = widget.render_data()
        
        assert data["style"] == "bold"
