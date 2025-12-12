# UCE Render Examples

This directory contains example configurations demonstrating the UCE Rendering System capabilities.

## Available Examples

### 1. Dashboard (Bento.Standard)

**File**: `dashboard.json`

A classic dashboard layout using the Bento.Standard 3x2 grid strategy with:
- Display headline
- BigNum metrics (users, projects)
- Trend indicators (revenue, growth)
- Progress bar
- Body text

**Render**:
```bash
uce-render examples/dashboard.json --output examples/dashboard.html
```

**Features Demonstrated**:
- Bento.Standard layout (6 S slots)
- Typography widgets (Type.Display, Type.Body)
- Data widgets (Data.BigNum, Data.Trend, Data.Progress)
- Widget parameters (style, align, color, format, direction)
- Theme customization (primary/accent colors)

---

### 2. Poster (Swiss.Poster)

**File**: `poster.json`

A full-bleed poster layout using the Swiss.Poster strategy with:
- Single XL slot for maximum impact
- Large display typography
- Minimalist design

**Render**:
```bash
uce-render examples/poster.json --output examples/poster.html
```

**Features Demonstrated**:
- Swiss.Poster layout (1 XL slot)
- Type.Display widget with bold-italic styling
- Full-bleed, single-focus design
- Center alignment for impact

---

## Creating Your Own Layouts

### Step 1: Choose a Strategy

Pick a layout strategy based on your content structure:

**Grid Layouts** (Bento Family):
- `Bento.Standard`: Equal 3x2 grid - good for dashboards
- `Bento.HeroLeft`: Hero + sidebar - good for feature highlights
- `Bento.HeroTop`: Hero + footer - good for landing pages
- `Bento.Quarter`: Four quadrants - good for comparisons

**Typography-Focused** (Swiss Family):
- `Swiss.Poster`: Single focus - good for announcements
- `Swiss.Asymmetry`: Large content - good for articles
- `Swiss.SplitTypo`: Headline + body - good for blog posts

**Widescreen** (Cinematic Family):
- `Cinematic.Split_50_50`: Equal split - good for before/after
- `Cinematic.FullBleed`: Single stage - good for hero sections
- `Cinematic.Split_30_70`: Sidebar + main - good for documentation

### Step 2: Configure Theme & Style

```json
{
  "strategy": "Bento.Standard",
  "theme": {
    "primary_color": "#2563eb",
    "accent_color": "#7c3aed",
    "font_family": "Inter, system-ui, sans-serif"
  },
  "style": {
    "theme_name": "default",
    "gap": "24px",
    "padding": "32px"
  }
}
```

### Step 3: Add Widgets

Assign widgets to slots based on the strategy's slot layout.

**Typography Widgets**:
```json
{
  "cell_1": {
    "type": "Type.Display",
    "parameters": {
      "text": "Your Headline",
      "style": "bold",
      "align": "center"
    }
  },
  "cell_2": {
    "type": "Type.Heading",
    "parameters": {
      "text": "Section Title",
      "level": 2,
      "align": "left"
    }
  },
  "cell_3": {
    "type": "Type.Body",
    "parameters": {
      "text": "Body content goes here...",
      "align": "justify"
    }
  },
  "cell_4": {
    "type": "Type.List",
    "parameters": {
      "items": ["Item 1", "Item 2", "Item 3"],
      "list_type": "ordered"
    }
  },
  "cell_5": {
    "type": "Type.Quote",
    "parameters": {
      "text": "A wise quote",
      "citation": "Famous Person",
      "align": "center"
    }
  }
}
```

**Data Widgets**:
```json
{
  "cell_1": {
    "type": "Data.BigNum",
    "parameters": {
      "value": 1247,
      "label": "Total Users",
      "color": "primary",
      "format": "number"
    }
  },
  "cell_2": {
    "type": "Data.Trend",
    "parameters": {
      "value": 342,
      "change": 12.5,
      "direction": "up",
      "label": "Monthly Revenue",
      "color": "success"
    }
  },
  "cell_3": {
    "type": "Data.Progress",
    "parameters": {
      "value": 75,
      "max": 100,
      "label": "Project Completion",
      "show_percentage": true,
      "color": "accent"
    }
  }
}
```

### Step 4: Validate & Render

```bash
# Validate configuration
uce-render your-layout.json --validate-only

# Render to HTML
uce-render your-layout.json --output your-layout.html

# Verbose mode for debugging
uce-render your-layout.json --output your-layout.html --verbose
```

## Size Constraints

Each strategy defines slot sizes (S/M/L/XL). Widgets have minimum size requirements:
- All widgets currently have **min_size: S**
- You can assign any widget to any slot of sufficient size
- Size validation automatically prevents invalid assignments

**Example**: You cannot assign a widget requiring size L to a slot with size S.

**Error Message**:
```
SizeConstraintError: Widget 'Type.Display' requires minimum size L but slot 'cell_1' only offers size S.
Suggestion: Use a larger slot or choose a widget with a smaller minimum size.
```

## Tips & Best Practices

1. **Start Simple**: Begin with Bento.Standard or Swiss.Poster
2. **Validate Early**: Use `--validate-only` before rendering
3. **Use Parameters**: Leverage widget parameters for customization
4. **Theme Consistency**: Define a consistent color palette in theme
5. **Size Appropriately**: Match widget importance to slot size
6. **Test Rendering**: Render to HTML frequently during development

## Need Help?

- See main [README.md](../README.md) for Python API usage
- Check [spec.md](../specs/001-uce-render/spec.md) for detailed feature descriptions
- Review [plan.md](../specs/001-uce-render/plan.md) for architecture details
