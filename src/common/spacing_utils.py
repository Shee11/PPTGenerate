"""Spacing utilities for parsing CSS units to pixels."""
import re
from typing import Union


def parse_spacing(value: Union[str, int, float], reference: float = 0, base_font_size: float = 16) -> float:
    """Parse spacing value from CSS string to pixels.
    
    Supports:
    - Pixels: "40px", "100px"
    - Percentages: "15%", "50%" (relative to reference)
    - Rems: "2rem", "1.5rem" (relative to base font size)
    - Numbers: 40, 100 (interpreted as pixels)
    
    Args:
        value: CSS value string or numeric value
        reference: Reference value for percentage calculations
        base_font_size: Base font size for rem calculations (default: 16px)
        
    Returns:
        Spacing value in pixels
        
    Raises:
        ValueError: If value format is invalid
        
    Examples:
        >>> parse_spacing("40px")
        40.0
        >>> parse_spacing("15%", reference=1000)
        150.0
        >>> parse_spacing("2rem", base_font_size=16)
        32.0
        >>> parse_spacing(40)
        40.0
    """
    # Handle None or empty strings
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return 0.0
    
    # Handle numeric values directly
    if isinstance(value, (int, float)):
        return float(value)
    
    # Handle string values
    value_str = str(value).strip().lower()
    
    # Match CSS unit patterns (support negative values)
    px_match = re.match(r'^(-?[\d.]+)px$', value_str)
    pct_match = re.match(r'^(-?[\d.]+)%$', value_str)
    rem_match = re.match(r'^(-?[\d.]+)rem$', value_str)
    em_match = re.match(r'^(-?[\d.]+)em$', value_str)
    plain_match = re.match(r'^(-?[\d.]+)$', value_str)
    
    if px_match:
        return float(px_match.group(1))
    elif pct_match:
        return float(pct_match.group(1)) / 100 * reference
    elif rem_match:
        return float(rem_match.group(1)) * base_font_size
    elif em_match:
        # For em, use base font size (in real implementation, would use parent font size)
        return float(em_match.group(1)) * base_font_size
    elif plain_match:
        # Plain number interpreted as pixels
        return float(plain_match.group(1))
    else:
        raise ValueError(f"Invalid spacing value: '{value}'. Expected format: '40px', '15%', '2rem', or numeric value")


def parse_margin(margin_value: Union[str, int, float], reference_width: float = 0, reference_height: float = 0) -> float:
    """Parse margin value to pixels.
    
    For horizontal margins, use reference_width.
    For vertical margins, use reference_height.
    
    Args:
        margin_value: CSS margin value
        reference_width: Canvas width for percentage calculations
        reference_height: Canvas height for percentage calculations
        
    Returns:
        Margin in pixels
    """
    # For margins, typically use width as reference (CSS box model convention)
    # but caller can specify which reference to use
    return parse_spacing(margin_value, reference=reference_width if reference_width else reference_height)


def parse_gutter(gutter_value: Union[str, int, float], content_width: float = 0) -> float:
    """Parse gutter spacing value to pixels.
    
    Args:
        gutter_value: CSS gutter value
        content_width: Content area width for percentage calculations
        
    Returns:
        Gutter spacing in pixels
    """
    return parse_spacing(gutter_value, reference=content_width)
