"""Unit tests for LayoutContext calculation."""
import pytest
from src.paged.layout.layout_protocol import LayoutContext


class TestLayoutContext:
    """Test the LayoutContext model for layout calculation."""
    
    def test_create_layout_context_basic(self):
        """Test creating a LayoutContext with basic values."""
        context = LayoutContext(
            canvas_width=1920,
            canvas_height=1080,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        assert context.canvas_width == 1920
        assert context.canvas_height == 1080
        assert context.margin_x == 40
        assert context.margin_y == 30
        assert context.gutter == 20
    
    def test_layout_context_calculates_content_area(self):
        """Test that LayoutContext calculates content area correctly."""
        context = LayoutContext(
            canvas_width=1920,
            canvas_height=1080,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        # Content area excludes margins
        assert context.content_x == 40  # margin_x
        assert context.content_y == 30  # margin_y
        assert context.content_width == 1840  # 1920 - (40 * 2)
        assert context.content_height == 1020  # 1080 - (30 * 2)
    
    def test_layout_context_with_header(self):
        """Test LayoutContext with header height."""
        context = LayoutContext(
            canvas_width=1920,
            canvas_height=1080,
            margin_x=40,
            margin_y=30,
            gutter=20,
            header_height=100
        )
        
        # Content y starts after margin + header
        assert context.content_y == 130  # margin_y + header_height
        # Content height excludes margins and header
        assert context.content_height == 920  # 1080 - (30 * 2) - 100
    
    def test_layout_context_with_footer(self):
        """Test LayoutContext with footer height."""
        context = LayoutContext(
            canvas_width=1920,
            canvas_height=1080,
            margin_x=40,
            margin_y=30,
            gutter=20,
            footer_height=80
        )
        
        # Footer reduces content height but doesn't affect content_y
        assert context.content_y == 30  # Just margin_y
        assert context.content_height == 940  # 1080 - (30 * 2) - 80
    
    def test_layout_context_with_header_and_footer(self):
        """Test LayoutContext with both header and footer."""
        context = LayoutContext(
            canvas_width=1920,
            canvas_height=1080,
            margin_x=40,
            margin_y=30,
            gutter=20,
            header_height=100,
            footer_height=80
        )
        
        assert context.content_y == 130  # margin_y + header_height
        assert context.content_height == 840  # 1080 - (30 * 2) - 100 - 80
    
    def test_layout_context_zero_margins(self):
        """Test LayoutContext with zero margins."""
        context = LayoutContext(
            canvas_width=1920,
            canvas_height=1080,
            margin_x=0,
            margin_y=0,
            gutter=20
        )
        
        # Content area equals canvas when no margins
        assert context.content_x == 0
        assert context.content_y == 0
        assert context.content_width == 1920
        assert context.content_height == 1080
    
    def test_layout_context_small_canvas(self):
        """Test LayoutContext with small canvas (mobile)."""
        context = LayoutContext(
            canvas_width=375,
            canvas_height=667,
            margin_x=16,
            margin_y=16,
            gutter=12
        )
        
        assert context.content_width == 343  # 375 - (16 * 2)
        assert context.content_height == 635  # 667 - (16 * 2)
    
    def test_layout_context_large_margins(self):
        """Test LayoutContext with large margins."""
        context = LayoutContext(
            canvas_width=1920,
            canvas_height=1080,
            margin_x=200,
            margin_y=150,
            gutter=20
        )
        
        assert context.content_width == 1520  # 1920 - (200 * 2)
        assert context.content_height == 780  # 1080 - (150 * 2)
    
    def test_layout_context_gutter_stored(self):
        """Test that gutter value is stored correctly."""
        context = LayoutContext(
            canvas_width=1920,
            canvas_height=1080,
            margin_x=40,
            margin_y=30,
            gutter=15
        )
        
        # Gutter is used by strategies for spacing between widgets
        assert context.gutter == 15
    
    def test_layout_context_attributes_accessible(self):
        """Test that all context attributes are accessible."""
        context = LayoutContext(
            canvas_width=1920,
            canvas_height=1080,
            margin_x=40,
            margin_y=30,
            gutter=20,
            header_height=100,
            footer_height=80
        )
        
        # All attributes should be accessible
        assert hasattr(context, 'canvas_width')
        assert hasattr(context, 'canvas_height')
        assert hasattr(context, 'margin_x')
        assert hasattr(context, 'margin_y')
        assert hasattr(context, 'gutter')
        assert hasattr(context, 'header_height')
        assert hasattr(context, 'footer_height')
        assert hasattr(context, 'content_x')
        assert hasattr(context, 'content_y')
        assert hasattr(context, 'content_width')
        assert hasattr(context, 'content_height')
