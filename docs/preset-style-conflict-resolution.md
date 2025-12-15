# Systematic Preset-Style Conflict Resolution

## Problem Statement

Inline styles were overriding preset CSS classes, causing visual conflicts like:
- Green text on green background (when `Solid_Brand` preset + `color: primary` inline style)
- Border-radius conflicts (when `shape` preset + `border-radius` inline style)
- Background conflicts (when `surface/fill` preset + `background` inline style)

## Root Cause

The style resolution system (`_resolve_widget_style`) was adding inline CSS properties that overlapped with preset-controlled properties, creating specificity conflicts where inline styles would override preset CSS classes.

## Solution Design

### 1. Principle: Presets Own Their Properties

Each preset category has exclusive control over specific CSS properties:

**Surface Presets** control:
- `background` / `background-color`
- `border` / `border-width` / `border-style` / `border-color`
- `box-shadow`
- `backdrop-filter`

**Shape Presets** control:
- `border-radius`

**Fill Presets** control:
- `background` / `background-color` / `background-image`
- `color` (text color for contrast)
- `border` (for subtle variants)

**Effect Presets** control:
- `filter`
- `box-shadow` (for glow)
- `animation`
- Pseudo-elements (`::before`, `::after`)

### 2. Style Resolution Logic

Modified `_resolve_widget_style()` to detect active preset categories and skip adding conflicting inline styles:

```python
def _resolve_widget_style(cls, widget_style, theme: Theme, preset: Optional[Dict[str, str]] = None):
    preset = preset or {}
    
    # Detect active preset categories
    has_surface = "surface" in preset
    has_shape = "shape" in preset
    has_fill = "fill" in preset
    has_effect = "effect" in preset
    
    # Only add inline styles that won't conflict with presets
    
    # Color: Skip if fill preset is active
    if widget_style.foreground and not has_fill:
        resolved["color"] = ...
    
    # Background: Skip if surface OR fill preset is active
    if widget_style.background and not (has_surface or has_fill):
        resolved["background-color"] = ...
    
    # Border-radius: Skip if shape preset is active
    if widget_style.border_radius and not has_shape:
        resolved["border-radius"] = ...
```

### 3. Default Presets

All widgets now get default presets even when not explicitly specified:

```python
_default_presets = {
    "Type.Display": {"surface": "Flat"},
    "Type.Heading": {"surface": "Flat"},
    "Type.Body": {"surface": "Flat"},
    "Data.BigNum": {"surface": "Flat"},
    # ... etc
}
```

The `Flat` surface preset means "no visual treatment" (transparent background, no border, no shadow), allowing widgets to still use style config colors when no explicit preset is given.

## Implementation Changes

### Modified Files

**src/layout/layout_engine.py:**
- Added `_default_presets` class variable with default preset mappings
- Modified `_resolve_widget_style()` to accept `preset` parameter
- Added logic to skip preset-controlled properties in inline styles
- Apply default presets when none specified

**docs/preset-controlled-properties.md:**
- Documented all CSS properties controlled by each preset category
- Listed properties safe for inline styles

## Behavior Matrix

| Preset Active | `color` | `background-color` | `border-radius` | `box-shadow` | `filter` |
|---------------|---------|-------------------|----------------|--------------|----------|
| None (Flat)   | ✅ Inline | ✅ Inline | ✅ Inline | - | - |
| surface       | ✅ Inline | ❌ Preset | ✅ Inline | ❌ Preset | - |
| shape         | ✅ Inline | ✅ Inline | ❌ Preset | - | - |
| fill          | ❌ Preset | ❌ Preset | ✅ Inline | - | - |
| effect        | ✅ Inline | ✅ Inline | ✅ Inline | - | ❌ Preset |

✅ = Property set via inline style
❌ = Property controlled by preset CSS

## Testing Results

All 10 slides in cyber-tech.json render correctly with:
- ✅ Slide 1: "99.97% Uptime" - white text on green background (Solid_Brand)
- ✅ Slide 7: "DEEP LEARNING" - white text on green background (Solid_Brand)
- ✅ All widgets: No inline style conflicts with active presets
- ✅ Widgets without fill presets: Still receive colors from style config
- ✅ Default presets: Applied to widgets without explicit preset configuration

## Future Considerations

1. **Custom Presets**: The system now makes it easy to add new preset categories without worrying about inline style conflicts

2. **Preset Combinations**: Multiple presets work together cleanly:
   - `surface: "Elevated"` + `shape: "Rounded"` + `fill: "Solid_Brand"` → All properties controlled by presets
   - `surface: "Glass"` + `effect: "Glow"` → No fill, so color comes from style config

3. **Style Config Simplification**: Widget style configs can now focus on typography and layout, leaving all visual styling to presets

## Migration Guide

For existing configurations:

1. **Widgets with explicit backgrounds**: Add appropriate `surface` or `fill` preset
2. **Widgets with border-radius**: Add appropriate `shape` preset
3. **Widgets needing colors**: Either add `fill` preset or rely on style config
4. **Widgets with no styling**: Will automatically get `Flat` preset (no visual treatment)
