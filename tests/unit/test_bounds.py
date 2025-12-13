"""Unit tests for Bounds model."""
import pytest
from src.common.bounds import Bounds


class TestBoundsModel:
    """Test the Bounds model for widget positioning."""
    
    def test_create_bounds_with_valid_values(self):
        """Test creating bounds with valid values."""
        bounds = Bounds(x=10, y=20, width=100, height=50)
        
        assert bounds.x == 10
        assert bounds.y == 20
        assert bounds.width == 100
        assert bounds.height == 50
    
    def test_bounds_calculated_properties(self):
        """Test calculated properties (right, bottom, center)."""
        bounds = Bounds(x=10, y=20, width=100, height=50)
        
        assert bounds.right == 110  # x + width
        assert bounds.bottom == 70  # y + height
        assert bounds.center_x == 60  # x + width/2
        assert bounds.center_y == 45  # y + height/2
    
    def test_bounds_rejects_negative_x(self):
        """Test that negative x is rejected."""
        with pytest.raises(Exception):  # Pydantic validation error
            Bounds(x=-10, y=20, width=100, height=50)
    
    def test_bounds_rejects_negative_y(self):
        """Test that negative y is rejected."""
        with pytest.raises(Exception):  # Pydantic validation error
            Bounds(x=10, y=-20, width=100, height=50)
    
    def test_bounds_rejects_zero_width(self):
        """Test that zero width is rejected (must be > 0)."""
        with pytest.raises(Exception):  # Pydantic validation error
            Bounds(x=10, y=20, width=0, height=50)
    
    def test_bounds_rejects_negative_width(self):
        """Test that negative width is rejected."""
        with pytest.raises(Exception):  # Pydantic validation error
            Bounds(x=10, y=20, width=-100, height=50)
    
    def test_bounds_rejects_zero_height(self):
        """Test that zero height is rejected (must be > 0)."""
        with pytest.raises(Exception):  # Pydantic validation error
            Bounds(x=10, y=20, width=100, height=0)
    
    def test_bounds_rejects_negative_height(self):
        """Test that negative height is rejected."""
        with pytest.raises(Exception):  # Pydantic validation error
            Bounds(x=10, y=20, width=100, height=-50)
    
    def test_contains_point_inside(self):
        """Test contains_point returns True for point inside."""
        bounds = Bounds(x=10, y=20, width=100, height=50)
        
        assert bounds.contains_point(50, 40) is True
    
    def test_contains_point_on_edge(self):
        """Test contains_point returns True for point on edge."""
        bounds = Bounds(x=10, y=20, width=100, height=50)
        
        assert bounds.contains_point(10, 20) is True  # top-left corner
        assert bounds.contains_point(110, 70) is True  # bottom-right corner
    
    def test_contains_point_outside(self):
        """Test contains_point returns False for point outside."""
        bounds = Bounds(x=10, y=20, width=100, height=50)
        
        assert bounds.contains_point(5, 40) is False  # left of bounds
        assert bounds.contains_point(120, 40) is False  # right of bounds
        assert bounds.contains_point(50, 10) is False  # above bounds
        assert bounds.contains_point(50, 80) is False  # below bounds
    
    def test_intersects_with_overlapping_bounds(self):
        """Test intersects returns True for overlapping bounds."""
        bounds1 = Bounds(x=10, y=20, width=100, height=50)
        bounds2 = Bounds(x=50, y=40, width=100, height=50)
        
        assert bounds1.intersects(bounds2) is True
        assert bounds2.intersects(bounds1) is True  # symmetric
    
    def test_intersects_with_non_overlapping_bounds(self):
        """Test intersects returns False for non-overlapping bounds."""
        bounds1 = Bounds(x=10, y=20, width=100, height=50)
        bounds2 = Bounds(x=200, y=20, width=100, height=50)
        
        assert bounds1.intersects(bounds2) is False
        assert bounds2.intersects(bounds1) is False  # symmetric
    
    def test_intersects_with_touching_bounds(self):
        """Test intersects returns True for bounds that touch at edge."""
        bounds1 = Bounds(x=10, y=20, width=100, height=50)
        bounds2 = Bounds(x=110, y=20, width=100, height=50)  # touching right edge
        
        # The current implementation considers touching at edge as intersecting
        # (based on <= comparison in intersects method)
        assert bounds1.intersects(bounds2) is True
    
    def test_str_representation(self):
        """Test string representation."""
        bounds = Bounds(x=10, y=20, width=100, height=50)
        
        str_repr = str(bounds)
        assert "10" in str_repr
        assert "20" in str_repr
        assert "100" in str_repr
        assert "50" in str_repr
