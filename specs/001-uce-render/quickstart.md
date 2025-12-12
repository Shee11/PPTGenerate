# Quickstart: UCE Rendering System

**Feature**: 001-uce-render  
**Purpose**: Get started with the Universal Content Engine rendering system in 5 minutes

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

## Installation

```bash
# Clone repository
git clone <repo-url>
cd gggg

# Install in development mode
pip install -e .

# Verify installation
uce-render --help
```

## Quick Example: Render Your First Layout

### Step 1: Create a Layouts Configuration

Create `my-layout.json`:

```json
{
  "layouts": {
    "hero": {
      "strategy": "Bento",
      "variant": "HeroLeft",
      "gap": "20px",
      "padding": "40px",
      "background": "#f5f5f5",
      "widget_assignments": [
        {
          "role": "main",
          "widget_type": "Chart.Bar",
          "atom_id": "revenue_chart",
          "params": {
            "palette": "corporate_blue",
            "show_values": true
          },
          "style_name": "modern"
        },
        {
          "role": "side_1",
          "widget_type": "Data.BigNum",
          "atom_id": "total_revenue",
          "params": {
            "layout": "stack",
            "color": "accent"
          },
          "style_name": "modern"
        },
        {
          "role": "side_2",
          "widget_type": "Data.Trend",
          "atom_id": "yoy_growth",
          "params": {
            "icon": "up",
            "chart": "sparkline"
          },
          "style_name": "modern"
        }
      ]
    }
  },
  "active_layout_id": "hero"
}
```

### Step 2: Create a Styles Configuration

Create `my-styles.json`:

```json
{
  "themes": {
    "corporate": {
      "primary_font": "Inter",
      "secondary_font": "Georgia",
      "foreground_primary_color": "#1a1a1a",
      "foreground_secondary_color": "#666666",
      "background_primary_color": "#ffffff",
      "background_secondary_color": "#f5f5f5",
      "accent_color": "#0066cc",
      "error_color": "#dc3545",
      "success_color": "#28a745"
    }
  },
  "styles": {
    "modern": {
      "theme_name": "corporate",
      "border_radius": "8px",
      "shadow_intensity": "medium",
      "spacing_scale": 1.0,
      "transition_duration": "200ms"
    }
  },
  "default_style_name": "modern"
}
```

### Step 3: Render to HTML

```bash
uce-render my-layout.json my-styles.json -o output.html
```

Open `output.html` in your browser to see the rendered layout!

## Common Layouts

### Bento Grid (3x2)

```json
{
  "strategy": "Bento",
  "variant": "Standard",
  "gap": "16px",
  "padding": "32px",
  "background": "#ffffff"
}
```

**Use case**: Dashboard with 6 equal-sized metrics or charts

### Swiss Poster (Full-Screen Text)

```json
{
  "strategy": "Swiss",
  "variant": "Poster",
  "gap": "0px",
  "padding": "60px",
  "background": "#000000"
}
```

**Use case**: Presentation title slide, hero banner

### Cinematic Split (50/50)

```json
{
  "strategy": "Cinematic",
  "variant": "Split_50_50",
  "gap": "0px",
  "padding": "0px",
  "background": "linear-gradient(to right, #1a1a1a, #333333)"
}
```

**Use case**: Before/after comparison, feature showcase

## Widget Catalog

### Typography Widgets

#### Type.Display (Giant Headlines)

```json
{
  "widget_type": "Type.Display",
  "params": {
    "style": "bold",
    "align": "center"
  }
}
```

**Minimum size**: L

#### Type.Body (Paragraphs)

```json
{
  "widget_type": "Type.Body",
  "params": {
    "cols": 2,
    "drop_cap": true
  }
}
```

**Minimum size**: M

### Data Widgets

#### Data.BigNum (KPI Display)

```json
{
  "widget_type": "Data.BigNum",
  "atom_id": "total_sales",
  "params": {
    "layout": "stack",
    "color": "accent"
  }
}
```

**Minimum size**: S

**Required atom_data**:
```json
{
  "number": 12345,
  "label": "Total Sales"
}
```

#### Data.Trend (With Arrow/Sparkline)

```json
{
  "widget_type": "Data.Trend",
  "atom_id": "growth_rate",
  "params": {
    "icon": "up",
    "chart": "sparkline"
  }
}
```

**Minimum size**: S

### Chart Widgets

#### Chart.Bar

```json
{
  "widget_type": "Chart.Bar",
  "atom_id": "quarterly_revenue",
  "params": {
    "palette": "sequential",
    "legend_position": "bottom",
    "show_values": true
  }
}
```

**Minimum size**: M

**Required atom_data**:
```json
{
  "categories": ["Q1", "Q2", "Q3", "Q4"],
  "series": [
    {
      "name": "Revenue",
      "data": [100, 120, 150, 180]
    }
  ]
}
```

## Validation

### Check Configuration Before Rendering

```bash
uce-render my-layout.json my-styles.json --validate-only
```

**Success**:
```
✓ Layouts file valid
✓ Styles file valid
✓ Size constraints satisfied
✓ All references resolved
Ready to render
```

**Error**:
```
✗ Validation failed

Error in my-layout.json:
  Widget "Chart.Sankey" requires size XL but assigned to slot "side_1" with size S
```

## Troubleshooting

### Size Constraint Error

**Problem**: Widget won't fit in assigned slot

**Solution**: Either:
1. Choose a smaller widget type for the slot
2. Assign the widget to a larger slot
3. Switch to a layout variant with larger slots

**Example**: Chart.Sankey needs XL, so use Cinematic.FullBleed or Swiss.Poster

### Missing Style Reference

**Problem**: `Style "modern_dark" not found`

**Solution**: Add the style to `styles.json`:

```json
{
  "styles": {
    "modern_dark": {
      "theme_name": "dark",
      "border_radius": "12px",
      "shadow_intensity": "strong",
      "spacing_scale": 1.2,
      "transition_duration": "300ms"
    }
  }
}
```

### Widget Missing Atom Data

**Problem**: Chart renders empty

**Solution**: Charts need data! Provide atom_data in your pipeline:

```python
from src.layout.layout_engine import LayoutEngine
from src.render.html_renderer import HTMLRenderer

# ... load layouts and styles ...

engine = LayoutEngine()
renderable = engine.calculate(layouts, styles)

# Inject atom data
atom_data = {
    "revenue_chart": {
        "categories": ["Jan", "Feb", "Mar"],
        "series": [{"name": "Sales", "data": [100, 150, 120]}]
    }
}

renderer = HTMLRenderer()
html = renderer.render(renderable, atom_data=atom_data)
```

## Next Steps

### Customize Themes

Edit `my-styles.json` to match your brand:

```json
{
  "themes": {
    "brand": {
      "primary_font": "Your Brand Font",
      "accent_color": "#FF6B35",
      "background_primary_color": "#FAFAFA"
    }
  }
}
```

### Create Custom Layouts

Mix and match layout variants:

1. Start with a strategy (Bento, Swiss, Cinematic)
2. Choose a variant (Standard, HeroLeft, Poster, etc.)
3. Add widget assignments for each slot
4. Apply styles

### Programmatic Usage

Use the Python API directly:

```python
from src.layout.layout_engine import LayoutEngine
from src.render.html_renderer import HTMLRenderer
from src.common.patchable_context_pydantic import Layouts, Styles

# Load from files
layouts = Layouts.model_validate_json(open("my-layout.json").read())
styles = Styles.model_validate_json(open("my-styles.json").read())

# Calculate layout
engine = LayoutEngine()
renderable = engine.calculate(layouts, styles)

# Render to HTML
renderer = HTMLRenderer()
html = renderer.render(renderable)

# Save or serve
with open("output.html", "w") as f:
    f.write(html)
```

### Explore All Layout Variants

Try each variant from the spec:

**Bento**:
- Standard (3x2 grid)
- HeroLeft (large left, 2 small right)
- HeroTop (large top, 3 small bottom)
- Quarter (4 equal quadrants)

**Swiss**:
- Poster (full-screen text)
- Asymmetry (left void, right content)
- SplitTypo (giant top, normal bottom)

**Cinematic**:
- FullBleed (background image with overlay)
- Split_30_70 (sidebar + stage)
- Split_50_50 (equal halves)

## Examples Directory

Check `examples/` for complete working examples:

```
examples/
├── executive-dashboard/     # Bento.HeroLeft with charts
├── product-launch/          # Swiss.Poster hero slide
└── comparison-view/         # Cinematic.Split_50_50
```

Each example includes:
- `layout.json` - Layout configuration
- `styles.json` - Style definitions
- `atom-data.json` - Sample data for widgets
- `output.html` - Pre-rendered result
- `README.md` - Explanation and use case

## Support

For issues or questions:
- Check `docs/` for detailed documentation
- Review `contracts/` for API specifications
- See `data-model.md` for entity relationships
- Read `research.md` for technology decisions
