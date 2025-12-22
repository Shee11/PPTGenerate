"""Unit tests for Slidev frontmatter generation."""
import pytest


class TestFrontmatterGeneration:
    """Test YAML frontmatter generation from slide JSON."""
    
    def test_frontmatter_includes_layout_field(self):
        """Verify frontmatter contains layout from JSON."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        slide = {
            "layout": "smart-grid",
            "parameters": {"cols": 3},
            "widgets": {}
        }
        
        result = renderer._generate_frontmatter(slide)
        assert "layout:" in result
        assert "smart-grid" in result
    
    def test_frontmatter_includes_theme_field(self):
        """Verify frontmatter contains resolved theme."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        slide = {
            "layout": "smart-grid",
            "theme": {"primary_color": "#2563eb"},
            "widgets": {}
        }
        
        result = renderer._generate_frontmatter(slide)
        assert "theme:" in result
        assert "business" in result
    
    def test_frontmatter_includes_cols_parameter(self):
        """Verify frontmatter includes cols parameter for smart-grid."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        slide = {
            "layout": "smart-grid",
            "parameters": {"cols": 4},
            "widgets": {}
        }
        
        result = renderer._generate_frontmatter(slide)
        assert "cols:" in result
        assert "4" in result
    
    def test_frontmatter_includes_ratio_parameter(self):
        """Verify frontmatter includes ratio parameter for hero-split."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        slide = {
            "layout": "hero-split",
            "parameters": {"ratio": "60-40"},
            "widgets": {}
        }
        
        result = renderer._generate_frontmatter(slide)
        assert "ratio:" in result
        assert "60-40" in result
    
    def test_frontmatter_yaml_format(self):
        """Verify frontmatter is valid YAML wrapped in ---."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        slide = {
            "layout": "full-bleed",
            "parameters": {"align": "center"},
            "widgets": {}
        }
        
        result = renderer._generate_frontmatter(slide)
        assert result.startswith("---")
        assert result.strip().endswith("---")
