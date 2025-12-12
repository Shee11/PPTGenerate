"""Integration tests for Bento layout rendering."""
import pytest
from src.layout.layout_engine import LayoutEngine
from src.layout.theme import Theme
from src.layout.style import Style
from src.render.html_renderer import HTMLRenderer


class TestBentoRendering:
    """Test end-to-end rendering of Bento layouts."""
    
    def test_bento_standard_with_typography_widgets(self) -> None:
        """Test rendering Bento.Standard with typography widgets."""
        # Setup theme and style
        theme = Theme()
        style = Style(theme_name="default")
        
        # Configure widget assignments
        widget_assignments = {
            "cell_1": {
                "type": "Type.Display",
                "parameters": {"text": "Hello World", "style": "bold"}
            },
            "cell_2": {
                "type": "Type.Heading",
                "parameters": {"text": "Section 1", "level": 2}
            },
            "cell_3": {
                "type": "Type.Body",
                "parameters": {"text": "This is body text content."}
            },
        }
        
        # Calculate layout
        renderable = LayoutEngine.calculate(
            strategy_name="Bento.Standard",
            widget_assignments=widget_assignments,
            theme=theme,
            style=style
        )
        
        # Verify renderable structure
        assert renderable.strategy_name == "Bento.Standard"
        assert len(renderable.widget_assignments) == 3
        assert len(renderable.theme_vars) > 0
        assert len(renderable.style_props) > 0
        
        # Render to HTML
        renderer = HTMLRenderer()
        html = renderer.render(renderable)
        
        # Verify HTML output
        assert "<!DOCTYPE html>" in html
        assert "Bento.Standard" in html
        assert "Hello World" in html
        assert "Section 1" in html
        assert "This is body text content." in html
    
    def test_bento_standard_with_data_widgets(self) -> None:
        """Test rendering Bento.Standard with data widgets."""
        theme = Theme()
        style = Style(theme_name="default")
        
        widget_assignments = {
            "cell_1": {
                "type": "Data.BigNum",
                "parameters": {"value": 42, "label": "Total Users"}
            },
            "cell_2": {
                "type": "Data.Trend",
                "parameters": {"value": 128, "change": 12, "direction": "up", "label": "Revenue"}
            },
        }
        
        renderable = LayoutEngine.calculate(
            "Bento.Standard",
            widget_assignments,
            theme,
            style
        )
        
        renderer = HTMLRenderer()
        html = renderer.render(renderable)
        
        assert "42" in html
        assert "Total Users" in html
        assert "128" in html
        assert "Revenue" in html
    
    def test_bento_standard_all_six_cells(self) -> None:
        """Test rendering all 6 cells in Bento.Standard."""
        theme = Theme()
        style = Style(theme_name="default")
        
        widget_assignments = {
            f"cell_{i}": {
                "type": "Type.Body",
                "parameters": {"text": f"Cell {i} content"}
            }
            for i in range(1, 7)
        }
        
        renderable = LayoutEngine.calculate(
            "Bento.Standard",
            widget_assignments,
            theme,
            style
        )
        
        assert len(renderable.widget_assignments) == 6
        
        renderer = HTMLRenderer()
        html = renderer.render(renderable)
        
        # Verify all cells are present
        for i in range(1, 7):
            assert f"Cell {i} content" in html
