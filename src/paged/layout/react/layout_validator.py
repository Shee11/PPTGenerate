"""Layout compatibility validator for React MDX widgets and layouts.

This module validates that widgets are compatible with their assigned layout slots
and suggests better alternatives when mismatches are detected.

It also provides whitespace and balance detection for identifying layout issues
like trapped empty space and unbalanced content distribution.
"""
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import re
import json


class LayoutIssueType(Enum):
    """Types of layout issues that can be detected."""
    TRAPPED_WHITESPACE = "trapped_whitespace"
    UNBALANCED_COLUMNS = "unbalanced_columns"
    SPARSE_CONTENT = "sparse_content"
    EMPTY_SLOT = "empty_slot"
    CONTENT_OVERFLOW = "content_overflow"
    CONTENT_CUTOFF = "content_cutoff"
    MISSING_VISUAL_BLOCK = "missing_visual_block"
    LONELY_ELEMENT = "lonely_element"
    INSUFFICIENT_PAGE_COVERAGE = "insufficient_page_coverage"  # Page-level coverage below 70%
    CONTENT_GAPS = "content_gaps"  # Holes between content blocks
    CONSECUTIVE_LISTS_WITHOUT_HEADER = "consecutive_lists_without_header"  # SmartLists without Heading between
    METRIC_VALUE_TOO_LONG = "metric_value_too_long"  # Metric value exceeds 10 characters
    DASHBOARD_CONTENT_MISMATCH = "dashboard_content_mismatch"  # Wrong content in dashboard main/sidebar
    PROCESSSTRIP_TOO_WIDE = "processstrip_too_wide"  # ProcessStrip has too many items for narrow layout


@dataclass
class LayoutIssue:
    """Represents a detected layout issue."""
    issue_type: LayoutIssueType
    severity: str  # "error" | "warning" | "info"
    slide_id: str
    location: str  # e.g., "left column", "sidebar", "bottom area"
    description: str
    suggestion: str
    affected_elements: List[str] = field(default_factory=list)


@dataclass
class SlotAnalysis:
    """Analysis of a layout slot's content."""
    slot_name: str
    element_count: int
    estimated_height_pct: float  # 0-100
    content_density: str  # "empty" | "sparse" | "moderate" | "dense"
    visual_weight: float  # 0-1 based on content type
    has_visual_block: bool  # Chart, Diagram, Image, BigNum
    has_text_block: bool
    elements: List[str] = field(default_factory=list)


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
    "Type.Subheading": {"width": "medium", "min_chars": 30, "typical_chars": 50},
    "Type.Body": {"width": "medium", "min_chars": 100, "typical_chars": 300},
    "Type.Caption": {"width": "narrow", "min_chars": 30, "typical_chars": 80},
    "Type.Code": {"width": "wide", "min_chars": 200, "typical_chars": 500},
    
    # List widgets
    "Type.List": {"width": "medium", "min_chars": 80, "typical_chars": 200},
    "Type.NumberedList": {"width": "medium", "min_chars": 80, "typical_chars": 200},
    
    # Chart widgets
    "Type.BarChart": {"width": "medium", "min_chars": 50, "typical_chars": 100},
    "Type.LineChart": {"width": "medium", "min_chars": 50, "typical_chars": 100},
    "Type.PieChart": {"width": "medium", "min_chars": 50, "typical_chars": 100},
    
    # Data widgets
    "Type.MetricGroup": {"width": "medium", "min_chars": 50, "typical_chars": 150},
    "Type.Table": {"width": "wide", "min_chars": 200, "typical_chars": 400},
    
    # Content widgets
    "Type.Quote": {"width": "wide", "min_chars": 100, "typical_chars": 250},
    "Type.Card": {"width": "narrow", "min_chars": 50, "typical_chars": 100},
    "Type.Image": {"width": "medium", "min_chars": 0, "typical_chars": 50},
    "Type.Callout": {"width": "medium", "min_chars": 50, "typical_chars": 150},
}


# Layout slot definitions with constraints
LAYOUT_CONSTRAINTS = {
    "cover": {
        "title": LayoutSlotConstraints(
            name="title",
            min_width="wide",
            preferred_widgets=["Type.Display", "Type.Heading"],
            avoid_widgets=["Type.Table", "Type.BarChart", "Type.List"],
            max_content_length=100
        ),
        "subtitle": LayoutSlotConstraints(
            name="subtitle",
            min_width="wide",
            preferred_widgets=["Type.Body", "Type.Subheading"],
            avoid_widgets=["Type.Table", "Type.BarChart"],
            max_content_length=200
        ),
    },
    
    "split": {
        "left": LayoutSlotConstraints(
            name="left",
            min_width="medium",
            preferred_widgets=["Type.Heading", "Type.Body", "Type.List", "Type.MetricGroup"],
            avoid_widgets=[],
            max_content_length=500
        ),
        "right": LayoutSlotConstraints(
            name="right",
            min_width="medium",
            preferred_widgets=["Type.Quote", "Type.Body", "Type.BarChart", "Type.Image"],
            avoid_widgets=[],
            max_content_length=500
        ),
    },
    
    "grid": {
        "col": LayoutSlotConstraints(
            name="col",
            min_width="narrow",
            preferred_widgets=["Type.Heading", "Type.Body", "Type.Card", "Type.MetricGroup"],
            avoid_widgets=["Type.Quote", "Type.Table", "Type.Code"],
            max_content_length=150
        ),
        "card": LayoutSlotConstraints(
            name="card",
            min_width="narrow",
            preferred_widgets=["Type.Card", "Type.Body", "Type.Heading"],
            avoid_widgets=["Type.Quote", "Type.Table", "Type.Code", "Type.BarChart"],
            max_content_length=100
        ),
    },
    
    "fullbleed": {
        "default": LayoutSlotConstraints(
            name="default",
            min_width="full",
            preferred_widgets=["Type.Display", "Type.Quote", "Type.Heading", "Type.Image"],
            avoid_widgets=["Type.Table", "Type.MetricGroup"],
            max_content_length=300
        ),
    },
    
    "timeline": {
        "step": LayoutSlotConstraints(
            name="step",
            min_width="narrow",
            preferred_widgets=["Type.Body", "Type.Heading"],
            avoid_widgets=["Type.Quote", "Type.Table", "Type.BarChart"],
            max_content_length=100
        ),
        "item": LayoutSlotConstraints(
            name="item",
            min_width="narrow",
            preferred_widgets=["Type.Body", "Type.Heading"],
            avoid_widgets=["Type.Quote", "Type.Table", "Type.BarChart"],
            max_content_length=100
        ),
    },
    
    "dashboard": {
        "header": LayoutSlotConstraints(
            name="header",
            min_width="wide",
            preferred_widgets=["Type.Heading", "Type.Display"],
            avoid_widgets=["Type.Table", "Type.Quote"],
            max_content_length=80
        ),
        "panel": LayoutSlotConstraints(
            name="panel",
            min_width="medium",
            preferred_widgets=["Type.MetricGroup", "Type.BarChart", "Type.LineChart", "Type.Heading"],
            avoid_widgets=["Type.Quote", "Type.Code"],
            max_content_length=200
        ),
    },
}


# Layout suggestions based on widget types
LAYOUT_RECOMMENDATIONS = {
    # Wide content widgets
    "Type.Quote": ["split", "fullbleed"],
    "Type.Table": ["split", "fullbleed"],
    "Type.Code": ["split", "fullbleed"],
    "Type.Display": ["cover", "fullbleed", "split"],
    
    # Chart widgets
    "Type.BarChart": ["split", "dashboard"],
    "Type.LineChart": ["split", "dashboard"],
    "Type.PieChart": ["split", "dashboard"],
    
    # Data widgets
    "Type.MetricGroup": ["dashboard", "grid", "split"],
    
    # Narrow widgets
    "Type.Card": ["grid"],
}


def _get_slot_type(slot_name: str) -> str:
    """Determine slot type from slot name pattern.
    
    Args:
        slot_name: Full slot name (e.g., "left_title", "col1_body", "step1")
        
    Returns:
        Base slot type (e.g., "left", "col", "step")
    """
    # Check for numbered patterns: col1_*, card1, step1, panel1, item1
    if re.match(r'col\d+', slot_name):
        return "col"
    if re.match(r'card\d+', slot_name):
        return "card"
    if re.match(r'step\d+', slot_name):
        return "step"
    if re.match(r'item\d+', slot_name):
        return "item"
    if re.match(r'panel\d+', slot_name):
        return "panel"
    
    # Check for prefixed patterns: left_*, right_*
    if slot_name.startswith("left"):
        return "left"
    if slot_name.startswith("right"):
        return "right"
    
    # Direct matches
    if slot_name in ["title", "subtitle", "header"]:
        return slot_name
    
    return "default"


def validate_widget_in_slot(
    widget_type: str,
    widget_data: dict,
    layout: str,
    slot_name: str
) -> Tuple[bool, List[str]]:
    """Validate if a widget fits well in a layout slot.
    
    Args:
        widget_type: Widget type (e.g., "Type.Quote", "Type.BarChart")
        widget_data: Widget parameters dict
        layout: Layout name (e.g., "grid", "split")
        slot_name: Slot name (e.g., "col1_body", "left_title")
        
    Returns:
        Tuple of (is_valid, warnings)
        - is_valid: True if widget fits well, False if problematic
        - warnings: List of warning messages
    """
    warnings = []
    
    # Get layout constraints
    layout_slots = LAYOUT_CONSTRAINTS.get(layout, {})
    
    # Determine slot type from slot name
    slot_type = _get_slot_type(slot_name)
    slot_constraints = layout_slots.get(slot_type)
    
    if not slot_constraints:
        # Check for default constraint
        slot_constraints = layout_slots.get("default")
        if not slot_constraints:
            # Unknown layout/slot, can't validate
            return True, []
    
    # Check if widget type is explicitly avoided
    if widget_type in slot_constraints.avoid_widgets:
        recommended = LAYOUT_RECOMMENDATIONS.get(widget_type, ["split", "fullbleed"])
        warnings.append(
            f"[WARN] {widget_type} is not recommended for {layout}.{slot_name} "
            f"(slot is too narrow). Consider using: {', '.join(recommended)}"
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
            f"[WARN] {widget_type} requires '{required_width}' width but {layout}.{slot_name} "
            f"only provides '{slot_constraints.min_width}'. Content may be cramped."
        )
        return False, warnings
    
    # Check content length for text widgets
    params = widget_data.get("parameters", {})
    if "text" in params and slot_constraints.max_content_length:
        text = params.get("text", "")
        if len(text) > slot_constraints.max_content_length:
            warnings.append(
                f"[WARN] Text content ({len(text)} chars) exceeds recommended max "
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
    has_quote = any(t == "Type.Quote" for t in widget_types)
    has_table = any(t == "Type.Table" for t in widget_types)
    has_metrics = sum(1 for t in widget_types if t == "Type.MetricGroup")
    has_charts = sum(1 for t in widget_types if t in ["Type.BarChart", "Type.LineChart", "Type.PieChart"])
    has_cards = sum(1 for t in widget_types if t == "Type.Card")
    has_code = any(t == "Type.Code" for t in widget_types)
    has_display = any(t == "Type.Display" for t in widget_types)
    
    suggestions = []
    
    # Quote-focused layouts
    if has_quote:
        suggestions.extend(["split", "fullbleed"])
    
    # Table/Code-focused layouts
    if has_table or has_code:
        suggestions.extend(["split", "fullbleed"])
    
    # Metric/Chart-focused layouts
    if has_metrics >= 2 or has_charts >= 2:
        suggestions.extend(["dashboard", "split"])
    
    # Card-focused layouts
    if has_cards >= 2:
        suggestions.extend(["grid"])
    
    # Display-focused layouts
    if has_display:
        suggestions.extend(["cover", "fullbleed", "split"])
    
    # Default fallbacks
    if not suggestions:
        suggestions = ["split", "grid"]
    
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
    layout = slide.get("layout", "split")
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
**REACT MDX WIDGET-LAYOUT COMPATIBILITY**:
| Widget | ✅ Use in | ❌ Avoid |
|--------|----------|----------|
| Type.Quote, Type.Table | split, fullbleed | grid columns, timeline |
| Type.Code | split, fullbleed | grid columns |
| Type.Display | cover, fullbleed, split | grid columns |
| Type.MetricGroup | dashboard, grid, split | timeline |
| Type.Card | grid | timeline, dashboard |
| Type.BarChart, Type.LineChart | split, dashboard | grid columns |

**Quick check**: Wide content (Quote/Table/Code) → split or fullbleed. Grid → brief content only."""


# =============================================================================
# WHITESPACE AND BALANCE DETECTION SYSTEM
# =============================================================================

# Estimated height percentages for different component types (of slide height)
COMPONENT_HEIGHT_ESTIMATES = {
    # Typography
    "Heading": 8,
    "Text": 10,
    "SmartList": 20,
    "QuoteBlock": 15,
    
    # Data visualization
    "BigNum": 15,
    "MetricGroup": 18,
    "MetricStrip": 10,
    "ChartBar": 30,
    "ChartLine": 30,
    "ChartPie": 30,
    "TableData": 25,
    
    # Blocks
    "CardGroup": 25,
    "Card": 12,
    "Callout": 12,
    "Diagram": 35,
    
    # Media
    "ImageBlock": 30,
    "ProcessDiagram": 25,
}

# Visual weight (how much visual attention a component draws)
COMPONENT_VISUAL_WEIGHT = {
    "BigNum": 0.9,
    "ChartBar": 0.8,
    "ChartLine": 0.8,
    "ChartPie": 0.8,
    "Diagram": 0.85,
    "ImageBlock": 0.75,
    "MetricGroup": 0.7,
    "CardGroup": 0.65,
    "QuoteBlock": 0.6,
    "TableData": 0.6,
    "Callout": 0.5,
    "SmartList": 0.4,
    "Heading": 0.3,
    "Text": 0.2,
}

# Components considered as "visual blocks" (non-text heavy)
VISUAL_BLOCK_COMPONENTS = {
    "BigNum", "ChartBar", "ChartLine", "ChartPie", 
    "Diagram", "ImageBlock", "MetricGroup", "CardGroup",
    "ProcessDiagram", "TableData"
}

# Maximum content thresholds for overflow detection
# These represent estimated heights as percentage of slide
OVERFLOW_THRESHOLDS = {
    "LayoutStacked": 95,      # Single column, can fit more
    "LayoutSplit": 90,        # Split layouts have less vertical space per side
    "LayoutDashboard": 85,    # Dashboard has header/footer reducing main area
    "LayoutCover": 70,        # Cover should be minimal
    "default": 90
}

# Minimum content thresholds for split layouts (per side)
# Below this is considered "under-constructed" and triggers error
MIN_CONTENT_THRESHOLDS = {
    "LayoutSplit": 65,        # Each side needs at least 65% height for visual balance
    "LayoutDashboard": 50,    # Main area needs substantial content
    "LayoutStacked": 60,      # Single column should be well-filled
    "default": 45
}

# Minimum TOTAL page coverage - 70% of page should have content
# This catches pages with holes/gaps even if individual slots aren't flagged
MIN_PAGE_COVERAGE = 70  # 70% minimum total content coverage for dense layouts

# Minimum elements per side for split layouts to avoid "under-construction" look
MIN_ELEMENTS_SPLIT_SIDE = 4  # At least 4 elements per side (Heading + visual + text + supporting)

# Minimum total elements for different layout types
MIN_TOTAL_ELEMENTS = {
    "LayoutStacked": 4,       # At least 4 elements for stacked
    "LayoutDashboard": 5,     # At least 5 elements across all slots
    "LayoutTimeline": 4,      # At least 4 timeline items
    "LayoutCover": 2,         # Cover can be minimal
    "default": 4
}

# Maximum element counts before overflow is likely
MAX_ELEMENTS_PER_LAYOUT = {
    "LayoutStacked": 8,
    "LayoutSplit": 5,         # Per side
    "LayoutDashboard": 6,     # Per slot
    "LayoutCover": 4,
    "default": 6
}

# Heavy components that take significant vertical space
HEAVY_COMPONENTS = {
    "TableData": 35,          # Tables can be very tall
    "Diagram": 40,
    "ChartBar": 35,
    "ChartLine": 35,
    "ChartPie": 30,
    "CardGroup": 30,
    "MetricGroup": 25,
}


def _extract_components_from_mdx(mdx_content: str) -> List[Dict[str, Any]]:
    """Extract component information from MDX content.
    
    Args:
        mdx_content: Raw MDX string
        
    Returns:
        List of component dicts with name, props, location
    """
    components = []
    
    # Pattern to match React components: <ComponentName ...props>
    component_pattern = r'<(\w+)(?:\s+[^>]*)?(?:/>|>)'
    
    for match in re.finditer(component_pattern, mdx_content):
        component_name = match.group(1)
        # Skip layout containers
        if component_name in ['Left', 'Right', 'Main', 'Sidebar', 'Header', 'Footer']:
            continue
        if component_name.startswith('Layout'):
            continue
        
        components.append({
            "name": component_name,
            "position": match.start(),
            "full_match": match.group(0)
        })
    
    return components


def _analyze_slot_content(slot_name: str, components: List[Dict]) -> SlotAnalysis:
    """Analyze the content of a specific layout slot.
    
    Args:
        slot_name: Name of the slot (e.g., "left", "right", "main")
        components: List of components in this slot
        
    Returns:
        SlotAnalysis with density and balance metrics
    """
    element_count = len(components)
    element_names = [c["name"] for c in components]
    
    # Calculate estimated height
    total_height = sum(
        COMPONENT_HEIGHT_ESTIMATES.get(c["name"], 10) 
        for c in components
    )
    
    # Calculate visual weight
    total_weight = sum(
        COMPONENT_VISUAL_WEIGHT.get(c["name"], 0.3)
        for c in components
    )
    avg_weight = total_weight / max(element_count, 1)
    
    # Check for visual blocks
    has_visual = any(c["name"] in VISUAL_BLOCK_COMPONENTS for c in components)
    has_text = any(c["name"] in ["Text", "Heading", "SmartList"] for c in components)
    
    # Determine density - stricter thresholds
    # For split layouts, each side should have substantial content
    # Consider both element count AND estimated height
    if element_count == 0:
        density = "empty"
    elif element_count < 3 or total_height < 45:
        density = "sparse"      # Need both 3+ elements AND 45% height
    elif element_count < 4 or total_height < 65:
        density = "moderate"    # Need both 4+ elements AND 65% height  
    else:
        density = "dense"
    
    return SlotAnalysis(
        slot_name=slot_name,
        element_count=element_count,
        estimated_height_pct=min(total_height, 100),
        content_density=density,
        visual_weight=avg_weight,
        has_visual_block=has_visual,
        has_text_block=has_text,
        elements=element_names
    )


def _detect_consecutive_lists_without_header(mdx_content: str, slide_id: str) -> List[LayoutIssue]:
    """Detect consecutive SmartList components without a Heading between them.
    
    This is a structural issue where the LLM generates multiple SmartLists
    that should either be merged into one, or each should have its own header.
    
    Args:
        mdx_content: MDX content to analyze
        slide_id: Slide identifier for error reporting
        
    Returns:
        List of LayoutIssue objects for detected violations
    """
    issues = []
    
    # Find all SmartList and Heading positions
    # Pattern matches <SmartList with any attributes and content
    smartlist_pattern = re.compile(r'<SmartList\s+[^>]*?/>', re.DOTALL)
    # Also match SmartList with children (closing tag)
    smartlist_pattern_with_children = re.compile(r'<SmartList\s+[^>]*?>.*?</SmartList>', re.DOTALL)
    # Heading pattern
    heading_pattern = re.compile(r'<Heading\s+[^>]*?>', re.DOTALL)
    
    # Extract component positions with their types
    components = []
    
    # Find self-closing SmartLists
    for match in smartlist_pattern.finditer(mdx_content):
        # Extract id if present
        id_match = re.search(r'id="([^"]*)"', match.group())
        list_id = id_match.group(1) if id_match else f"smartlist_at_{match.start()}"
        components.append({
            'type': 'SmartList',
            'start': match.start(),
            'end': match.end(),
            'id': list_id
        })
    
    # Find SmartLists with children (shouldn't overlap with self-closing)
    for match in smartlist_pattern_with_children.finditer(mdx_content):
        # Check if this overlaps with already found self-closing lists
        overlaps = any(
            c['start'] <= match.start() < c['end'] or c['start'] < match.end() <= c['end']
            for c in components if c['type'] == 'SmartList'
        )
        if not overlaps:
            id_match = re.search(r'id="([^"]*)"', match.group())
            list_id = id_match.group(1) if id_match else f"smartlist_at_{match.start()}"
            components.append({
                'type': 'SmartList',
                'start': match.start(),
                'end': match.end(),
                'id': list_id
            })
    
    # Find Headings
    for match in heading_pattern.finditer(mdx_content):
        components.append({
            'type': 'Heading',
            'start': match.start(),
            'end': match.end(),
            'id': None
        })
    
    # Sort by position
    components.sort(key=lambda x: x['start'])
    
    # Detect consecutive SmartLists without Heading between them
    prev_smartlist = None
    for comp in components:
        if comp['type'] == 'SmartList':
            if prev_smartlist is not None:
                # Found consecutive SmartLists without Heading
                issues.append(LayoutIssue(
                    issue_type=LayoutIssueType.CONSECUTIVE_LISTS_WITHOUT_HEADER,
                    severity="error",
                    slide_id=slide_id,
                    location="content area",
                    description=f"Consecutive SmartList components without a Heading between them. "
                               f"'{prev_smartlist['id']}' is immediately followed by '{comp['id']}'. "
                               f"The second list appears orphaned without context.",
                    suggestion="Either merge these lists into a single SmartList with all items combined, "
                              "or add a Heading before the second SmartList to provide context. "
                              "Each distinct list topic needs its own header.",
                    affected_elements=[prev_smartlist['id'], comp['id']]
                ))
            prev_smartlist = comp
        elif comp['type'] == 'Heading':
            # Reset - Heading breaks the consecutive chain
            prev_smartlist = None
    
    return issues


def _detect_long_metric_values(mdx_content: str, slide_id: str, max_length: int = 10) -> List[LayoutIssue]:
    """Detect Metric components with value text exceeding maximum length.
    
    Metric values should be short (e.g., "42%", "1.2M", "$5.4B"). Long values
    will overflow the metric display. Long text should be moved to the label
    or description prop instead.
    
    Args:
        mdx_content: MDX content to analyze
        slide_id: Slide identifier for error reporting
        max_length: Maximum allowed characters for value prop (default 10)
        
    Returns:
        List of LayoutIssue objects for detected violations
    """
    issues = []
    
    # Pattern to match Metric components and extract value prop
    # Handles both value="..." and value={"..."} formats
    metric_pattern = re.compile(
        r'<Metric\s+[^>]*?value=["\']([^"\']*)["\'][^>]*?>',
        re.DOTALL
    )
    # Also check for value={"..."} JSX format
    metric_pattern_jsx = re.compile(
        r'<Metric\s+[^>]*?value=\{["\']([^"\']*)["\']\}[^>]*?>',
        re.DOTALL
    )
    
    for pattern in [metric_pattern, metric_pattern_jsx]:
        for match in pattern.finditer(mdx_content):
            value = match.group(1)
            if len(value) > max_length:
                # Try to extract id or label for better error message
                id_match = re.search(r'id=["\']([^"\']*)["\']', match.group())
                label_match = re.search(r'label=["\']([^"\']*)["\']', match.group())
                metric_id = id_match.group(1) if id_match else None
                metric_label = label_match.group(1) if label_match else None
                
                identifier = metric_id or metric_label or f"metric_at_{match.start()}"
                
                issues.append(LayoutIssue(
                    issue_type=LayoutIssueType.METRIC_VALUE_TOO_LONG,
                    severity="warning",
                    slide_id=slide_id,
                    location="Metric component",
                    description=f"Metric value '{value}' ({len(value)} chars) exceeds {max_length} character limit. "
                               f"Long values will overflow the metric display.",
                    suggestion=f"Shorten the value to a compact format (e.g., '1.2M', '$5.4B', '42%'). "
                              f"Move descriptive text to the 'label' or 'description' prop instead.",
                    affected_elements=[identifier]
                ))
    
    return issues


def _detect_processstrip_width_issues(mdx_content: str, slide_id: str) -> List[LayoutIssue]:
    """Detect ProcessStrip components with too many items for narrow layouts.
    
    ProcessStrip is horizontal and needs width. Rules:
    - 1:1 split column: max 3 items
    - 1:2 split small side: max 2 items
    - 2:1 split large side: max 4 items
    - Full width (LayoutStacked, Dashboard Main): 5+ items OK
    
    Args:
        mdx_content: MDX content to analyze
        slide_id: Slide identifier for error reporting
        
    Returns:
        List of LayoutIssue objects for detected violations
    """
    issues = []
    
    # Detect layout type and ratio
    layout_match = re.search(r'<(Layout\w+)', mdx_content)
    layout_type = layout_match.group(1) if layout_match else "LayoutStacked"
    
    # Get split ratio if applicable
    ratio_match = re.search(r'ratio=["\'](\d+):(\d+)["\']', mdx_content)
    ratio = (int(ratio_match.group(1)), int(ratio_match.group(2))) if ratio_match else (1, 1)
    
    # Pattern to find ProcessStrip and count items
    processstrip_pattern = re.compile(
        r'<ProcessStrip[^>]*items=\{?\[([^\]]+)\]',
        re.DOTALL
    )
    
    # Determine which slot each ProcessStrip is in
    left_pattern = re.compile(r'<Left>(.*?)</Left>', re.DOTALL)
    right_pattern = re.compile(r'<Right>(.*?)</Right>', re.DOTALL)
    main_pattern = re.compile(r'<Main>(.*?)</Main>', re.DOTALL)
    sidebar_pattern = re.compile(r'<Sidebar>(.*?)</Sidebar>', re.DOTALL)
    
    left_content = left_pattern.search(mdx_content)
    right_content = right_pattern.search(mdx_content)
    main_content = main_pattern.search(mdx_content)
    sidebar_content = sidebar_pattern.search(mdx_content)
    
    def count_items(items_str: str) -> int:
        """Count items in ProcessStrip items array."""
        # Count quoted strings or object literals
        # Simple strings: "item1", "item2" or 'item1', 'item2'
        # Objects: {label: "..."}, {label: "..."}
        string_items = re.findall(r'["\'][^"\']+["\']', items_str)
        obj_items = re.findall(r'\{[^}]+\}', items_str)
        # If objects found, count objects; otherwise count strings
        if obj_items:
            return len(obj_items)
        return len(string_items)
    
    def get_max_items_for_slot(slot: str) -> int:
        """Get max ProcessStrip items based on slot and layout."""
        if layout_type == "LayoutSplit":
            if slot == "left":
                # Left side: check ratio
                if ratio[0] >= ratio[1]:  # 1:1 or larger left
                    return 3 if ratio[0] == ratio[1] else 4
                else:  # smaller left
                    return 2
            elif slot == "right":
                # Right side: check ratio
                if ratio[1] >= ratio[0]:  # 1:1 or larger right
                    return 3 if ratio[0] == ratio[1] else 4
                else:  # smaller right
                    return 2
        elif layout_type == "LayoutDashboard":
            if slot == "main":
                return 4
            elif slot == "sidebar":
                return 2
        # Full width layouts
        return 6
    
    # Check ProcessStrips in each slot
    slots_to_check = []
    if left_content:
        slots_to_check.append(("left", left_content.group(1)))
    if right_content:
        slots_to_check.append(("right", right_content.group(1)))
    if main_content:
        slots_to_check.append(("main", main_content.group(1)))
    if sidebar_content:
        slots_to_check.append(("sidebar", sidebar_content.group(1)))
    
    # If no slots found, check full content (LayoutStacked, etc.)
    if not slots_to_check:
        slots_to_check.append(("main", mdx_content))
    
    for slot_name, slot_content in slots_to_check:
        for match in processstrip_pattern.finditer(slot_content):
            items_str = match.group(1)
            item_count = count_items(items_str)
            max_items = get_max_items_for_slot(slot_name)
            
            if item_count > max_items:
                # Extract id if available
                id_match = re.search(r'id=["\']([^"\']*)["\']', match.group())
                strip_id = id_match.group(1) if id_match else "ProcessStrip"
                
                issues.append(LayoutIssue(
                    issue_type=LayoutIssueType.PROCESSSTRIP_TOO_WIDE,
                    severity="error",
                    slide_id=slide_id,
                    location=f"{slot_name} slot",
                    description=f"ProcessStrip '{strip_id}' has {item_count} items but max {max_items} allowed "
                               f"in {layout_type} {slot_name}. Items will overflow horizontally.",
                    suggestion=f"Use StepList instead (vertical layout fits narrow columns) or move to "
                              f"a wider layout. StepList handles 4+ items well in split columns.",
                    affected_elements=[strip_id]
                ))
    
    return issues


def _detect_dashboard_content_mismatch(mdx_content: str, slide_id: str) -> List[LayoutIssue]:
    """Detect improper content placement in LayoutDashboard.
    
    Dashboard best practices:
    - Main: Should contain the PRIMARY content (MetricGroup, Charts, Tables) that needs width
    - Sidebar: Should contain SUPPORTING content (SmartList, Callout, small visuals)
    
    Anti-patterns:
    - Main has only NetworkGraph (horizontal diagrams waste space, leave gaps)
    - Sidebar has MetricGroup (not enough width for metrics)
    
    Args:
        mdx_content: MDX content to analyze
        slide_id: Slide identifier for error reporting
        
    Returns:
        List of LayoutIssue objects for detected violations
    """
    issues = []
    
    # Check if this is a LayoutDashboard
    if '<LayoutDashboard' not in mdx_content:
        return issues
    
    # Extract Main and Sidebar content
    main_pattern = re.compile(r'<Main>(.*?)</Main>', re.DOTALL)
    sidebar_pattern = re.compile(r'<Sidebar>(.*?)</Sidebar>', re.DOTALL)
    
    main_match = main_pattern.search(mdx_content)
    sidebar_match = sidebar_pattern.search(mdx_content)
    
    if not main_match or not sidebar_match:
        return issues
    
    main_content = main_match.group(1)
    sidebar_content = sidebar_match.group(1)
    
    # Check for MetricGroup in sidebar (should be in main)
    has_metric_in_sidebar = '<MetricGroup' in sidebar_content
    has_metric_in_main = '<MetricGroup' in main_content
    
    # Check for diagram in main
    has_diagram_in_main = '<NetworkGraph' in main_content or '<SmartDiagram' in main_content
    
    # Check for charts in main/sidebar
    has_chart_in_main = '<Chart' in main_content or '<ChartBar' in main_content or '<ChartLine' in main_content
    has_chart_in_sidebar = '<Chart' in sidebar_content or '<ChartBar' in sidebar_content or '<ChartLine' in sidebar_content
    
    # Anti-pattern 1: MetricGroup in sidebar without metrics in main
    # (MetricGroup needs width, should be in main)
    if has_metric_in_sidebar and not has_metric_in_main and not has_chart_in_main:
        issues.append(LayoutIssue(
            issue_type=LayoutIssueType.DASHBOARD_CONTENT_MISMATCH,
            severity="warning",
            slide_id=slide_id,
            location="Sidebar slot",
            description="MetricGroup in Sidebar may not have enough width for proper display. "
                       "Sidebar is designed for supporting content like lists and callouts.",
            suggestion="Move MetricGroup to Main slot for better visual display. "
                      "Use Sidebar for SmartList, Callout, or compact supporting content.",
            affected_elements=["MetricGroup", "Sidebar"]
        ))
    
    # Anti-pattern 2: Only diagram in main (diagrams often leave empty space)
    if has_diagram_in_main and not has_metric_in_main and not has_chart_in_main:
        # Check if main has substantial other content
        has_substantial_main = (
            main_content.count('<') > 3 or  # Multiple components
            '<BigNum' in main_content or
            '<TableData' in main_content
        )
        if not has_substantial_main:
            issues.append(LayoutIssue(
                issue_type=LayoutIssueType.DASHBOARD_CONTENT_MISMATCH,
                severity="info",
                slide_id=slide_id,
                location="Main slot",
                description="Main slot has only NetworkGraph which may leave empty space. "
                           "Horizontal diagrams don't fill the wide main area well.",
                suggestion="Add MetricGroup, ChartBar, or BigNum to Main for better density. "
                          "Consider moving diagram to a LayoutSplit instead if it's the primary visual.",
                affected_elements=["NetworkGraph", "Main"]
            ))
    
    # Anti-pattern 3: Chart in sidebar (charts need width)
    if has_chart_in_sidebar and not has_chart_in_main:
        issues.append(LayoutIssue(
            issue_type=LayoutIssueType.DASHBOARD_CONTENT_MISMATCH,
            severity="warning",
            slide_id=slide_id,
            location="Sidebar slot",
            description="Chart in Sidebar may be too compressed. "
                       "Charts need width for proper data visualization.",
            suggestion="Move Chart to Main slot. Use Sidebar for SmartList or text content.",
            affected_elements=["Chart", "Sidebar"]
        ))
    
    return issues


def _detect_slot_boundaries(mdx_content: str) -> Dict[str, str]:
    """Detect layout slot boundaries in MDX content.
    
    Args:
        mdx_content: Raw MDX string
        
    Returns:
        Dict mapping slot names to their content
    """
    slots = {}
    
    # Pattern for slot containers: <Left>...</Left>, <Right>...</Right>, etc.
    slot_patterns = [
        (r'<Left>(.*?)</Left>', 'left'),
        (r'<Right>(.*?)</Right>', 'right'),
        (r'<Main>(.*?)</Main>', 'main'),
        (r'<Sidebar>(.*?)</Sidebar>', 'sidebar'),
        (r'<Header>(.*?)</Header>', 'header'),
        (r'<Footer>(.*?)</Footer>', 'footer'),
    ]
    
    for pattern, slot_name in slot_patterns:
        match = re.search(pattern, mdx_content, re.DOTALL)
        if match:
            slots[slot_name] = match.group(1)
    
    # If no slots found, treat entire content as "main"
    if not slots:
        slots["main"] = mdx_content
    
    return slots


# Components forbidden on cover pages (keep cover clean and minimal)
FORBIDDEN_ON_COVER = {
    "BigNum", "MetricGroup", "Metric", "ChartBar", "ChartLine", "ChartPie",
    "NetworkGraph", "SmartDiagram", "Diagram", "CardGroup", "Card",
    "ProcessStrip", "StepList", "TableData", "SmartList"
}


def analyze_slide_whitespace(
    slide_mdx: str, 
    slide_id: str = "unknown",
    is_cover_or_closing: bool = False
) -> List[LayoutIssue]:
    """Analyze a single slide for whitespace and balance issues.
    
    Args:
        slide_mdx: MDX content for one slide
        slide_id: Identifier for the slide
        is_cover_or_closing: If True, skip density checks (cover/closing should be minimal)
        
    Returns:
        List of detected LayoutIssue objects
    """
    issues = []
    
    # Detect layout type
    layout_match = re.search(r'<(Layout\w+)', slide_mdx)
    layout_type = layout_match.group(1) if layout_match else "LayoutStacked"
    
    # === SPECIAL CHECK: Cover page should be minimal ===
    if layout_type == "LayoutCover":
        # Check for forbidden components on cover
        for component in FORBIDDEN_ON_COVER:
            if f'<{component}' in slide_mdx:
                issues.append(LayoutIssue(
                    issue_type=LayoutIssueType.CONTENT_OVERFLOW,
                    severity="error",
                    slide_id=slide_id,
                    location="cover page",
                    description=f"Cover page has {component} which makes it look cluttered. "
                               f"Cover pages should be clean: just title + subtitle.",
                    suggestion=f"Remove {component} from cover page. Use LayoutSplit or LayoutDashboard "
                              f"for data-heavy content. Cover should only have Heading + Text + optional QuoteBlock.",
                    affected_elements=[component]
                ))
        # Skip other density checks for cover pages
        return issues
    
    # Skip most checks for closing slides (they should be minimal like cover)
    if is_cover_or_closing:
        return issues
    
    # Get slot boundaries
    slots = _detect_slot_boundaries(slide_mdx)
    
    # Analyze each slot
    slot_analyses = {}
    for slot_name, slot_content in slots.items():
        components = _extract_components_from_mdx(slot_content)
        slot_analyses[slot_name] = _analyze_slot_content(slot_name, components)
    
    # === CHECK 1: Empty slots (trapped whitespace) ===
    for slot_name, analysis in slot_analyses.items():
        if analysis.content_density == "empty":
            issues.append(LayoutIssue(
                issue_type=LayoutIssueType.EMPTY_SLOT,
                severity="error",
                slide_id=slide_id,
                location=f"{slot_name} slot",
                description=f"The {slot_name} slot is completely empty, creating trapped whitespace.",
                suggestion=f"Add content to {slot_name} or switch to a layout that doesn't require this slot.",
                affected_elements=[]
            ))
    
    # === CHECK 2: Sparse content (underutilized space) ===
    for slot_name, analysis in slot_analyses.items():
        if analysis.content_density == "sparse" and analysis.element_count > 0:
            issues.append(LayoutIssue(
                issue_type=LayoutIssueType.SPARSE_CONTENT,
                severity="warning",
                slide_id=slide_id,
                location=f"{slot_name} slot",
                description=f"The {slot_name} slot has sparse content ({analysis.estimated_height_pct:.0f}% filled). "
                           f"Elements: {', '.join(analysis.elements)}",
                suggestion="Add more content blocks (CardGroup, Callout, additional Text) or use a more compact layout.",
                affected_elements=analysis.elements
            ))
    
    # === CHECK 3: Underfilled split layout ===
    # Split layouts need BOTH sides to have substantial content for visual balance
    # Without this, the layout looks like a partially-filled 2x3 grid (under-construction)
    if "left" in slot_analyses and "right" in slot_analyses:
        left = slot_analyses["left"]
        right = slot_analyses["right"]
        
        min_threshold = MIN_CONTENT_THRESHOLDS.get(layout_type, MIN_CONTENT_THRESHOLDS["default"])
        min_elements = MIN_ELEMENTS_SPLIT_SIDE
        
        # Check 3a: Insufficient elements per side (looks like sparse 2x3 grid)
        left_elements_ok = left.element_count >= min_elements
        right_elements_ok = right.element_count >= min_elements
        
        if not left_elements_ok or not right_elements_ok:
            sparse_side = "left" if left.element_count < right.element_count else "right"
            sparse_count = min(left.element_count, right.element_count)
            issues.append(LayoutIssue(
                issue_type=LayoutIssueType.SPARSE_CONTENT,
                severity="error",  # Critical - makes slide look unfinished
                slide_id=slide_id,
                location=f"{sparse_side} column",
                description=f"Split layout has too few elements ({sparse_side}: {sparse_count} elements, need {min_elements}+). "
                           f"Page looks like an unfinished 2x3 grid. "
                           f"Left: {left.element_count} elements, Right: {right.element_count} elements.",
                suggestion=f"Add more blocks to {sparse_side}: Heading + visual (BigNum/Diagram/Chart) + text (SmartList/Text) + Callout. "
                          f"Each side needs {min_elements}+ elements. If content is limited, use LayoutStacked instead.",
                affected_elements=left.elements + right.elements
            ))
        
        # Check 3b: Both sides underfilled by height percentage
        both_underfilled = (
            left.estimated_height_pct < min_threshold and 
            right.estimated_height_pct < min_threshold
        )
        
        if both_underfilled and not (not left_elements_ok or not right_elements_ok):
            # Only report if we didn't already report element count issue
            issues.append(LayoutIssue(
                issue_type=LayoutIssueType.SPARSE_CONTENT,
                severity="error",
                slide_id=slide_id,
                location="split layout",
                description=f"Split layout is underfilled (looks under-construction). "
                           f"Left: {left.estimated_height_pct:.0f}%, Right: {right.estimated_height_pct:.0f}% "
                           f"(both need >{min_threshold}% for visual balance).",
                suggestion="Add more content to BOTH sides: BigNum, MetricGroup, Diagram, CardGroup, or additional text blocks. "
                          "Consider switching to LayoutStacked if content is limited.",
                affected_elements=left.elements + right.elements
            ))
        
        # Check 3c: Height imbalance (no vertical overlap)
        # When one side is much shorter than the other, it creates visual disconnect
        height_diff = abs(left.estimated_height_pct - right.estimated_height_pct)
        if height_diff > 35:  # Tightened from 40 to 35
            lighter_side = "left" if left.estimated_height_pct < right.estimated_height_pct else "right"
            heavier_side = "right" if lighter_side == "left" else "left"
            issues.append(LayoutIssue(
                issue_type=LayoutIssueType.UNBALANCED_COLUMNS,
                severity="error" if height_diff > 50 else "warning",  # Error if very unbalanced
                slide_id=slide_id,
                location="split layout",
                description=f"Columns lack vertical overlap (no visual connection). "
                           f"Left: {left.estimated_height_pct:.0f}%, Right: {right.estimated_height_pct:.0f}% "
                           f"(diff: {height_diff:.0f}%, should be <35%).",
                suggestion=f"Add content to {lighter_side} so both columns span similar vertical range. "
                          f"Try adding Callout, CardGroup, or additional SmartList to {lighter_side}.",
                affected_elements=left.elements + right.elements
            ))
    
    # === CHECK 4: Missing visual blocks ===
    total_elements = sum(a.element_count for a in slot_analyses.values())
    has_any_visual = any(a.has_visual_block for a in slot_analyses.values())
    
    if total_elements >= 2 and not has_any_visual and layout_type != "LayoutCover":
        issues.append(LayoutIssue(
            issue_type=LayoutIssueType.MISSING_VISUAL_BLOCK,
            severity="info",
            slide_id=slide_id,
            location="entire slide",
            description="Slide has no visual blocks (BigNum, Chart, Diagram, CardGroup). "
                       "Text-only slides can feel monotonous.",
            suggestion="Consider adding a BigNum, MetricGroup, Diagram, or CardGroup to increase visual interest.",
            affected_elements=[]
        ))
    
    # === CHECK 5: Lonely element (single item in a slot) ===
    for slot_name, analysis in slot_analyses.items():
        if analysis.element_count == 1 and analysis.estimated_height_pct < 25:
            issues.append(LayoutIssue(
                issue_type=LayoutIssueType.LONELY_ELEMENT,
                severity="info",
                slide_id=slide_id,
                location=f"{slot_name} slot",
                description=f"Single small element ({analysis.elements[0]}) in {slot_name} creates visual imbalance.",
                suggestion="Add supporting content or move element to a different slot.",
                affected_elements=analysis.elements
            ))
    
    # === CHECK 6: Content overflow (too much content causing scrollbar) ===
    overflow_threshold = OVERFLOW_THRESHOLDS.get(layout_type, OVERFLOW_THRESHOLDS["default"])
    max_elements = MAX_ELEMENTS_PER_LAYOUT.get(layout_type, MAX_ELEMENTS_PER_LAYOUT["default"])
    
    # Check total slide content
    total_height = sum(a.estimated_height_pct for a in slot_analyses.values())
    total_elements = sum(a.element_count for a in slot_analyses.values())
    
    # Count heavy components
    heavy_count = 0
    heavy_names = []
    for analysis in slot_analyses.values():
        for elem in analysis.elements:
            if elem in HEAVY_COMPONENTS:
                heavy_count += 1
                heavy_names.append(elem)
    
    # Overflow detection: total height exceeds threshold OR too many elements OR multiple heavy components
    is_overflow = (
        total_height > overflow_threshold or 
        total_elements > max_elements + 2 or  # Some buffer
        (heavy_count >= 2 and total_height > overflow_threshold - 10)
    )
    
    if is_overflow:
        issues.append(LayoutIssue(
            issue_type=LayoutIssueType.CONTENT_OVERFLOW,
            severity="error",
            slide_id=slide_id,
            location="entire slide",
            description=f"Content likely overflows visible area. "
                       f"Estimated height: {total_height:.0f}% (threshold: {overflow_threshold}%), "
                       f"Elements: {total_elements} (max recommended: {max_elements}), "
                       f"Heavy components: {heavy_count}",
            suggestion="Remove some content blocks, use a simpler layout, or split into multiple slides. "
                      f"Consider removing: {', '.join(heavy_names[:2]) if heavy_names else 'some text blocks'}.",
            affected_elements=[e for a in slot_analyses.values() for e in a.elements]
        ))
    
    # === CHECK 7: Content cutoff (specific slots overflow) ===
    for slot_name, analysis in slot_analyses.items():
        slot_overflow_threshold = 100 if slot_name == "main" else 80
        
        if analysis.estimated_height_pct > slot_overflow_threshold:
            issues.append(LayoutIssue(
                issue_type=LayoutIssueType.CONTENT_CUTOFF,
                severity="error",
                slide_id=slide_id,
                location=f"{slot_name} slot",
                description=f"Content in {slot_name} likely gets cut off. "
                           f"Estimated height: {analysis.estimated_height_pct:.0f}% (max: {slot_overflow_threshold}%). "
                           f"Elements: {', '.join(analysis.elements)}",
                suggestion=f"Reduce content in {slot_name}: remove 1-2 elements or shorten text. "
                          f"Consider moving some content to other slots or another slide.",
                affected_elements=analysis.elements
            ))
    
    # === CHECK 8: Insufficient page coverage (70% minimum for dense pages) ===
    # This catches pages with overall sparse content even if individual slots aren't flagged
    min_total_elements = MIN_TOTAL_ELEMENTS.get(layout_type, MIN_TOTAL_ELEMENTS["default"])
    
    # Calculate effective page coverage (exclude cover layouts which can be minimal)
    if layout_type not in ("LayoutCover", "LayoutFullBleed"):
        # Check total height coverage
        if total_height < MIN_PAGE_COVERAGE:
            issues.append(LayoutIssue(
                issue_type=LayoutIssueType.INSUFFICIENT_PAGE_COVERAGE,
                severity="error",
                slide_id=slide_id,
                location="entire page",
                description=f"Page has insufficient content coverage: {total_height:.0f}% (minimum: {MIN_PAGE_COVERAGE}%). "
                           f"Total elements: {total_elements}. The page looks sparse and incomplete.",
                suggestion=f"Add more content to reach {MIN_PAGE_COVERAGE}% coverage. "
                          f"Add BigNum, MetricGroup, CardGroup, additional SmartList, or Callout blocks. "
                          f"Every dense page should feel substantial, not like a work-in-progress.",
                affected_elements=[e for a in slot_analyses.values() for e in a.elements]
            ))
        
        # Check minimum element count
        if total_elements < min_total_elements:
            issues.append(LayoutIssue(
                issue_type=LayoutIssueType.INSUFFICIENT_PAGE_COVERAGE,
                severity="error",
                slide_id=slide_id,
                location="entire page",
                description=f"Page has too few elements: {total_elements} (minimum: {min_total_elements}). "
                           f"This creates visible gaps/holes in the layout.",
                suggestion=f"Add at least {min_total_elements - total_elements} more elements. "
                          f"Include: Heading + visual block (BigNum/Chart/Diagram) + text content + supporting element.",
                affected_elements=[e for a in slot_analyses.values() for e in a.elements]
            ))
    
    # === CHECK 9: Content gaps (holes between content blocks) ===
    # Detect when slots have very uneven content distribution
    if len(slot_analyses) >= 2:
        heights = [a.estimated_height_pct for a in slot_analyses.values()]
        max_height = max(heights) if heights else 0
        min_height = min(heights) if heights else 0
        
        # If one slot is much fuller than others, there are visible gaps
        if max_height > 50 and min_height < 25 and (max_height - min_height) > 40:
            sparse_slots = [name for name, a in slot_analyses.items() if a.estimated_height_pct < 25]
            full_slots = [name for name, a in slot_analyses.items() if a.estimated_height_pct > 50]
            
            if sparse_slots:
                issues.append(LayoutIssue(
                    issue_type=LayoutIssueType.CONTENT_GAPS,
                    severity="warning",
                    slide_id=slide_id,
                    location=f"{', '.join(sparse_slots)} slot(s)",
                    description=f"Content is unevenly distributed creating visible gaps. "
                               f"Sparse slots ({', '.join(sparse_slots)}): <25% filled. "
                               f"Full slots ({', '.join(full_slots)}): >50% filled.",
                    suggestion=f"Balance content across slots. Move some elements from {', '.join(full_slots)} "
                              f"to {', '.join(sparse_slots)}, or add new content to sparse slots.",
                    affected_elements=[e for a in slot_analyses.values() for e in a.elements]
                ))
    
    # === CHECK 10: Consecutive SmartLists without header ===
    # Detect SmartList components that appear consecutively without a Heading between them
    consecutive_list_issues = _detect_consecutive_lists_without_header(slide_mdx, slide_id)
    issues.extend(consecutive_list_issues)
    
    # === CHECK 11: Metric value length ===
    # Detect Metric components with values that are too long and will overflow
    metric_value_issues = _detect_long_metric_values(slide_mdx, slide_id)
    issues.extend(metric_value_issues)
    
    # === CHECK 12: Dashboard content placement ===
    # Detect improper content in LayoutDashboard main/sidebar slots
    dashboard_issues = _detect_dashboard_content_mismatch(slide_mdx, slide_id)
    issues.extend(dashboard_issues)
    
    # === CHECK 13: ProcessStrip width in narrow columns ===
    # Detect ProcessStrip with too many items for narrow layouts (splits, sidebars)
    processstrip_issues = _detect_processstrip_width_issues(slide_mdx, slide_id)
    issues.extend(processstrip_issues)
    
    return issues


def analyze_presentation_whitespace(slides_mdx: List[str], slide_ids: List[str] = None) -> Dict[str, Any]:
    """Analyze entire presentation for whitespace and balance issues.
    
    Args:
        slides_mdx: List of MDX content strings, one per slide
        slide_ids: Optional list of slide identifiers
        
    Returns:
        Dict with issues, summary, and recommendations
    """
    if slide_ids is None:
        slide_ids = [f"slide_{i+1:02d}" for i in range(len(slides_mdx))]
    
    all_issues = []
    slide_summaries = []
    total_slides = len(slides_mdx)
    
    for idx, (mdx, slide_id) in enumerate(zip(slides_mdx, slide_ids)):
        # Determine if this is a cover or closing slide (should be minimal)
        is_first_slide = (idx == 0)
        is_last_slide = (idx == total_slides - 1)
        layout_match = re.search(r'<(Layout\w+)', mdx)
        layout_type = layout_match.group(1) if layout_match else "LayoutStacked"
        
        # Cover/closing detection: first slide, last slide, or explicit LayoutCover
        is_cover_or_closing = (
            is_first_slide or 
            is_last_slide or 
            layout_type == "LayoutCover"
        )
        
        issues = analyze_slide_whitespace(mdx, slide_id, is_cover_or_closing)
        all_issues.extend(issues)
        
        # Summarize slide health
        error_count = sum(1 for i in issues if i.severity == "error")
        warning_count = sum(1 for i in issues if i.severity == "warning")
        
        slide_summaries.append({
            "slide_id": slide_id,
            "errors": error_count,
            "warnings": warning_count,
            "status": "error" if error_count > 0 else ("warning" if warning_count > 0 else "ok")
        })
    
    # Calculate summary stats
    total_errors = sum(1 for i in all_issues if i.severity == "error")
    total_warnings = sum(1 for i in all_issues if i.severity == "warning")
    total_info = sum(1 for i in all_issues if i.severity == "info")
    
    # Count issue types
    issue_type_counts = {}
    for issue in all_issues:
        key = issue.issue_type.value
        issue_type_counts[key] = issue_type_counts.get(key, 0) + 1
    
    return {
        "issues": all_issues,
        "slide_summaries": slide_summaries,
        "summary": {
            "total_slides": len(slides_mdx),
            "slides_with_errors": sum(1 for s in slide_summaries if s["status"] == "error"),
            "slides_with_warnings": sum(1 for s in slide_summaries if s["status"] == "warning"),
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "total_info": total_info,
            "issue_type_counts": issue_type_counts,
        },
        "overall_status": "error" if total_errors > 0 else ("warning" if total_warnings > 0 else "ok")
    }


def format_whitespace_report(analysis_result: Dict[str, Any]) -> str:
    """Format whitespace analysis results as a readable report.
    
    Args:
        analysis_result: Output from analyze_presentation_whitespace
        
    Returns:
        Formatted string report
    """
    lines = []
    lines.append("=" * 60)
    lines.append("LAYOUT WHITESPACE ANALYSIS REPORT")
    lines.append("=" * 60)
    
    summary = analysis_result["summary"]
    lines.append(f"\n[Summary]:")
    lines.append(f"   Total slides: {summary['total_slides']}")
    lines.append(f"   Slides with errors: {summary['slides_with_errors']}")
    lines.append(f"   Slides with warnings: {summary['slides_with_warnings']}")
    lines.append(f"   Total issues: {summary['total_errors']} errors, {summary['total_warnings']} warnings, {summary['total_info']} info")
    
    if summary["issue_type_counts"]:
        lines.append(f"\n[Issue breakdown]:")
        for issue_type, count in sorted(summary["issue_type_counts"].items()):
            lines.append(f"   - {issue_type}: {count}")
    
    # Group issues by slide
    issues_by_slide = {}
    for issue in analysis_result["issues"]:
        if issue.slide_id not in issues_by_slide:
            issues_by_slide[issue.slide_id] = []
        issues_by_slide[issue.slide_id].append(issue)
    
    if issues_by_slide:
        lines.append(f"\n[Detailed Issues]:")
        for slide_id, issues in issues_by_slide.items():
            lines.append(f"\n  [{slide_id}]")
            for issue in issues:
                icon = "[ERR]" if issue.severity == "error" else ("[WARN]" if issue.severity == "warning" else "[INFO]")
                lines.append(f"    {icon} {issue.issue_type.value.upper()}: {issue.description}")
                lines.append(f"       -> {issue.suggestion}")
    
    lines.append("\n" + "=" * 60)
    
    status = analysis_result["overall_status"]
    if status == "ok":
        lines.append("[OK] All slides pass whitespace checks!")
    elif status == "warning":
        lines.append("[WARN] Some slides have minor balance issues.")
    else:
        lines.append("[ERR] Some slides have significant whitespace problems.")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)


def validate_mdx_file(mdx_path: str, verbose: bool = True) -> Dict[str, Any]:
    """Validate an MDX file for whitespace issues.
    
    Args:
        mdx_path: Path to MDX file
        verbose: If True, print report to stdout
        
    Returns:
        Analysis result dict
    """
    from pathlib import Path
    
    mdx_content = Path(mdx_path).read_text(encoding='utf-8')
    
    # Split into individual slides
    # MDX slides are separated by {/* Slide N */} comments
    slide_pattern = r'\{/\*\s*Slide\s*\d+\s*\*/\}'
    slides = re.split(slide_pattern, mdx_content)
    
    # Filter out empty/metadata-only slides
    slides = [s.strip() for s in slides if s.strip() and '<Layout' in s]
    
    # Generate slide IDs (zero-padded to match state format)
    slide_ids = [f"slide_{i+1:02d}" for i in range(len(slides))]

    # Run analysis
    result = analyze_presentation_whitespace(slides, slide_ids)

    if verbose:
        print(format_whitespace_report(result))

    return result


def run_post_export_validation(output_dir: str, verbose: bool = True) -> Dict[str, Any]:
    """Run whitespace validation after MDX export.
    
    Args:
        output_dir: Directory containing exported slides.mdx
        verbose: If True, print report
        
    Returns:
        Analysis result dict
    """
    from pathlib import Path
    
    mdx_path = Path(output_dir) / "slides.mdx"
    
    if not mdx_path.exists():
        if verbose:
            print(f"[WARN] No slides.mdx found at {mdx_path}")
        return {"error": "No slides.mdx found", "issues": [], "summary": {}}
    
    return validate_mdx_file(str(mdx_path), verbose=verbose)


def validate_mdx_content(mdx_content: str, verbose: bool = True) -> Dict[str, Any]:
    """Validate MDX content string for whitespace issues.
    
    Args:
        mdx_content: MDX content as string
        verbose: If True, print report to stdout
        
    Returns:
        Analysis result dict
    """
    # Split into individual slides
    # MDX slides are separated by {/* Slide N */} comments or --- separators
    slide_pattern = r'\{/\*\s*Slide\s*\d+\s*\*/\}'
    slides = re.split(slide_pattern, mdx_content)
    
    # Filter out empty/metadata-only slides
    slides = [s.strip() for s in slides if s.strip() and '<Layout' in s]
    
    # Generate slide IDs (zero-padded to match state format)
    slide_ids = [f"slide_{i+1:02d}" for i in range(len(slides))]
    
    # Run analysis
    result = analyze_presentation_whitespace(slides, slide_ids)
    
    if verbose:
        print(format_whitespace_report(result))
    
    return result


def format_issues_for_llm_refinement(analysis_result: Dict[str, Any]) -> str:
    """Format validation issues as LLM-friendly feedback for refinement.
    
    Args:
        analysis_result: Output from analyze_presentation_whitespace or validate_mdx_content
        
    Returns:
        Formatted string suitable for LLM refinement prompt
    """
    issues = analysis_result.get("issues", [])
    if not issues:
        return ""
    
    # Only include errors and warnings, not info
    actionable_issues = [i for i in issues if i.severity in ("error", "warning")]
    if not actionable_issues:
        return ""
    
    lines = ["## LAYOUT ISSUES TO FIX:\n"]
    
    # Group by slide
    by_slide = {}
    for issue in actionable_issues:
        if issue.slide_id not in by_slide:
            by_slide[issue.slide_id] = []
        by_slide[issue.slide_id].append(issue)
    
    for slide_id, slide_issues in by_slide.items():
        lines.append(f"### {slide_id}:")
        for issue in slide_issues:
            severity = "ERROR" if issue.severity == "error" else "WARNING"
            lines.append(f"- [{severity}] {issue.issue_type.value}: {issue.description}")
            lines.append(f"  FIX: {issue.suggestion}")
        lines.append("")
    
    return "\n".join(lines)


def has_critical_issues(analysis_result: Dict[str, Any]) -> bool:
    """Check if analysis result has critical issues requiring refinement.
    
    Args:
        analysis_result: Output from validate_mdx_content
        
    Returns:
        True if there are errors that should trigger refinement
    """
    summary = analysis_result.get("summary", {})
    return summary.get("total_errors", 0) > 0
