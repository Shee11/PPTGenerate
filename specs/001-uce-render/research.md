# Research: Universal Content Engine - Rendering System

**Feature**: 001-uce-render  
**Created**: 2025-12-11  
**Purpose**: Resolve technical unknowns and document technology decisions

## Research Questions

### 1. Python HTML Rendering Strategy

**Question**: What's the best approach for generating HTML from Python layout specifications?

**Decision**: **Template-based rendering using Jinja2**

**Rationale**:
- **Jinja2** is the de facto standard for Python templating with excellent performance
- Provides separation of concerns: Python handles logic, templates handle presentation
- Supports template inheritance for layout strategies (base template + variant overrides)
- Built-in HTML escaping prevents XSS vulnerabilities
- Easy to test (templates can be unit tested with mock data)

**Alternatives considered**:
- **Direct string concatenation**: Rejected - unmaintainable, error-prone, no auto-escaping
- **dominate library**: Rejected - Python-only approach loses designer collaboration benefits
- **React/JSX via PyReact**: Rejected - adds JavaScript dependency, unnecessary complexity

### 2. Pydantic Configuration Pattern

**Question**: How should we implement the `PatchableContextPydantic` base class for Layouts and Styles collections?

**Decision**: **Pydantic BaseModel with ConfigDict and model_validate pattern**

**Rationale**:
- Pydantic v2 provides `model_validate` for partial updates (patching)
- `ConfigDict(extra='forbid')` prevents typos in configuration
- Built-in JSON schema generation for documentation
- Type validation at runtime ensures configuration correctness
- `model_dump(exclude_unset=True)` enables clean patching behavior

**Pattern**:
```python
from pydantic import BaseModel, ConfigDict

class PatchableContextPydantic(BaseModel):
    model_config = ConfigDict(extra='forbid', validate_assignment=True)
    
    def patch(self, updates: dict):
        """Apply partial updates to model"""
        data = self.model_dump()
        data.update(updates)
        return self.__class__.model_validate(data)
```

**Alternatives considered**:
- **dataclasses**: Rejected - no runtime validation, no JSON schema
- **attrs**: Rejected - less common in Python ecosystem, no built-in validation

### 3. Layout Calculation Strategy

**Question**: How should the LayoutEngine calculate widget positions for different layout strategies?

**Decision**: **Strategy Pattern with CSS Grid coordinate system**

**Rationale**:
- Each layout variant is a concrete strategy (Bento.Standard, Swiss.Poster, etc.)
- CSS Grid provides natural 2D coordinate system (row/column spans)
- Calculations use relative units (percentages, fr units) for responsiveness
- Output is coordinate dictionary: `{"role": {"grid-row": "1/3", "grid-column": "1/2"}}`
- Easy to extend with new layout variants without modifying engine core

**Output format**:
```python
{
    "main": {
        "grid_row": "1 / 3",      # Spans rows 1-2
        "grid_column": "1 / 3",   # Spans columns 1-2
        "size_class": "L"
    }
}
```

**Alternatives considered**:
- **Absolute pixel positioning**: Rejected - not responsive, breaks on different screen sizes
- **Flexbox**: Rejected - harder to achieve complex 2D layouts like Bento grids
- **Canvas coordinates**: Rejected - requires JavaScript for rendering, less accessible

### 4. Widget Registry Pattern

**Question**: How should widgets be registered and instantiated?

**Decision**: **Type-based registry with factory pattern**

**Rationale**:
- Registry maps widget type strings to widget classes (`"Type.Display"` → `TypeDisplayWidget`)
- Factory validates size constraints before instantiation
- Enables dynamic widget loading (future extensibility for custom widgets)
- Type hints ensure compile-time safety: `registry: dict[str, Type[BaseWidget]]`

**Implementation**:
```python
class WidgetRegistry:
    _widgets: dict[str, Type[BaseWidget]] = {}
    
    @classmethod
    def register(cls, widget_type: str):
        def decorator(widget_class: Type[BaseWidget]):
            cls._widgets[widget_type] = widget_class
            return widget_class
        return decorator
    
    @classmethod
    def create(cls, widget_type: str, size: SizeClass, **params) -> BaseWidget:
        widget_class = cls._widgets[widget_type]
        if size < widget_class.min_size:
            raise SizeConstraintError(...)
        return widget_class(size=size, **params)
```

**Alternatives considered**:
- **Import-based**: Rejected - requires manual imports, fragile
- **Plugin system**: Rejected - overkill for initial version

### 5. Size Class Representation

**Question**: How should T-Shirt sizes (S/M/L/XL) be represented in code?

**Decision**: **Enum with ordering support**

**Rationale**:
- Python `Enum` with `@total_ordering` enables size comparisons (`M < L`)
- Explicit mapping to numeric values for calculations (S=1, M=2, L=3, XL=4)
- Type-safe: prevents invalid size strings
- Self-documenting code: `SizeClass.MEDIUM` vs magic string `"M"`

**Implementation**:
```python
from enum import IntEnum

class SizeClass(IntEnum):
    S = 1   # Small: ~25% screen area
    M = 2   # Medium: ~40% screen area
    L = 3   # Large: ~60% screen area
    XL = 4  # Extra-Large: ~90%+ screen area
```

**Alternatives considered**:
- **String literals**: Rejected - no ordering, typo-prone
- **Integer constants**: Rejected - lose semantic meaning

### 6. CLI Framework

**Question**: What CLI framework should be used for the command-line interface?

**Decision**: **Click with JSON output support**

**Rationale**:
- **Click** is the most popular Python CLI framework (used by Flask, pip)
- Supports complex command hierarchies and option validation
- Easy to test (CliRunner for unit tests)
- Can output both human-readable and JSON formats
- Excellent error messages and help text generation

**Example**:
```bash
uce-render --layouts layouts.json --styles styles.json --output output.html
uce-render --layouts layouts.json --styles styles.json --format json  # Machine output
```

**Alternatives considered**:
- **argparse**: Rejected - more verbose, harder to test
- **typer**: Rejected - less mature, smaller ecosystem

### 7. Testing Strategy

**Question**: What testing approach aligns with TDD requirements?

**Decision**: **pytest with contract/integration/unit hierarchy**

**Rationale**:
- **Contract tests**: Validate JSON schema for Layouts/Styles/RenderableLayout
- **Integration tests**: Test full pipeline (Layout + Style → HTML output)
- **Unit tests**: Test individual components (LayoutEngine, widgets, validation)
- **Fixtures**: pytest fixtures for sample layouts, styles, and expected outputs
- **Snapshot testing**: Use pytest-regressions for HTML output verification

**Test structure**:
```
tests/
├── contract/
│   ├── test_layout_schema.py      # JSON schema validation
│   └── test_style_schema.py
├── integration/
│   ├── test_bento_rendering.py    # End-to-end layout tests
│   ├── test_swiss_rendering.py
│   └── test_cinematic_rendering.py
└── unit/
    ├── test_layout_engine.py      # Layout calculations
    ├── test_size_validation.py    # Size constraints
    └── test_widgets/              # Widget-specific tests
```

**Alternatives considered**:
- **unittest**: Rejected - more verbose, less powerful fixtures
- **nose2**: Rejected - pytest is industry standard

## Technology Stack Summary

| Category | Technology | Version | Justification |
|----------|-----------|---------|---------------|
| **Language** | Python | 3.11+ | Type hints, pattern matching, performance |
| **Validation** | Pydantic | 2.x | Runtime validation, JSON schema |
| **Templating** | Jinja2 | 3.x | Industry standard, security, testability |
| **CLI** | Click | 8.x | Robust, testable, great UX |
| **Testing** | pytest | 7.x | Fixtures, parametrization, ecosystem |
| **HTML** | Jinja2 Templates | - | Separation of concerns, designer-friendly |

## Architecture Decisions

### Module Organization

**Decision**: Separate `layout` and `render` modules with clear boundaries

**Structure**:
```
src/
├── common/
│   └── patchable_context_pydantic.py  # Base class for config collections
├── layout/
│   ├── theme.py                        # Theme configuration (fonts, colors)
│   ├── style.py                        # Style definitions (rounded, combos)
│   ├── layout_engine.py                # Position calculation
│   └── strategies/                     # Layout strategy implementations
│       ├── bento.py
│       ├── swiss.py
│       └── cinematic.py
└── render/
    ├── html_renderer.py                # HTML generation
    ├── widgets/                        # Widget implementations
    │   ├── typography.py
    │   ├── data.py
    │   ├── media.py
    │   └── charts.py
    └── templates/                      # Jinja2 templates
        ├── base.html.j2
        └── widgets/
```

**Rationale**:
- Clear separation: layout = position calculation, render = output generation
- Future extensibility: easy to add PDF/SVG renderers alongside HTML
- Testing: can test layout engine without rendering (just validate coordinates)

### Data Flow

**Decision**: Pipeline architecture with explicit stages

**Flow**:
```
Layouts + Styles → LayoutEngine → RenderableLayout → HTMLRenderer → HTML
```

**Stages**:
1. **Input**: Layouts (collection) + Styles (collection)
2. **Layout Engine**: Calculates positions, validates sizes, binds styles
3. **RenderableLayout**: Intermediate representation with all calculations done
4. **HTML Renderer**: Translates RenderableLayout to HTML using Jinja2
5. **Output**: HTML file

**Rationale**:
- Each stage has single responsibility
- Intermediate `RenderableLayout` can be inspected/tested independently
- Easy to add alternative renderers (PDF, SVG) that consume `RenderableLayout`

## Performance Considerations

### Target Performance

- **Simple layouts** (≤6 widgets): <100ms total rendering time
- **Complex layouts** (10+ widgets, charts): <500ms
- **Memory**: <50MB per render operation

### Optimization Strategies

1. **Lazy template compilation**: Compile Jinja2 templates once, reuse
2. **Widget caching**: Memoize widget HTML generation for repeated widgets
3. **Size validation early**: Fail fast before expensive rendering
4. **Minimal dependencies**: Keep HTML output small, avoid heavy JS frameworks

## Security Considerations

### Input Validation

- **Pydantic**: All inputs validated against schema (types, ranges, enums)
- **Jinja2 auto-escaping**: Prevents XSS in user-provided text
- **Size limits**: Reject configurations with >100 widgets (DoS prevention)

### Safe Defaults

- All theme colors validated as valid CSS color strings
- File paths sanitized (no directory traversal)
- External URLs validated if Media.Frame supports remote images

## Open Questions for Implementation Phase

None - all critical decisions resolved. Ready to proceed to Phase 1 design.
