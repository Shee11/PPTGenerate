"""Unit tests for Typography widget parameter validation."""
import pytest
from pydantic_core import ValidationError
from src.paged.widgets.typography import (
    TypeDisplayWidget, 
    TypeHeadingWidget, 
    TypeBodyWidget,
    TypeListWidget,
    TypeQuoteWidget
)
from src.common.size_class import SizeClass


class TestTypeDisplayParameters:
    """Test parameter validation for Type.Display widget."""
    
    def test_text_parameter_required(self):
        """Text parameter is required."""
        widget = TypeDisplayWidget(parameters={})
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "text" in str(exc_info.value).lower()
    
    def test_text_parameter(self):
        """Text parameter should be rendered."""
        widget = TypeDisplayWidget(
            parameters={"text": "Custom Display"}
        )
        widget.validate_parameters()
        data = widget.render_data()
        assert data["content"] == "Custom Display"


class TestTypeHeadingParameters:
    """Test parameter validation for Type.Heading widget."""
    
    def test_text_parameter_required(self):
        """Text parameter is required."""
        widget = TypeHeadingWidget(parameters={})
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "text" in str(exc_info.value).lower()
    
    def test_valid_level_parameter(self):
        """Valid heading levels (1-6) should be accepted."""
        for level in range(1, 7):
            widget = TypeHeadingWidget(
                parameters={"level": level, "text": "Test"}
            )
            widget.validate_parameters()
            assert widget.parameters["level"] == level
    
    def test_invalid_level_parameter(self):
        """Invalid heading levels should raise ValidationError."""
        widget = TypeHeadingWidget(
            parameters={"level": 7, "text": "Test"}
        )
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "level" in str(exc_info.value).lower()
    
    def test_default_level(self):
        """Default level should be 2."""
        widget = TypeHeadingWidget(parameters={"text": "Test"})
        data = widget.render_data()
        assert data["level"] == 2


class TestTypeBodyParameters:
    """Test parameter validation for Type.Body widget."""
    
    def test_text_parameter_required(self):
        """Text parameter is required."""
        widget = TypeBodyWidget(parameters={})
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "text" in str(exc_info.value).lower()
    
    def test_text_parameter(self):
        """Text parameter should be rendered."""
        widget = TypeBodyWidget(
            parameters={"text": "Custom body text."}
        )
        widget.validate_parameters()
        data = widget.render_data()
        assert data["content"] == "Custom body text."


class TestTypeListParameters:
    """Test parameter validation for Type.List widget."""
    
    def test_items_parameter_required(self):
        """Items parameter is required."""
        widget = TypeListWidget(parameters={})
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "items" in str(exc_info.value).lower()
    
    def test_valid_list_type_ordered(self):
        """Valid list_type 'ordered' should be accepted."""
        widget = TypeListWidget(
            parameters={"list_type": "ordered", "items": ["Item 1", "Item 2"]}
        )
        widget.validate_parameters()
        assert widget.parameters["list_type"] == "ordered"
    
    def test_valid_list_type_unordered(self):
        """Valid list_type 'unordered' should be accepted."""
        widget = TypeListWidget(
            parameters={"list_type": "unordered", "items": ["Item 1", "Item 2"]}
        )
        widget.validate_parameters()
        assert widget.parameters["list_type"] == "unordered"
    
    def test_invalid_list_type(self):
        """Invalid list_type values should raise ValidationError."""
        widget = TypeListWidget(
            parameters={"list_type": "invalid", "items": ["Item 1"]}
        )
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "list_type" in str(exc_info.value).lower()
    
    def test_items_parameter(self):
        """Items parameter should be rendered."""
        widget = TypeListWidget(
            parameters={"items": ["First", "Second", "Third"]}
        )
        widget.validate_parameters()
        data = widget.render_data()
        assert data["items"] == ["First", "Second", "Third"]
        assert len(data["items"]) == 3
    
    def test_default_list_type(self):
        """Default list_type should be unordered."""
        widget = TypeListWidget(parameters={"items": ["Item"]})
        data = widget.render_data()
        assert data["list_type"] == "unordered"


class TestTypeQuoteParameters:
    """Test parameter validation for Type.Quote widget."""
    
    def test_text_parameter_required(self):
        """Text parameter is required."""
        widget = TypeQuoteWidget(parameters={})
        with pytest.raises(ValidationError) as exc_info:
            widget.validate_parameters()
        assert "text" in str(exc_info.value).lower()
    
    def test_quote_text_parameter(self):
        """Quote text parameter should be rendered."""
        widget = TypeQuoteWidget(
            parameters={"text": "To be or not to be"}
        )
        widget.validate_parameters()
        data = widget.render_data()
        assert data["content"] == "To be or not to be"
    
    def test_citation_parameter(self):
        """Citation parameter should be rendered."""
        widget = TypeQuoteWidget(
            parameters={"text": "Test quote", "citation": "Author Name"}
        )
        widget.validate_parameters()
        data = widget.render_data()
        assert data["citation"] == "Author Name"
    
    def test_default_citation(self):
        """Default citation should be None."""
        widget = TypeQuoteWidget(parameters={"text": "Quote"})
        widget.validate_parameters()
        data = widget.render_data()
        assert data.get("citation") is None

