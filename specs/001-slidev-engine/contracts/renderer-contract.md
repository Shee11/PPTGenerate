# Contract: SlidevRenderer

**Interface**: `Renderer` protocol (extends, not strictly implements)  
**Implementation**: `src/render/slidev/markdown_renderer.py`  
**Purpose**: Transform slide JSON to Slidev-compatible markdown with frontmatter and slot syntax

## Method Signatures

### 1. `render(self, renderable: Union[dict, List[dict]]) -> str`

**Contract**: Render single slide JSON or list of slide JSONs to Slidev markdown

**Input**:
- `renderable`: Single slide JSON dict OR list of slide JSON dicts
- Slide JSON structure per `data-model.md` schema

**Output**: String (complete Slidev markdown file)

**Behavior**:
- If input is dict → delegate to `render_single_slide()`
- If input is list → delegate to `render_multi_slide()`
- Otherwise → raise `TypeError`

**Requirements**:
- ✅ FR-006: Translate slide JSON to Slidev Markdown format
- ✅ FR-011: Output `.md` files compatible with Slidev CLI

**Test Contract**:
- Single dict input returns markdown with 1 frontmatter block
- List input returns markdown with N frontmatter blocks, N-1 separators
- Invalid input type raises `TypeError` with clear message

---

### 2. `render_single_slide(self, slide: dict) -> str`

**Contract**: Transform single slide JSON to markdown with frontmatter and slots

**Input**: Slide JSON dict with fields:
- `layout` (required): str
- `parameters` (optional): dict
- `theme` (optional): dict with `primary_color`
- `widgets` (required): dict mapping slot names → widget configs

**Output**: String (markdown for one slide)

**Example Output**:
```markdown
---
layout: smart-grid
theme: cyber
cols: 3
---

::header::
# Q4 Revenue Analysis
::

::col1::
<MetricCard label="Revenue" value="$5.2M" variant="primary" />
::

::col2::
Key insights...
::

::col3::
```sql
SELECT * FROM revenue
```
::
```

**Requirements**:
- ✅ FR-007: Generate frontmatter section (layout, theme, parameters)
- ✅ FR-008: Distribute widget content to slot sections (`::slotName::`)
- ✅ FR-009: Preserve markdown formatting in widget text

**Transform Logic**:
1. **Frontmatter**: Extract `layout`, resolve theme from colors, merge `parameters`
2. **Widgets**: Iterate `widgets` dict, render each widget based on type
3. **Slots**: Wrap widget content in `::slotName::` ... `::` syntax
4. **Assembly**: Join frontmatter + slot sections

**Test Contract**:
- Output starts with `---` (frontmatter)
- Contains `layout:` field matching input
- Each widget slot name appears as `::name::`
- Typography widgets rendered as markdown, data widgets as components
- Preserves `**bold**`, `==highlight==`, code blocks from widget text

---

### 3. `render_multi_slide(self, slides: List[dict]) -> str`

**Contract**: Render multiple slides separated by `---` delimiter

**Input**: List of slide JSON dicts

**Output**: String (complete multi-slide presentation)

**Example Output**:
```markdown
---
layout: smart-grid
theme: cyber
---

::header::
Slide 1
::

---
layout: hero-split
theme: business
---

::left::
Slide 2
::
```

**Requirements**:
- ✅ FR-010: Separate slides with `---` delimiters
- ✅ SC-003: Process 10 slides in <500ms

**Transform Logic**:
1. Render each slide independently via `render_single_slide()`
2. Join rendered slides with `\n---\n` separator

**Test Contract**:
- Output contains exactly `len(slides) - 1` occurrences of `\n---\n`
- Each slide has independent frontmatter block
- Performance: 10 slides render in <500ms

---

## Helper Methods (Internal)

### `_generate_frontmatter(self, layout: str, parameters: dict, theme: dict) -> str`

**Purpose**: Generate YAML frontmatter block

**Logic**:
1. Determine semantic theme name from `theme.primary_color`
2. Merge layout name, theme name, and all parameters
3. Serialize to YAML format

**Output**:
```yaml
---
layout: smart-grid
theme: cyber
cols: 3
gap: 24px
---
```

**Test Contract**:
- Output starts and ends with `---`
- Contains `layout: {name}` line
- Color `#00ffa3` → `theme: cyber`
- Color `#2563eb` → `theme: business`
- Unknown colors → `theme: business` (default)

---

### `_render_widget(self, widget_type: str, parameters: dict) -> str`

**Purpose**: Convert widget JSON to markdown/component string

**Logic**:
- If `widget_type` starts with `"Type."` → render as markdown (delegate to `_render_typography()`)
- If `widget_type` starts with `"Data."` → render as component (delegate to `_render_component()`)
- Otherwise → log warning, return empty string

**Test Contract**:
- `Type.Display` returns markdown text
- `Type.Code` returns ` ```language\ncode\n``` `
- `Data.BigNum` returns `<MetricCard ... />`
- Unknown type returns `""` and logs warning

---

### `_render_typography(self, widget_type: str, parameters: dict) -> str`

**Purpose**: Render typography widgets as markdown

**Mapping**:
- `Type.Display` → `parameters.text` (plain)
- `Type.Heading` → `# {text}` (or `## `, `### ` based on level)
- `Type.Body` → `parameters.text` (plain)
- `Type.List` → `- {item1}\n- {item2}` (from `parameters.items`)
- `Type.Quote` → `> {text}\n> — {author}`
- `Type.Code` → ` ```{language}\n{code}\n``` `

**Test Contract**:
- Preserves markdown syntax in input (`**bold**`, `==highlight==`)
- Code blocks properly fenced with language
- Lists properly bulleted

---

### `_render_component(self, widget_type: str, parameters: dict) -> str`

**Purpose**: Render data widgets as Vue component tags

**Mapping**:
- `Data.BigNum` → `<MetricCard label="..." value="..." variant="..." />`
  - Split `text` on `\n`: line 1 = label, line 2 = value
  - Extract `preset.variant` or default to "primary"
- `Data.Progress` → `<ProgressBar label="..." :value="number" status="..." />`
- `Data.Trend` → `<StatusBadge status="..." text="..." />`

**Test Contract**:
- `Data.BigNum` with `text: "Revenue\n$5.2M"` → `<MetricCard label="Revenue" value="$5.2M" ... />`
- Variant from preset correctly extracted
- Number props use `:prop=` syntax (Vue binding)

---

## Data Contract

### Input Validation

Must validate before transformation:
- [ ] `layout` field exists and is non-empty string
- [ ] `widgets` field exists and is dict
- [ ] Each widget has `type` and `parameters` fields

**On Validation Failure**: Raise `ValueError` with descriptive message

### Output Guarantees

- Output is valid UTF-8 string
- Output parseable by Slidev CLI (no syntax errors)
- Frontmatter is valid YAML
- All slots properly opened/closed (`::name::` ... `::`)

---

## Performance Contract

### Targets

- Single slide: <40ms
- 10 slides: <500ms (SC-003)
- Template compilation: <50ms (one-time, cached)

### Optimization Requirements

- Use Jinja2 template caching (compile once, reuse)
- Batch process slides (no per-slide overhead)
- Use list + join for string assembly (no repeated concatenation)

**Test Contract**:
- Benchmark with 10 realistic slides
- Average render time <50ms per slide
- Total time <500ms

---

## Error Handling

### Input Errors

| Error Condition | Exception | Message |
|----------------|-----------|---------|
| Missing `layout` field | `ValueError` | "Slide JSON missing required field: layout" |
| Missing `widgets` field | `ValueError` | "Slide JSON missing required field: widgets" |
| Invalid `widgets` type | `TypeError` | "widgets must be dict, got {type}" |
| Unknown widget type | Warning (log) | "Unknown widget type: {type}, rendering empty" |

### Transformation Errors

| Error Condition | Behavior | Recovery |
|----------------|----------|----------|
| Invalid `cols` value | Log warning | Clamp to 2-4 range |
| Unknown theme color | Log warning | Default to "business" theme |
| Malformed widget text | Pass through | Let Slidev handle |
| Missing widget parameter | Use empty string | Continue rendering |

**Contract**: Renderer should be fault-tolerant - log warnings but produce output when possible

---

## Integration Contract

### Usage Pattern

```python
from src.render.slidev.markdown_renderer import SlidevRenderer

renderer = SlidevRenderer()

# Single slide
slide_json = {...}  # per data-model.md
markdown = renderer.render(slide_json)
with open("slides.md", "w") as f:
    f.write(markdown)

# Multi-slide
slides_json = [{...}, {...}, {...}]
markdown = renderer.render(slides_json)
with open("presentation.md", "w") as f:
    f.write(markdown)

# Slidev CLI consumption
# $ slidev slides.md
```

**Contract**:
- Output file directly usable with `slidev <filename>`
- No post-processing required
- Compatible with Slidev export commands (`slidev build`)

---

## Acceptance Criteria

- [ ] Implements core rendering methods (`render`, `render_single_slide`, `render_multi_slide`)
- [ ] Handles both single and multi-slide inputs
- [ ] Generates valid frontmatter (passes YAML parser)
- [ ] Maps widget types correctly (typography → markdown, data → components)
- [ ] Preserves markdown formatting from input
- [ ] Meets performance target (<500ms for 10 slides)
- [ ] Fault-tolerant (handles missing fields with warnings)
- [ ] Integration test: Output runs in Slidev CLI without errors
- [ ] Contract test: Output schema validation (frontmatter + slots present)

---

## Change Impact

Adding new widget type requires:
1. Update widget-to-component mapping in `_render_widget()`
2. Add rendering logic in `_render_typography()` or `_render_component()`
3. Update `data-model.md` transformation rules
4. Add test cases for new widget type

Adding new layout requires:
1. Update layout name validation (if strict)
2. Document slot names in `data-model.md`
3. Create corresponding Vue layout component
4. Add test cases for new layout rendering
