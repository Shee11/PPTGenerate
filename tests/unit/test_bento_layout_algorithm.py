"""Unit tests for Bento layout strategy calculate_layout() algorithms."""
import pytest
from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.common.measurement import MeasuredSize
from src.layout.layout_protocol import LayoutContext, WidgetLayoutInput
from src.layout.strategies.bento import (
    BentoStandardStrategy,
    BentoHeroLeftStrategy,
    BentoHeroTopStrategy,
    BentoQuarterStrategy,
)


class TestBentoStandardCalculateLayout:
    """Test BentoStandardStrategy.calculate_layout() algorithm."""
    
    def test_standard_grid_3x2_equal_cells(self):
        """Test that 3x2 grid creates equal-sized cells."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        # Create 6 widgets
        widgets = [
            WidgetLayoutInput(
                role=f"cell_{i}",
                measured_size=MeasuredSize(width=100, height=100),
                slot=Slot(role=f"cell_{i}", size=SizeClass.S),
                style={}
            )
            for i in range(1, 7)
        ]
        
        bounds_map = BentoStandardStrategy.calculate_layout(widgets, context)
        
        # Should have 6 cells
        assert len(bounds_map) == 6
        
        # Calculate expected cell dimensions
        # content_width = 1200 - (40 * 2) = 1120
        # content_height = 800 - (30 * 2) = 740
        # cell_width = (1120 - 40) / 3 = 360
        # cell_height = (740 - 20) / 2 = 360
        expected_cell_width = 360
        expected_cell_height = 360
        
        # All cells should have same size
        for role in [f"cell_{i}" for i in range(1, 7)]:
            bounds = bounds_map[role]
            assert bounds.width == expected_cell_width
            assert bounds.height == expected_cell_height
    
    def test_standard_grid_positioning(self):
        """Test that cells are positioned correctly in 3x2 grid."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role=f"cell_{i}",
                measured_size=MeasuredSize(width=100, height=100),
                slot=Slot(role=f"cell_{i}", size=SizeClass.S),
                style={}
            )
            for i in range(1, 7)
        ]
        
        bounds_map = BentoStandardStrategy.calculate_layout(widgets, context)
        
        # Check first row (cell_1, cell_2, cell_3)
        assert bounds_map["cell_1"].x == 40  # content_x
        assert bounds_map["cell_1"].y == 30  # content_y
        
        # cell_2 should be offset by cell_width + gutter
        assert bounds_map["cell_2"].x == 40 + 360 + 20
        assert bounds_map["cell_2"].y == 30
        
        # cell_3 should be offset by 2 * (cell_width + gutter)
        assert bounds_map["cell_3"].x == 40 + (360 + 20) * 2
        assert bounds_map["cell_3"].y == 30
        
        # Check second row (cell_4, cell_5, cell_6)
        assert bounds_map["cell_4"].x == 40
        assert bounds_map["cell_4"].y == 30 + 360 + 20  # offset by cell_height + gutter
    
    def test_standard_grid_with_zero_gutter(self):
        """Test grid layout with no gutter spacing."""
        context = LayoutContext(
            canvas_width=900,
            canvas_height=600,
            margin_x=0,
            margin_y=0,
            gutter=0
        )
        
        widgets = [
            WidgetLayoutInput(
                role=f"cell_{i}",
                measured_size=MeasuredSize(width=100, height=100),
                slot=Slot(role=f"cell_{i}", size=SizeClass.S),
                style={}
            )
            for i in range(1, 7)
        ]
        
        bounds_map = BentoStandardStrategy.calculate_layout(widgets, context)
        
        # With no gutter: cell_width = 900 / 3 = 300, cell_height = 600 / 2 = 300
        assert bounds_map["cell_1"].width == 300
        assert bounds_map["cell_1"].height == 300
        
        # Cells should be adjacent with no gap
        assert bounds_map["cell_2"].x == 300
        assert bounds_map["cell_4"].y == 300


class TestBentoHeroLeftCalculateLayout:
    """Test BentoHeroLeftStrategy.calculate_layout() algorithm."""
    
    def test_hero_left_2_3_split(self):
        """Test that hero takes 2/3 width and side cells take 1/3."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="hero",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="hero", size=SizeClass.L),
                style={}
            ),
            WidgetLayoutInput(
                role="side_1",
                measured_size=MeasuredSize(width=100, height=100),
                slot=Slot(role="side_1", size=SizeClass.S),
                style={}
            ),
        ]
        
        bounds_map = BentoHeroLeftStrategy.calculate_layout(widgets, context)
        
        # content_width = 1120, gutter = 20
        # hero_width = 1120 * 2/3 - 10 = 736.67
        
        hero_bounds = bounds_map["hero"]
        assert abs(hero_bounds.width - 736.67) < 0.1
        assert hero_bounds.height == 740  # Full height
    
    def test_hero_left_side_cells_2x2_grid(self):
        """Test that 4 side cells are arranged in 2x2 grid."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="main",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="main", size=SizeClass.L),
                style={}
            ),
            *[
                WidgetLayoutInput(
                    role=f"side_{i}",
                    measured_size=MeasuredSize(width=100, height=100),
                    slot=Slot(role=f"side_{i}", size=SizeClass.S),
                    style={}
                )
                for i in range(1, 5)
            ]
        ]
        
        bounds_map = BentoHeroLeftStrategy.calculate_layout(widgets, context)
        
        # All side cells should have same width
        side_1 = bounds_map["side_1"]
        side_2 = bounds_map["side_2"]
        assert abs(side_1.width - side_2.width) < 0.01
        
        # Side cells should be in 2x2 arrangement
        # side_1 and side_2 should be in first row
        assert side_1.y == side_2.y
        # side_3 and side_4 should be in second row
        assert bounds_map["side_3"].y == bounds_map["side_4"].y
        # Second row should be below first row
        assert bounds_map["side_3"].y > side_1.y


class TestBentoHeroTopCalculateLayout:
    """Test BentoHeroTopStrategy.calculate_layout() algorithm."""
    
    def test_hero_top_2_3_height(self):
        """Test that hero takes 2/3 height and footer takes 1/3."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=900,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="hero",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="hero", size=SizeClass.L),
                style={}
            ),
        ]
        
        bounds_map = BentoHeroTopStrategy.calculate_layout(widgets, context)
        
        # content_height = 840, gutter = 20
        # hero_height = 840 * 2/3 - 10 = 550
        
        hero_bounds = bounds_map["hero"]
        assert abs(hero_bounds.height - 550) < 0.1
        assert hero_bounds.width == 1120  # Full width
    
    def test_hero_top_footer_cells(self):
        """Test that 2 footer cells split width equally."""
        context = LayoutContext(
            canvas_width=1200,
            canvas_height=900,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role="hero",
                measured_size=MeasuredSize(width=500, height=500),
                slot=Slot(role="hero", size=SizeClass.L),
                style={}
            ),
            WidgetLayoutInput(
                role="footer_1",
                measured_size=MeasuredSize(width=100, height=100),
                slot=Slot(role="footer_1", size=SizeClass.S),
                style={}
            ),
            WidgetLayoutInput(
                role="footer_2",
                measured_size=MeasuredSize(width=100, height=100),
                slot=Slot(role="footer_2", size=SizeClass.S),
                style={}
            ),
        ]
        
        bounds_map = BentoHeroTopStrategy.calculate_layout(widgets, context)
        
        # Footer cells should have equal width
        footer_1 = bounds_map["footer_1"]
        footer_2 = bounds_map["footer_2"]
        
        assert abs(footer_1.width - footer_2.width) < 0.01
        assert footer_1.height == footer_2.height
        
        # Footer cells should be side by side
        assert footer_1.y == footer_2.y
        assert footer_2.x > footer_1.x


class TestBentoQuarterCalculateLayout:
    """Test BentoQuarterStrategy.calculate_layout() algorithm."""
    
    def test_quarter_2x2_equal_cells(self):
        """Test that 2x2 grid creates 4 equal M-sized cells."""
        context = LayoutContext(
            canvas_width=1000,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role=f"quadrant_{i}",
                measured_size=MeasuredSize(width=200, height=200),
                slot=Slot(role=f"quadrant_{i}", size=SizeClass.M),
                style={}
            )
            for i in range(1, 5)
        ]
        
        bounds_map = BentoQuarterStrategy.calculate_layout(widgets, context)
        
        # Should have 4 quadrants
        assert len(bounds_map) == 4
        
        # content_width = 920, content_height = 740
        # cell_width = (920 - 20) / 2 = 450
        # cell_height = (740 - 20) / 2 = 360
        
        quad_1 = bounds_map["quadrant_1"]
        assert quad_1.width == 450
        assert quad_1.height == 360
        
        # All cells should have same size
        for i in range(1, 5):
            bounds = bounds_map[f"quadrant_{i}"]
            assert bounds.width == 450
            assert bounds.height == 360
    
    def test_quarter_positioning(self):
        """Test that quadrants are positioned correctly."""
        context = LayoutContext(
            canvas_width=1000,
            canvas_height=800,
            margin_x=40,
            margin_y=30,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(
                role=f"quadrant_{i}",
                measured_size=MeasuredSize(width=200, height=200),
                slot=Slot(role=f"quadrant_{i}", size=SizeClass.M),
                style={}
            )
            for i in range(1, 5)
        ]
        
        bounds_map = BentoQuarterStrategy.calculate_layout(widgets, context)
        
        # Top-left quadrant
        assert bounds_map["quadrant_1"].x == 40
        assert bounds_map["quadrant_1"].y == 30
        
        # Top-right quadrant
        assert bounds_map["quadrant_2"].x == 40 + 450 + 20
        assert bounds_map["quadrant_2"].y == 30
        
        # Bottom-left quadrant
        assert bounds_map["quadrant_3"].x == 40
        assert bounds_map["quadrant_3"].y == 30 + 360 + 20
        
        # Bottom-right quadrant
        assert bounds_map["quadrant_4"].x == 40 + 450 + 20
        assert bounds_map["quadrant_4"].y == 30 + 360 + 20
