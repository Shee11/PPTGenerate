"""Unit tests for Cinematic layout strategy calculate_layout() algorithms."""
import pytest
from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.common.measurement import MeasuredSize
from src.paged.layout.layout_protocol import LayoutContext, WidgetLayoutInput
from src.paged.layout.strategies.cinematic import (
    CinematicSplit5050Strategy,
    CinematicFullBleedStrategy,
    CinematicSplit3070Strategy,
)


class TestCinematicSplit5050CalculateLayout:
    """Test CinematicSplit5050Strategy.calculate_layout() algorithm."""
    
    def test_split_50_50_equal_width(self):
        """Test that left and right panels have equal width."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="left",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="left", size=SizeClass.L),
                style={}
            ),
            WidgetLayoutInput(
                role="right",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="right", size=SizeClass.L),
                style={}
            ),
        ]
        
        bounds_map = CinematicSplit5050Strategy.calculate_layout(widgets, context)
        
        # content_width = 1120, gutter = 20
        # panel_width = (1120 - 20) / 2 = 550
        
        left_bounds = bounds_map["left"]
        right_bounds = bounds_map["right"]
        
        assert left_bounds.width == 550
        assert right_bounds.width == 550
    
    def test_split_50_50_full_height(self):
        """Test that both panels take full content height."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="left",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="left", size=SizeClass.L),
                style={}
            ),
            WidgetLayoutInput(
                role="right",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="right", size=SizeClass.L),
                style={}
            ),
        ]
        
        bounds_map = CinematicSplit5050Strategy.calculate_layout(widgets, context)
        
        left_bounds = bounds_map["left"]
        right_bounds = bounds_map["right"]
        
        # content_height = 740
        assert left_bounds.height == 740
        assert right_bounds.height == 740
        
        # Both should be at same vertical position
        assert left_bounds.y == 30
        assert right_bounds.y == 30
    
    def test_split_50_50_positioning(self):
        """Test that right panel is positioned after left panel with gutter."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="left",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="left", size=SizeClass.L),
                style={}
            ),
            WidgetLayoutInput(
                role="right",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="right", size=SizeClass.L),
                style={}
            ),
        ]
        
        bounds_map = CinematicSplit5050Strategy.calculate_layout(widgets, context)
        
        left_bounds = bounds_map["left"]
        right_bounds = bounds_map["right"]
        
        # Left should be at content_x
        assert left_bounds.x == 40
        
        # Right should be positioned after left + gutter
        expected_right_x = 40 + 550 + 20
        assert right_bounds.x == expected_right_x


class TestCinematicFullBleedCalculateLayout:
    """Test CinematicFullBleedStrategy.calculate_layout() algorithm."""
    
    def test_full_bleed_fills_content_area(self):
        """Test that stage fills entire content area."""
        context = LayoutContext(
            canvas_width=1920,
            canvas_height=1080,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="stage",
                measured_size=MeasuredSize(width=1000, height=800),
                slot=Slot(role="stage", size=SizeClass.XL),
                style={}
            ),
        ]
        
        bounds_map = CinematicFullBleedStrategy.calculate_layout(widgets, context)
        
        stage_bounds = bounds_map["stage"]
        
        # Should fill entire content area
        assert stage_bounds.x == 40
        assert stage_bounds.y == 30
        assert stage_bounds.width == 1840  # content_width
        assert stage_bounds.height == 1020  # content_height
    
    def test_full_bleed_with_zero_margins(self):
        """Test full bleed with no margins (true full bleed)."""
        context = LayoutContext(
            canvas_width=1920,
            canvas_height=1080,
            margin_x=0,
            margin_y=0,
            gutter=0
        )
        
        widgets = [
            WidgetLayoutInput(
                role="stage",
                measured_size=MeasuredSize(width=1000, height=800),
                slot=Slot(role="stage", size=SizeClass.XL),
                style={}
            ),
        ]
        
        bounds_map = CinematicFullBleedStrategy.calculate_layout(widgets, context)
        
        stage_bounds = bounds_map["stage"]
        
        # Should fill entire canvas
        assert stage_bounds.x == 0
        assert stage_bounds.y == 0
        assert stage_bounds.width == 1920
        assert stage_bounds.height == 1080


class TestCinematicSplit3070CalculateLayout:
    """Test CinematicSplit3070Strategy.calculate_layout() algorithm."""
    
    def test_split_30_70_width_proportions(self):
        """Test that sidebar takes 30% and stage takes 70% of width."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="sidebar",
                measured_size=MeasuredSize(width=200, height=500),
                slot=Slot(role="sidebar", size=SizeClass.M),
                style={}
            ),
            WidgetLayoutInput(
                role="stage",
                measured_size=MeasuredSize(width=600, height=500),
                slot=Slot(role="stage", size=SizeClass.XL),
                style={}
            ),
        ]
        
        bounds_map = CinematicSplit3070Strategy.calculate_layout(widgets, context)
        
        # content_width = 1120, gutter = 20
        # sidebar_width = 1120 * 0.3 - 10 = 326
        # stage_width = 1120 * 0.7 - 10 = 774
        
        sidebar_bounds = bounds_map["sidebar"]
        stage_bounds = bounds_map["stage"]
        
        assert sidebar_bounds.width == 326
        assert stage_bounds.width == 774
    
    def test_split_30_70_full_height(self):
        """Test that both sidebar and stage take full content height."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="sidebar",
                measured_size=MeasuredSize(width=200, height=500),
                slot=Slot(role="sidebar", size=SizeClass.M),
                style={}
            ),
            WidgetLayoutInput(
                role="stage",
                measured_size=MeasuredSize(width=600, height=500),
                slot=Slot(role="stage", size=SizeClass.XL),
                style={}
            ),
        ]
        
        bounds_map = CinematicSplit3070Strategy.calculate_layout(widgets, context)
        
        sidebar_bounds = bounds_map["sidebar"]
        stage_bounds = bounds_map["stage"]
        
        # content_height = 740
        assert sidebar_bounds.height == 740
        assert stage_bounds.height == 740
        
        # Both should be at same vertical position
        assert sidebar_bounds.y == 30
        assert stage_bounds.y == 30
    
    def test_split_30_70_positioning(self):
        """Test that stage is positioned after sidebar with gutter."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="sidebar",
                measured_size=MeasuredSize(width=200, height=500),
                slot=Slot(role="sidebar", size=SizeClass.M),
                style={}
            ),
            WidgetLayoutInput(
                role="stage",
                measured_size=MeasuredSize(width=600, height=500),
                slot=Slot(role="stage", size=SizeClass.XL),
                style={}
            ),
        ]
        
        bounds_map = CinematicSplit3070Strategy.calculate_layout(widgets, context)
        
        sidebar_bounds = bounds_map["sidebar"]
        stage_bounds = bounds_map["stage"]
        
        # Sidebar should be at content_x
        assert sidebar_bounds.x == 40
        
        # Stage should be positioned after sidebar + gutter
        expected_stage_x = 40 + 326 + 20
        assert stage_bounds.x == expected_stage_x
    
    def test_split_30_70_with_different_canvas_size(self):
        """Test proportions hold with different canvas dimensions."""
        context = LayoutContext(
            canvas_width=2000,
            canvas_height=1000,
            margin_x=50,
            margin_y=40,
            gutter=30
        )
        
        widgets = [
            WidgetLayoutInput(
                role="sidebar",
                measured_size=MeasuredSize(width=200, height=500),
                slot=Slot(role="sidebar", size=SizeClass.M),
                style={}
            ),
            WidgetLayoutInput(
                role="stage",
                measured_size=MeasuredSize(width=600, height=500),
                slot=Slot(role="stage", size=SizeClass.XL),
                style={}
            ),
        ]
        
        bounds_map = CinematicSplit3070Strategy.calculate_layout(widgets, context)
        
        # content_width = 1900, gutter = 30
        # sidebar_width = 1900 * 0.3 - 15 = 555
        # stage_width = 1900 * 0.7 - 15 = 1315
        
        sidebar_bounds = bounds_map["sidebar"]
        stage_bounds = bounds_map["stage"]
        
        assert sidebar_bounds.width == 555
        assert stage_bounds.width == 1315
