"""Unit tests for Data widget parameter validation."""
import pytest
from pydantic import ValidationError
from src.widgets.data import DataBigNumWidget, DataTrendWidget, DataProgressWidget
from src.common.size_class import SizeClass


class TestDataBigNumParameters:
    """Test parameter validation for Data.BigNum widget."""
    
    def test_valid_color_parameter(self):
        """Valid color values should be accepted."""
        for color in ["primary", "accent", "success", "warning", "danger"]:
            widget = DataBigNumWidget(
                parameters={"color": color}
            )
            widget.validate_parameters()
            assert widget.parameters["color"] == color
    
    def test_invalid_color_parameter(self):
        """Invalid color values should raise ValidationError."""
        widget = DataBigNumWidget(
            parameters={"color": "invalid_color"}
        )
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "color" in str(exc_info.value).lower()
    
    def test_valid_format_parameter(self):
        """Valid number formats should be accepted."""
        for fmt in ["number", "currency", "percentage"]:
            widget = DataBigNumWidget(
                parameters={"format": fmt}
            )
            widget.validate_parameters()
            assert widget.parameters["format"] == fmt
    
    def test_default_color(self):
        """Default color should be primary."""
        widget = DataBigNumWidget(parameters={})
        data = widget.render_data()
        assert data["color"] == "primary"
    
    def test_default_format(self):
        """Default format should be number."""
        widget = DataBigNumWidget(parameters={})
        data = widget.render_data()
        assert data["format"] == "number"
    
    def test_show_label_parameter(self):
        """Boolean show_label parameter should be accepted."""
        widget = DataBigNumWidget(
            parameters={"show_label": False}
        )
        widget.validate_parameters()
        assert widget.parameters["show_label"] is False


class TestDataTrendParameters:
    """Test parameter validation for Data.Trend widget."""
    
    def test_valid_direction_parameter(self):
        """Valid trend directions should be accepted."""
        for direction in ["up", "down", "flat"]:
            widget = DataTrendWidget(
                parameters={"direction": direction}
            )
            widget.validate_parameters()
            assert widget.parameters["direction"] == direction
    
    def test_invalid_direction_parameter(self):
        """Invalid direction values should raise ValidationError."""
        widget = DataTrendWidget(
            parameters={"direction": "sideways"}
        )
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "direction" in str(exc_info.value).lower()
    
    def test_valid_color_parameter(self):
        """Valid color values should be accepted."""
        widget = DataTrendWidget(
            parameters={"color": "success"}
        )
        widget.validate_parameters()
        assert widget.parameters["color"] == "success"
    
    def test_default_direction(self):
        """Default direction should be up."""
        widget = DataTrendWidget(parameters={})
        data = widget.render_data()
        assert data["direction"] == "up"


class TestDataProgressParameters:
    """Test parameter validation for Data.Progress widget."""
    
    def test_valid_color_parameter(self):
        """Valid color values should be accepted."""
        widget = DataProgressWidget(
            parameters={"color": "accent"}
        )
        widget.validate_parameters()
        assert widget.parameters["color"] == "accent"
    
    def test_valid_show_percentage_parameter(self):
        """Boolean show_percentage should be accepted."""
        widget = DataProgressWidget(
            parameters={"show_percentage": True}
        )
        widget.validate_parameters()
        assert widget.parameters["show_percentage"] is True
    
    def test_default_color(self):
        """Default color should be primary."""
        widget = DataProgressWidget(parameters={})
        data = widget.render_data()
        assert data["color"] == "primary"
    
    def test_default_show_percentage(self):
        """Default show_percentage should be True."""
        widget = DataProgressWidget(parameters={})
        data = widget.render_data()
        assert data["show_percentage"] is True
