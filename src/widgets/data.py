"""Data and metrics widgets."""
from typing import Any, ClassVar

from src.common.size_class import SizeClass
from src.widgets.base import BaseWidget, WidgetRegistry

# Valid parameter values for content
VALID_FORMATS = ["number", "currency", "percentage"]
VALID_DIRECTIONS = ["up", "down", "flat"]


@WidgetRegistry.register
class DataBigNumWidget(BaseWidget):
    """Large numerical display for key metrics.
    
    Minimum size: S
    
    Parameters:
    - number (int | float): Numerical value to display (required)
    - label (str): Label text for the metric (required)
    - format (str): Number format - "number", "currency", "percentage" (default: "number")
    - show_label (bool): Whether to show the label (default: True)
    
    Styling (defined in Style config, not widget parameters):
    - font: Typography token for number and label
    - foreground: Color token for the number
    - background: Background color token
    """

    widget_type: ClassVar[str] = "Data.BigNum"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate DataBigNum-specific parameters."""
        if "number" not in self.parameters:
            from pydantic_core import ValidationError
            raise ValidationError.from_exception_data(
                "ValueError",
                [
                    {
                        "type": "value_error",
                        "loc": ("number",),
                        "msg": "number parameter is required",
                        "input": self.parameters,
                        "ctx": {"error": ValueError("number parameter is required")},
                    }
                ],
            )
        
        if "label" not in self.parameters:
            from pydantic_core import ValidationError
            raise ValidationError.from_exception_data(
                "ValueError",
                [
                    {
                        "type": "value_error",
                        "loc": ("label",),
                        "msg": "label parameter is required",
                        "input": self.parameters,
                        "ctx": {"error": ValueError("label parameter is required")},
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
            "number": self.parameters.get("number", 0),
            "label": self.parameters.get("label", "Metric"),
            "format": self.parameters.get("format", "number"),
            "show_label": self.parameters.get("show_label", True),
        }


@WidgetRegistry.register
class DataTrendWidget(BaseWidget):
    """Trend indicator with value and direction.
    
    Minimum size: S
    
    Parameters:
    - value (int | float): Current value (required)
    - change (int | float): Change amount (required)
    - direction (str): Trend direction - "up", "down", "flat" (default: "up")
    - label (str): Label text for the trend (required)
    
    Styling (defined in Style config, not widget parameters):
    - font: Typography token for value and label
    - foreground: Color token for the trend
    """

    widget_type: ClassVar[str] = "Data.Trend"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate DataTrend-specific parameters."""
        required = ["value", "change", "label"]
        for param in required:
            if param not in self.parameters:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": (param,),
                            "msg": f"{param} parameter is required",
                            "input": self.parameters,
                            "ctx": {"error": ValueError(f"{param} parameter is required")},
                        }
                    ],
                )
        
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
    - percentage (int | float): Progress percentage 0-100 (required)
    - label (str): Label text for the progress (required)
    - show_percentage (bool): Whether to show percentage (default: True)
    
    Styling (defined in Style config, not widget parameters):
    - font: Typography token for label
    - foreground: Color token for progress bar
    - background: Background color token
    """

    widget_type: ClassVar[str] = "Data.Progress"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate DataProgress-specific parameters."""
        if "percentage" not in self.parameters:
            from pydantic_core import ValidationError
            raise ValidationError.from_exception_data(
                "ValueError",
                [
                    {
                        "type": "value_error",
                        "loc": ("percentage",),
                        "msg": "percentage parameter is required",
                        "input": self.parameters,
                        "ctx": {"error": ValueError("percentage parameter is required")},
                    }
                ],
            )
        
        if "label" not in self.parameters:
            from pydantic_core import ValidationError
            raise ValidationError.from_exception_data(
                "ValueError",
                [
                    {
                        "type": "value_error",
                        "loc": ("label",),
                        "msg": "label parameter is required",
                        "input": self.parameters,
                        "ctx": {"error": ValueError("label parameter is required")},
                    }
                ],
            )

    def render_data(self) -> dict[str, Any]:
        """Generate data for template rendering."""
        return {
            "widget_type": self.widget_type,
            "atom_id": self.atom_id,
            "parameters": self.parameters,
            "percentage": self.parameters.get("percentage", 0),
            "label": self.parameters.get("label", "Progress"),
            "show_percentage": self.parameters.get("show_percentage", True),
        }
