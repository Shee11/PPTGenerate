"""Data and metrics widgets."""
from typing import Any, ClassVar

from src.common.size_class import SizeClass
from src.widgets.base import BaseWidget, WidgetRegistry

# Valid parameter values
VALID_COLORS = ["primary", "accent", "success", "warning", "danger"]
VALID_FORMATS = ["number", "currency", "percentage"]
VALID_DIRECTIONS = ["up", "down", "flat"]


@WidgetRegistry.register
class DataBigNumWidget(BaseWidget):
    """Large numerical display for key metrics.
    
    Minimum size: S
    
    Parameters:
    - value (int | float): Numerical value to display
    - label (str): Label text for the metric
    - color (str): Color theme - "primary", "accent", "success", "warning", "danger" (default: "primary")
    - format (str): Number format - "number", "currency", "percentage" (default: "number")
    - show_label (bool): Whether to show the label (default: True)
    """

    widget_type: ClassVar[str] = "Data.BigNum"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate DataBigNum-specific parameters."""
        if "color" in self.parameters:
            if self.parameters["color"] not in VALID_COLORS:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("color",),
                            "msg": f"Invalid color '{self.parameters['color']}'. Must be one of: {', '.join(VALID_COLORS)}",
                            "input": self.parameters["color"],
                            "ctx": {"error": ValueError(f"Invalid color '{self.parameters['color']}'")},
                        }
                    ],
                )

        if "format" in self.parameters:
            if self.parameters["format"] not in VALID_FORMATS:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("format",),
                            "msg": f"Invalid format '{self.parameters['format']}'. Must be one of: {', '.join(VALID_FORMATS)}",
                            "input": self.parameters["format"],
                            "ctx": {"error": ValueError(f"Invalid format '{self.parameters['format']}'")},
                        }
                    ],
                )

    def render_data(self) -> dict[str, Any]:
        """Generate data for template rendering."""
        return {
            "widget_type": self.widget_type,
            "atom_id": self.atom_id,
            "parameters": self.parameters,
            "value": self.parameters.get("value", 0),
            "label": self.parameters.get("label", "Metric"),
            "color": self.parameters.get("color", "primary"),
            "format": self.parameters.get("format", "number"),
        }


@WidgetRegistry.register
class DataTrendWidget(BaseWidget):
    """Trend indicator with value and direction.
    
    Minimum size: S
    
    Parameters:
    - value (int | float): Current value
    - change (int | float): Change amount
    - direction (str): Trend direction - "up", "down", "flat" (default: "up")
    - label (str): Label text for the trend
    - color (str): Color theme - "primary", "accent", "success", "warning", "danger" (default: "primary")
    """

    widget_type: ClassVar[str] = "Data.Trend"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate DataTrend-specific parameters."""
        if "direction" in self.parameters:
            if self.parameters["direction"] not in VALID_DIRECTIONS:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("direction",),
                            "msg": f"Invalid direction '{self.parameters['direction']}'. Must be one of: {', '.join(VALID_DIRECTIONS)}",
                            "input": self.parameters["direction"],
                            "ctx": {"error": ValueError(f"Invalid direction '{self.parameters['direction']}'")},
                        }
                    ],
                )

        if "color" in self.parameters:
            if self.parameters["color"] not in VALID_COLORS:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("color",),
                            "msg": f"Invalid color '{self.parameters['color']}'. Must be one of: {', '.join(VALID_COLORS)}",
                            "input": self.parameters["color"],
                            "ctx": {"error": ValueError(f"Invalid color '{self.parameters['color']}'")},
                        }
                    ],
                )

    def render_data(self) -> dict[str, Any]:
        """Generate data for template rendering."""
        return {
            "widget_type": self.widget_type,
            "atom_id": self.atom_id,
            "parameters": self.parameters,
            "value": self.parameters.get("value", 0),
            "change": self.parameters.get("change", 0),
            "direction": self.parameters.get("direction", "up"),
            "label": self.parameters.get("label", "Trend"),
        }


@WidgetRegistry.register
class DataProgressWidget(BaseWidget):
    """Progress bar or circular progress indicator.
    
    Minimum size: S
    
    Parameters:
    - value (int | float): Current progress value
    - max (int | float): Maximum value (default: 100)
    - label (str): Label text for the progress
    - type (str): Progress type - "bar" or "circle" (default: "bar")
    - color (str): Color theme - "primary", "accent", "success", "warning", "danger" (default: "primary")
    - show_percentage (bool): Whether to show percentage (default: True)
    """

    widget_type: ClassVar[str] = "Data.Progress"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate DataProgress-specific parameters."""
        if "color" in self.parameters:
            if self.parameters["color"] not in VALID_COLORS:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("color",),
                            "msg": f"Invalid color '{self.parameters['color']}'. Must be one of: {', '.join(VALID_COLORS)}",
                            "input": self.parameters["color"],
                            "ctx": {"error": ValueError(f"Invalid color '{self.parameters['color']}'")},
                        }
                    ],
                )

    def render_data(self) -> dict[str, Any]:
        """Generate data for template rendering."""
        return {
            "widget_type": self.widget_type,
            "atom_id": self.atom_id,
            "parameters": self.parameters,
            "value": self.parameters.get("value", 0),
            "max": self.parameters.get("max", 100),
            "label": self.parameters.get("label", "Progress"),
            "type": self.parameters.get("type", "bar"),
            "color": self.parameters.get("color", "primary"),
            "show_percentage": self.parameters.get("show_percentage", True),
        }
