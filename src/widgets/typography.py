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
