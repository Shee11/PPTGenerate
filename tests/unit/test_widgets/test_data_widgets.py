"""Unit tests for Data widget parameter validation."""
import pytest
from pydantic_core import ValidationError
from src.widgets.data import DataBigNumWidget, DataTrendWidget, DataProgressWidget
from src.common.size_class import SizeClass


class TestDataBigNumParameters:
    """Test parameter validation for Data.BigNum widget."""
    
    def test_number_parameter_required(self):
        """Number parameter is required."""
        widget = DataBigNumWidget(parameters={"label": "Test"})
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "number" in str(exc_info.value).lower()
    
    def test_label_parameter_required(self):
        """Label parameter is required."""
        widget = DataBigNumWidget(parameters={"number": 42})
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "label" in str(exc_info.value).lower()
    
    def test_valid_format_parameter(self):
        """Valid number formats should be accepted."""
        for fmt in ["number", "currency", "percentage"]:
            widget = DataBigNumWidget(
                parameters={"number": 100, "label": "Test", "format": fmt}
            )
            widget.validate_parameters()
            assert widget.parameters["format"] == fmt
    
    def test_invalid_format_parameter(self):
        """Invalid format values should raise ValidationError."""
        widget = DataBigNumWidget(
            parameters={"number": 100, "label": "Test", "format": "invalid"}
        )
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "format" in str(exc_info.value).lower()
    
    def test_default_format(self):
        """Default format should be number."""
        widget = DataBigNumWidget(parameters={"number": 100, "label": "Test"})
        widget.validate_parameters()
        data = widget.render_data()
        assert data["format"] == "number"
    
    def test_show_label_parameter(self):
        """Boolean show_label parameter should be accepted."""
        widget = DataBigNumWidget(
            parameters={"number": 100, "label": "Test", "show_label": False}
        )
        widget.validate_parameters()
        assert widget.parameters["show_label"] is False
    
    def test_number_and_label_rendered(self):
        """Number and label should be rendered."""
        widget = DataBigNumWidget(
            parameters={"number": 42, "label": "Answer"}
        )
        widget.validate_parameters()
        data = widget.render_data()
        assert data["number"] == 42
        assert data["label"] == "Answer"


class TestDataTrendParameters:
    """Test parameter validation for Data.Trend widget."""
    
    def test_value_parameter_required(self):
        """Value parameter is required."""
        widget = DataTrendWidget(parameters={"change": 10, "label": "Test"})
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "value" in str(exc_info.value).lower()
    
    def test_change_parameter_required(self):
        """Change parameter is required."""
        widget = DataTrendWidget(parameters={"value": 100, "label": "Test"})
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "change" in str(exc_info.value).lower()
    
    def test_label_parameter_required(self):
        """Label parameter is required."""
        widget = DataTrendWidget(parameters={"value": 100, "change": 10})
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "label" in str(exc_info.value).lower()
    
    def test_valid_direction_parameter(self):
        """Valid trend directions should be accepted."""
        for direction in ["up", "down", "flat"]:
            widget = DataTrendWidget(
                parameters={"value": 100, "change": 10, "label": "Test", "direction": direction}
            )
            widget.validate_parameters()
            assert widget.parameters["direction"] == direction
    
    def test_invalid_direction_parameter(self):
        """Invalid direction values should raise ValidationError."""
        widget = DataTrendWidget(
            parameters={"value": 100, "change": 10, "label": "Test", "direction": "sideways"}
        )
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "direction" in str(exc_info.value).lower()
    
    def test_default_direction(self):
        """Default direction should be up."""
        widget = DataTrendWidget(parameters={"value": 100, "change": 10, "label": "Test"})
        widget.validate_parameters()
        data = widget.render_data()
        assert data["direction"] == "up"
    
    def test_all_parameters_rendered(self):
        """Value, change, and label should be rendered."""
        widget = DataTrendWidget(
            parameters={"value": 100, "change": 15, "label": "Sales"}
        )
        widget.validate_parameters()
        data = widget.render_data()
        assert data["value"] == 100
        assert data["change"] == 15
        assert data["label"] == "Sales"


class TestDataProgressParameters:
    """Test parameter validation for Data.Progress widget."""
    
    def test_percentage_parameter_required(self):
        """Percentage parameter is required."""
        widget = DataProgressWidget(parameters={"label": "Test"})
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "percentage" in str(exc_info.value).lower()
    
    def test_label_parameter_required(self):
        """Label parameter is required."""
        widget = DataProgressWidget(parameters={"percentage": 75})
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "label" in str(exc_info.value).lower()
    
    def test_valid_show_percentage_parameter(self):
        """Boolean show_percentage should be accepted."""
        widget = DataProgressWidget(
            parameters={"percentage": 75, "label": "Test", "show_percentage": True}
        )
        widget.validate_parameters()
        assert widget.parameters["show_percentage"] is True
    
    def test_default_show_percentage(self):
        """Default show_percentage should be True."""
        widget = DataProgressWidget(parameters={"percentage": 50, "label": "Test"})
        widget.validate_parameters()
        data = widget.render_data()
        assert data["show_percentage"] is True
    
    def test_percentage_and_label_rendered(self):
        """Percentage and label should be rendered."""
        widget = DataProgressWidget(
            parameters={"percentage": 85, "label": "Complete"}
        )
        widget.validate_parameters()
        data = widget.render_data()
        assert data["percentage"] == 85
        assert data["label"] == "Complete"
