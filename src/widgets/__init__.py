"""Widget implementations."""

# Import all widget modules to trigger registration
from src.widgets.base import BaseWidget, WidgetRegistry
from src.widgets.data import DataBigNumWidget, DataProgressWidget, DataTrendWidget
from src.widgets.typography import TypeBodyWidget, TypeDisplayWidget, TypeHeadingWidget

__all__ = [
    "BaseWidget",
    "WidgetRegistry",
    "TypeDisplayWidget",
    "TypeHeadingWidget",
    "TypeBodyWidget",
    "DataBigNumWidget",
    "DataTrendWidget",
    "DataProgressWidget",
]
