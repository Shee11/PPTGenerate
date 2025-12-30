"""Post-generation validator to check and fix layout-widget compatibility issues."""
import json
from typing import Dict, List, Tuple
from pathlib import Path

from src.paged.layout.slidev.layout_validator import (
    validate_slide_layout,
    suggest_better_layout,
    WIDGET_SPACE_REQUIREMENTS
)

# Layout alternatives for consecutive layout fix
LAYOUT_ALTERNATIVES = {
    "hero-split": ["comparison", "smart-grid", "dashboard", "spotlight"],
    "smart-grid": ["hero-split", "comparison", "dashboard", "timeline"],
    "dashboard": ["hero-split", "smart-grid", "comparison", "timeline"],
    "comparison": ["hero-split", "smart-grid", "dashboard", "timeline"],
    "timeline": ["hero-split", "smart-grid", "comparison", "dashboard"],
    "spotlight": ["hero-split", "smart-grid", "comparison", "center"],
    "center": ["hero-split", "spotlight", "smart-grid", "comparison"],
    "stats-showcase": ["hero-split", "smart-grid", "comparison", "dashboard"],
}


def fix_consecutive_layouts(slides: List[dict], verbose: bool = False) -> Tuple[List[dict], List[str]]:
    """Fix consecutive same-layout issues by rotating layouts.
    
    Args:
        slides: List of slide dicts with 'layout' field or 'mdx' field
        verbose: If True, include detailed report
        
    Returns:
        Tuple of (fixed_slides, report_lines)
    """
    report = []
    report.append("=" * 80)
    report.append("CONSECUTIVE LAYOUT FIX REPORT")
    report.append("=" * 80)
    
    # Skip validation for MDX slides (they don't have 'layout' field)
    # MDX slides store layout in the MDX content itself
    has_mdx_slides = any(s.get('mdx') for s in slides)
    if has_mdx_slides:
        report.append("  ℹ Skipping consecutive layout fix for MDX slides")
        report.append("=" * 80)
        return slides, report
    
    fixes_applied = 0
    
    for i in range(1, len(slides)):
        current_layout = slides[i].get('layout', 'unknown')
        prev_layout = slides[i-1].get('layout', 'unknown')
        
        # Handle case where layout is a dict instead of string (LLM error)
        if isinstance(current_layout, dict):
            current_layout = current_layout.get('name', current_layout.get('type', 'unknown'))
            slides[i]['layout'] = current_layout
        if isinstance(prev_layout, dict):
            prev_layout = prev_layout.get('name', prev_layout.get('type', 'unknown'))
            slides[i-1]['layout'] = prev_layout
        
        if current_layout == prev_layout:
            # Need to change this slide's layout
            slide_id = slides[i].get('id', f'slide_{i+1}')
            alternatives = LAYOUT_ALTERNATIVES.get(current_layout, ["smart-grid", "comparison", "hero-split"])
            
            # Pick first alternative not matching previous or next
            next_layout = slides[i+1].get('layout') if i+1 < len(slides) else None
            
            new_layout = None
            for alt in alternatives:
                if alt != prev_layout and alt != next_layout:
                    new_layout = alt
                    break
            
            if new_layout is None:
                new_layout = alternatives[0]  # Fallback
            
            old_layout = slides[i]['layout']
            slides[i]['layout'] = new_layout
            fixes_applied += 1
            
            report.append(f"  ✅ Slide {i+1} ({slide_id}): {old_layout} → {new_layout} (was same as slide {i})")
    
    report.append("")
    report.append(f"Total consecutive layout fixes: {fixes_applied}")
    report.append("=" * 80)
    
    return slides, report


def validate_slides_json(slides_path: str, fix: bool = False) -> Tuple[List[dict], List[str]]:
    """Validate slides JSON for layout-widget compatibility.
    
    Args:
        slides_path: Path to debug_content.json or slides JSON file
        fix: If True, attempt to fix issues by changing layouts
        
    Returns:
        Tuple of (validated_slides, report_lines)
    """
    # Load slides
    with open(slides_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    slides = data.get('contexts', []) if 'contexts' in data else data
    
    report = []
    report.append("=" * 80)
    report.append("LAYOUT-WIDGET COMPATIBILITY VALIDATION REPORT")
    report.append("=" * 80)
    
    issues_found = 0
    fixes_applied = 0
    
    for i, slide in enumerate(slides, 1):
        slide_id = slide.get('id', f'slide_{i}')
        layout = slide.get('layout', 'unknown')
        widgets = slide.get('widgets', {})
        
        # Validate slide
        is_valid, warnings, suggestions = validate_slide_layout(slide)
        
        if not is_valid:
            issues_found += 1
            report.append(f"\n❌ Slide {i} ({slide_id}): {layout} layout")
            report.append("-" * 60)
            
            # Show widget types
            widget_summary = []
            for slot, widget_data in widgets.items():
                wtype = widget_data.get('type', 'unknown')
                text_len = len(widget_data.get('text', ''))
                widget_summary.append(f"  • {slot}: {wtype} ({text_len} chars)")
            
            report.append("  Widgets:")
            report.extend(widget_summary)
            
            # Show warnings
            report.append("\n  Issues:")
            for warning in warnings:
                report.append(f"  {warning}")
            
            # Show suggestions
            if suggestions:
                report.append(f"\n  💡 Suggested layouts: {', '.join(suggestions)}")
                
                # Apply fix if requested
                if fix and suggestions:
                    old_layout = layout
                    new_layout = suggestions[0]
                    slide['layout'] = new_layout
                    
                    # Update slot names if needed
                    # (This is simplified - full implementation would remap slots)
                    if new_layout == 'full-bleed':
                        # Combine all widgets into single default slot
                        combined_text = []
                        for widget_data in widgets.values():
                            if 'text' in widget_data:
                                combined_text.append(widget_data['text'])
                        
                        if combined_text:
                            # Use the first widget type (usually Quote)
                            first_widget = list(widgets.values())[0]
                            slide['widgets'] = {
                                'default': {
                                    'type': first_widget.get('type', 'Type.Body'),
                                    'text': '\\n\\n'.join(combined_text),
                                    **{k: v for k, v in first_widget.items() if k not in ['type', 'text']}
                                }
                            }
                    
                    fixes_applied += 1
                    report.append(f"  ✅ FIXED: Changed layout {old_layout} → {new_layout}")
        else:
            report.append(f"\n✅ Slide {i} ({slide_id}): {layout} layout - OK")
    
    # Summary
    report.append("\n" + "=" * 80)
    report.append("SUMMARY")
    report.append("=" * 80)
    report.append(f"Total slides: {len(slides)}")
    report.append(f"Issues found: {issues_found}")
    if fix:
        report.append(f"Fixes applied: {fixes_applied}")
    report.append("")
    
    return slides, report


def print_validation_report(slides_path: str, fix: bool = False):
    """Print validation report for slides JSON.
    
    Args:
        slides_path: Path to slides JSON file
        fix: If True, save fixed version
    """
    slides, report = validate_slides_json(slides_path, fix=fix)
    
    # Print report
    for line in report:
        print(line)
    
    # Save fixed version if requested
    if fix:
        fixed_path = Path(slides_path).parent / f"{Path(slides_path).stem}_fixed.json"
        with open(fixed_path, 'w', encoding='utf-8') as f:
            json.dump({'contexts': slides, 'id': 'slides', 'model': 'Slide'}, f, indent=2)
        print(f"\n✅ Fixed version saved to: {fixed_path}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m src.layout.slidev.validate_slides <slides.json> [--fix]")
        sys.exit(1)
    
    slides_path = sys.argv[1]
    fix = "--fix" in sys.argv
    
    print_validation_report(slides_path, fix=fix)
