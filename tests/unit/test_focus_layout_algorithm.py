"""Tests for Focus family layout algorithm implementations."""
import math
import pytest

from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.common.measurement import MeasuredSize
from src.paged.layout.layout_protocol import LayoutContext, WidgetLayoutInput
from src.paged.layout.strategies.focus import (
    FocusSolarSystemStrategy,
    FocusOffsetTitleStrategy,
)


class TestFocusSolarSystemLayout:
    """Test FocusSolarSystemStrategy.calculate_layout()."""
    
    def test_sun_is_40_percent_size(self) -> None:
        """Test that sun is 40% of content dimensions."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="sun", measured_size=MeasuredSize(width=600, height=320), slot=Slot(role="sun", size=SizeClass.XL), style={}),
            WidgetLayoutInput(role="planet_1", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_1", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_2", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_2", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_3", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_3", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_4", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_4", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_5", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_5", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_6", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_6", size=SizeClass.S), style={})
        ]
        
        layout = FocusSolarSystemStrategy.calculate_layout(widgets, context)
        sun = layout["sun"]
        
        # sun_size = min(content_width, content_height) * 0.4 = 800 * 0.4 = 320 (square)
        assert sun.width == 320
        assert sun.height == 320
    
    def test_sun_is_centered(self) -> None:
        """Test that sun is centered in content area."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="sun", measured_size=MeasuredSize(width=600, height=320), slot=Slot(role="sun", size=SizeClass.XL), style={}),
            WidgetLayoutInput(role="planet_1", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_1", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_2", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_2", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_3", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_3", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_4", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_4", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_5", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_5", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_6", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_6", size=SizeClass.S), style={})
        ]
        
        layout = FocusSolarSystemStrategy.calculate_layout(widgets, context)
        sun = layout["sun"]
        
        # sun_size = min(content_width, content_height) * 0.4 = 320
        # sun_x = content_x + (content_width - sun_size) / 2 = 50 + (1500 - 320) / 2 = 640
        # sun_y = content_y + (content_height - sun_size) / 2 = 50 + (800 - 320) / 2 = 290
        assert sun.x == 640
        assert sun.y == 290
    
    def test_planets_are_12_percent_size(self) -> None:
        """Test that all planets are 12% of content dimensions."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="sun", measured_size=MeasuredSize(width=600, height=320), slot=Slot(role="sun", size=SizeClass.XL), style={}),
            WidgetLayoutInput(role="planet_1", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_1", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_2", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_2", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_3", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_3", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_4", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_4", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_5", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_5", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="planet_6", measured_size=MeasuredSize(width=180, height=96), slot=Slot(role="planet_6", size=SizeClass.S), style={})
        ]
        
        layout = FocusSolarSystemStrategy.calculate_layout(widgets, context)
        
        # planet_size = min(content_width, content_height) * 0.12 = 800 * 0.12 = 96 (square)
        expected_size = 96
        
        for i in range(1, 7):
            planet = layout[f"planet_{i}"]
            assert planet.width == expected_size
            assert planet.height == expected_size


class TestFocusOffsetTitleLayout:
    """Test FocusOffsetTitleStrategy.calculate_layout()."""
    
    def test_main_is_30_percent_width(self) -> None:
        """Test that main element is 30% of content width."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="main", measured_size=MeasuredSize(width=450, height=120), slot=Slot(role="main", size=SizeClass.M), style={})
        ]
        
        layout = FocusOffsetTitleStrategy.calculate_layout(widgets, context)
        main = layout["main"]
        
        # main_width = content_width * 0.3 = 1500 * 0.3 = 450
        assert main.width == 450
    
    def test_main_is_15_percent_height(self) -> None:
        """Test that main element is 15% of content height."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="main", measured_size=MeasuredSize(width=450, height=120), slot=Slot(role="main", size=SizeClass.M), style={})
        ]
        
        layout = FocusOffsetTitleStrategy.calculate_layout(widgets, context)
        main = layout["main"]
        
        # main_height = content_height * 0.15 = 800 * 0.15 = 120
        assert main.height == 120
    
    def test_main_in_bottom_left_corner(self) -> None:
        """Test that main element is positioned in bottom-left corner."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="main", measured_size=MeasuredSize(width=450, height=120), slot=Slot(role="main", size=SizeClass.M), style={})
        ]
        
        layout = FocusOffsetTitleStrategy.calculate_layout(widgets, context)
        main = layout["main"]
        
        # main_x = content_x = 50
        assert main.x == 50
        
        # main_y = content_y + content_height - main_height = 50 + 800 - 120 = 730
        assert main.y == 730

