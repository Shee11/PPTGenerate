"""Integration tests for style application through LayoutEngine."""
import pytest
from src.paged.layout.dummy.layout_engine import LayoutEngine
from src.paged.layout.dummy.theme import Theme
from src.paged.layout.dummy.style import Style
from src.paged.widgets.typography import TypeDisplayWidget
from src.paged.widgets.data import DataBigNumWidget


class TestStyleApplication:
    """Test that styles are correctly applied to widgets by LayoutEngine."""
    
    def test_theme_colors_available_as_css_vars(self):
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
    
    def test_widget_style_resolved_from_config(self):
        """Widget styles should be resolved from style config via LayoutEngine."""
        theme = Theme()
        style = Style(
            theme_name="default",
            widgets={
                "Type.Display": {
                    "font": "h1",
                    "align": "center",
                    "foreground": "primary_color"
                }
            }
        )
        
        widget_assignments = {
            "cell_1": {
                "type": "Type.Display",
                "parameters": {"text": "Test Display"}
            }
        }
        
        renderable = LayoutEngine.calculate(
            strategy_name="Bento.Standard",
            widget_assignments=widget_assignments,
            theme=theme,
            style=style
        )
        
        # Verify the widget assignment has applied_style
        assert len(renderable.widget_assignments) == 1
        assignment = renderable.widget_assignments[0]
        assert assignment.applied_style is not None
        assert "text-align" in assignment.applied_style
        assert assignment.applied_style["text-align"] == "center"
        assert "color" in assignment.applied_style
    
    def test_widget_style_with_different_colors(self):
        """Different color tokens should resolve to different CSS colors."""
        theme = Theme(
            primary_color="#FF0000",
            accent_color="#00FF00"
        )
        style = Style(
            theme_name="default",
            widgets={
                "Data.BigNum": {
                    "font": "h1",
                    "foreground": "accent_color"
                }
            }
        )
        
        widget_assignments = {
            "cell_1": {
                "type": "Data.BigNum",
                "parameters": {"number": 42, "label": "Count"}
            }
        }
        
        renderable = LayoutEngine.calculate(
            strategy_name="Bento.Standard",
            widget_assignments=widget_assignments,
            theme=theme,
            style=style
        )
        
        assignment = renderable.widget_assignments[0]
        assert assignment.applied_style is not None
        assert "color" in assignment.applied_style
        # Should be accent color, not primary
        assert assignment.applied_style["color"] == "#00FF00"
    
    def test_widget_style_with_background(self):
        """Background colors should be applied when specified."""
        theme = Theme(
            secondary_color="#F5F5F5"
        )
        style = Style(
            theme_name="default",
            widgets={
                "Type.Display": {
                    "font": "h1",
                    "background": "secondary_color"
                }
            }
        )
        
        widget_assignments = {
            "cell_1": {
                "type": "Type.Display",
                "parameters": {"text": "Test"}
            }
        }
        
        renderable = LayoutEngine.calculate(
            strategy_name="Bento.Standard",
            widget_assignments=widget_assignments,
            theme=theme,
            style=style
        )
        
        assignment = renderable.widget_assignments[0]
        assert "background-color" in assignment.applied_style
        assert assignment.applied_style["background-color"] == "#F5F5F5"
    
    def test_widget_parameters_remain_content_only(self):
        """Widget parameters should only contain content, not styling."""
        widget = TypeDisplayWidget(
            parameters={"text": "Test Display"}
        )
        
        # Parameters should only have text, not style/align
        assert "text" in widget.parameters
        assert "style" not in widget.parameters
        assert "align" not in widget.parameters
        
        widget.validate_parameters()
        data = widget.render_data()
        
        assert data["content"] == "Test Display"
    
    def test_data_widget_parameters_content_only(self):
        """Data widgets should only have content parameters."""
        widget = DataBigNumWidget(
            parameters={"number": 100, "label": "Test"}
        )
        
        # Parameters should have number/label, not color
        assert "number" in widget.parameters
        assert "label" in widget.parameters
        assert "color" not in widget.parameters
        
        widget.validate_parameters()
        data = widget.render_data()
        
        assert data["number"] == 100
        assert data["label"] == "Test"
