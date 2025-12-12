# Comprehensive Theme System

## Overview

The UCE Rendering System now supports a comprehensive theme model designed for multi-slide presentations with:

- **Grid System**: 12-column responsive grid with configurable margins and gutters
- **Header Strategy**: Flexible header positioning and decoration
- **Sequence Patterns**: Visual rhythm across multiple slides (alternating backgrounds, section breaks)
- **Typography Tokens**: Semantic type scale (h1, h2, h3, body, caption)
- **Color Palette**: Primary, secondary, accent, background, and text colors
- **Background Slots**: Primary and secondary backgrounds for alternating patterns

## Architecture Flow

```
Theme (defines slots) → Layout (fills slots) → LayoutEngine (assigns per slide) → Renderer (generates HTML)
```

### Example Flow

1. **Theme** defines `sequence_pattern: "alternating_background"` with `primary_background` and `secondary_background`
2. **Layout** provides values for backgrounds (e.g., `"#f8fafc"` and `"#ffffff"`)
3. **LayoutEngine** assigns backgrounds to slides following the pattern (slide 0: primary, slide 1: secondary, slide 2: primary...)
4. **Renderer** creates HTML with assigned backgrounds

## Theme Structure

### Grid System

```json
{
  "grid_system": {
    "columns": 12,        // Number of columns
    "margin_x": "40px",   // Horizontal page margin
    "margin_y": "30px",   // Vertical page margin
    "gutter": "20px"      // Space between columns
  }
}
```

### Header Strategy

```json
{
  "header_strategy": {
    "position": "fixed_top_left",      // "fixed_top_left" | "centered" | "floating"
    "height": "15%",                    // Header area height
    "decoration": "underline_accent"    // "none" | "underline_accent" | "border_bottom" | "background_block"
  }
}
```

### Sequence Patterns

- **`uniform`**: Same background for all slides
- **`alternating_background`**: Alternates between primary and secondary backgrounds (0: primary, 1: secondary, 2: primary...)
- **`section_break`**: Every 3rd slide uses primary background as visual section divider

### Typography Tokens

```json
{
  "typography": {
    "h1": {
      "size": 60,           // Font size in pixels
      "weight": "bold",     // "thin" | "light" | "regular" | "medium" | "semibold" | "bold" | "black"
      "line_height": 1.1    // Line height multiplier
    },
    "h2": { "size": 40, "weight": "medium", "line_height": 1.2 },
    "h3": { "size": 28, "weight": "medium", "line_height": 1.3 },
    "body": { "size": 18, "weight": "regular", "line_height": 1.5 },
    "caption": { "size": 14, "weight": "regular", "line_height": 1.4 }
  }
}
```

### Color Palette

```json
{
  "primary_color": "#2563eb",      // Primary brand color
  "secondary_color": "#64748b",    // Secondary brand color
  "accent_color": "#f59e0b",       // Accent/highlight color
  "background_color": "#ffffff",   // Default background
  "text_color": "#1e293b"          // Default text color
}
```

### Background Slots

```json
{
  "primary_background": "#f8fafc",   // Background for even slides (0, 2, 4...)
  "secondary_background": "#ffffff"  // Background for odd slides (1, 3, 5...)
}
```

## Complete Example: Corporate Modern Theme

```json
{
  "id": "corp_modern_v1",
  "grid_system": {
    "columns": 12,
    "margin_x": "40px",
    "margin_y": "30px",
    "gutter": "20px"
  },
  "header_strategy": {
    "position": "fixed_top_left",
    "height": "15%",
    "decoration": "underline_accent"
  },
  "sequence_pattern": "alternating_background",
  "typography": {
    "h1": { "size": 60, "weight": "bold", "line_height": 1.1 },
    "h2": { "size": 40, "weight": "medium", "line_height": 1.2 },
    "h3": { "size": 28, "weight": "medium", "line_height": 1.3 },
    "body": { "size": 18, "weight": "regular", "line_height": 1.5 },
    "caption": { "size": 14, "weight": "regular", "line_height": 1.4 }
  },
  "primary_color": "#2563eb",
  "secondary_color": "#64748b",
  "accent_color": "#f59e0b",
  "background_color": "#ffffff",
  "text_color": "#1e293b",
  "primary_background": "#f8fafc",
  "secondary_background": "#ffffff",
  "font_family": "Inter, system-ui, sans-serif",
  "heading_font": "Inter, system-ui, sans-serif"
}
```

## CSS Custom Properties

The theme generates CSS custom properties that can be used in templates:

### Color Variables
- `--color-primary`
- `--color-secondary`
- `--color-accent`
- `--color-background`
- `--color-text`

### Grid Variables
- `--grid-columns`
- `--margin-x`
- `--margin-y`
- `--gutter`

### Header Variables
- `--header-height`

### Typography Variables
- `--font-h1-size`, `--font-h1-weight`, `--font-h1-line-height`
- `--font-h2-size`, `--font-h2-weight`, `--font-h2-line-height`
- `--font-h3-size`, `--font-h3-weight`, `--font-h3-line-height`
- `--font-body-size`, `--font-body-weight`, `--font-body-line-height`
- `--font-caption-size`, `--font-caption-weight`, `--font-caption-line-height`

### Background Variables
- `--background-primary` (if defined)
- `--background-secondary` (if defined)

### Font Variables
- `--font-family`
- `--font-heading`

## Backward Compatibility

The theme system maintains full backward compatibility with the previous simple theme model:

- **Legacy fields**: `base_font_size` and `line_height` are deprecated but still supported
- **Default values**: All new fields have sensible defaults, so existing themes work without modification
- **Optional ID**: Theme `id` field defaults to `"default_theme"` if not provided

Example of minimal backward-compatible theme:

```python
from src.layout.theme import Theme

# Old style still works
theme = Theme(
    primary_color="#FF0000",
    font_family="Arial"
)

# New comprehensive style
theme = Theme(
    id="my_theme",
    grid_system={"columns": 12, "margin_x": "40px"},
    header_strategy={"position": "centered"},
    sequence_pattern="alternating_background",
    typography={
        "h1": {"size": 60, "weight": "bold"}
    }
)
```

## Usage Examples

### Loading from JSON

```python
from src.layout.theme import Theme
import json

# Load theme from file
with open("data/corp_modern_theme.json") as f:
    theme_data = json.load(f)
    theme = Theme(**theme_data)

# Access properties
print(f"Grid columns: {theme.grid_system.columns}")
print(f"H1 size: {theme.typography.h1.size}px")
```

### Slide Background Assignment

```python
# Get background for specific slide
bg_0 = theme.get_slide_background(0)  # Primary background
bg_1 = theme.get_slide_background(1)  # Secondary background
bg_2 = theme.get_slide_background(2)  # Primary background (alternates)
```

### CSS Variables Generation

```python
# Convert to CSS custom properties
css_vars = theme.to_css_vars()

# Use in templates
for var_name, var_value in css_vars.items():
    print(f"{var_name}: {var_value};")
```

## Example Themes

### 1. Corporate Modern (`corp_modern_v1`)
- **Use case**: Professional corporate presentations
- **Grid**: 12 columns, 40px margins
- **Header**: Fixed top-left with accent underline
- **Sequence**: Alternating light backgrounds (#f8fafc / #ffffff)
- **Typography**: Inter font, balanced scale (60/40/28/18/14px)
- **Colors**: Blue primary (#2563eb), orange accent (#f59e0b)

### 2. Minimal Dark (`minimal_dark_v1`)
- **Use case**: Modern dark-themed presentations
- **Grid**: 12 columns, 60px margins (more spacious)
- **Header**: Centered with no decoration
- **Sequence**: Section breaks every 3 slides
- **Typography**: Helvetica, bold headlines (72/48/32/20/16px)
- **Colors**: Dark slate background (#0f172a), cyan accent (#06b6d4)

## Next Steps

To fully support multi-slide presentations, the following components need updates:

1. **LayoutEngine**: Extend `calculate()` to return `List[RenderableLayout]` for multiple slides
2. **RenderableLayout**: Add slide-specific fields (slide_number, grid_settings, header_config, background)
3. **HTMLRenderer**: Handle `List[RenderableLayout]` and generate slide navigation
4. **Templates**: Apply grid system, header positioning, and alternating backgrounds

See the architecture section for the complete flow from theme definition to HTML rendering.
