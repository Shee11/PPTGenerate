# Style System Refactoring - Summary

## Overview
The style system has been completely refactored to separate content from presentation. Widget parameters now only contain content data, while all styling is defined in the Style configuration using theme tokens.

## Key Changes

### 1. **New Style Model** (`src/layout/style.py`)
The Style model now defines styling rules for each widget type:

```python
class WidgetStyle(BaseModel):
    font: Optional[str]  # Theme typography token (h1, h2, h3, body, caption)
    align: Optional[Literal["left", "center", "right", "justify"]]
    vertical_align: Optional[Literal["top", "center", "bottom"]]
    foreground: Optional[str]  # Theme color token (primary_color, text_color, etc.)
    background: Optional[str]  # Theme color token
    border_radius: Optional[str]  # CSS value (e.g., "8px")

class Style(BaseModel):
    theme_name: str
    widgets: Dict[str, WidgetStyle]  # Keyed by widget type
```

**Example Style Config:**
```json
{
  "theme_name": "corp_modern_v1",
  "widgets": {
    "Type.Display": {
      "font": "h1",
      "align": "center",
      "foreground": "text_color"
    },
    "Data.BigNum": {
      "font": "h1",
      "align": "center",
      "foreground": "primary_color"
    }
  }
}
```

### 2. **Simplified Widgets** (`src/widgets/`)
Widgets no longer accept style-related parameters:

**Before:**
```json
{
  "type": "Type.Display",
  "parameters": {
    "text": "Hello",
    "style": "bold",
    "align": "center"
  }
}
```

**After:**
```json
{
  "type": "Type.Display",
  "parameters": {
    "text": "Hello"
  }
}
```

**Typography Widgets:**
- `Type.Display`: Only `text` parameter
- `Type.Heading`: `text` and `level` parameters
- `Type.Body`: Only `text` parameter
- `Type.List`: `items` and `list_type` parameters
- `Type.Quote`: `text` and optional `citation` parameters

**Data Widgets:**
- `Data.BigNum`: `number`, `label`, `format`, `show_label` parameters (removed `color`)
- `Data.Trend`: `value`, `change`, `direction`, `label` parameters (removed `color`)
- `Data.Progress`: `percentage`, `label`, `show_percentage` parameters (removed `color`)

### 3. **LayoutEngine Enhancements** (`src/layout/layout_engine.py`)
The LayoutEngine now:

1. **Validates** that every widget type has a style defined in the Style config
2. **Resolves** theme tokens to actual CSS values
3. **Applies** resolved styles to each WidgetAssignment

**New method:** `_resolve_widget_style(widget_style, theme) -> Dict[str, Any]`
- Converts theme typography tokens to CSS font properties
- Resolves color tokens to actual color values
- Returns ready-to-use CSS properties

**Enhanced WidgetAssignment:**
```python
class WidgetAssignment(BaseModel):
    role: str
    widget: BaseWidget
    slot: Slot
    applied_style: Dict[str, Any]  # NEW: Resolved CSS properties
```

### 4. **Error Handling**
If a widget type is used but not defined in the Style config:
```
UCERenderError: No style defined for widget type 'Type.Display'. 
All widget types must be explicitly styled in the Style config.
```

## Migration Guide

### For Configuration Files

1. **Remove style parameters from widgets:**
   ```json
   // OLD - Don't do this
   "widgets": {
     "headline": {
       "type": "Type.Display",
       "parameters": {
         "text": "Title",
         "style": "bold",
         "align": "center"
       }
     }
   }
   
   // NEW - Do this
   "widgets": {
     "headline": {
       "type": "Type.Display",
       "parameters": {
         "text": "Title"
       }
     }
   }
   ```

2. **Define widget styles in Style config:**
   ```json
   "style": {
     "theme_name": "corp_modern_v1",
     "widgets": {
       "Type.Display": {
         "font": "h1",
         "align": "center",
         "foreground": "text_color"
       },
       "Type.Heading": {
         "font": "h2",
         "align": "left",
         "foreground": "text_color"
       },
       "Type.Body": {
         "font": "body",
         "align": "left",
         "foreground": "text_color"
       },
       "Data.BigNum": {
         "font": "h1",
         "align": "center",
         "foreground": "primary_color"
       },
       "Data.Progress": {
         "font": "body",
         "foreground": "accent_color",
         "background": "primary_background"
       }
     }
   }
   ```

### For Templates (TODO)

Templates need to be updated to use `assignment.applied_style` instead of widget parameters:

```jinja2
{# OLD #}
<div style="text-align: {{ data.align }}; font-weight: {{ data.style }};">
  {{ data.content }}
</div>

{# NEW #}
<div style="{% for prop, value in assignment.applied_style.items() %}{{ prop }}: {{ value }};{% endfor %}">
  {{ data.content }}
</div>
```

### For Tests (TODO)

All tests need to be updated to:
1. Remove style parameters from widget configurations
2. Add complete Style config with all widget types used in the test
3. Update assertions to check applied_style instead of widget parameters

## Benefits

1. **Separation of Concerns**: Content vs. presentation clearly separated
2. **Consistency**: All styling goes through theme tokens
3. **Reusability**: Same widgets with different styles via Style config
4. **Validation**: Explicit error if widget style is undefined
5. **Flexibility**: Easy to create style variations without changing content

## Remaining Work

1. ✅ Update Style model with widget styling rules
2. ✅ Clean up widget parameters (remove style-related)
3. ✅ Enhance LayoutEngine to resolve and apply styles
4. ⏳ Update templates to use applied_style
5. ⏳ Update all example configs
6. ⏳ Update all tests (131 tests need migration)
7. ⏳ Update asset style files

## Example Files

- `examples/style_example.json` - Complete style configuration example
- Run `python -m cli.uce_render --list-styles` to see the new style schema
