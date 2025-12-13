"""Unit tests for spacing parsing utilities (px, %, rem)."""
import pytest
from src.common.spacing_utils import parse_spacing


class TestSpacingParsing:
    """Test the parse_spacing utility for converting CSS units to pixels."""
    
    def test_parse_px_value(self):
        """Test parsing pixel values."""
        result = parse_spacing("40px", reference=1000)
        assert result == 40
    
    def test_parse_px_with_decimal(self):
        """Test parsing pixel values with decimals."""
        result = parse_spacing("16.5px", reference=1000)
        assert result == 16.5
    
    def test_parse_percentage_value(self):
        """Test parsing percentage values."""
        result = parse_spacing("50%", reference=1000)
        assert result == 500  # 50% of 1000
    
    def test_parse_percentage_with_decimal(self):
        """Test parsing percentage with decimal."""
        result = parse_spacing("12.5%", reference=800)
        assert result == 100  # 12.5% of 800
    
    def test_parse_rem_value(self):
        """Test parsing rem values."""
        result = parse_spacing("2rem", reference=1000, base_font_size=16)
        assert result == 32  # 2 * 16
    
    def test_parse_rem_with_decimal(self):
        """Test parsing rem values with decimal."""
        result = parse_spacing("1.5rem", reference=1000, base_font_size=16)
        assert result == 24  # 1.5 * 16
    
    def test_parse_em_value(self):
        """Test parsing em values (same as rem for spacing)."""
        result = parse_spacing("3em", reference=1000, base_font_size=16)
        assert result == 48  # 3 * 16
    
    def test_parse_plain_number(self):
        """Test parsing plain numbers (treated as pixels)."""
        result = parse_spacing("25", reference=1000)
        assert result == 25
    
    def test_parse_zero(self):
        """Test parsing zero values."""
        assert parse_spacing("0", reference=1000) == 0
        assert parse_spacing("0px", reference=1000) == 0
        assert parse_spacing("0%", reference=1000) == 0
    
    def test_parse_percentage_zero_reference(self):
        """Test percentage with zero reference."""
        result = parse_spacing("50%", reference=0)
        assert result == 0
    
    def test_parse_with_different_reference_values(self):
        """Test that reference value affects percentage calculations."""
        assert parse_spacing("10%", reference=100) == 10
        assert parse_spacing("10%", reference=200) == 20
        assert parse_spacing("10%", reference=1000) == 100
    
    def test_parse_with_different_base_font_sizes(self):
        """Test that base_font_size affects rem calculations."""
        assert parse_spacing("2rem", reference=1000, base_font_size=10) == 20
        assert parse_spacing("2rem", reference=1000, base_font_size=16) == 32
        assert parse_spacing("2rem", reference=1000, base_font_size=20) == 40
    
    def test_parse_negative_values(self):
        """Test parsing negative values."""
        assert parse_spacing("-10px", reference=1000) == -10
        assert parse_spacing("-5%", reference=1000) == -50
    
    def test_parse_whitespace_handling(self):
        """Test that whitespace is handled correctly."""
        assert parse_spacing(" 20px ", reference=1000) == 20
        assert parse_spacing("  10%  ", reference=1000) == 100
    
    def test_parse_invalid_unit_falls_back_to_pixels(self):
        """Test that invalid units fall back to pixel parsing."""
        # Invalid unit should try to parse as number
        result = parse_spacing("50", reference=1000)
        assert result == 50
    
    def test_parse_empty_string(self):
        """Test parsing empty string defaults to 0."""
        result = parse_spacing("", reference=1000)
        assert result == 0
    
    def test_parse_none_defaults_to_zero(self):
        """Test that None defaults to 0."""
        result = parse_spacing(None, reference=1000)
        assert result == 0
    
    def test_default_base_font_size(self):
        """Test that default base font size is 16."""
        # When not specified, should use 16 as default
        result = parse_spacing("1rem", reference=1000)
        assert result == 16
