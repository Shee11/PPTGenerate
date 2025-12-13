"""Unit tests for Swiss layout strategy calculate_layout() algorithms."""
import pytest
from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.common.measurement import MeasuredSize
from src.layout.layout_protocol import LayoutContext, WidgetLayoutInput
from src.layout.strategies.swiss import (
    SwissPosterStrategy,
    SwissAsymmetryStrategy,
    SwissSplitTypoStrategy,
)


class TestSwissPosterCalculateLayout:
    """Test SwissPosterStrategy.calculate_layout() algorithm."""
    
    def test_poster_full_content_area(self):
        """Test that poster strategy fills entire content area."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="headline",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="headline", size=SizeClass.XL),
                style={}
            ),
        ]
        
        bounds_map = SwissPosterStrategy.calculate_layout(widgets, context)
        
        # Should fill entire content area
        content_bounds = bounds_map["headline"]
        assert content_bounds.x == 40  # content_x
        assert content_bounds.y == 30  # content_y
        assert content_bounds.width == 1120  # content_width
        assert content_bounds.height == 740  # content_height
    
    def test_poster_with_zero_margins(self):
        """Test poster strategy with no margins."""
        context = LayoutContext(
            canvas_width=1920,
            canvas_height=1080,
            margin_x=0,
            margin_y=0,
            gutter=0
        )
        
        widgets = [
            WidgetLayoutInput(
                role="headline",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="headline", size=SizeClass.XL),
                style={}
            ),
        ]
        
        bounds_map = SwissPosterStrategy.calculate_layout(widgets, context)
        
        # Should fill entire canvas
        content_bounds = bounds_map["headline"]
        assert content_bounds.x == 0
        assert content_bounds.y == 0
        assert content_bounds.width == 1920
        assert content_bounds.height == 1080


class TestSwissAsymmetryCalculateLayout:
    """Test SwissAsymmetryStrategy.calculate_layout() algorithm."""
    
    def test_asymmetry_40_60_split(self):
        """Test that content takes 60% width on right side."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="content",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="content", size=SizeClass.L),
                style={}
            ),
        ]
        
        bounds_map = SwissAsymmetryStrategy.calculate_layout(widgets, context)
        
        # content_width = 1120
        # void_width = 1120 * 0.4 = 448
        # content_width = 1120 * 0.6 = 672
        
        content_bounds = bounds_map["content"]
        assert abs(content_bounds.width - 672) < 0.1
        assert content_bounds.height == 740  # Full height
        
        # Content should be on right side (offset by void)
        assert abs(content_bounds.x - (40 + 448)) < 0.1
    
    def test_asymmetry_full_height(self):
        """Test that content takes full content height."""
        context = LayoutContext(
            canvas_width=1000,
            canvas_height=600,
            margin_x=50,
            margin_y=40,
            gutter=10
        )
        
        widgets = [
            WidgetLayoutInput(
                role="content",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="content", size=SizeClass.L),
                style={}
            ),
        ]
        
        bounds_map = SwissAsymmetryStrategy.calculate_layout(widgets, context)
        
        # content_height = 600 - (40 * 2) = 520
        content_bounds = bounds_map["content"]
        assert content_bounds.y == 40  # content_y
        assert content_bounds.height == 520


class TestSwissSplitTypoCalculateLayout:
    """Test SwissSplitTypoStrategy.calculate_layout() algorithm."""
    
    def test_split_typo_35_65_height(self):
        """Test that headline takes 35% and body takes 65% of height."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=900,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="headline",
                measured_size=MeasuredSize(width=500, height=200),
                slot=Slot(role="headline", size=SizeClass.M),
                style={}
            ),
            WidgetLayoutInput(
                role="body",
                measured_size=MeasuredSize(width=500, height=400),
                slot=Slot(role="body", size=SizeClass.L),
                style={}
            ),
        ]
        
        bounds_map = SwissSplitTypoStrategy.calculate_layout(widgets, context)
        
        headline_bounds = bounds_map["headline"]
        body_bounds = bounds_map["body"]
        
        # content_height = 840 (900 - 60), gutter = 20
        # headline_height = 840 * 0.35 - 10 = 284
        # body_height = 840 * 0.65 - 10 = 536
        assert abs(headline_bounds.height - 284) < 0.1
        assert abs(body_bounds.height - 536) < 0.1
    
    def test_split_typo_full_width(self):
        """Test that both headline and body take full content width."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=900,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="headline",
                measured_size=MeasuredSize(width=500, height=200),
                slot=Slot(role="headline", size=SizeClass.M),
                style={}
            ),
            WidgetLayoutInput(
                role="body",
                measured_size=MeasuredSize(width=500, height=400),
                slot=Slot(role="body", size=SizeClass.L),
                style={}
            ),
        ]
        
        bounds_map = SwissSplitTypoStrategy.calculate_layout(widgets, context)
        
        headline_bounds = bounds_map["headline"]
        body_bounds = bounds_map["body"]
        
        # Both should have full content width (1120)
        assert headline_bounds.width == 1120
        assert body_bounds.width == 1120
        
        # Both should start at content_x
        assert headline_bounds.x == 40
        assert body_bounds.x == 40
    
    def test_split_typo_vertical_positioning(self):
        """Test that body is positioned below headline with gutter."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=900,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="headline",
                measured_size=MeasuredSize(width=500, height=200),
                slot=Slot(role="headline", size=SizeClass.M),
                style={}
            ),
            WidgetLayoutInput(
                role="body",
                measured_size=MeasuredSize(width=500, height=400),
                slot=Slot(role="body", size=SizeClass.L),
                style={}
            ),
        ]
        
        bounds_map = SwissSplitTypoStrategy.calculate_layout(widgets, context)
        
        headline_bounds = bounds_map["headline"]
        body_bounds = bounds_map["body"]
        
        # Headline should be at content_y
        assert headline_bounds.y == 30
        
        # Body should be positioned after headline + gutter
        expected_body_y = 30 + headline_bounds.height + 20
        assert abs(body_bounds.y - expected_body_y) < 0.1
