"""Integration tests for JSON-to-Markdown transformation."""
import pytest


class TestSingleSlideRendering:
    """Test complete single slide rendering from JSON to markdown."""
    
    def test_render_smart_grid_slide_with_mixed_widgets(self):
        """Verify full JSON produces valid markdown with frontmatter and slots."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        slide = {
            "layout": "smart-grid",
            "parameters": {"cols": 3},
            "theme": {"primary_color": "#2563eb"},
            "widgets": {
                "header": {"type": "Type.Heading", "text": "Dashboard Overview", "level": 1},
                "col1": {"type": "Data.BigNum", "label": "Revenue", "value": "$1.2M", "variant": "primary"},
                "col2": {"type": "Data.BigNum", "label": "Users", "value": "25K", "variant": "success"},
                "col3": {"type": "Type.Body", "text": "Growth trends looking positive."}
            }
        }
        
        result = renderer.render_single_slide(slide)
        
        # Verify frontmatter
        assert result.startswith("---")
        assert "layout: smart-grid" in result
        assert "theme: business" in result
        assert "cols: 3" in result
        
        # Verify slots
        assert "::header::" in result
        assert "Dashboard Overview" in result
        assert "::col1::" in result
        assert "<MetricCard" in result
        assert "::col2::" in result
        assert "::col3::" in result
    
    def test_render_hero_split_slide(self):
        """Verify hero-split layout renders with left/right slots."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        slide = {
            "layout": "hero-split",
            "parameters": {"ratio": "60-40"},
            "widgets": {
                "left": {"type": "Type.Display", "text": "Big Announcement"},
                "right": {"type": "Type.Body", "text": "Details here."}
            }
        }
        
        result = renderer.render_single_slide(slide)
        
        assert "layout: hero-split" in result
        assert "ratio: 60-40" in result or "ratio: '60-40'" in result
        assert "::left::" in result
        assert "::right::" in result
    
    def test_render_raises_error_for_missing_layout(self):
        """Verify ValueError raised if layout field missing."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        slide = {"widgets": {}}
        
        with pytest.raises(ValueError, match="layout"):
            renderer.render_single_slide(slide)
    
    def test_render_raises_error_for_missing_widgets(self):
        """Verify ValueError raised if widgets field missing."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        slide = {"layout": "smart-grid"}
        
        with pytest.raises(ValueError, match="widgets"):
            renderer.render_single_slide(slide)
