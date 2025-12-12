"""Unit tests for size constraint validation logic."""
import pytest
from src.common.size_class import SizeClass
from src.common.exceptions import SizeConstraintError


class TestSizeValidation:
    """Test size constraint validation."""
    
    def test_size_class_ordering(self) -> None:
        """Test that size class ordering works correctly."""
        # S is smallest
        assert SizeClass.S < SizeClass.M
        assert SizeClass.S < SizeClass.L
        assert SizeClass.S < SizeClass.XL
        
        # M is middle-small
        assert SizeClass.M > SizeClass.S
        assert SizeClass.M < SizeClass.L
        assert SizeClass.M < SizeClass.XL
        
        # L is middle-large
        assert SizeClass.L > SizeClass.S
        assert SizeClass.L > SizeClass.M
        assert SizeClass.L < SizeClass.XL
        
        # XL is largest
        assert SizeClass.XL > SizeClass.S
        assert SizeClass.XL > SizeClass.M
        assert SizeClass.XL > SizeClass.L
    
    def test_widget_fits_in_equal_size_slot(self) -> None:
        """Test that a widget fits in a slot of equal size."""
        widget_min_size = SizeClass.M
        slot_size = SizeClass.M
        
        # Widget should fit (min_size <= slot_size)
        assert widget_min_size <= slot_size
    
    def test_widget_fits_in_larger_slot(self) -> None:
        """Test that a widget fits in a larger slot."""
        widget_min_size = SizeClass.S
        slot_size = SizeClass.L
        
        # Widget should fit
        assert widget_min_size <= slot_size
    
    def test_widget_does_not_fit_in_smaller_slot(self) -> None:
        """Test that a widget does not fit in a smaller slot."""
        widget_min_size = SizeClass.XL
        slot_size = SizeClass.M
        
        # Widget should NOT fit
        assert widget_min_size > slot_size
    
    def test_size_constraint_error_message_format(self) -> None:
        """Test that SizeConstraintError has proper message format."""
        error = SizeConstraintError(
            widget_type="Chart.Sankey",
            widget_min_size="XL",
            slot_role="sidebar",
            slot_size="M"
        )
        
        error_message = str(error)
        
        # Error message should contain all relevant information
        assert "Chart.Sankey" in error_message
        assert "XL" in error_message
        assert "sidebar" in error_message
        assert "M" in error_message
        assert "Suggestion" in error_message
    
    def test_size_constraint_error_attributes(self) -> None:
        """Test that SizeConstraintError preserves all attributes."""
        error = SizeConstraintError(
            widget_type="Data.BigNum",
            widget_min_size="S",
            slot_role="main",
            slot_size="S"
        )
        
        assert error.widget_type == "Data.BigNum"
        assert error.widget_min_size == "S"
        assert error.slot_role == "main"
        assert error.slot_size == "S"
