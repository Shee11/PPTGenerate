# Architecture: Style System & Asset Management

**Feature**: 001-uce-render  
**Created**: 2025-01-XX  
**Purpose**: Document the style system architecture and relationships between Widget, Layout, Style, and Theme

## Overview

The Universal Content Engine uses a **separation of concerns** architecture where content, styling, and layout are independently managed and resolved at runtime by the LayoutEngine.

## Component Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                    Asset Discovery Layer                        │
│  (File-based, auto-discovered from assets/ directory)          │
├─────────────────────────────────────────────────────────────────┤
│  assets/themes/*.json      →  Theme (color/font tokens)        │
│  assets/styles/*.json      →  Style (widget styling rules)     │
│  assets/strategies/*.json  →  LayoutStrategy (slot defs)       │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                   Configuration Layer (JSON)                    │
├─────────────────────────────────────────────────────────────────┤
│  {                                                               │
│    "style_name": "corp_modern_default",  ← references Style    │
│    "slides": [{                                                 │
│      "layout_strategy": "Bento.Standard",  ← references Layout │
│      "widgets": [{                                              │
│        "role": "cell_1",        ← references Slot              │
│        "widget_type": "Type.Display",                          │
│        "parameters": {          ← CONTENT ONLY                 │
│          "text": "Hello World"                                 │
│        }                                                        │
│      }]                                                         │
│    }]                                                           │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Resolution Layer                             │
│                   (LayoutEngine Runtime)                        │
├─────────────────────────────────────────────────────────────────┤
│  1. Widget provides: widget_type + content parameters          │
│  2. Style provides: widgets[widget_type] → WidgetStyle         │
│  3. WidgetStyle has: tokens (font="primary", fg="accent")      │
│  4. Theme provides: token values (primary_font="Inter")        │
│  5. Engine resolves: tokens → CSS dict                         │
│  6. Template receives: applied_style dict                      │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                     Rendering Layer                             │
│                    (Jinja2 Templates)                           │
├─────────────────────────────────────────────────────────────────┤
│  <div style="{{ render_style(applied_style) }}">               │
│    {{ widget.parameters.text }}                                │
│  </div>                                                         │
│                                                                 │
│  Result:                                                        │
│  <div style="font-family: Inter; color: #1a1a1a">              │
│    Hello World                                                  │
│  </div>                                                         │
└─────────────────────────────────────────────────────────────────┘
```

## Core Concepts

### 1. Theme (Design Tokens)

**Purpose**: Defines the visual design language with reusable tokens.

**Contains**:
- **Typography**: `primary_font`, `secondary_font` (e.g., "Inter", "Georgia")
- **Foreground Colors**: `foreground_primary_color`, `foreground_secondary_color`
- **Background Colors**: `background_primary_color`, `background_secondary_color`
- **Semantic Colors**: `accent_color`, `error_color`, `success_color`

**Location**: `assets/themes/*.json`

**Example** (`assets/themes/corp_modern.json`):
```json
{
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
```

**Key Characteristics**:
- Reusable across multiple styles
- Provides consistent brand identity
- Token-based (not direct CSS values in usage)

### 2. Style (Widget Styling Rules)

**Purpose**: Maps widget types to visual styling using theme tokens.

**Contains**:
- `name`: Unique identifier (e.g., "corp_modern_default")
- `theme_name`: Reference to Theme (e.g., "corp_modern")
- `widgets`: Dict mapping widget types to WidgetStyle configurations

**Location**: `assets/styles/*.json`

**Example** (`assets/styles/corp_modern_default.json`):
```json
{
  "name": "corp_modern_default",
  "theme_name": "corp_modern",
  "widgets": {
    "Type.Display": {
      "font": "primary",
      "foreground": "primary",
      "align": "center",
      "font_size": "48px"
    },
    "Type.Body": {
      "font": "secondary",
      "foreground": "secondary",
      "line_height": 1.6,
      "font_size": "16px"
    },
    "Data.BigNum": {
      "font": "primary",
      "foreground": "accent",
      "font_size": "64px"
    }
  }
}
```

**Key Characteristics**:
- One style references one theme
- Multiple styles can share the same theme
- Defines HOW widgets look (not WHAT they contain)

### 3. WidgetStyle (Token-Based Styling)

**Purpose**: Optional styling configuration for individual widget types.

**Token Fields** (reference Theme):
- `font`: "primary" | "secondary" → `theme.primary_font` | `theme.secondary_font`
- `foreground`: "primary" | "secondary" | "accent" | "error" | "success" → theme color
- `background`: "primary" | "secondary" → theme background color

**Direct CSS Fields**:
- `font_size`: CSS value (e.g., "48px", "1.5rem")
- `font_weight`: Integer 100-900
- `line_height`: Float (e.g., 1.6)
- `align`: "left" | "center" | "right" | "justify"
- `vertical_align`: "top" | "middle" | "bottom"
- `border_radius`: CSS value (e.g., "8px")

**All fields are optional** - allows granular customization per widget type.

### 4. Widget (Content Only)

**Purpose**: Defines WHAT content to display, with NO styling information.

**Content Parameters by Category**:
- **Type (Typography)**: `text`, `citation`
- **Data**: `number`, `label`, `trend`
- **Chart**: `categories`, `series`, `show_values`
- **Media**: `src`, `alt`, `fit`

**Explicitly Excluded** (handled by Style/Theme):
- ❌ `color`, `foreground`, `background`
- ❌ `font`, `font_size`, `font_weight`
- ❌ `align`, `vertical_align`, `style`

**Example**:
```python
# Widget definition - content only
{
  "widget_type": "Type.Display",
  "parameters": {
    "text": "Hello World"  # NO styling fields
  }
}

# Styling comes from Style.widgets["Type.Display"]
{
  "font": "primary",      # → Theme.primary_font → "Inter"
  "foreground": "primary", # → Theme.foreground_primary_color → "#1a1a1a"
  "align": "center"       # → Direct CSS → "text-align: center"
}
```

### 5. Layout Strategy (Spatial Arrangement)

**Purpose**: Defines WHERE widgets are placed (spatial grid structure).

**Contains**:
- Strategy family: "Bento", "Swiss", "Cinematic"
- Variant: "Standard", "HeroLeft", "Poster", etc.
- Slots: Dict of `role → Slot` with size classes and grid positions

**Location**: `assets/strategies/*.json`

**Example** (`assets/strategies/Bento_Standard.json`):
```json
{
  "strategy": "Bento",
  "variant": "Standard",
  "slots": {
    "cell_1": {"size_class": "S", "grid_row": "1/2", "grid_column": "1/2"},
    "cell_2": {"size_class": "S", "grid_row": "1/2", "grid_column": "2/3"},
    "cell_3": {"size_class": "S", "grid_row": "2/3", "grid_column": "1/2"}
  }
}
```

**Key Characteristics**:
- Style-agnostic: same layout works with any style
- Size constraints: Widget.min_size must be <= Slot.size_class
- Grid-based positioning using CSS Grid

## Style Resolution Process

The **LayoutEngine** is the central resolver that combines content, styling, and layout.

### Resolution Workflow

```python
# 1. Input: Widget (content)
widget = {
  "widget_type": "Type.Display",
  "parameters": {"text": "Q4 Results"}
}

# 2. Lookup: Style.widgets[widget_type]
style = styles["corp_modern_default"]
widget_style = style.widgets["Type.Display"]
# Result:
{
  "font": "primary",
  "foreground": "primary",
  "align": "center",
  "font_size": "48px"
}

# 3. Resolve: Theme tokens → CSS values
theme = themes["corp_modern"]
applied_style = {}

# Token resolution
applied_style["font-family"] = theme.primary_font + ", sans-serif"  # "Inter, sans-serif"
applied_style["color"] = theme.foreground_primary_color             # "#1a1a1a"

# Direct CSS
applied_style["text-align"] = "center"
applied_style["font-size"] = "48px"

# 4. Result: Applied Style (CSS dict)
{
  "font-family": "Inter, sans-serif",
  "color": "#1a1a1a",
  "text-align": "center",
  "font-size": "48px"
}

# 5. Template: Render with applied_style
<div style="{{ render_style(applied_style) }}">
  {{ widget.parameters.text }}
</div>

# 6. Output: Final HTML
<div style="font-family: Inter, sans-serif; color: #1a1a1a; text-align: center; font-size: 48px">
  Q4 Results
</div>
```

### Token Resolution Rules

| WidgetStyle Field | Token Value | Theme Field | CSS Property | Example Result |
|-------------------|-------------|-------------|--------------|----------------|
| `font` | "primary" | `primary_font` | `font-family` | "Inter, sans-serif" |
| `font` | "secondary" | `secondary_font` | `font-family` | "Georgia, serif" |
| `foreground` | "primary" | `foreground_primary_color` | `color` | "#1a1a1a" |
| `foreground` | "secondary" | `foreground_secondary_color` | `color` | "#666666" |
| `foreground` | "accent" | `accent_color` | `color` | "#0066cc" |
| `background` | "primary" | `background_primary_color` | `background-color` | "#ffffff" |
| `background` | "secondary" | `background_secondary_color` | `background-color` | "#f5f5f5" |
| `align` | "center" | N/A (direct CSS) | `text-align` | "center" |
| `font_size` | "48px" | N/A (direct CSS) | `font-size` | "48px" |

## Asset Management

### Discovery Process

The **AssetManager** automatically discovers assets from the file system:

```python
asset_manager = AssetManager()

# Auto-discovers from directories
themes = asset_manager.load_themes()      # assets/themes/*.json
styles = asset_manager.load_styles()      # assets/styles/*.json
strategies = asset_manager.load_strategies()  # assets/strategies/*.json
```

### CLI Commands

**List Themes**:
```bash
uce-render --list-themes
```
Output shows all available themes with their color/font tokens.

**List Styles**:
```bash
uce-render --list-styles
```
Output shows all available styles with widget styling definitions.

**List Layout Strategies**:
```bash
uce-render --list-strategies
```
Output shows all layout variants with slot configurations.

**List Widgets**:
```bash
uce-render --list-widgets
```
Output shows all widget types with their content parameter schemas.

### Creating New Assets

**Adding a New Theme**:
1. Create `assets/themes/my_theme.json`
2. Define all 9 required fields:
   - `primary_font`, `secondary_font`
   - `foreground_primary_color`, `foreground_secondary_color`
   - `background_primary_color`, `background_secondary_color`
   - `accent_color`, `error_color`, `success_color`
3. Verify: `uce-render --list-themes`

**Adding a New Style**:
1. Create `assets/styles/my_style.json`
2. Set `theme_name` to reference existing theme
3. Define `widgets` dict with WidgetStyle configurations
4. Verify: `uce-render --list-styles`
5. Use in config: `"style_name": "my_style"`

**Adding a New Widget Type**:
1. Create widget class in `src/widgets/`
2. Define content-only parameters in docstring format:
   ```python
   """
   Widget description.
   
   Parameters:
   - text (str): Display text content (required)
   - citation (str, optional): Attribution text
   """
   ```
3. Register in widget registry
4. Create template in `templates/widgets/`
5. Add styling to existing styles' `widgets` dict
6. Verify: `uce-render --list-widgets`

**Adding a New Layout Strategy**:
1. Create `assets/strategies/Family_Variant.json`
2. Define slots with size classes and grid positions
3. Verify: `uce-render --list-strategies`
4. Use in config: `"layout_strategy": "Family.Variant"`

## Benefits of This Architecture

### 1. Separation of Concerns
- **Content creators** focus on data (widgets)
- **Designers** focus on themes/styles
- **Layout designers** focus on spatial arrangement
- Each concern can evolve independently

### 2. Reusability
- One theme → many styles
- One style → many configurations
- One widget → any style/theme combination
- One layout → any style

### 3. Consistency
- Theme tokens ensure visual coherence
- All widgets using "primary" foreground get the same color
- Brand changes require only theme update

### 4. Flexibility
- Swap entire visual appearance by changing `style_name`
- No widget modifications needed for styling changes
- Easy A/B testing of visual designs

### 5. Extensibility
- Add new widgets without modifying themes
- Add new themes without changing widgets
- Add new layout strategies independently
- Add new styles by combining existing themes with new widget rules

## Migration Notes

### Old Architecture (Pre-Refactoring)
- Widgets contained styling parameters: `color`, `align`, `style`
- Templates directly used widget styling fields
- No separation between content and styling
- Hard to change visual appearance without config updates

### New Architecture (Current)
- Widgets are content-only
- Style/Theme provide all visual rules
- LayoutEngine resolves tokens to CSS
- Templates use `applied_style` dict
- Visual changes require only style/theme updates

### Key Changes
1. Widget parameters: Removed all styling fields
2. Style.widgets: Added WidgetStyle dict mapping
3. LayoutEngine: Added `_resolve_widget_style()` method
4. Templates: Changed from `widget.color` to `applied_style["color"]`
5. Configuration: Added `style_name` field, removed widget styling params
