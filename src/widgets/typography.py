"""Typography widgets for text content."""
from typing import Any, ClassVar

from src.common.size_class import SizeClass
from src.widgets.base import BaseWidget, WidgetRegistry

# Valid parameter values
VALID_STYLES = ["normal", "bold", "italic", "bold-italic"]
VALID_ALIGNS = ["left", "center", "right", "justify"]
VALID_LIST_TYPES = ["ordered", "unordered"]


@WidgetRegistry.register
class TypeDisplayWidget(BaseWidget):
    """Large display typography for headlines and hero text.
    
    Minimum size: S (can scale up to any size)
    
    Parameters:
    - text (str): Display text content
    - style (str): Text style - "normal", "bold", "italic", "bold-italic" (default: "normal")
    - align (str): Text alignment - "left", "center", "right", "justify" (default: "left")
    """

    widget_type: ClassVar[str] = "Type.Display"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate TypeDisplay-specific parameters."""
        if "style" in self.parameters:
            if self.parameters["style"] not in VALID_STYLES:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("style",),
                            "msg": f"Invalid style '{self.parameters['style']}'. Must be one of: {', '.join(VALID_STYLES)}",
                            "input": self.parameters["style"],
                            "ctx": {"error": ValueError(f"Invalid style '{self.parameters['style']}'")},
                        }
                    ],
                )

        if "align" in self.parameters:
            if self.parameters["align"] not in VALID_ALIGNS:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("align",),
                            "msg": f"Invalid align '{self.parameters['align']}'. Must be one of: {', '.join(VALID_ALIGNS)}",
                            "input": self.parameters["align"],
                            "ctx": {"error": ValueError(f"Invalid align '{self.parameters['align']}'")},
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
            "style": self.parameters.get("style", "normal"),
            "align": self.parameters.get("align", "left"),
        }


@WidgetRegistry.register
class TypeHeadingWidget(BaseWidget):
    """Heading typography for section titles.
    
    Minimum size: S
    
    Parameters:
    - text (str): Heading text content
    - level (int): Heading level 1-6 (default: 2)
    - align (str): Text alignment - "left", "center", "right", "justify" (default: "left")
    """

    widget_type: ClassVar[str] = "Type.Heading"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate TypeHeading-specific parameters."""
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

        if "align" in self.parameters:
            if self.parameters["align"] not in VALID_ALIGNS:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("align",),
                            "msg": f"Invalid align '{self.parameters['align']}'. Must be one of: {', '.join(VALID_ALIGNS)}",
                            "input": self.parameters["align"],
                            "ctx": {"error": ValueError(f"Invalid align '{self.parameters['align']}'")},
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
            "align": self.parameters.get("align", "left"),
        }


@WidgetRegistry.register
class TypeBodyWidget(BaseWidget):
    """Body text for paragraphs and general content.
    
    Minimum size: S
    
    Parameters:
    - text (str): Body text content
    - align (str): Text alignment - "left", "center", "right", "justify" (default: "left")
    """

    widget_type: ClassVar[str] = "Type.Body"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate TypeBody-specific parameters."""
        if "align" in self.parameters:
            if self.parameters["align"] not in VALID_ALIGNS:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("align",),
                            "msg": f"Invalid align '{self.parameters['align']}'. Must be one of: {', '.join(VALID_ALIGNS)}",
                            "input": self.parameters["align"],
                            "ctx": {"error": ValueError(f"Invalid align '{self.parameters['align']}'")},
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
            "align": self.parameters.get("align", "left"),
        }


@WidgetRegistry.register
class TypeListWidget(BaseWidget):
    """List widget for bullet/numbered lists.
    
    Minimum size: S
    
    Parameters:
    - items (list[str]): List items
    - list_type (str): List style - "ordered", "unordered" (default: "unordered")
    """

    widget_type: ClassVar[str] = "Type.List"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate TypeList-specific parameters."""
        if "list_type" in self.parameters:
            if self.parameters["list_type"] not in VALID_LIST_TYPES:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("list_type",),
                            "msg": f"Invalid list_type '{self.parameters['list_type']}'. Must be one of: {', '.join(VALID_LIST_TYPES)}",
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
    - text (str): Quote text content
    - citation (str, optional): Attribution/source
    - align (str): Text alignment - "left", "center", "right" (default: "left")
    """

    widget_type: ClassVar[str] = "Type.Quote"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate TypeQuote-specific parameters."""
        if "align" in self.parameters:
            # Quote only supports left, center, right (not justify)
            valid_quote_aligns = ["left", "center", "right"]
            if self.parameters["align"] not in valid_quote_aligns:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("align",),
                            "msg": f"Invalid align '{self.parameters['align']}'. Must be one of: {', '.join(valid_quote_aligns)}",
                            "input": self.parameters["align"],
                            "ctx": {"error": ValueError(f"Invalid align '{self.parameters['align']}'")},
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
            "align": self.parameters.get("align", "left"),
        }
