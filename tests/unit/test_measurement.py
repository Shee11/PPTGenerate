"""Unit tests for WidgetMeasurement utilities."""
import pytest
from src.common.measurement import MeasuredSize, WidgetMeasurement


class TestMeasuredSize:
    """Test the MeasuredSize dataclass."""
    
    def test_create_measured_size(self):
        """Test creating a MeasuredSize with basic dimensions."""
        size = MeasuredSize(width=100, height=50)
        
        assert size.width == 100
        assert size.height == 50
        assert size.min_width == 0
        assert size.min_height == 0
        assert size.max_width == float('inf')
        assert size.max_height == float('inf')
    
    def test_measured_size_with_constraints(self):
        """Test MeasuredSize with min/max constraints."""
        size = MeasuredSize(
            width=100, height=50,
            min_width=50, min_height=25,
            max_width=200, max_height=100
        )
        
        assert size.width == 100
        assert size.height == 50
        assert size.min_width == 50
        assert size.min_height == 25
        assert size.max_width == 200
        assert size.max_height == 100
    
    def test_constrain_within_available_space(self):
        """Test constraining size to available space."""
        size = MeasuredSize(width=100, height=50)
        
        constrained = size.constrain(available_width=150, available_height=75)
        
        # Size fits within available space, so no change
        assert constrained.width == 100
        assert constrained.height == 50
    
    def test_constrain_exceeds_available_width(self):
        """Test constraining when width exceeds available space."""
        size = MeasuredSize(width=200, height=50)
        
        constrained = size.constrain(available_width=100, available_height=75)
        
        assert constrained.width == 100  # Clamped to available
        assert constrained.height == 50  # Unchanged
    
    def test_constrain_exceeds_available_height(self):
        """Test constraining when height exceeds available space."""
        size = MeasuredSize(width=100, height=200)
        
        constrained = size.constrain(available_width=150, available_height=75)
        
        assert constrained.width == 100  # Unchanged
        assert constrained.height == 75  # Clamped to available
    
    def test_constrain_respects_min_width(self):
        """Test that constraining respects minimum width."""
        size = MeasuredSize(width=100, height=50, min_width=80)
        
        constrained = size.constrain(available_width=50, available_height=75)
        
        assert constrained.width == 80  # Uses min_width, not available
        assert constrained.height == 50
    
    def test_constrain_respects_min_height(self):
        """Test that constraining respects minimum height."""
        size = MeasuredSize(width=100, height=50, min_height=60)
        
        constrained = size.constrain(available_width=150, available_height=30)
        
        assert constrained.width == 100
        assert constrained.height == 60  # Uses min_height, not available
    
    def test_constrain_respects_max_width(self):
        """Test that constraining respects maximum width."""
        size = MeasuredSize(width=100, height=50, max_width=80)
        
        constrained = size.constrain(available_width=200, available_height=75)
        
        assert constrained.width == 80  # Uses max_width
        assert constrained.height == 50
    
    def test_constrain_respects_max_height(self):
        """Test that constraining respects maximum height."""
        size = MeasuredSize(width=100, height=50, max_height=40)
        
        constrained = size.constrain(available_width=150, available_height=100)
        
        assert constrained.width == 100
        assert constrained.height == 40  # Uses max_height


class TestWidgetMeasurement:
    """Test the WidgetMeasurement utility class."""
    
    def test_measure_text_single_line(self):
        """Test measuring single-line text."""
        text = "Hello World"
        font_size = 16
        
        size = WidgetMeasurement.measure_text_widget(
            text=text,
            font_size=font_size,
            max_width=float('inf'),  # No wrapping
            padding=20
        )
        
        # Should have width based on characters + padding
        assert size.width > 0
        assert size.height > 0
        assert size.height > font_size  # At least font size + padding
    
    def test_measure_text_with_wrapping(self):
        """Test measuring text that wraps to multiple lines."""
        text = "This is a long text that should wrap to multiple lines"
        font_size = 16
        
        size = WidgetMeasurement.measure_text_widget(
            text=text,
            font_size=font_size,
            max_width=100,  # Force wrapping
            padding=20
        )
        
        # Wrapped text should be taller than single line
        single_line = WidgetMeasurement.measure_text_widget(
            text=text,
            font_size=font_size,
            max_width=float('inf'),  # No wrapping
            padding=20
        )
        
        assert size.height > single_line.height
    
    def test_measure_text_with_custom_line_height(self):
        """Test measuring text with custom line height."""
        text = "Line 1\nLine 2\nLine 3"
        font_size = 16
        
        size_normal = WidgetMeasurement.measure_text_widget(
            text=text,
            font_size=font_size,
            line_height=1.2,
            padding=0
        )
        
        size_loose = WidgetMeasurement.measure_text_widget(
            text=text,
            font_size=font_size,
            line_height=2.0,  # Double spacing
            padding=0
        )
        
        assert size_loose.height > size_normal.height
    
    def test_measure_text_empty_string(self):
        """Test measuring empty text."""
        size = WidgetMeasurement.measure_text_widget(
            text="",
            font_size=16,
            padding=20
        )
        
        # Even empty text has size due to font metrics + padding
        assert size.width > 0
        assert size.height > 0
    
    def test_measure_text_padding_affects_size(self):
        """Test that padding increases measured size."""
        text = "Test"
        font_size = 16
        
        size_no_padding = WidgetMeasurement.measure_text_widget(
            text=text,
            font_size=font_size,
            padding=0
        )
        
        size_with_padding = WidgetMeasurement.measure_text_widget(
            text=text,
            font_size=font_size,
            padding=40
        )
        
        assert size_with_padding.width > size_no_padding.width
        assert size_with_padding.height > size_no_padding.height
