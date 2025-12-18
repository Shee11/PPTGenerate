# Contract: SlidevLayoutEngine

**Interface**: `LayoutEngine` protocol  
**Implementation**: `src/layout/slidev/layout_engine.py`  
**Purpose**: Provide Slidev-specific layout documentation for LLM content generation

## Protocol Compliance

Must implement all methods defined in `src/layout/layout_engine_protocol.py`:

### Required Methods

#### 1. `get_layout_documentation() -> str` (classmethod)

**Contract**: Return complete formatted documentation describing Slidev layouts, slot structures, widget-to-component mappings, and theme options.

**Input**: None (classmethod)

**Output**: String (formatted markdown or plain text)

**Requirements**:
- ✅ FR-002: Describe available layouts (Smart Grid, Hero Split, Full Bleed) with slot names
- ✅ FR-003: List widget type → Vue component mappings
- ✅ FR-004: Specify supported themes (business, cyber) with visual descriptions

**Example Output Format**:

```
SLIDEV LAYOUT SYSTEM

Available Layouts:

1. Smart Grid (layout: "smart-grid")
   - Dynamic column-based layout supporting 2-4 columns
   - Slot names: 'header' (full-width), 'col1', 'col2', 'col3', 'col4'
   - Parameters: cols (integer, range 2-4)
   - Best for: Multi-column content, data dashboards, comparison views

2. Hero Split (layout: "hero-split")
   - Two-panel layout with left/right content areas
   - Slot names: 'left', 'right'
   - Parameters: ratio (string, e.g., "60-40", "50-50")
   - Best for: Featured content, before/after, visual storytelling

3. Full Bleed (layout: "full-bleed")
   - Single full-screen content area
   - Slot names: default (unnamed slot)
   - Parameters: align (vertical alignment: top/center/bottom)
   - Best for: Hero slides, large images, title slides

Widget-to-Component Mappings:

Typography Widgets (render as markdown):
- Type.Display → Plain text with markdown formatting
- Type.Heading → # Heading (level 1-3)
- Type.Body → Paragraph text
- Type.List → - Bulleted list
- Type.Quote → > Blockquote
- Type.Code → ```language\ncode\n```

Data Widgets (render as Vue components):
- Data.BigNum → <MetricCard label="..." value="..." variant="primary|success|danger" />
- Data.Progress → <ProgressBar label="..." :value="number" status="success|warning|error" />
- Data.Trend → <StatusBadge status="..." text="..." />

Supported Themes:

1. Business Theme (theme: "business")
   - Colors: White background (#ffffff), Blue primary (#2563eb)
   - Typography: Inter font family, clean sans-serif
   - Visual style: Professional, minimal shadows, rounded corners
   - Use for: Corporate presentations, reports, formal content

2. Cyber Theme (theme: "cyber")
   - Colors: Dark background (#050505), Neon green primary (#00ffa3)
   - Typography: Orbitron monospace, tech aesthetic
   - Visual style: Grid overlay, glow effects, sharp edges
   - Use for: Tech presentations, developer content, futuristic themes
```

**Test Contract**:
- Output string length > 500 characters (comprehensive)
- Contains all 3 layout names ("smart-grid", "hero-split", "full-bleed")
- Contains all widget type prefixes ("Type.", "Data.")
- Contains both theme names ("business", "cyber")
- Describes slot names for each layout

---

#### 2. `calculate(cls, slides: Slides, theme: Theme, style: Style) -> List[RenderableLayout]` (classmethod)

**Contract**: Process slides and return renderable layouts (NOT IMPLEMENTED for Slidev engine - renderer bypasses this)

**Behavior**: Raise `NotImplementedError` with message: "Slidev engine does not use calculate() - use SlidevRenderer directly"

**Rationale**: Slidev engine is render-only; content generation produces JSON that SlidevRenderer translates to markdown. No layout calculation phase needed.

**Test Contract**:
- Calling this method raises `NotImplementedError`
- Error message indicates Slidev engine usage pattern

---

## Registration Contract

Must register with `LayoutEngineRegistry` on module import:

```python
# In src/layout/slidev/__init__.py
from src.layout.engine_registry import LayoutEngineRegistry
from src.layout.slidev.layout_engine import SlidevLayoutEngine

LayoutEngineRegistry.register("slidev", SlidevLayoutEngine)
```

**Requirements**:
- ✅ FR-005: Register under name `"slidev"`
- Engine accessible via `LayoutEngineRegistry.get_engine("slidev")`
- Engine switchable at runtime via registry

**Test Contract**:
- After import, `LayoutEngineRegistry.list_engines()` includes `"slidev"`
- `LayoutEngineRegistry.get_engine("slidev")` returns `SlidevLayoutEngine` class
- Engine name stored correctly in registry

---

## Usage Contract

### Content Generation Integration

```python
from src.layout.engine_registry import LayoutEngineRegistry

# In src/generation/content/generator.py
engine = LayoutEngineRegistry.get_engine("slidev")  # or from env var
layout_docs = engine.get_layout_documentation()

# Inject into LLM prompt
prompt = f"""
Generate slide content using the following layout system:

{layout_docs}

User request: {user_request}
"""
```

**Contract**:
- Documentation used verbatim in prompts (no post-processing)
- LLM generates JSON with layout names, slot names, widget types from docs
- JSON structure matches data-model.md schema

---

## Acceptance Criteria

- [ ] Implements `LayoutEngine` protocol (passes `isinstance(SlidevLayoutEngine, LayoutEngine)` check)
- [ ] `get_layout_documentation()` returns string with all required sections
- [ ] Documentation includes 3 layouts, typography widgets, data widgets, 2 themes
- [ ] Registered in `LayoutEngineRegistry` under name `"slidev"`
- [ ] `calculate()` raises `NotImplementedError` with clear message
- [ ] Integration test: Retrieve docs, verify LLM can parse layout names
- [ ] Contract test: Output schema validation (must contain specific keywords)

---

## Non-Functional Requirements

- **Performance**: Documentation generation <10ms (static string, no computation)
- **Maintainability**: Documentation format easy to update when adding layouts/themes
- **Clarity**: Documentation readable by LLMs (no ambiguous terminology)
- **Completeness**: No undocumented layouts/widgets/themes exist in renderer

---

## Change Impact

Adding new layout requires:
1. Update `get_layout_documentation()` string with new layout description
2. Add layout name → slot mapping in `data-model.md`
3. Create corresponding Vue layout component in Slidev project

Adding new theme requires:
1. Update `get_layout_documentation()` string with theme description
2. Add theme name → CSS variable set in `SlideShell.vue`
3. Update color-to-theme mapping in `SlidevRenderer`
