"""Media widgets for images, code, and icons."""
from typing import Any, ClassVar

from src.common.size_class import SizeClass
from src.paged.widgets.base import BaseWidget, WidgetRegistry

# Valid parameter values for content
VALID_FIT_MODES = ["cover", "contain", "fill", "none"]
VALID_ICON_SIZES = ["small", "medium", "large", "xlarge"]


@WidgetRegistry.register
class MediaFrameWidget(BaseWidget):
    """Image or media frame widget.
    
    Minimum size: M
    
    Parameters:
    - src (str): Image URL or path (required)
    - alt (str): Alternative text for accessibility (required)
    - fit (str): How image fits in frame - "cover", "contain", "fill", "none" (default: "cover")
    - aspect_ratio (str): CSS aspect ratio (e.g., "16/9", "1/1") (optional)
    
    Styling (defined in Style config, not widget parameters):
    - border_radius: Corner rounding
    - background: Background color (for letterboxing)
    """

    widget_type: ClassVar[str] = "Media.Frame"
    min_size: ClassVar[SizeClass] = SizeClass.M

    def validate_parameters(self) -> None:
        """Validate MediaFrame-specific parameters."""
        if "src" not in self.parameters:
            from pydantic_core import ValidationError
            raise ValidationError.from_exception_data(
                "ValueError",
                [
                    {
                        "type": "value_error",
                        "loc": ("src",),
                        "msg": "src parameter is required",
                        "input": self.parameters,
                        "ctx": {"error": ValueError("src parameter is required")},
                    }
                ],
            )
        
        if "alt" not in self.parameters:
            from pydantic_core import ValidationError
            raise ValidationError.from_exception_data(
                "ValueError",
                [
                    {
                        "type": "value_error",
                        "loc": ("alt",),
                        "msg": "alt parameter is required",
                        "input": self.parameters,
                        "ctx": {"error": ValueError("alt parameter is required")},
                    }
                ],
            )

        if "fit" in self.parameters:
            if self.parameters["fit"] not in VALID_FIT_MODES:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("fit",),
                            "msg": f"Invalid fit mode '{self.parameters['fit']}'. Must be one of: {', '.join(VALID_FIT_MODES)}",
                            "input": self.parameters["fit"],
                            "ctx": {"error": ValueError(f"Invalid fit mode '{self.parameters['fit']}'")},
                        }
                    ],
                )

    def render_data(self) -> dict[str, Any]:
        """Generate data for template rendering."""
        return {
            "widget_type": self.widget_type,
            "atom_id": self.atom_id,
            "parameters": self.parameters,
            "src": self.parameters.get("src", ""),
            "alt": self.parameters.get("alt", "Image"),
            "fit": self.parameters.get("fit", "cover"),
            "aspect_ratio": self.parameters.get("aspect_ratio"),
        }

    def measure(self, style: dict[str, Any], max_width: float = float('inf'), max_height: float = float('inf')):
        """Calculate widget content size for MediaFrame.
        
        Media frames are typically fixed size based on slot dimensions.
        """
        from src.common.measurement import MeasuredSize
        
        # If aspect ratio is specified, use it to calculate dimensions
        aspect_ratio = self.parameters.get("aspect_ratio")
        
        if aspect_ratio:
            # Parse aspect ratio (e.g., "16/9" or "16:9")
            ratio_parts = aspect_ratio.replace(":", "/").split("/")
            if len(ratio_parts) == 2:
                try:
                    width_ratio = float(ratio_parts[0])
                    height_ratio = float(ratio_parts[1])
                    
                    # Calculate dimensions maintaining aspect ratio
                    if max_width < float('inf'):
                        width = min(max_width, 800)  # Default max
                        height = width * (height_ratio / width_ratio)
                    else:
                        width = 800
                        height = width * (height_ratio / width_ratio)
                    
                    return MeasuredSize(
                        width=width,
                        height=height,
                        min_width=200,
                        min_height=200 * (height_ratio / width_ratio)
                    )
                except (ValueError, ZeroDivisionError):
                    pass
        
        # Default: Square-ish media frame
        size = min(max_width, 600) if max_width < float('inf') else 600
        
        return MeasuredSize(
            width=size,
            height=size * 0.75,  # 4:3 default aspect ratio
            min_width=200,
            min_height=150
        )


@WidgetRegistry.register
class MediaCodeWidget(BaseWidget):
    """Code snippet display widget.
    
    Minimum size: M
    
    Parameters:
    - code (str): Code snippet to display (required)
    - language (str): Programming language for syntax highlighting (optional)
    - show_line_numbers (bool): Whether to show line numbers (default: False)
    - highlight_lines (str): Comma-separated line numbers to highlight (optional, e.g., "1,5-7")
    
    Styling (defined in Style config, not widget parameters):
    - font: Monospace font token
    - foreground: Text color token
    - background: Background color token
    - border_radius: Corner rounding
    """

    widget_type: ClassVar[str] = "Media.Code"
    min_size: ClassVar[SizeClass] = SizeClass.M

    def validate_parameters(self) -> None:
        """Validate MediaCode-specific parameters."""
        if "code" not in self.parameters:
            from pydantic_core import ValidationError
            raise ValidationError.from_exception_data(
                "ValueError",
                [
                    {
                        "type": "value_error",
                        "loc": ("code",),
                        "msg": "code parameter is required",
                        "input": self.parameters,
                        "ctx": {"error": ValueError("code parameter is required")},
                    }
                ],
            )

    def render_data(self) -> dict[str, Any]:
        """Generate data for template rendering."""
        return {
            "widget_type": self.widget_type,
            "atom_id": self.atom_id,
            "parameters": self.parameters,
            "code": self.parameters.get("code", ""),
            "language": self.parameters.get("language", ""),
            "show_line_numbers": self.parameters.get("show_line_numbers", False),
            "highlight_lines": self.parameters.get("highlight_lines", ""),
        }

    def measure(self, style: dict[str, Any], max_width: float = float('inf'), max_height: float = float('inf')):
        """Calculate widget content size for MediaCode.
        
        Code blocks are text-based, so we measure based on lines and character count.
        """
        from src.common.measurement import WidgetMeasurement
        
        code = self.parameters.get("code", "")
        lines = code.split("\n")
        num_lines = len(lines)
        
        # Get font size for code (typically smaller than body text)
        font_size = style.get("font_size", 14)
        if isinstance(font_size, str):
            if font_size.endswith("px"):
                font_size = float(font_size[:-2])
            else:
                font_size = 14
        
        # Monospace font: width is more predictable
        # Average line length
        avg_line_length = sum(len(line) for line in lines) / max(num_lines, 1)
        char_width = font_size * 0.6  # Monospace char width
        
        # Calculate dimensions
        padding = 40  # Code blocks need more padding
        line_height = 1.5
        
        width = min(
            avg_line_length * char_width + padding,
            max_width if max_width < float('inf') else 800
        )
        
        height = num_lines * font_size * line_height + padding
        
        return WidgetMeasurement.measure_text_widget(
            text=code,
            font_size=font_size,
            max_width=max_width,
            line_height=line_height,
            padding=padding
        )


@WidgetRegistry.register
class MediaIconWidget(BaseWidget):
    """Icon display widget.
    
    Minimum size: S
    
    Parameters:
    - icon (str): Icon identifier (e.g., "check", "arrow-right", "warning") (required)
    - size (str): Icon size - "small", "medium", "large", "xlarge" (default: "medium")
    - label (str): Optional label text below icon (optional)
    
    Styling (defined in Style config, not widget parameters):
    - foreground: Icon color token
    - background: Background color token (for circular backgrounds)
    """

    widget_type: ClassVar[str] = "Media.Icon"
    min_size: ClassVar[SizeClass] = SizeClass.S

    def validate_parameters(self) -> None:
        """Validate MediaIcon-specific parameters."""
        if "icon" not in self.parameters:
            from pydantic_core import ValidationError
            raise ValidationError.from_exception_data(
                "ValueError",
                [
                    {
                        "type": "value_error",
                        "loc": ("icon",),
                        "msg": "icon parameter is required",
                        "input": self.parameters,
                        "ctx": {"error": ValueError("icon parameter is required")},
                    }
                ],
            )
        
        if "size" in self.parameters:
            if self.parameters["size"] not in VALID_ICON_SIZES:
                from pydantic_core import ValidationError
                raise ValidationError.from_exception_data(
                    "ValueError",
                    [
                        {
                            "type": "value_error",
                            "loc": ("size",),
                            "msg": f"Invalid icon size '{self.parameters['size']}'. Must be one of: {', '.join(VALID_ICON_SIZES)}",
                            "input": self.parameters["size"],
                            "ctx": {"error": ValueError(f"Invalid icon size '{self.parameters['size']}'")},
                        }
                    ],
                )

    def render_data(self) -> dict[str, Any]:
        """Generate data for template rendering."""
        return {
            "widget_type": self.widget_type,
            "atom_id": self.atom_id,
            "parameters": self.parameters,
            "icon": self.parameters.get("icon", ""),
            "size": self.parameters.get("size", "medium"),
            "label": self.parameters.get("label"),
        }

    def measure(self, style: dict[str, Any], max_width: float = float('inf'), max_height: float = float('inf')):
        """Calculate widget content size for MediaIcon.
        
        Icons are fixed size based on the size parameter.
        """
        from src.common.measurement import MeasuredSize, WidgetMeasurement
        
        # Icon sizes in pixels
        icon_sizes = {
            "small": 24,
            "medium": 48,
            "large": 96,
            "xlarge": 144,
        }
        
        size_name = self.parameters.get("size", "medium")
        icon_size = icon_sizes.get(size_name, 48)
        
        # If there's a label, add height for it
        label = self.parameters.get("label")
        if label:
            font_size = style.get("font_size", 14)
            if isinstance(font_size, str):
                if font_size.endswith("px"):
                    font_size = float(font_size[:-2])
                else:
                    font_size = 14
            
            # Measure label text
            label_size = WidgetMeasurement.measure_text_widget(
                text=label,
                font_size=font_size,
                max_width=max_width,
                padding=20
            )
            
            return MeasuredSize(
                width=max(icon_size, label_size.width),
                height=icon_size + 10 + label_size.height,  # icon + gap + label
                min_width=icon_size,
                min_height=icon_size + 10 + font_size
            )
        else:
            # Just icon, no label
            return MeasuredSize(
                width=icon_size,
                height=icon_size,
                min_width=icon_size,
                min_height=icon_size
            )
