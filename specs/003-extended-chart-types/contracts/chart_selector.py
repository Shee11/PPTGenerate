# Chart Selector Python Contract
# Feature: 003-extended-chart-types
# Location: src/generation/content/chart_selector.py

"""
Type definitions for LLM-based chart type selection.
"""

from typing import TypedDict, Optional, List, Literal
from dataclasses import dataclass

# Supported chart types
ChartTypeLiteral = Literal[
    "area",
    "bar", 
    "barStats",
    "bubble",
    "doughnut",
    "pie",
    "line",
    "polarArea",
    "radar"
]


class ChartDataPoint(TypedDict, total=False):
    """Data point structure passed to chart selector."""
    label: str          # Required
    value: float        # Required
    color: str          # Optional
    before: float       # Optional (cluster charts)
    after: float        # Optional (cluster charts)
    x: float            # Optional (bubble/scatter)
    y: float            # Optional (bubble/scatter)
    size: float         # Optional (bubble)


@dataclass
class ChartSelectionContext:
    """Context provided to LLM for chart selection."""
    
    data: List[dict]
    """The raw data points to visualize."""
    
    description: str
    """Human description of what the data represents."""
    
    slide_context: str = ""
    """Surrounding slide content for context."""
    
    suggested_type: Optional[str] = None
    """Hint from author if provided."""


@dataclass
class ChartSelectionResult:
    """Result from chart type selection."""
    
    chart_type: ChartTypeLiteral
    """The selected chart type."""
    
    confidence: float
    """Confidence score between 0.0 and 1.0."""
    
    reasoning: str
    """Explanation for why this chart type was selected."""


# Function signatures

async def select_chart_type(context: ChartSelectionContext) -> ChartSelectionResult:
    """
    Use LLM to select the optimal chart type for the given data.
    
    Args:
        context: Selection context with data and description
        
    Returns:
        ChartSelectionResult with type, confidence, and reasoning
        
    Raises:
        ChartSelectionError: If selection fails
    """
    ...


def validate_chart_data(data: List[dict], chart_type: ChartTypeLiteral) -> bool:
    """
    Validate that data matches the requirements for the chart type.
    
    Args:
        data: The data points to validate
        chart_type: The target chart type
        
    Returns:
        True if valid, raises exception if not
        
    Raises:
        ChartDataValidationError: If data is invalid for chart type
    """
    ...
