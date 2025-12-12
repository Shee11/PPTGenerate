"""Integration tests for Cinematic layout rendering."""
import pytest
from src.layout.layout_engine import LayoutEngine
from src.layout.theme import Theme
from src.layout.style import Style
from src.render.html_renderer import HTMLRenderer


class TestCinematicRendering:
    """Test end-to-end rendering of Cinematic layouts."""
    
    def test_cinematic_split_50_50(self) -> None:
        """Test rendering Cinematic.Split_50_50 with two widgets."""
        theme = Theme()
        style = Style(
            theme_name="default",
            widgets={
                "Type.Heading": {"font": "h1", "align": "left", "foreground": "text_color"}
            }
        )
        
        widget_assignments = {
            "left": {
                "type": "Type.Heading",
                "parameters": {"text": "Left Panel", "level": 1}
            },
            "right": {
                "type": "Type.Heading",
                "parameters": {"text": "Right Panel", "level": 1}
            }
        }
        
        renderable = LayoutEngine.calculate(
            strategy_name="Cinematic.Split_50_50",
            widget_assignments=widget_assignments,
            theme=theme,
            style=style
        )
        
        assert renderable.strategy_name == "Cinematic.Split_50_50"
        assert len(renderable.widget_assignments) == 2
        
        renderer = HTMLRenderer()
        html = renderer.render(renderable)
        
        assert "<!DOCTYPE html>" in html
        assert "Cinematic.Split_50_50" in html
        assert "Left Panel" in html
        assert "Right Panel" in html
        assert "cinematic-split" in html
