"""Contract tests for Slidev Renderer protocol compliance."""
import pytest


class TestSlidevRendererProtocol:
    """Test that SlidevRenderer implements the Renderer protocol."""
    
    def test_renderer_has_render_method(self):
        """Verify SlidevRenderer has render() method."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        assert hasattr(renderer, 'render')
        assert callable(renderer.render)
    
    def test_renderer_has_render_single_slide_method(self):
        """Verify SlidevRenderer has render_single_slide() method."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        assert hasattr(renderer, 'render_single_slide')
        assert callable(renderer.render_single_slide)
    
    def test_renderer_has_render_multi_slide_method(self):
        """Verify SlidevRenderer has render_multi_slide() method."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        assert hasattr(renderer, 'render_multi_slide')
        assert callable(renderer.render_multi_slide)
    
    def test_renderer_initializes_successfully(self):
        """Verify SlidevRenderer can be instantiated."""
        from src.paged.render.slidev.markdown_renderer import SlidevRenderer
        
        renderer = SlidevRenderer()
        assert renderer is not None
