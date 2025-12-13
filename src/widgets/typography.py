"""Typography widgets for text content."""
from typing import Any, ClassVar

from src.common.size_class import SizeClass
from src.widgets.base import BaseWidget, WidgetRegistry


@WidgetRegistry.register
class TypeDisplayWidget(BaseWidget):
    """Large display typography for headlines and hero text.
    
    Minimum size: S (can scale up to any size)
    
    Parameters:
    - text (str): Display text content (required)
    
    Styling (defined in Style config, not widget parameters):
    - font: Typography token from theme
    - align: Text alignment
    - foreground: Text color token
    - background: Background color token
    """

    widget_type: ClassVar[str] = "Type.Display"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate TypeDisplay-specific parameters."""
        if "text" not in self.parameters:
            from pydantic_core import ValidationError
            raise ValidationError.from_exception_data(
                "ValueError",
                [
                    {
                        "type": "value_error",
                        "loc": ("text",),
                        "msg": "text parameter is required",
                        "input": self.parameters,
                        "ctx": {"error": ValueError("text parameter is required")},
                    }
                ],
            )

    def render_data(self) -> dict[str, Any]:
        """Generate data for template rendering."""
        return {
            "widget_type": self.widget_type,
            "atom_id": self.atom_id,
            "parameters": self.parameters,
            "content": self.parameters.get("text", "Display Text"),
        }

    def measure(self, style: dict[str, Any], max_width: float = float('inf'), max_height: float = float('inf')):
        """Calculate widget content size for TypeDisplay.
        
        Display text uses large font sizes and minimal wrapping.
        """
        from src.common.measurement import WidgetMeasurement
        
        text = self.parameters.get("text", "Display Text")
        
        # Extract font size from style (default to large display size)
        font_size_str = style.get("font-size", "64px")
        # Parse font size - handle "64px" format
        font_size = float(font_size_str.replace("px", "")) if isinstance(font_size_str, str) else 64
        
        # Extract line height from style (default 1.1 for display text)
        line_height = float(style.get("line-height", 1.1))
        
        return WidgetMeasurement.measure_text_widget(
            text=text,
            font_size=font_size,
            max_width=max_width,
            line_height=line_height,
            padding=30  # Display text has more padding
        )


@WidgetRegistry.register
class TypeHeadingWidget(BaseWidget):
    """Heading typography for section titles.
    
    Minimum size: S
    
    Parameters:
    - text (str): Heading text content (required)
    - level (int): Heading level 1-6 (default: 2)
    
    Styling (defined in Style config, not widget parameters):
    - font: Typography token from theme
    - align: Text alignment
    - foreground: Text color token
    """

    widget_type: ClassVar[str] = "Type.Heading"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate TypeHeading-specific parameters."""
        if "text" not in self.parameters:
            from pydantic_core import ValidationError
            raise ValidationError.from_exception_data(
                "ValueError",
                [
                    {
                        "type": "value_error",
                        "loc": ("text",),
                        "msg": "text parameter is required",
                        "input": self.parameters,
                        "ctx": {"error": ValueError("text parameter is required")},
                    }
                ],
            )
        
        if "level" in self.parameters:
            level = self.parameters["level"]
            if not isinstance(level, int) or level < 1 or level > 6:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("level",),
                            "msg": f"Invalid level '{level}'. Must be an integer between 1 and 6",
                            "input": level,
                            "ctx": {"error": ValueError(f"Invalid level '{level}'")},
                        }
                    ],
                )

    def render_data(self) -> dict[str, Any]:
        """Generate data for template rendering."""
        return {
            "widget_type": self.widget_type,
            "atom_id": self.atom_id,
            "parameters": self.parameters,
            "content": self.parameters.get("text", "Heading"),
            "level": self.parameters.get("level", 2),
        }

    def measure(self, style: dict[str, Any], max_width: float = float('inf'), max_height: float = float('inf')):
        """Calculate widget content size for TypeHeading.
        
        Headings use larger font sizes based on level.
        """
        from src.common.measurement import WidgetMeasurement
        
        text = self.parameters.get("text", "Heading")
        level = self.parameters.get("level", 2)
        
        # Extract font size from style (default varies by heading level)
        default_sizes = {1: "40px", 2: "32px", 3: "28px", 4: "24px", 5: "20px", 6: "18px"}
        font_size_str = style.get("font-size", default_sizes.get(level, "32px"))
        font_size = float(font_size_str.replace("px", "")) if isinstance(font_size_str, str) else 32
        
        # Extract line height from style (default 1.2 for headings)
        line_height = float(style.get("line-height", 1.2))
        
        return WidgetMeasurement.measure_text_widget(
            text=text,
            font_size=font_size,
            max_width=max_width,
            line_height=line_height,
            padding=24  # Headings have medium padding
        )


@WidgetRegistry.register
class TypeBodyWidget(BaseWidget):
    """Body text for paragraphs and general content.
    
    Minimum size: S
    
    Parameters:
    - text (str): Body text content (required)
    
    Styling (defined in Style config, not widget parameters):
    - font: Typography token from theme
    - align: Text alignment
    - foreground: Text color token
    """

    widget_type: ClassVar[str] = "Type.Body"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate TypeBody-specific parameters."""
        if "text" not in self.parameters:
            from pydantic_core import ValidationError
            raise ValidationError.from_exception_data(
                "ValueError",
                [
                    {
                        "type": "value_error",
                        "loc": ("text",),
                        "msg": "text parameter is required",
                        "input": self.parameters,
                        "ctx": {"error": ValueError("text parameter is required")},
                    }
                ],
            )

    def render_data(self) -> dict[str, Any]:
        """Generate data for template rendering."""
        return {
            "widget_type": self.widget_type,
            "atom_id": self.atom_id,
            "parameters": self.parameters,
            "content": self.parameters.get("text", "Body text content."),
        }

    def measure(self, style: dict[str, Any], max_width: float = float('inf'), max_height: float = float('inf')):
        """Calculate widget content size for TypeBody.
        
        Body text wraps more readily and uses standard reading sizes.
        """
        from src.common.measurement import WidgetMeasurement
        
        text = self.parameters.get("text", "Body text content.")
        
        # Extract font size from style (default to body size)
        font_size_str = style.get("font-size", "16px")
        font_size = float(font_size_str.replace("px", "")) if isinstance(font_size_str, str) else 16
        
        # Extract line height from style (default 1.5 for body text)
        line_height = float(style.get("line-height", 1.5))
        
        return WidgetMeasurement.measure_text_widget(
            text=text,
            font_size=font_size,
            max_width=max_width,
            line_height=line_height,
            padding=20  # Standard padding for body text
        )


@WidgetRegistry.register
class TypeListWidget(BaseWidget):
    """List widget for bullet/numbered lists.
    
    Minimum size: S
    
    Parameters:
    - items (list[str]): List items (required)
    - list_type (str): List style - "ordered", "unordered" (default: "unordered")
    
    Styling (defined in Style config, not widget parameters):
    - font: Typography token from theme
    - foreground: Text color token
    """

    widget_type: ClassVar[str] = "Type.List"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate TypeList-specific parameters."""
        if "items" not in self.parameters:
            from pydantic_core import ValidationError
            raise ValidationError.from_exception_data(
                "ValueError",
                [
                    {
                        "type": "value_error",
                        "loc": ("items",),
                        "msg": "items parameter is required",
                        "input": self.parameters,
                        "ctx": {"error": ValueError("items parameter is required")},
                    }
                ],
            )
        
        if "list_type" in self.parameters:
            valid_list_types = ["ordered", "unordered"]
            if self.parameters["list_type"] not in valid_list_types:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("list_type",),
                            "msg": f"Invalid list_type '{self.parameters['list_type']}'. Must be one of: {', '.join(valid_list_types)}",
                            "input": self.parameters["list_type"],
                            "ctx": {"error": ValueError(f"Invalid list_type '{self.parameters['list_type']}'")},
                        }
                    ],
                )

    def render_data(self) -> dict[str, Any]:
        """Generate data for template rendering."""
        # Convert items from string (newline-separated) to list if needed
        items_param = self.parameters.get("items", [])
        if isinstance(items_param, str):
            items = [item.strip() for item in items_param.split("\n") if item.strip()]
        else:
            items = items_param
        
        return {
            "widget_type": self.widget_type,
            "atom_id": self.atom_id,
            "parameters": self.parameters,
            "items": items,
            "list_type": self.parameters.get("list_type", "unordered"),
        }

    def measure(self, style: dict[str, Any], max_width: float = float('inf'), max_height: float = float('inf')):
        """Calculate widget content size for TypeList.
        
        Lists stack items vertically with bullet/number spacing.
        """
        from src.common.measurement import WidgetMeasurement, MeasuredSize
        
        items_param = self.parameters.get("items", [])
        if isinstance(items_param, str):
            items = [item.strip() for item in items_param.split("\n") if item.strip()]
        else:
            items = items_param
        
        # Extract font size from style
        font_size_str = style.get("font-size", "16px")
        font_size = float(font_size_str.replace("px", "")) if isinstance(font_size_str, str) else 16
        
        # Extract line height from style
        line_height = float(style.get("line-height", 1.4))
        
        # Measure each item and stack vertically
        total_height = 0
        max_item_width = 0
        
        for item in items:
            item_size = WidgetMeasurement.measure_text_widget(
                text=item,
                font_size=font_size,
                max_width=max_width - 40,  # Account for bullet/number
                line_height=line_height,
                padding=0
            )
            total_height += item_size.height + 8  # Item spacing
            max_item_width = max(max_item_width, item_size.width + 40)  # Add bullet/number width
        
        return MeasuredSize(
            width=max_item_width + 40,  # Add padding
            height=total_height + 40,
            min_width=200,
            min_height=100
        )


@WidgetRegistry.register
class TypeQuoteWidget(BaseWidget):
    """Blockquote widget for quotations.
    
    Minimum size: S
    
    Parameters:
    - text (str): Quote text content (required)
    - citation (str, optional): Attribution/source
    
    Styling (defined in Style config, not widget parameters):
    - font: Typography token from theme
    - align: Text alignment
    - foreground: Text color token
    """

    widget_type: ClassVar[str] = "Type.Quote"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate TypeQuote-specific parameters."""
        if "text" not in self.parameters:
            from pydantic_core import ValidationError
            raise ValidationError.from_exception_data(
                "ValueError",
                [
                    {
                        "type": "value_error",
                        "loc": ("text",),
                        "msg": "text parameter is required",
                        "input": self.parameters,
                        "ctx": {"error": ValueError("text parameter is required")},
                    }
                ],
            )

    def render_data(self) -> dict[str, Any]:
        """Generate data for template rendering."""
        return {
            "widget_type": self.widget_type,
            "atom_id": self.atom_id,
            "parameters": self.parameters,
            "content": self.parameters.get("text", "Quote text."),
            "citation": self.parameters.get("citation"),
        }

    def measure(self, style: dict[str, Any], max_width: float = float('inf'), max_height: float = float('inf')):
        """Calculate widget content size for TypeQuote.
        
        Quotes include quote text and optional citation.
        """
        from src.common.measurement import WidgetMeasurement, MeasuredSize
        
        text = self.parameters.get("text", "Quote text.")
        citation = self.parameters.get("citation")
        
        # Extract font size from style (quotes typically larger)
        font_size_str = style.get("font-size", "20px")
        font_size = float(font_size_str.replace("px", "")) if isinstance(font_size_str, str) else 20
        
        # Extract line height from style
        line_height = float(style.get("line-height", 1.5))
        
        # Measure quote text
        quote_size = WidgetMeasurement.measure_text_widget(
            text=text,
            font_size=font_size,
            max_width=max_width,
            line_height=line_height,
            padding=0
        )
        
        total_height = quote_size.height
        total_width = quote_size.width
        
        # Add citation if present
        if citation:
            citation_size = WidgetMeasurement.measure_text_widget(
                text=f"— {citation}",
                font_size=font_size * 0.8,  # Citation is smaller
                max_width=max_width,
                line_height=line_height,
                padding=0
            )
            total_height += citation_size.height + 12  # Spacing between quote and citation
            total_width = max(total_width, citation_size.width)
        
        return MeasuredSize(
            width=total_width + 60,  # Extra padding for quote marks
            height=total_height + 40,
            min_width=200,
            min_height=80
        )
