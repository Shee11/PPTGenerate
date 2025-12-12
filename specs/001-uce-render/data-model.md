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

### 3. Style

Visual styling configuration combining theme with geometric properties.

**Attributes**:
- `name`: str (unique identifier, e.g., "modern_rounded")
- `theme_name`: str (reference to Theme)
- `border_radius`: str (CSS value, e.g., "8px", "0.5rem")
- `shadow_intensity`: Literal["none", "subtle", "medium", "strong"]
- `spacing_scale`: float (multiplier for gaps/padding, default 1.0)
- `transition_duration`: str (CSS duration, e.g., "200ms")

**Validation Rules**:
- `name` must be unique within Styles collection
- `theme_name` must reference an existing Theme
- `border_radius` must be valid CSS length or percentage
- `shadow_intensity` must be one of defined literals
- `spacing_scale` must be positive (> 0)

**Relationships**:
- References `Theme` via `theme_name`
- Referenced by `WidgetAssignment.style_name`
- One Style can be used by multiple WidgetAssignments

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

Base class for all renderable components.

**Attributes**:
- `widget_type`: str (e.g., "Type.Display", "Chart.Bar")
- `min_size`: SizeClass (minimum slot size required)
- `atom_id`: str | None (reference to data source, optional)
- `params`: dict[str, Any] (widget-specific parameters)

**Validation Rules**:
- `widget_type` must be registered in WidgetRegistry
- `min_size` must be a valid SizeClass
- `params` keys must match widget's parameter schema

**Relationships**:
- Subclassed by concrete widget types (Typography, Data, Media, Charts)
- Referenced by `WidgetAssignment.widget`

**Concrete Subtypes**:
- `TypographyWidget`: Display, Heading, Body, List, Quote
- `DataWidget`: BigNum, Trend, Progress
- `MediaWidget`: Frame, Code, Icon
- `ChartWidget`: Bar, Line, Pie, Radar, Sankey

---

### 7. WidgetAssignment

Binds a widget to a slot with a style.

**Attributes**:
- `role`: str (references Slot.role)
- `widget`: Widget (the widget instance)
- `style_name`: str (references Style.name)

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

Collection of Style configurations, extends PatchableContextPydantic.

**Attributes**:
- `themes`: dict[str, Theme] (theme_name → Theme mapping)
- `styles`: dict[str, Style] (style_name → Style mapping)
- `default_style_name`: str (fallback style)

**Validation Rules**:
- All `Style.theme_name` references must exist in `themes` dict
- `default_style_name` must exist in `styles` dict
- Theme names and style names must be unique

**Methods**:
- `get_style(name: str) -> Style`: Returns a style by name
- `get_theme(name: str) -> Theme`: Returns a theme by name
- `patch(updates: dict)`: Apply partial updates

**Relationships**:
- Contains multiple `Theme` and `Style` instances
- Passed to LayoutEngine for rendering

---

### 10. RenderableLayout

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
Layouts (Collection)
  └── contains many → Layout
                        └── owns many → Slot
                                          ↑
                                          | references
                                          |
                        WidgetAssignment ─┘
                          ├── references → Style ──→ references → Theme
                          └── owns → Widget (abstract)
                                      ├── TypographyWidget
                                      ├── DataWidget
                                      ├── MediaWidget
                                      └── ChartWidget

Styles (Collection)
  ├── contains many → Theme
  └── contains many → Style

LayoutEngine (processor)
  ├── input: Layouts + Styles
  └── output: RenderableLayout
                ├── references → Layout
                ├── contains → WidgetAssignment[]
                └── contains → resolved_styles

HTMLRenderer (processor)
  ├── input: RenderableLayout
  └── output: HTML string
```

## Validation Rules Summary

### Cross-Entity Constraints

1. **Size Constraint**: `Widget.min_size <= Slot.size_class` (enforced by WidgetAssignment)
2. **Reference Integrity**: All style_name, theme_name, role references must exist
3. **Uniqueness**: Slot roles unique within Layout, Style names unique within Styles
4. **Active References**: active_layout_id and default_style_name must point to existing items

### Immutability Patterns

- **Layouts and Styles**: Use `patch()` method for updates (creates new instance)
- **RenderableLayout**: Immutable once created
- **Widget**: Immutable after instantiation (params frozen)

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
