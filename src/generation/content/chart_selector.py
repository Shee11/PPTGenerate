"""Chart Selector - LLM-based intelligent chart type selection.

This module provides automatic chart type selection based on data patterns.
The LLM analyzes data characteristics to choose the most effective visualization.

Feature: 003-extended-chart-types
"""
from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Literal

from src.utils.llm_client import call_llm

# =============================================================================
# Types
# =============================================================================

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

# Default fallback when selection fails or confidence is low
DEFAULT_CHART_TYPE: ChartTypeLiteral = "bar"

# Confidence threshold for accepting LLM selection
CONFIDENCE_THRESHOLD = 0.5

logger = logging.getLogger(__name__)


@dataclass
class ChartSelectionContext:
    """Context provided to LLM for chart type selection."""
    
    data: List[Dict[str, Any]]
    """The raw data points to visualize."""
    
    description: str = ""
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


# =============================================================================
# Chart Selection Prompt
# =============================================================================

CHART_SELECTION_SYSTEM_PROMPT = """You are an expert data visualization consultant.
Your task is to analyze data and select the most appropriate chart type.

## Chart Type Guidelines

| Chart Type | Best For | Data Pattern |
|------------|----------|--------------|
| area | Cumulative trends, time-series with volume | Sequential labels (dates, months), shows accumulation |
| bar | Categorical comparisons | Discrete categories, comparing values side-by-side |
| barStats | Rankings, sorted comparisons | Ordered items, emphasizing relative differences |
| bubble | 3D relationships | Data with x, y, and size dimensions |
| doughnut | Proportions (with emphasis) | Parts of a whole, percentages, market share |
| pie | Simple proportions | Parts of a whole, 3-7 segments ideal |
| line | Trends over time | Sequential data, showing change direction |
| polarArea | Cyclical/periodic data | Hours, days, months, seasons - circular patterns |
| radar | Multivariate comparison | 3+ attributes per item, comparing profiles |

## Selection Rules

1. **Time-series data** (dates, months, quarters): Use `area` or `line`
2. **Categorical comparison** (products, regions, teams): Use `bar`
3. **Proportions summing to ~100%**: Use `pie` or `doughnut`
4. **Sorted rankings**: Use `barStats` (horizontal bars)
5. **3D data** (x, y, size present): Use `bubble`
6. **4+ attributes per item**: Use `radar`
7. **Cyclical/periodic patterns**: Use `polarArea`

## Response Format

Return a JSON object:
```json
{
  "chart_type": "bar",
  "confidence": 0.85,
  "reasoning": "The data shows categorical comparison between products with no time dimension."
}
```

Confidence levels:
- 0.9+: Very clear pattern match
- 0.7-0.9: Good fit with minor ambiguity
- 0.5-0.7: Reasonable choice but alternatives exist
- <0.5: Uncertain, fallback to bar chart recommended
"""

CHART_SELECTION_USER_TEMPLATE = """Analyze this data and select the best chart type.

## Data to Visualize
```json
{data_json}
```

## Context
{description}

{slide_context_section}

{suggested_type_section}

Select the most appropriate chart type and explain your reasoning.
"""


# =============================================================================
# Main Functions
# =============================================================================

async def select_chart_type_async(context: ChartSelectionContext) -> ChartSelectionResult:
    """
    Use LLM to select the optimal chart type for the given data (async version).
    
    Args:
        context: Selection context with data and description
        
    Returns:
        ChartSelectionResult with type, confidence, and reasoning
    """
    # If explicit type suggested and valid, honor it
    if context.suggested_type and context.suggested_type in get_valid_chart_types():
        logger.info(f"Honoring explicit chart type: {context.suggested_type}")
        return ChartSelectionResult(
            chart_type=context.suggested_type,  # type: ignore
            confidence=1.0,
            reasoning=f"Explicit chart type '{context.suggested_type}' specified by author."
        )
    
    # Build user prompt
    user_prompt = _build_selection_prompt(context)
    
    # Call LLM
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o')
    
    try:
        response = call_llm(
            system_prompt=CHART_SELECTION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            deployment=deployment,
            temperature=0.3,  # Lower temperature for more consistent selection
            max_tokens=500,
        )
        
        result = _parse_selection_response(response)
        
        # Apply confidence threshold
        if result.confidence < CONFIDENCE_THRESHOLD:
            logger.info(
                f"Chart selection confidence {result.confidence} below threshold {CONFIDENCE_THRESHOLD}. "
                f"Using fallback: {DEFAULT_CHART_TYPE}"
            )
            return ChartSelectionResult(
                chart_type=DEFAULT_CHART_TYPE,
                confidence=result.confidence,
                reasoning=f"Low confidence ({result.confidence}). Fallback to {DEFAULT_CHART_TYPE}. "
                          f"Original selection was {result.chart_type}: {result.reasoning}"
            )
        
        logger.info(f"Chart selection: {result.chart_type} (confidence: {result.confidence})")
        return result
        
    except Exception as e:
        logger.error(f"Chart selection failed: {e}")
        return ChartSelectionResult(
            chart_type=DEFAULT_CHART_TYPE,
            confidence=0.0,
            reasoning=f"Selection failed with error: {str(e)}. Using fallback."
        )


def select_chart_type(context: ChartSelectionContext) -> ChartSelectionResult:
    """
    Use LLM to select the optimal chart type for the given data (sync version).
    
    This is a synchronous wrapper around select_chart_type_async.
    
    Args:
        context: Selection context with data and description
        
    Returns:
        ChartSelectionResult with type, confidence, and reasoning
    """
    import asyncio
    
    # Check if we're already in an event loop
    try:
        loop = asyncio.get_running_loop()
        # We're in an async context, need to use a different approach
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                asyncio.run,
                select_chart_type_async(context)
            )
            return future.result()
    except RuntimeError:
        # No running loop, we can use asyncio.run directly
        return asyncio.run(select_chart_type_async(context))


def get_valid_chart_types() -> List[str]:
    """Get list of valid chart type strings."""
    return ["area", "bar", "barStats", "bubble", "doughnut", "pie", "line", "polarArea", "radar"]


def validate_chart_data(data: List[Dict], chart_type: ChartTypeLiteral) -> bool:
    """
    Validate that data matches the requirements for the chart type.
    
    Args:
        data: The data points to validate
        chart_type: The target chart type
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If data is invalid for chart type
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    if chart_type == "bubble":
        # Bubble requires x, y, size
        for i, point in enumerate(data):
            if not all(k in point for k in ['x', 'y', 'size']):
                raise ValueError(
                    f"Bubble chart requires x, y, size fields. "
                    f"Point {i} missing: {set(['x', 'y', 'size']) - set(point.keys())}"
                )
    
    elif chart_type == "radar":
        # Radar needs at least 3 points
        if len(data) < 3:
            raise ValueError(f"Radar chart requires at least 3 data points, got {len(data)}")
        # Each point needs label and value
        for i, point in enumerate(data):
            if 'label' not in point or 'value' not in point:
                raise ValueError(f"Radar chart point {i} missing label or value")
    
    else:
        # Most charts need label and value
        for i, point in enumerate(data):
            if 'label' not in point:
                raise ValueError(f"Chart data point {i} missing 'label' field")
            if 'value' not in point and 'before' not in point and 'after' not in point:
                raise ValueError(f"Chart data point {i} missing value field (value, before, or after)")
    
    return True


# =============================================================================
# Helper Functions
# =============================================================================

def _build_selection_prompt(context: ChartSelectionContext) -> str:
    """Build the user prompt for chart selection."""
    # Data JSON
    data_json = json.dumps(context.data, indent=2)
    
    # Slide context section
    slide_context_section = ""
    if context.slide_context:
        slide_context_section = f"## Slide Context\n{context.slide_context}"
    
    # Suggested type section
    suggested_type_section = ""
    if context.suggested_type:
        suggested_type_section = f"## Author Suggestion\nPreferred chart type: {context.suggested_type}"
    
    return CHART_SELECTION_USER_TEMPLATE.format(
        data_json=data_json,
        description=context.description or "No description provided.",
        slide_context_section=slide_context_section,
        suggested_type_section=suggested_type_section,
    )


def _parse_selection_response(response: str) -> ChartSelectionResult:
    """Parse LLM response into ChartSelectionResult."""
    # Try to extract JSON from response
    try:
        # Handle markdown code blocks
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        elif "```" in response:
            json_start = response.find("```") + 3
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            # Try to find JSON object directly
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            json_str = response[json_start:json_end]
        
        data = json.loads(json_str)
        
        chart_type = data.get("chart_type", DEFAULT_CHART_TYPE)
        if chart_type not in get_valid_chart_types():
            logger.warning(f"Invalid chart type '{chart_type}' from LLM, using fallback")
            chart_type = DEFAULT_CHART_TYPE
        
        return ChartSelectionResult(
            chart_type=chart_type,  # type: ignore
            confidence=float(data.get("confidence", 0.5)),
            reasoning=data.get("reasoning", "No reasoning provided.")
        )
        
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        logger.error(f"Failed to parse chart selection response: {e}")
        return ChartSelectionResult(
            chart_type=DEFAULT_CHART_TYPE,
            confidence=0.0,
            reasoning=f"Failed to parse LLM response: {str(e)}"
        )


# =============================================================================
# Integration Helper
# =============================================================================

def should_select_chart_type(atom_data: Dict[str, Any]) -> bool:
    """
    Determine if chart type selection should be invoked for an atom.
    
    Args:
        atom_data: The atom dictionary from content generation
        
    Returns:
        True if chart selection should be invoked
    """
    # Check if this is a chart-related visual
    visual = atom_data.get("visual", "").lower()
    if "chart" not in visual:
        return False
    
    # Check if chart type is already specified
    chart_type = atom_data.get("chart_type") or atom_data.get("chartType")
    if chart_type and chart_type in get_valid_chart_types():
        return False  # Already specified, skip selection
    
    # Check if there's data to analyze
    data = atom_data.get("data") or atom_data.get("chart_data")
    if not data or not isinstance(data, list):
        return False  # No data to analyze
    
    return True
