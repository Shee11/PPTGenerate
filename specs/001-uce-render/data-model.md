# Data Model: Universal Content Engine - Rendering System

**Feature**: 001-uce-render  
**Created**: 2025-12-11  
**Purpose**: Define all entities, their attributes, relationships, and validation rules

## Core Entities

### 1. SizeClass (Enum)

Represents T-Shirt sizing for slots and widget constraints.

**Attributes**:
- `S` (Small): Integer value 1
- `M` (Medium): Integer value 2
- `L` (Large): Integer value 3
- `XL` (Extra-Large): Integer value 4

**Validation Rules**:
- Must be one of the four defined values
- Supports ordering comparisons (e.g., `S < M`)

**Relationships**:
- Referenced by `Slot.size_class`
- Referenced by `Widget.min_size`

---

### 2. Theme

Color and typography configuration for visual consistency.

**Attributes**:
- `primary_font`: str (e.g., "Inter", "SF Pro Display")
- `secondary_font`: str (e.g., "Georgia", "Menlo")
- `foreground_primary_color`: str (CSS color, e.g., "#1a1a1a")
- `foreground_secondary_color`: str (CSS color, e.g., "#666666")
- `background_primary_color`: str (CSS color, e.g., "#ffffff")
- `background_secondary_color`: str (CSS color, e.g., "#f5f5f5")
- `accent_color`: str (CSS color, e.g., "#0066cc")
- `error_color`: str (CSS color, e.g., "#dc3545")
- `success_color`: str (CSS color, e.g., "#28a745")

**Validation Rules**:
- All color values must be valid CSS colors (hex, rgb, named)
- Font names must be non-empty strings
- All fields are required (no optional theme values)

**Relationships**:
- Referenced by `Style.theme_name` (string reference)
- Multiple Styles can reference the same Theme

---

### 3. WidgetStyle

Optional styling configuration for individual widget types within a Style.

**Attributes**:
- `font`: Literal["primary", "secondary"] | None (references Theme font)
- `font_size`: str | None (CSS font-size, e.g., "16px", "1.5rem")
- `font_weight`: int | None (100-900, e.g., 400, 700)
- `line_height`: float | None (unitless multiplier, e.g., 1.5)
- `align`: Literal["left", "center", "right", "justify"] | None (horizontal text alignment)
- `vertical_align`: Literal["top", "middle", "bottom"] | None (vertical alignment)
- `foreground`: Literal["primary", "secondary", "accent", "error", "success"] | None (references Theme color)
- `background`: Literal["primary", "secondary"] | None (references Theme background color)
- `border_radius`: str | None (CSS value, e.g., "4px", "0.5rem")

**Validation Rules**:
- All fields are optional (None allowed)
- `font` must reference "primary" or "secondary" from Theme
- `font_size` and `border_radius` must be valid CSS length values
- `font_weight` must be in range 100-900
- `line_height` must be positive (> 0)
- Color references ("primary", "secondary", etc.) must exist in Theme

**Relationships**:
- Nested within `Style.widgets` dict (widget_type → WidgetStyle mapping)
- References `Theme` colors and fonts via string tokens
- Resolved to CSS by LayoutEngine

**Resolution Example**:
```python
# Style definition
style = Style(
    theme_name="corp_modern",
    widgets={
        "Type.Display": WidgetStyle(
            font="primary",
            foreground="primary",
            align="center"
        )
    }
)

# Theme definition
theme = Theme(
    primary_font="Inter",
    foreground_primary_color="#1a1a1a"
)

# LayoutEngine resolves to CSS
applied_style = {
    "font-family": "Inter, sans-serif",
    "color": "#1a1a1a",
    "text-align": "center"
}
```

---

### 4. Style

Visual styling configuration combining theme with widget-specific styling rules.

**Attributes**:
- `name`: str (unique identifier, e.g., "corp_modern_default")
- `theme_name`: str (reference to Theme)
- `widgets`: dict[str, WidgetStyle] (widget_type → WidgetStyle mapping, e.g., {"Type.Display": WidgetStyle(...)})

**Validation Rules**:
- `name` must be unique within Styles collection
- `theme_name` must reference an existing Theme
- `widgets` dict keys must be valid widget type strings (e.g., "Type.Display", "Chart.Bar")
- All WidgetStyle instances must use valid theme token references

**Relationships**:
- References `Theme` via `theme_name`
- Contains multiple `WidgetStyle` instances in `widgets` dict
- Referenced by widget assignments in configuration
- One Style can be used by multiple widget instances

**Style Resolution Process**:
1. Widget requests styling for its type (e.g., "Type.Display")
2. LayoutEngine looks up `style.widgets["Type.Display"]`
3. WidgetStyle contains tokens like `font="primary"`, `foreground="primary"`
4. LayoutEngine resolves tokens using `theme.primary_font`, `theme.foreground_primary_color`
5. Returns CSS dict: `{"font-family": "Inter", "color": "#1a1a1a"}`
6. Template applies CSS to widget HTML

**Example**:
```python
style = Style(
    name="corp_modern_default",
    theme_name="corp_modern",
    widgets={
        "Type.Display": WidgetStyle(font="primary", font_size="48px", align="center"),
        "Type.Body": WidgetStyle(font="secondary", font_size="16px", line_height=1.6),
        "Chart.Bar": WidgetStyle(foreground="accent", background="secondary")
    }
)
```

---

### 4. Slot

A positioned region within a layout that can contain a widget.

**Attributes**:
- `role`: str (unique within layout, e.g., "main", "sidebar", "cell_1")
- `size_class`: SizeClass (S/M/L/XL)
- `grid_row`: str (CSS Grid syntax, e.g., "1 / 3")
- `grid_column`: str (CSS Grid syntax, e.g., "1 / 2")

**Validation Rules**:
- `role` must be unique within a Layout
- `size_class` must be a valid SizeClass enum value
- `grid_row` and `grid_column` must be valid CSS Grid line syntax

**Relationships**:
- Owned by `Layout` (composition)
- Referenced by `WidgetAssignment.role`
- One-to-one with WidgetAssignment (each slot can have max one widget)

---

### 5. Layout

Defines the spatial division of screen into slots.

**Attributes**:
- `strategy`: Literal["Bento", "Swiss", "Cinematic"]
- `variant`: str (e.g., "Standard", "HeroLeft", "Poster")
- `gap`: str (CSS gap value, e.g., "20px", "1rem")
- `padding`: str (CSS padding value, e.g., "40px", "2rem")
- `background`: str (CSS background, e.g., "#f0f0f0", "url(...)")
- `slots`: dict[str, Slot] (role → Slot mapping)

**Validation Rules**:
- `strategy` must be one of three defined strategies
- `variant` must be valid for the chosen strategy (e.g., "Poster" only valid for "Swiss")
- `gap` and `padding` must be valid CSS length values
- `slots` dict must not be empty
- All slot roles in `slots` dict must match slot.role attribute

**Relationships**:
- Owns multiple `Slot` instances (composition)
- Part of `Layouts` collection
- Referenced by `RenderableLayout.layout`

**State Transitions**:
- Immutable after creation (use PatchableContextPydantic.patch for updates)

---

### 6. Widget (Abstract Base)

Base class for all renderable content components. Widgets are **content-only** and do NOT contain styling information.

**Attributes**:
- `widget_type`: str (e.g., "Type.Display", "Chart.Bar")
- `min_size`: SizeClass (minimum slot size required)
- `atom_id`: str | None (reference to data source, optional)
- `parameters`: dict[str, Any] (widget-specific content parameters, NO styling)

**Content-Only Parameters**:
Widget parameters define WHAT to display, not HOW to style it:
- **Typography widgets**: `text` (str), `citation` (str)
- **Data widgets**: `number` (float), `label` (str), `trend` (str)
- **Chart widgets**: `categories` (list), `series` (list), `show_values` (bool)
- **Media widgets**: `src` (str), `alt` (str), `fit` (str)

**Styling Exclusions** (handled by Style/Theme):
- NO `color`, `foreground`, `background` parameters
- NO `font`, `font_size`, `font_weight` parameters
- NO `align`, `vertical_align`, `style` parameters
- All visual styling comes from Style.widgets[widget_type]

**Validation Rules**:
- `widget_type` must be registered in WidgetRegistry
- `min_size` must be a valid SizeClass
- `parameters` keys must match widget's content parameter schema
- `parameters` must NOT contain styling fields (enforced by widget class)

**Relationships**:
- Subclassed by concrete widget types (Typography, Data, Media, Charts)
- Styled by `Style.widgets[widget_type]` (external styling)
- Theme tokens resolved by LayoutEngine

**Concrete Subtypes**:
- `TypeWidget`: Display, Heading, Body, List, Quote (5 types)
- `DataWidget`: BigNum, Trend, Progress (3 types)
- `MediaWidget`: Frame, Code, Icon (planned)
- `ChartWidget`: Bar, Line, Pie, Radar, Sankey (planned)

**Example - Content vs Styling Separation**:
```python
# Widget defines content only
widget = TypeWidget(
    widget_type="Type.Display",
    parameters={"text": "Hello World"}  # NO color, font, align
)

# Style defines visual appearance
style = Style(
    theme_name="corp_modern",
    widgets={
        "Type.Display": WidgetStyle(
            font="primary",           # From theme.primary_font
            foreground="primary",     # From theme.foreground_primary_color
            align="center",          # Layout alignment
            font_size="48px"         # Typography sizing
        )
    }
)

# LayoutEngine combines them
applied_style = engine._resolve_widget_style(widget, style, theme)
# Result: {"font-family": "Inter", "color": "#1a1a1a", "text-align": "center", "font-size": "48px"}
```

---

### 7. WidgetAssignment

Binds a widget to a slot (deprecated in new configuration format, kept for reference).

**Note**: In the current implementation, widget assignments are defined directly in the configuration JSON under `slides[].widgets[]` with `role`, `widget_type`, and `parameters` fields. Style is specified at the slide level via `style_name`.

**Conceptual Attributes** (for understanding):
- `role`: str (references Slot.role)
- `widget`: Widget (the widget instance)
- `style_name`: str (references Style.name, now at slide level)

**Validation Rules**:
- `role` must exist in the Layout's slots
- `widget.min_size` must be <= slot's `size_class`
- `style_name` must reference an existing Style

**Relationships**:
- References `Slot` via `role`
- References `Style` via `style_name`
- Owns `Widget` instance (composition)

---

### 8. Layouts (Collection)

Collection of Layout configurations, extends PatchableContextPydantic.

**Attributes**:
- `layouts`: dict[str, Layout] (layout_id → Layout mapping)
- `active_layout_id`: str (currently selected layout)

**Validation Rules**:
- `layouts` dict must not be empty
- `active_layout_id` must exist in `layouts` dict
- All layout IDs must be unique

**Methods**:
- `get_active() -> Layout`: Returns the active layout
- `patch(updates: dict)`: Apply partial updates to layouts

**Relationships**:
- Contains multiple `Layout` instances
- Passed to LayoutEngine for rendering

---

### 9. Styles (Collection)

Collection of Style and Theme configurations for the rendering system.

**Attributes**:
- `themes`: dict[str, Theme] (theme_name → Theme mapping)
- `styles`: dict[str, Style] (style_name → Style mapping)

**Validation Rules**:
- All `Style.theme_name` references must exist in `themes` dict
- Theme names and style names must be unique
- At least one theme and one style must exist

**Methods**:
- `get_style(name: str) -> Style`: Returns a style by name
- `get_theme(name: str) -> Theme`: Returns a theme by name

**Relationships**:
- Contains multiple `Theme` and `Style` instances
- Passed to LayoutEngine for rendering
- Styles reference Themes via `theme_name` field

**Asset Loading**:
- Themes loaded from `assets/themes/*.json`
- Styles loaded from `assets/styles/*.json`
- AssetManager provides `--list-themes` and `--list-styles` CLI commands
- Each style file must reference an existing theme

**Creating New Themes**:
1. Create JSON file in `assets/themes/` directory
2. Define all required color and typography tokens:
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
3. Theme is automatically discovered by AssetManager
4. Use `uce-render --list-themes` to verify

**Creating New Styles**:
1. Create JSON file in `assets/styles/` directory
2. Reference existing theme and define widget styling rules:
   ```json
   {
     "name": "my_custom_style",
     "theme_name": "corp_modern",
     "widgets": {
       "Type.Display": {
         "font": "primary",
         "font_size": "48px",
         "align": "center",
         "foreground": "primary"
       },
       "Type.Body": {
         "font": "secondary",
         "font_size": "16px",
         "line_height": 1.6,
         "foreground": "secondary"
       }
     }
   }
   ```
3. Style is automatically discovered by AssetManager
4. Use `uce-render --list-styles` to verify
5. Reference in configuration via `style_name: "my_custom_style"`

---

### 10. LayoutEngine

Core processor that resolves styling and prepares widgets for rendering.

**Purpose**: Bridge between content (widgets), styling (themes/styles), and layout (strategies/slots). Converts theme tokens into concrete CSS properties.

**Key Responsibilities**:
1. **Style Resolution**: Converts theme tokens to CSS values
2. **Size Validation**: Ensures widgets fit in assigned slots
3. **Widget Preparation**: Combines content + styling for templates

**Critical Method - `_resolve_widget_style()`**:
```python
def _resolve_widget_style(
    self,
    widget: Widget,
    style: Style,
    theme: Theme
) -> dict[str, str]:
    """
    Resolves theme tokens to CSS properties for a widget.
    
    Process:
    1. Look up style.widgets[widget.widget_type]
    2. Get WidgetStyle with tokens (font="primary", foreground="accent")
    3. Resolve tokens using theme (primary_font="Inter", accent_color="#0066cc")
    4. Return CSS dict: {"font-family": "Inter", "color": "#0066cc"}
    """
```

**Token Resolution Examples**:
- `font="primary"` → `theme.primary_font` → `"font-family": "Inter, sans-serif"`
- `foreground="accent"` → `theme.accent_color` → `"color": "#0066cc"`
- `background="secondary"` → `theme.background_secondary_color` → `"background-color": "#f5f5f5"`
- `align="center"` → `"text-align": "center"` (direct CSS, no token)

**Workflow**:
```python
# 1. Load assets
themes, styles = asset_manager.load_all()
layout_strategy = asset_manager.get_strategy("Bento.Standard")

# 2. Configuration specifies content
config = {
    "style_name": "corp_modern_default",
    "widgets": [
        {"role": "main", "widget_type": "Type.Display", "parameters": {"text": "Hello"}}
    ]
}

# 3. LayoutEngine resolves styling
engine = LayoutEngine()
theme = themes[styles[config["style_name"]].theme_name]
style = styles[config["style_name"]]
widget_style = style.widgets.get("Type.Display")
applied_style = engine._resolve_widget_style(widget, style, theme)

# 4. Template receives applied_style
# Result: <div style="font-family: Inter; color: #1a1a1a; text-align: center">Hello</div>
```

**Relationships**:
- Input: Widgets (content), Styles (styling rules), Themes (design tokens)
- Output: Applied styles (CSS dicts) for templates
- Used by: HTMLRenderer to inject styles into templates

---

### 11. RenderableLayout (Deprecated)

Intermediate representation after layout calculation, ready for rendering.

**Attributes**:
- `layout`: Layout (original layout definition)
- `widget_assignments`: list[WidgetAssignment] (all widgets with positions)
- `resolved_styles`: dict[str, dict] (style_name → CSS properties dict)
- `metadata`: dict[str, Any] (rendering metadata, timestamps, etc.)

**Validation Rules**:
- `widget_assignments` must not violate size constraints
- All `resolved_styles` keys must match styles used in widget_assignments
- Each widget_assignment.role must exist in layout.slots

**Relationships**:
- References `Layout` (the source layout)
- Contains multiple `WidgetAssignment` instances
- Output of LayoutEngine, input to HTMLRenderer

**State Transitions**:
- Created by LayoutEngine
- Consumed by HTMLRenderer (immutable during rendering)

---

## Entity Relationships Diagram

```
Asset Management (File-based Discovery)
  ├── assets/themes/*.json ──→ Theme (design tokens)
  ├── assets/styles/*.json ──→ Style (widget styling rules)
  └── assets/strategies/*.json ─→ LayoutStrategy (slot definitions)

Configuration (JSON Input)
  ├── style_name (references Style)
  ├── layout_strategy (references LayoutStrategy)
  └── slides[]
        ├── widgets[]
        │     ├── role (references Slot in LayoutStrategy)
        │     ├── widget_type (e.g., "Type.Display")
        │     └── parameters (content only, NO styling)
        └── style_name (optional override)

Resolution Flow (LayoutEngine)
  ┌─────────────────────────────────────────────────────────┐
  │  1. Widget provides: widget_type + content parameters   │
  │  2. Style provides: widgets[widget_type] → WidgetStyle  │
  │  3. WidgetStyle has: tokens (font="primary", fg="accent")│
  │  4. Theme provides: token values (primary_font="Inter") │
  │  5. Engine resolves: tokens → CSS ({"font-family": ...})│
  │  6. Template receives: applied_style dict               │
  └─────────────────────────────────────────────────────────┘

Data Model Relationships
  Theme (design tokens)
    ↑
    | referenced by theme_name
    |
  Style (widget styling rules)
    ├── widgets: dict[widget_type, WidgetStyle]
    │     └── WidgetStyle (token-based styling)
    │           ├── font: "primary" | "secondary"
    │           ├── foreground: "primary" | "secondary" | "accent"
    │           ├── background: "primary" | "secondary"
    │           ├── align, font_size, line_height, etc.
    │           └── resolved by LayoutEngine → CSS dict
    │
  Widget (content only)
    ├── widget_type: str (e.g., "Type.Display")
    ├── parameters: dict (content only)
    │     ├── Type widgets: text, citation
    │     ├── Data widgets: number, label, trend
    │     └── Chart widgets: categories, series, show_values
    └── NO styling fields (color, font, align, etc.)

  LayoutStrategy (spatial arrangement)
    └── slots: dict[role, Slot]
          ├── size_class: S | M | L | XL
          └── grid_row, grid_column (CSS Grid)

Rendering Pipeline
  Configuration JSON
    ↓
  1. Load Theme (from assets/themes/)
  2. Load Style (from assets/styles/, references Theme)
  3. Load LayoutStrategy (from assets/strategies/)
  4. Validate: Widget.min_size <= Slot.size_class
    ↓
  LayoutEngine._resolve_widget_style()
    - Input: Widget (content), Style (rules), Theme (tokens)
    - Process: style.widgets[widget_type] → resolve tokens → CSS
    - Output: applied_style dict
    ↓
  Template Rendering (Jinja2)
    - {{ render_style(applied_style) }} → inline CSS
    - {{ widget.parameters.text }} → content
    ↓
  HTML Output
```

## Validation Rules Summary

### Cross-Entity Constraints

1. **Size Constraint**: `Widget.min_size <= Slot.size_class` (enforced during configuration validation)
2. **Reference Integrity**: 
   - `Style.theme_name` must exist in available themes
   - `config.style_name` must exist in available styles
   - `widget.role` must exist in LayoutStrategy.slots
   - `style.widgets` keys must be valid widget types
3. **Token Validity**: All WidgetStyle token references (font="primary", foreground="accent") must exist in referenced Theme
4. **Content Parameters**: Widget parameters must NOT include styling fields (color, font, align, etc.)

### Separation of Concerns

- **Widgets**: Content ONLY (text, numbers, data structures)
- **Styles**: Visual rules ONLY (how widgets look)
- **Themes**: Design tokens ONLY (color palette, typography)
- **Layouts**: Spatial arrangement ONLY (where widgets go)
- **LayoutEngine**: Resolution bridge (tokens → CSS)

### Immutability Patterns

- **Theme/Style/LayoutStrategy**: Loaded from JSON files, immutable at runtime
- **Widget**: Parameters frozen after instantiation
- **Applied Styles**: Computed once per widget, cached during rendering

## Example Data Flow

```python
# Input collections
layouts = Layouts(
    layouts={
        "hero": Layout(strategy="Bento", variant="HeroLeft", ...)
    },
    active_layout_id="hero"
)

styles = Styles(
    themes={"dark": Theme(primary_font="Inter", ...)},
    styles={"modern": Style(theme_name="dark", border_radius="8px", ...)},
    default_style_name="modern"
)

# Layout engine processes
engine = LayoutEngine()
renderable = engine.calculate(layouts, styles)

# Renderable layout contains
# - Validated widget assignments
# - Calculated positions (grid coordinates)
# - Resolved CSS styles

# HTML renderer generates output
renderer = HTMLRenderer()
html = renderer.render(renderable)
```
