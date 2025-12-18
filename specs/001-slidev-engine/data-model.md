# Data Model: Slidev Layout Engine

**Feature**: 001-slidev-engine  
**Date**: 2024-12-18  
**Phase**: 1 (Design & Contracts)

## Purpose

This document defines the complete data transformation flow from input JSON (content generation) through rendering to output Markdown (Slidev consumption).

## Data Flow Overview

```
Content Generation (LLM)
    ↓ produces
Slide JSON (existing schema)
    ↓ consumed by
SlidevRenderer
    ↓ transforms to
Slidev Markdown (.md file)
    ↓ consumed by
Slidev CLI
    ↓ produces
Web Presentation (HTML/CSS/JS)
```

## Input: Slide JSON Schema

### Single Slide Structure

```json
{
  "layout": "smart-grid",
  "parameters": {
    "cols": 3,
    "gap": "24px"
  },
  "theme": {
    "primary_color": "#00ffa3",
    "accent_color": "#ff006e",
    "font_family": "Orbitron, monospace"
  },
  "style": {
    "gap": "24px",
    "padding": "32px"
  },
  "widgets": {
    "header": {
      "type": "Type.Heading",
      "parameters": {
        "text": "Q4 Revenue Analysis"
      }
    },
    "col1": {
      "type": "Data.BigNum",
      "parameters": {
        "text": "Revenue\n$5.2M",
        "preset": {
          "variant": "primary"
        }
      }
    },
    "col2": {
      "type": "Type.Body",
      "parameters": {
        "text": "Key insights about revenue growth..."
      }
    },
    "col3": {
      "type": "Type.Code",
      "parameters": {
        "code": "SELECT * FROM revenue WHERE quarter = 'Q4'",
        "language": "sql"
      }
    }
  }
}
```

### Field Definitions

| Field | Type | Required | Description | Validation Rules |
|-------|------|----------|-------------|------------------|
| `layout` | string | Yes | Layout strategy name | Must match registered Slidev layout name (e.g., "smart-grid", "hero-split") |
| `parameters` | object | No | Layout-specific parameters | Keys depend on layout (e.g., `cols` for smart-grid) |
| `parameters.cols` | integer | If smart-grid | Number of columns | Range: 2-4, clamp to max if exceeded |
| `theme` | object | No | Theme color configuration | If missing, infer from layout or use "business" default |
| `theme.primary_color` | string | No | Primary accent color (hex) | Used to determine semantic theme (business vs cyber) |
| `widgets` | object | Yes | Slot → widget mappings | Keys are slot names, values are widget configs |
| `widgets.{slot}.type` | string | Yes | Widget type identifier | Format: `Category.Name` (e.g., "Type.Display", "Data.BigNum") |
| `widgets.{slot}.parameters` | object | Yes | Widget-specific parameters | Structure depends on widget type |

### Multi-Slide Structure

Array of single slide objects:

```json
[
  { "layout": "smart-grid", "widgets": {...} },
  { "layout": "hero-split", "widgets": {...} },
  { "layout": "full-bleed", "widgets": {...} }
]
```

## Transformation Rules

### 1. Layout Mapping

| Input Layout | Output Layout | Slot Mapping |
|-------------|---------------|--------------|
| `smart-grid` | `smart-grid` | `header` → `::header::`, `col1` → `::col1::`, `col2` → `::col2::`, `col3` → `::col3::` (up to `colN` where N = `parameters.cols`) |
| `hero-split` | `hero-split` | `left` → `::left::`, `right` → `::right::` |
| `full-bleed` | `full-bleed` | `content` → `::default::` (unnamed slot) |

**Rule**: Slot names from JSON `widgets` keys map 1:1 to Slidev slot syntax `::slotName::` ... `::`

### 2. Theme Translation

| Input (theme.primary_color) | Output (theme frontmatter) | Logic |
|------------------------------|---------------------------|-------|
| `#00ffa3` (neon green) | `theme: cyber` | If primary color in cyber palette (#00ffa3, #00ff00, #39ff14) |
| `#2563eb` (blue) | `theme: business` | If primary color in business palette (#2563eb, #1e40af, #3b82f6) |
| Missing or unknown | `theme: business` | Default fallback |

**Rule**: Renderer maintains color-to-theme mapping table; exact hex match determines semantic theme name.

### 3. Widget-to-Content Mapping

#### Typography Widgets (Type.*)

| Widget Type | Input Parameters | Output Markdown | Example |
|------------|------------------|-----------------|---------|
| `Type.Display` | `{text: "Big Text"}` | Plain text with markdown | `**Big Text**` |
| `Type.Heading` | `{text: "Title"}` | Heading level 1-3 | `# Title` |
| `Type.Body` | `{text: "Paragraph"}` | Plain text | `Paragraph with **bold**` |
| `Type.List` | `{items: ["A", "B"]}` | Bulleted list | `- A\n- B` |
| `Type.Quote` | `{text: "Quote", author: "X"}` | Blockquote | `> Quote\n> — X` |
| `Type.Code` | `{code: "...", language: "py"}` | Code fence | ` ```python\ncode\n``` ` |

**Rule**: Extract `text` parameter, preserve markdown formatting (`**bold**`, `==highlight==`), render as markdown.

#### Data Widgets (Data.*)

| Widget Type | Input Parameters | Output Component | Props Extraction |
|------------|------------------|------------------|------------------|
| `Data.BigNum` | `{text: "Revenue\n$5.2M", preset: {variant: "primary"}}` | `<MetricCard ... />` | Split on `\n`: line 1 = label, line 2 = value; variant from preset |
| `Data.Progress` | `{label: "CPU", value: 85, status: "warning"}` | `<ProgressBar ... />` | Direct mapping: label, value, status (or derive status from value thresholds) |
| `Data.Trend` | `{label: "Growth", value: "+15%", trend: "up"}` | `<StatusBadge ... />` | Map trend to status: up=success, down=error, neutral=warning |

**Rule**: Identify component from widget type, extract props from parameters, generate Vue component tag.

#### Component Tag Format

```
<ComponentName prop1="value1" prop2="value2" />
```

Props serialization:
- Strings: `label="Revenue"`
- Numbers: `:value="5.2"` (Vue binding syntax)
- Booleans: `:success="true"`

### 4. Frontmatter Generation

**Inputs**: `layout`, `parameters`, `theme`  
**Output**: YAML frontmatter block

```yaml
---
layout: smart-grid
theme: cyber
cols: 3
gap: 24px
---
```

**Rules**:
- Always include `layout` (required by Slidev)
- Include `theme` if determinable from colors or explicit
- Include all `parameters` as top-level keys (e.g., `cols`, `gap`)
- Omit `style` object (converted to CSS variables in SlideShell.vue)

### 5. Multi-Slide Assembly

**Input**: Array of N slide JSONs  
**Output**: Single markdown file with N-1 `---` separators

```markdown
[Slide 1 frontmatter + content]

---

[Slide 2 frontmatter + content]

---

[Slide 3 frontmatter + content]
```

**Rule**: Join slides with `\n---\n` separator (blank line before/after for readability).

## Output: Slidev Markdown Structure

### Single Slide Example

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
Key insights about revenue growth trends observed in Q4. Notable increase in enterprise segment.
::

::col3::
```sql
SELECT * FROM revenue WHERE quarter = 'Q4'
```
::
```

### Multi-Slide Example

```markdown
---
layout: smart-grid
theme: cyber
cols: 3
---

::header::
# Overview
::

::col1::
Content
::

---
layout: hero-split
theme: business
---

::left::
# Details
::

::right::
More content
::
```

## Validation Rules

### Input Validation

1. **Required Fields**: `layout`, `widgets` must be present
2. **Layout Existence**: `layout` must match a registered Slidev layout name
3. **Slot Consistency**: Widget slot names must match layout's expected slots (log warning if mismatch, ignore unmapped widgets)
4. **Parameter Constraints**: `cols` must be 2-4 for smart-grid (clamp to range)
5. **Widget Type Format**: Must follow `Category.Name` pattern

### Output Validation

1. **Frontmatter Syntax**: Valid YAML (no unescaped special chars)
2. **Slot Syntax**: Every slot must have opening `::name::` and closing `::`
3. **Component Props**: All prop values properly escaped for markdown/Vue
4. **Markdown Validity**: Code fences properly closed, blockquotes formatted

## Edge Case Handling

| Edge Case | Input | Handling | Output |
|-----------|-------|----------|--------|
| Extra slots | `col4` when `cols: 3` | Ignore unmapped widgets, log warning | No `::col4::` section |
| Missing slots | No `header` widget | Render empty slot section | `::header::\n::` (empty) |
| Invalid cols | `cols: 5` | Clamp to max (4), log warning | `cols: 4` in frontmatter |
| Unknown theme | `primary_color: "#rainbow"` | Fallback to "business" | `theme: business` |
| Malformed text | `text: "<div>unclosed"` | Pass through (Slidev markdown parser handles) | Raw text in slot |
| Empty widget | `parameters: {}` | Render empty content | Slot section exists but empty |

## State Transitions

### Renderer State Machine

```
Input Validation → Theme Resolution → Frontmatter Generation → Widget Rendering → Slot Assembly → Output
```

**No persistent state** - pure functional transformation. Each render call is independent.

## Performance Considerations

### Complexity Analysis

- **Frontmatter generation**: O(1) - fixed number of fields
- **Widget iteration**: O(W) where W = number of widgets per slide
- **Component mapping**: O(1) - dict lookup
- **Text processing**: O(L) where L = text length
- **Multi-slide assembly**: O(N × W) where N = number of slides

### Memory Footprint

- **Input JSON**: ~1-5 KB per slide
- **Template cache**: ~10 KB (Jinja2 compiled templates)
- **Output markdown**: ~2-10 KB per slide
- **Working memory**: O(N) for N slides (no accumulation)

### Optimization Targets

- Single slide render: <40ms
- 10-slide render: <500ms (SC-003)
- Template compilation: <50ms (one-time, cached)

## Data Integrity

### Immutability Guarantees

- Input JSON never modified (read-only)
- Transformation is pure function (no side effects)
- Output markdown deterministic (same input → same output)

### Error Propagation

- **Validation errors**: Raise exception with context (slide index, field name)
- **Transformation errors**: Log warning, use fallback values (e.g., default theme)
- **Template errors**: Re-raise with full traceback (Jinja2 errors)

## Summary

Complete data model defined covering:

- ✅ Input JSON schema (single + multi-slide)
- ✅ Transformation rules (layout, theme, widget→content)
- ✅ Output markdown structure
- ✅ Validation rules (input + output)
- ✅ Edge case handling (6 scenarios)
- ✅ Performance targets (<500ms for 10 slides)

No ambiguities remain. Ready to proceed to contracts definition.
