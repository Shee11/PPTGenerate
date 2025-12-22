"""Widget implementations."""

# Import all widget modules to trigger registration
from src.paged.widgets.base import BaseWidget, WidgetRegistry
from src.paged.widgets.comparison import ComparisonWidget
from src.paged.widgets.data import DataBigNumWidget, DataProgressWidget, DataTrendWidget
from src.paged.widgets.typography import TypeBodyWidget, TypeDisplayWidget, TypeHeadingWidget

__all__ = [
    "BaseWidget",
    "WidgetRegistry",
    "TypeDisplayWidget",
    "TypeHeadingWidget",
    "TypeBodyWidget",
    "ComparisonWidget",
    "DataBigNumWidget",
    "DataTrendWidget",
    "DataProgressWidget",
]
