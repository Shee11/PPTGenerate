# Python API Contract: Layout Engine

**Version**: 1.0.0  
**Purpose**: Define the programmatic interface for layout calculation and rendering

## Module: `src.layout.layout_engine`

### Class: `LayoutEngine`

Core engine for calculating widget positions and validating constraints.

#### Method: `calculate`

Calculates positions for all widgets in a layout, validates size constraints, and produces a RenderableLayout.

**Signature**:
```python
def calculate(
    self,
    layouts: Layouts,
    styles: Styles,
    *,
    layout_id: str | None = None
) -> RenderableLayout
```

**Parameters**:
- `layouts` (Layouts): Collection of layout configurations
- `styles` (Styles): Collection of style and theme configurations
- `layout_id` (str | None): Specific layout to render. If None, uses `layouts.active_layout_id`

**Returns**:
- `RenderableLayout`: Calculated layout ready for rendering

**Raises**:
- `SizeConstraintError`: Widget minimum size exceeds slot size
- `MissingReferenceError`: Referenced style, theme, or slot not found
- `ValidationError`: Pydantic validation error in input data

**Example**:
```python
from src.layout.layout_engine import LayoutEngine
from src.common.patchable_context_pydantic import Layouts, Styles

layouts = Layouts.model_validate_json(layouts_json)
styles = Styles.model_validate_json(styles_json)

engine = LayoutEngine()
renderable = engine.calculate(layouts, styles)

# Access calculated data
for assignment in renderable.widget_assignments:
    print(f"{assignment.role}: {assignment.widget.widget_type}")
```

**Contract Tests**:
```python
# Test: Valid configuration succeeds
def test_calculate_valid_layout():
    engine = LayoutEngine()
    renderable = engine.calculate(valid_layouts, valid_styles)
    assert renderable.layout.strategy == "Bento"
    assert len(renderable.widget_assignments) > 0

# Test: Size violation detected
def test_calculate_size_violation():
    with pytest.raises(SizeConstraintError) as exc:
        engine.calculate(invalid_size_layouts, valid_styles)
    assert "Chart.Sankey" in str(exc.value)
    assert "requires XL" in str(exc.value)

# Test: Missing style reference
def test_calculate_missing_style():
    with pytest.raises(MissingReferenceError) as exc:
        engine.calculate(missing_style_layouts, valid_styles)
    assert "modern_dark" in str(exc.value)
```

---

## Module: `src.render.html_renderer`

### Class: `HTMLRenderer`

Converts RenderableLayout to HTML using Jinja2 templates.

#### Method: `render`

Generates HTML from a RenderableLayout.

**Signature**:
```python
def render(
    self,
    renderable: RenderableLayout,
    *,
    minify: bool = False
) -> str
```

**Parameters**:
- `renderable` (RenderableLayout): Calculated layout from LayoutEngine
- `minify` (bool): Whether to minify HTML output (remove whitespace)

**Returns**:
- `str`: Complete HTML document as a string

**Raises**:
- `TemplateError`: Jinja2 template rendering error
- `WidgetRenderError`: Widget-specific rendering error

**Example**:
```python
from src.render.html_renderer import HTMLRenderer

renderer = HTMLRenderer()
html = renderer.render(renderable, minify=True)

# Write to file
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html)
```

**Contract Tests**:
```python
# Test: HTML output is valid
def test_render_valid_html():
    renderer = HTMLRenderer()
    html = renderer.render(valid_renderable)
    assert html.startswith("<!DOCTYPE html>")
    assert "</html>" in html

# Test: All widgets rendered
def test_render_all_widgets():
    html = renderer.render(renderable_with_6_widgets)
    for assignment in renderable_with_6_widgets.widget_assignments:
        assert assignment.role in html

# Test: Styles applied
def test_render_styles_applied():
    html = renderer.render(renderable_with_modern_style)
    assert "border-radius: 8px" in html or "border-radius:8px" in html
```

---

## Module: `src.common.patchable_context_pydantic`

### Class: `PatchableContextPydantic` (Base)

Base class for Layouts and Styles collections, supporting partial updates.

#### Method: `patch`

Apply partial updates to the collection.

**Signature**:
```python
def patch(self, updates: dict[str, Any]) -> Self
```

**Parameters**:
- `updates` (dict): Partial updates to apply (nested dict structure)

**Returns**:
- `Self`: New instance with updates applied (original unchanged)

**Raises**:
- `ValidationError`: If updates violate schema

**Example**:
```python
# Update a single layout's gap
updated_layouts = layouts.patch({
    "layouts": {
        "hero": {
            "gap": "30px"
        }
    }
})

# Original unchanged
assert layouts.layouts["hero"].gap == "20px"
assert updated_layouts.layouts["hero"].gap == "30px"
```

**Contract Tests**:
```python
# Test: Partial update works
def test_patch_partial_update():
    original = Layouts.model_validate(base_data)
    updated = original.patch({"active_layout_id": "minimal"})
    assert updated.active_layout_id == "minimal"
    assert original.active_layout_id == "hero"  # Unchanged

# Test: Invalid update rejected
def test_patch_invalid_update():
    with pytest.raises(ValidationError):
        layouts.patch({"active_layout_id": "nonexistent"})
```

---

## Module: `src.layout.strategies`

### Strategy Classes

Each layout strategy variant is a strategy class.

#### Interface: `LayoutStrategy` (Protocol)

**Methods**:
```python
def get_slots(self) -> dict[str, Slot]:
    """Return slot definitions for this layout variant"""
    ...

def get_grid_template(self) -> tuple[str, str]:
    """Return (grid_template_rows, grid_template_columns) CSS values"""
    ...
```

#### Example: `BentoStandardStrategy`

```python
class BentoStandardStrategy:
    def get_slots(self) -> dict[str, Slot]:
        return {
            "cell_1": Slot(role="cell_1", size_class=SizeClass.S, 
                          grid_row="1 / 2", grid_column="1 / 2"),
            "cell_2": Slot(role="cell_2", size_class=SizeClass.S,
                          grid_row="1 / 2", grid_column="2 / 3"),
            # ... cells 3-6
        }
    
    def get_grid_template(self) -> tuple[str, str]:
        return ("1fr 1fr", "1fr 1fr 1fr")  # 2 rows, 3 columns
```

**Contract Test**:
```python
def test_bento_standard_slots():
    strategy = BentoStandardStrategy()
    slots = strategy.get_slots()
    assert len(slots) == 6
    assert all(slot.size_class == SizeClass.S for slot in slots.values())
```

---

## Module: `src.widgets`

### Widget Base Class

All widgets inherit from `BaseWidget`.

#### Method: `validate_params`

Validates widget-specific parameters.

**Signature**:
```python
@classmethod
def validate_params(cls, params: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize widget parameters"""
    ...
```

**Raises**:
- `ValidationError`: Invalid parameter value or missing required parameter

#### Method: `render_html`

Renders widget to HTML fragment.

**Signature**:
```python
def render_html(
    self,
    style: dict[str, str],
    *,
    atom_data: dict[str, Any] | None = None
) -> str:
    """Render widget to HTML using its template"""
    ...
```

**Parameters**:
- `style` (dict): Resolved CSS properties from Style
- `atom_data` (dict | None): Data payload for the widget (charts, dynamic content)

**Returns**:
- `str`: HTML fragment (not a complete document)

**Example**:
```python
from src.widgets.typography import TypeDisplayWidget

widget = TypeDisplayWidget(
    widget_type="Type.Display",
    min_size=SizeClass.L,
    params={"style": "bold", "align": "center"}
)

html = widget.render_html(
    style={"border-radius": "8px", "color": "#1a1a1a"},
    atom_data={"text": "Welcome to UCE"}
)
```

**Contract Tests**:
```python
# Test: Widget validates params
def test_widget_validates_params():
    with pytest.raises(ValidationError):
        TypeDisplayWidget(
            widget_type="Type.Display",
            params={"invalid_param": "value"}
        )

# Test: Widget renders HTML
def test_widget_renders_html():
    widget = DataBigNumWidget(min_size=SizeClass.S, params={})
    html = widget.render_html(
        style={},
        atom_data={"number": 12345, "label": "Revenue"}
    )
    assert "12345" in html
    assert "Revenue" in html
```

---

## Error Classes

All custom exceptions with their contracts.

### `SizeConstraintError`

Raised when widget minimum size exceeds slot size.

**Attributes**:
- `widget_type` (str): The widget type that violated constraint
- `required_size` (SizeClass): Minimum size required
- `provided_size` (SizeClass): Size of the assigned slot
- `slot_role` (str): Role of the slot

**Message Format**:
```
Widget "{widget_type}" requires size {required_size} but assigned to slot "{slot_role}" with size {provided_size}
```

### `MissingReferenceError`

Raised when a referenced entity (style, theme, slot) doesn't exist.

**Attributes**:
- `reference_type` (str): Type of reference (e.g., "style", "theme", "slot")
- `reference_name` (str): Name that was referenced
- `available_names` (list[str]): Available valid names

**Message Format**:
```
{reference_type} "{reference_name}" not found. Available: {available_names}
```

### `WidgetRenderError`

Raised during widget HTML rendering.

**Attributes**:
- `widget_type` (str): Widget that failed to render
- `cause` (Exception): Original exception

**Message Format**:
```
Failed to render widget "{widget_type}": {cause}
```

---

## Type Definitions

### `SizeClass` Enum

```python
from enum import IntEnum

class SizeClass(IntEnum):
    S = 1
    M = 2
    L = 3
    XL = 4
```

**Usage**:
```python
assert SizeClass.M < SizeClass.L  # True
assert SizeClass.S >= SizeClass.XL  # False
```

---

## Contract Test Coverage Requirements

Each public API must have:

1. **Happy path test**: Valid inputs produce expected outputs
2. **Validation test**: Invalid inputs raise appropriate exceptions
3. **Edge case tests**: Boundary conditions (empty collections, max sizes, etc.)
4. **Integration test**: End-to-end flow through multiple components

**Minimum Coverage**: 90% line coverage for all modules
