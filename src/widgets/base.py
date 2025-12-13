"""Base widget class and widget registry."""
from abc import ABC, abstractmethod
from typing import Any, ClassVar, Dict, Optional, Type

from pydantic import BaseModel, Field

from src.common.size_class import SizeClass
from src.common.measurement import MeasuredSize, WidgetMeasurement


class BaseWidget(BaseModel, ABC):
    """Abstract base class for all widgets.
    
    All widgets must:
    - Define a minimum size requirement
    - Specify their widget type (category.name)
    - Implement render method (returns data for template)
    - Implement measure method (calculates content size)
    """

    # Class-level attributes (must be overridden by subclasses)
    widget_type: ClassVar[str]
    min_size: ClassVar[SizeClass]

    # Instance attributes
    atom_id: Optional[str] = Field(default=None, description="Reference to atom data")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Widget-specific parameters")

    @abstractmethod
    def render_data(self) -> dict[str, Any]:
        """Generate data dictionary for template rendering.
        
        Returns:
            Dictionary containing all data needed by the widget's template
        """
        pass

    @abstractmethod
    def measure(self, style: Dict[str, Any], max_width: float = float('inf'), max_height: float = float('inf')) -> MeasuredSize:
        """Calculate widget content size based on parameters and styling.
        
        This is the core auto-layout measurement that determines how much
        space the widget needs based on its content.
        
        Args:
            style: Applied style dictionary (font-size, padding, etc.)
            max_width: Maximum available width (for wrapping)
            max_height: Maximum available height
            
        Returns:
            MeasuredSize with calculated dimensions
            
        Note:
            Implementations should:
            1. Extract content from parameters (text, number, etc.)
            2. Extract styling (font-size, padding, etc.)
            3. Calculate required dimensions
            4. Return MeasuredSize with width/height
        """
        pass

    def validate_parameters(self) -> None:
        """Validate widget-specific parameters.
        
        Override this method in subclasses to add parameter validation.
        Raises ValidationError if parameters are invalid.
        """
        pass

    @classmethod
    def get_widget_type(cls) -> str:
        """Get the widget type identifier."""
        return cls.widget_type

    @classmethod
    def get_min_size(cls) -> SizeClass:
        """Get the minimum size requirement."""
        return cls.min_size


class WidgetRegistry:
    """Registry for widget types.
    
    Allows dynamic widget creation from type strings.
    """

    _widgets: Dict[str, Type[BaseWidget]] = {}

    @classmethod
    def register(cls, widget_class: Type[BaseWidget]) -> Type[BaseWidget]:
        """Register a widget class.
        
        Args:
            widget_class: Widget class to register
            
        Returns:
            The same widget class (for use as decorator)
        """
        widget_type = widget_class.get_widget_type()
        cls._widgets[widget_type] = widget_class
        return widget_class

    @classmethod
    def get(cls, widget_type: str) -> Optional[Type[BaseWidget]]:
        """Get a widget class by type.
        
        Args:
            widget_type: Widget type string (e.g., "Type.Display")
            
        Returns:
            Widget class or None if not found
        """
        return cls._widgets.get(widget_type)

    @classmethod
    def list_types(cls) -> list[str]:
        """List all registered widget types."""
        return list(cls._widgets.keys())
