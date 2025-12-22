"""Layout compatibility validator for Slidev widgets and layouts.

This module validates that widgets are compatible with their assigned layout slots
and suggests better alternatives when mismatches are detected.
"""
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class LayoutSlotConstraints:
    """Constraints for a layout slot."""
    
    name: str
    min_width: str  # "narrow" | "medium" | "wide" | "full"
    preferred_widgets: List[str]  # Widget types that work well
    avoid_widgets: List[str]  # Widget types that don't fit well
    max_content_length: Optional[int] = None  # Recommended max chars for text
    

# Widget size/space requirements
WIDGET_SPACE_REQUIREMENTS = {
    # Typography widgets
    "Type.Display": {"width": "wide", "min_chars": 50, "typical_chars": 100},
    "Type.Heading": {"width": "medium", "min_chars": 30, "typical_chars": 60},
    "Type.Body": {"width": "medium", "min_chars": 100, "typical_chars": 300},
    "Type.List": {"width": "medium", "min_chars": 80, "typical_chars": 200},
    "Type.Quote": {"width": "wide", "min_chars": 100, "typical_chars": 250},  # Quotes need space!
    "Type.Code": {"width": "wide", "min_chars": 200, "typical_chars": 500},
    
    # Data widgets
    "TableWidget": {"width": "wide", "min_chars": 200, "typical_chars": 400},
    "ChartWidget": {"width": "medium", "min_chars": 50, "typical_chars": 100},
    "MetricWidget": {"width": "narrow", "min_chars": 20, "typical_chars": 50},
    "QuoteWidget": {"width": "wide", "min_chars": 100, "typical_chars": 250},  # Same as Type.Quote
}


# Layout slot definitions with constraints
LAYOUT_CONSTRAINTS = {
    "hero-split": {
        "left": LayoutSlotConstraints(
            name="left",
            min_width="medium",
            preferred_widgets=["Type.Heading", "Type.Body", "Type.List", "MetricWidget"],
            avoid_widgets=["TableWidget", "Type.Quote", "QuoteWidget"],
            max_content_length=200
        ),
        "right": LayoutSlotConstraints(
            name="right",
            min_width="medium",
            preferred_widgets=["Type.Quote", "QuoteWidget", "Type.Body", "ChartWidget"],
            avoid_widgets=["TableWidget"],
            max_content_length=300
        ),
    },
    
    "smart-grid": {
        "col1": LayoutSlotConstraints(
            name="col1",
            min_width="narrow",
            preferred_widgets=["Type.Heading", "Type.Body", "MetricWidget"],
            avoid_widgets=["Type.Quote", "QuoteWidget", "TableWidget", "Type.Code"],
            max_content_length=150
        ),
        "col2": LayoutSlotConstraints(
            name="col2",
            min_width="narrow",
            preferred_widgets=["Type.Heading", "Type.Body", "MetricWidget"],
            avoid_widgets=["Type.Quote", "QuoteWidget", "TableWidget", "Type.Code"],
            max_content_length=150
        ),
        "col3": LayoutSlotConstraints(
            name="col3",
            min_width="narrow",
            preferred_widgets=["Type.Heading", "Type.Body", "MetricWidget"],
            avoid_widgets=["Type.Quote", "QuoteWidget", "TableWidget", "Type.Code"],
            max_content_length=150
        ),
        "col4": LayoutSlotConstraints(
            name="col4",
            min_width="narrow",
            preferred_widgets=["Type.Heading", "Type.Body", "MetricWidget"],
            avoid_widgets=["Type.Quote", "QuoteWidget", "TableWidget", "Type.Code"],
            max_content_length=150
        ),
    },
    
    "timeline": {
        "step1": LayoutSlotConstraints(
            name="step1",
            min_width="narrow",
            preferred_widgets=["Type.Heading", "Type.Body"],
            avoid_widgets=["Type.Quote", "QuoteWidget", "TableWidget"],
            max_content_length=100
        ),
        # Similar for step2-step6
    },
    
    "full-bleed": {
        "default": LayoutSlotConstraints(
            name="default",
            min_width="full",
            preferred_widgets=["Type.Quote", "QuoteWidget", "Type.Display", "Type.Heading"],
            avoid_widgets=[],
            max_content_length=500
        ),
    },
    
    "default": {
        "default": LayoutSlotConstraints(
            name="default",
            min_width="full",
            preferred_widgets=["Type.Heading", "Type.Body", "Type.List", "Type.Quote"],
            avoid_widgets=[],
            max_content_length=400
        ),
    },
}


# Layout suggestions based on widget types
LAYOUT_RECOMMENDATIONS = {
    # When you have quotes
    "Type.Quote": ["full-bleed", "hero-split", "default", "center"],
    "QuoteWidget": ["full-bleed", "hero-split", "default", "center"],
    
    # When you have tables
    "TableWidget": ["full-bleed", "default", "dashboard"],
    
    # When you have multiple metrics
    "MetricWidget": ["smart-grid", "dashboard", "feature-grid"],
    
    # When you have code
    "Type.Code": ["full-bleed", "default", "two-cols"],
}


def validate_widget_in_slot(
    widget_type: str,
    widget_data: dict,
    layout: str,
    slot_name: str
) -> Tuple[bool, List[str]]:
    """Validate if a widget fits well in a layout slot.
    
    Args:
        widget_type: Widget type (e.g., "Type.Quote", "QuoteWidget")
        widget_data: Widget parameters dict
        layout: Layout name (e.g., "smart-grid")
        slot_name: Slot name (e.g., "col1")
        
    Returns:
        Tuple of (is_valid, warnings)
        - is_valid: True if widget fits well, False if problematic
        - warnings: List of warning messages
    """
    warnings = []
    
    # Get layout constraints
    layout_slots = LAYOUT_CONSTRAINTS.get(layout, {})
    slot_constraints = layout_slots.get(slot_name)
    
    if not slot_constraints:
        # Unknown layout/slot, can't validate
        return True, []
    
    # Check if widget type is explicitly avoided
    if widget_type in slot_constraints.avoid_widgets:
        warnings.append(
            f"⚠️ {widget_type} is not recommended for {layout}.{slot_name} "
            f"(slot is too narrow). Consider using {', '.join(LAYOUT_RECOMMENDATIONS.get(widget_type, ['full-bleed']))}"
        )
        return False, warnings
    
    # Check widget space requirements
    widget_reqs = WIDGET_SPACE_REQUIREMENTS.get(widget_type, {})
    required_width = widget_reqs.get("width", "narrow")
    
    # Width compatibility check
    width_hierarchy = ["narrow", "medium", "wide", "full"]
    slot_width_idx = width_hierarchy.index(slot_constraints.min_width)
    required_width_idx = width_hierarchy.index(required_width)
    
    if required_width_idx > slot_width_idx:
        warnings.append(
            f"⚠️ {widget_type} requires '{required_width}' width but {layout}.{slot_name} "
            f"only provides '{slot_constraints.min_width}'. Content may be cramped."
        )
        return False, warnings
    
    # Check content length for text widgets
    if "text" in widget_data and slot_constraints.max_content_length:
        text = widget_data.get("text", "")
        if len(text) > slot_constraints.max_content_length:
            warnings.append(
                f"⚠️ Text content ({len(text)} chars) exceeds recommended max "
                f"({slot_constraints.max_content_length} chars) for {layout}.{slot_name}"
            )
            return False, warnings
    
    return True, warnings


def suggest_better_layout(widgets: Dict[str, dict]) -> List[str]:
    """Suggest better layouts based on widget types.
    
    Args:
        widgets: Dict mapping slot names to widget dicts (with 'type' field)
        
    Returns:
        List of suggested layout names, ordered by suitability
    """
    widget_types = [w.get("type", "") for w in widgets.values()]
    
    # Count widget types
    has_quote = any(t in ["Type.Quote", "QuoteWidget"] for t in widget_types)
    has_table = any(t == "TableWidget" for t in widget_types)
    has_metrics = sum(1 for t in widget_types if t == "MetricWidget")
    has_code = any(t == "Type.Code" for t in widget_types)
    
    suggestions = []
    
    # Quote-focused layouts
    if has_quote:
        suggestions.extend(["full-bleed", "hero-split", "center"])
    
    # Table-focused layouts
    if has_table:
        suggestions.extend(["full-bleed", "default"])
    
    # Metric-focused layouts
    if has_metrics >= 3:
        suggestions.extend(["smart-grid", "dashboard", "feature-grid"])
    
    # Code-focused layouts
    if has_code:
        suggestions.extend(["full-bleed", "two-cols"])
    
    # Default fallbacks
    if not suggestions:
        suggestions = ["default", "hero-split"]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_suggestions = []
    for layout in suggestions:
        if layout not in seen:
            seen.add(layout)
            unique_suggestions.append(layout)
    
    return unique_suggestions


def validate_slide_layout(slide: dict) -> Tuple[bool, List[str], List[str]]:
    """Validate entire slide layout and widget compatibility.
    
    Args:
        slide: Slide dict with 'layout', 'widgets' fields
        
    Returns:
        Tuple of (is_valid, warnings, suggestions)
        - is_valid: True if all widgets fit well
        - warnings: List of warning messages
        - suggestions: List of suggested alternative layouts
    """
    layout = slide.get("layout", "default")
    widgets = slide.get("widgets", {})
    
    all_warnings = []
    all_valid = True
    
    # Validate each widget in its slot
    for slot_name, widget_data in widgets.items():
        widget_type = widget_data.get("type", "")
        if not widget_type:
            continue
        
        is_valid, warnings = validate_widget_in_slot(
            widget_type, widget_data, layout, slot_name
        )
        
        if not is_valid:
            all_valid = False
            all_warnings.extend(warnings)
    
    # Generate layout suggestions if validation failed
    suggestions = []
    if not all_valid:
        suggestions = suggest_better_layout(widgets)
    
    return all_valid, all_warnings, suggestions


def get_layout_guidance_prompt() -> str:
    """Get guidance prompt for LLM to avoid layout-widget mismatches.
    
    Returns:
        Formatted guidance string to include in slide generation prompts
    """
    return """
**WIDGET-LAYOUT COMPATIBILITY**:
| Widget | ✅ Use in | ❌ Avoid |
|--------|----------|----------|
| Quote/Type.Quote | full-bleed, hero-split, center | smart-grid, timeline |
| Table/Code | full-bleed | grid columns, hero-split |
| Metric | smart-grid, dashboard | - |

**Quick check**: Quote/Table → wide layout. Grid columns → short text only."""
