"""Data and metrics widgets."""
from typing import Any, ClassVar

from src.common.size_class import SizeClass
from src.paged.widgets.base import BaseWidget, WidgetRegistry

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

    def measure(self, style: dict[str, Any], max_width: float = float('inf'), max_height: float = float('inf')):
        """Calculate widget content size for DataBigNum.
        
        Big numbers use large font for the value and smaller font for label.
        """
        from src.common.measurement import WidgetMeasurement
        
        # Get number and format it
        number = self.parameters.get("number", 0)
        label = self.parameters.get("label", "Metric")
        show_label = self.parameters.get("show_label", True)
        
        # Format number for display
        format_type = self.parameters.get("format", "number")
        if format_type == "currency":
            formatted_num = f"${number:,.2f}"
        elif format_type == "percentage":
            formatted_num = f"{number}%"
        else:
            formatted_num = f"{number:,}"
        
        # Extract font size for number (default to large size)
        font_size_str = style.get("font-size", "48px")
        number_font_size = float(font_size_str.replace("px", "")) if isinstance(font_size_str, str) else 48
        
        # Label is typically smaller (60% of number size)
        label_font_size = number_font_size * 0.6
        
        # Measure number
        number_size = WidgetMeasurement.measure_text_widget(
            text=formatted_num,
            font_size=number_font_size,
            max_width=max_width,
            line_height=1.0,
            padding=0
        )
        
        # Measure label if shown
        if show_label:
            label_size = WidgetMeasurement.measure_text_widget(
                text=label,
                font_size=label_font_size,
                max_width=max_width,
                line_height=1.2,
                padding=0
            )
            # Stack vertically: number + label + spacing
            total_height = number_size.height + label_size.height + 10
            total_width = max(number_size.width, label_size.width)
        else:
            total_height = number_size.height
            total_width = number_size.width
        
        # Add padding
        from src.common.measurement import MeasuredSize
        return MeasuredSize(
            width=total_width + 40,
            height=total_height + 40,
            min_width=150,
            min_height=100
        )


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

    def measure(self, style: dict[str, Any], max_width: float = float('inf'), max_height: float = float('inf')):
        """Calculate widget content size for DataTrend.
        
        Trend shows value, change indicator, and label.
        """
        from src.common.measurement import WidgetMeasurement, MeasuredSize
        
        value = self.parameters.get("value", 0)
        change = self.parameters.get("change", 0)
        label = self.parameters.get("label", "Trend")
        
        # Format values
        value_str = f"{value:,}"
        change_str = f"+{change:,}" if change >= 0 else f"{change:,}"
        
        # Extract font size from style
        font_size_str = style.get("font-size", "36px")
        value_font_size = float(font_size_str.replace("px", "")) if isinstance(font_size_str, str) else 36
        
        # Change and label are smaller
        change_font_size = value_font_size * 0.7
        label_font_size = value_font_size * 0.5
        
        # Measure components
        value_size = WidgetMeasurement.measure_text_widget(
            text=value_str,
            font_size=value_font_size,
            max_width=max_width,
            line_height=1.0,
            padding=0
        )
        
        change_size = WidgetMeasurement.measure_text_widget(
            text=change_str,
            font_size=change_font_size,
            max_width=max_width,
            line_height=1.0,
            padding=0
        )
        
        label_size = WidgetMeasurement.measure_text_widget(
            text=label,
            font_size=label_font_size,
            max_width=max_width,
            line_height=1.2,
            padding=0
        )
        
        # Stack vertically: value + change + label
        total_height = value_size.height + change_size.height + label_size.height + 20  # spacing
        total_width = max(value_size.width, change_size.width, label_size.width)
        
        return MeasuredSize(
            width=total_width + 40,
            height=total_height + 40,
            min_width=150,
            min_height=120
        )


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

    def measure(self, style: dict[str, Any], max_width: float = float('inf'), max_height: float = float('inf')):
        """Calculate widget content size for DataProgress.
        
        Progress bar with label and optional percentage display.
        """
        from src.common.measurement import WidgetMeasurement, MeasuredSize
        
        label = self.parameters.get("label", "Progress")
        show_percentage = self.parameters.get("show_percentage", True)
        percentage = self.parameters.get("percentage", 0)
        
        # Extract font size from style
        font_size_str = style.get("font-size", "16px")
        font_size = float(font_size_str.replace("px", "")) if isinstance(font_size_str, str) else 16
        
        # Measure label
        label_size = WidgetMeasurement.measure_text_widget(
            text=label,
            font_size=font_size,
            max_width=max_width,
            line_height=1.2,
            padding=0
        )
        
        # Progress bar height (fixed)
        progress_bar_height = 24
        
        # Percentage text if shown
        percentage_height = 0
        if show_percentage:
            percentage_size = WidgetMeasurement.measure_text_widget(
                text=f"{percentage}%",
                font_size=font_size * 1.2,
                max_width=max_width,
                line_height=1.0,
                padding=0
            )
            percentage_height = percentage_size.height
        
        # Stack: label + progress bar + percentage (if shown)
        total_height = label_size.height + progress_bar_height + percentage_height + 20  # spacing
        total_width = max(label_size.width, 200)  # Min width for progress bar
        
        return MeasuredSize(
            width=total_width + 40,
            height=total_height + 40,
            min_width=200,
            min_height=100
        )
