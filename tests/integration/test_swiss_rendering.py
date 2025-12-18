"""Integration tests for Swiss layout rendering."""
import pytest
from src.layout.dummy.layout_engine import LayoutEngine
from src.layout.dummy.theme import Theme
from src.layout.dummy.style import Style
from src.render.dummy.html_renderer import HTMLRenderer


class TestSwissRendering:
    """Test end-to-end rendering of Swiss layouts."""
    
    def test_swiss_poster_with_display_widget(self) -> None:
        """Test rendering Swiss.Poster with Type.Display widget."""
        theme = Theme()
        style = Style(
            theme_name="default",
            widgets={
                "Type.Display": {"font": "h1", "align": "center", "foreground": "text_color"}
            }
        )
        
        widget_assignments = {
            "headline": {
                "type": "Type.Display",
                "parameters": {"text": "Big Bold Headline"}
            }
        }
        
        renderable = LayoutEngine.calculate(
            strategy_name="Swiss.Poster",
            widget_assignments=widget_assignments,
            theme=theme,
            style=style
        )
        
        assert renderable.strategy_name == "Swiss.Poster"
        assert len(renderable.widget_assignments) == 1
        
        renderer = HTMLRenderer()
        html = renderer.render(renderable)
        
        assert "<!DOCTYPE html>" in html
        assert "Swiss.Poster" in html
        assert "Big Bold Headline" in html
        assert "text-align: center" in html
