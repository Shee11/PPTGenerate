"""Tests for Data family layout algorithm implementations."""
import pytest

from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.common.measurement import MeasuredSize
from src.paged.layout.layout_protocol import LayoutContext, WidgetLayoutInput
from src.paged.layout.strategies.data import DataKPIRowStrategy


class TestDataKPIRowLayout:
    """Test DataKPIRowStrategy.calculate_layout()."""
    
    def test_header_is_30_percent_height(self) -> None:
        """Test that header occupies 30% of content height."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="header", measured_size=MeasuredSize(width=1500, height=230), slot=Slot(role="header", size=SizeClass.M), style={}),
            WidgetLayoutInput(role="kpi_1", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_1", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="kpi_2", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_2", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="kpi_3", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_3", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="kpi_4", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_4", size=SizeClass.S), style={})
        ]
        
        layout = DataKPIRowStrategy.calculate_layout(widgets, context)
        header = layout["header"]
        
        # header_height = content_height * 0.3 - gutter/2 = 800 * 0.3 - 10 = 230
        assert header.height == 230
    
    def test_header_full_width(self) -> None:
        """Test that header spans full content width."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="header", measured_size=MeasuredSize(width=1500, height=230), slot=Slot(role="header", size=SizeClass.M), style={}),
            WidgetLayoutInput(role="kpi_1", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_1", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="kpi_2", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_2", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="kpi_3", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_3", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="kpi_4", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_4", size=SizeClass.S), style={})
        ]
        
        layout = DataKPIRowStrategy.calculate_layout(widgets, context)
        header = layout["header"]
        
        assert header.x == 50
        assert header.width == 1500
    
    def test_kpis_are_equal_width(self) -> None:
        """Test that all 4 KPIs have equal width."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="header", measured_size=MeasuredSize(width=1500, height=230), slot=Slot(role="header", size=SizeClass.M), style={}),
            WidgetLayoutInput(role="kpi_1", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_1", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="kpi_2", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_2", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="kpi_3", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_3", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="kpi_4", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_4", size=SizeClass.S), style={})
        ]
        
        layout = DataKPIRowStrategy.calculate_layout(widgets, context)
        
        # kpi_width = (content_width - gutter*3) / 4 = (1500 - 60) / 4 = 360
        expected_width = 360
        
        for i in range(1, 5):
            kpi = layout[f"kpi_{i}"]
            assert kpi.width == expected_width
    
    def test_kpis_are_evenly_spaced(self) -> None:
        """Test that KPIs are evenly spaced with gutter between them."""
        context = LayoutContext(
            canvas_width=1600,
            canvas_height=900,
            margin_x=50,
            margin_y=50,
            gutter=20
        )
        
        widgets = [
            WidgetLayoutInput(role="header", measured_size=MeasuredSize(width=1500, height=230), slot=Slot(role="header", size=SizeClass.M), style={}),
            WidgetLayoutInput(role="kpi_1", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_1", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="kpi_2", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_2", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="kpi_3", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_3", size=SizeClass.S), style={}),
            WidgetLayoutInput(role="kpi_4", measured_size=MeasuredSize(width=360, height=550), slot=Slot(role="kpi_4", size=SizeClass.S), style={})
        ]
        
        layout = DataKPIRowStrategy.calculate_layout(widgets, context)
        
        kpi1 = layout["kpi_1"]
        kpi2 = layout["kpi_2"]
        kpi3 = layout["kpi_3"]
        kpi4 = layout["kpi_4"]
        
        # Verify gutter spacing
        assert kpi2.x == kpi1.x + kpi1.width + 20
        assert kpi3.x == kpi2.x + kpi2.width + 20
        assert kpi4.x == kpi3.x + kpi3.width + 20

