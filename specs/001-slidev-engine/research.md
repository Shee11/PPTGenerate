# Research Document: Slidev Layout Engine

**Feature**: 001-slidev-engine  
**Date**: 2024-12-18  
**Phase**: 0 (Outline & Research)

## Purpose

This document consolidates research findings to resolve all "NEEDS CLARIFICATION" items from the Technical Context and provides best practices for key technology decisions.

## Research Tasks

### 1. Slidev Architecture & Markdown Slot Syntax

**Question**: How does Slidev's markdown slot syntax work and how do we map JSON slots to `::slotName::` sections?

**Decision**: Use Slidev's built-in slot syntax with custom Vue layout components

**Rationale**:
- Slidev supports custom layouts via Vue SFC (Single File Components)
- Slots defined in layouts using standard Vue `<slot name="slotName" />` syntax
- Markdown uses `::slotName::` ... `::` to populate named slots
- Frontmatter configuration passes layout parameters (e.g., `cols: 3`)

**Implementation Pattern**:
```markdown
---
layout: smart-grid
cols: 3
theme: cyber
---

::header::
# Main Title
::

::col1::
Content for column 1
::

::col2::
Content for column 2
::
```

Maps to Vue layout:
```vue
<template>
  <div class="smart-grid" :style="gridStyle">
    <div class="header"><slot name="header" /></div>
    <div class="col1"><slot name="col1" /></div>
    <div class="col2"><slot name="col2" /></div>
    <!-- cols determined by frontmatter -->
  </div>
</template>
```

**Alternatives Considered**:
- Generate HTML directly (rejected: loses Slidev's built-in navigation, presenter mode, export features)
- Use MDX instead of Slidev (rejected: more complex, less presentation-focused)

**References**:
- Slidev Custom Layouts: https://sli.dev/custom/
- Vue Named Slots: https://vuejs.org/guide/components/slots.html#named-slots

---

### 2. Vue Component Patterns for Widget Translation

**Question**: How should we translate widget types (Data.BigNum, Data.Progress) to Vue components (MetricCard, StatusBadge)?

**Decision**: Create mapping table in renderer; use Jinja2 templates with conditional logic based on widget type

**Rationale**:
- Widget types follow existing taxonomy (Type.*, Data.*, Media.*)
- Renderer maintains 1:1 mapping: Data.BigNum → MetricCard template
- Typography widgets (Type.Display, Type.Heading) render as markdown
- Data widgets render as Vue component tags with props extracted from parameters

**Implementation Pattern**:
```python
# In SlidevRenderer
WIDGET_TO_COMPONENT = {
    "Data.BigNum": "MetricCard",
    "Data.Progress": "ProgressBar", 
    "Data.Trend": "StatusBadge",
}

def render_widget(widget_type, parameters):
    if widget_type.startswith("Type."):
        # Render as markdown
        return parameters.get("text", "")
    elif widget_type in WIDGET_TO_COMPONENT:
        # Render as Vue component
        component = WIDGET_TO_COMPONENT[widget_type]
        props = extract_props(widget_type, parameters)
        return f"<{component} {props} />"
```

**Alternatives Considered**:
- Use widget registry pattern (rejected: adds unnecessary abstraction for 3-5 components)
- Embed all logic in Jinja2 templates (rejected: harder to test, less maintainable)

**References**:
- Vue Component Props: https://vuejs.org/guide/components/props.html
- Existing widget system: `src/widgets/base.py`

---

### 3. UnoCSS Integration & Theme CSS Variables

**Question**: How should we implement theme switching using CSS variables and UnoCSS shortcuts?

**Decision**: Define themes as CSS variable sets in SlideShell.vue, use UnoCSS shortcuts for semantic class names

**Rationale**:
- CSS variables enable runtime theme switching without component changes
- UnoCSS shortcuts provide semantic names (`bg-theme-base`, `text-theme-main`)
- SlideShell reads `theme` from frontmatter, applies corresponding variable set
- All components reference `var(--c-primary)`, not hardcoded colors

**Implementation Pattern**:
```vue
<!-- SlideShell.vue -->
<template>
  <div :class="['slide-shell', `theme-${theme}`]" :style="themeVars">
    <slot />
  </div>
</template>

<script setup>
const theme = defineProps(['theme'])
const themeVars = computed(() => {
  if (theme === 'cyber') {
    return {
      '--c-primary': '#00ffa3',
      '--c-bg': '#050505',
      '--font-main': 'Orbitron, monospace'
    }
  } else { // business
    return {
      '--c-primary': '#2563eb',
      '--c-bg': '#ffffff',
      '--font-main': 'Inter, sans-serif'
    }
  }
})
</script>
```

UnoCSS config:
```js
// uno.config.ts
export default defineConfig({
  shortcuts: {
    'bg-theme-base': 'bg-[var(--c-bg)]',
    'text-theme-main': 'text-[var(--c-text)]',
    'border-theme': 'border-[var(--c-border)]',
  }
})
```

**Alternatives Considered**:
- Tailwind CSS (rejected: UnoCSS is Slidev's default, better performance)
- CSS-in-JS (rejected: adds runtime overhead, harder to override)
- Separate CSS files per theme (rejected: can't switch at runtime)

**References**:
- UnoCSS Shortcuts: https://unocss.dev/config/shortcuts
- CSS Variables Guide: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties

---

### 4. JSON Schema Compatibility

**Question**: What is the exact JSON structure we must support for compatibility with `src/generation/content/generator.py`?

**Decision**: Use existing slide JSON schema with `layout`, `parameters`, `theme`, `widgets` fields (confirmed in Clarifications)

**Rationale**:
- Already validated in spec.md Clarifications section
- Matches dummy engine schema: `{"layout": "...", "parameters": {...}, "widgets": {"slot_name": {"type": "...", "parameters": {...}}}}`
- No changes needed to content generation pipeline
- Renderer is pure transformation layer

**Schema Reference**:
```json
{
  "layout": "smart-grid",
  "parameters": {"cols": 3},
  "theme": {
    "primary_color": "#00ffa3",
    "accent_color": "#ff006e"
  },
  "widgets": {
    "header": {"type": "Type.Heading", "parameters": {"text": "..."}},
    "col1": {"type": "Data.BigNum", "parameters": {"text": "Revenue\n$5.2M"}}
  }
}
```

**Alternatives Considered**: None - schema is fixed by existing system

**References**:
- Existing schema: `data/test_01_bento_standard_typography.json`
- Slide model: `src/common/slide.py`

---

### 5. Slidev CLI Integration & Output Format

**Question**: How do we generate output that Slidev CLI can consume and render?

**Decision**: Renderer outputs single `.md` file with frontmatter + slots, Slidev CLI handles parsing and presentation

**Rationale**:
- Slidev CLI expects markdown file as input: `slidev slides.md`
- Multi-slide presentations use `---` separators between slides
- Each slide has independent frontmatter block
- Slidev handles all presentation logic (navigation, presenter mode, export)

**Output Example**:
```markdown
---
layout: smart-grid
theme: cyber
cols: 3
---

::header::
# Slide 1 Title
::

::col1::
Content...
::

---
layout: hero-split
theme: business
---

::left::
# Slide 2
::

::right::
Content...
::
```

**CLI Usage**:
```bash
# Development
slidev slides.md

# Export to PDF
slidev build slides.md --format pdf

# Export to SPA
slidev build slides.md
```

**Alternatives Considered**:
- Generate separate .md files per slide (rejected: harder to manage, no Slidev support)
- Generate HTML directly (rejected: loses Slidev features)

**References**:
- Slidev CLI: https://sli.dev/guide/
- Multi-slide format: https://sli.dev/guide/syntax.html#multiple-entries

---

### 6. Performance Optimization Strategy

**Question**: How do we achieve <500ms rendering for 10-slide presentation (SC-003)?

**Decision**: Use Jinja2 template caching, minimal string operations, batch processing

**Rationale**:
- Jinja2 template compilation is one-time cost (cache templates)
- String concatenation is bottleneck - use list + join pattern
- Widget-to-component mapping is O(1) dict lookup
- No external API calls, pure transformation logic

**Implementation Pattern**:
```python
class SlidevRenderer:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))
        # Templates cached after first load
        self.slide_template = self.env.get_template('slide.md.j2')
    
    def render_multi_slide(self, slides: List[Dict]) -> str:
        # Batch process all slides
        rendered_slides = []
        for slide in slides:
            rendered = self.slide_template.render(slide)
            rendered_slides.append(rendered)
        # Single join operation at end
        return "\n---\n".join(rendered_slides)
```

**Performance Targets**:
- Template compilation: <50ms (one-time)
- Per-slide rendering: <40ms (10 slides × 40ms = 400ms)
- String assembly: <50ms
- Total: <500ms for 10 slides

**Alternatives Considered**:
- Pre-compiled templates (rejected: premature optimization, Jinja2 cache sufficient)
- Parallel rendering (rejected: overhead not worth it for 10 slides)

**References**:
- Jinja2 Performance: https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment

---

## Summary

All technical decisions resolved:

1. **Slidev Integration**: Use custom Vue layouts with named slots, markdown `::slot::` syntax
2. **Widget Translation**: Mapping table with Jinja2 conditional rendering (Type.* → markdown, Data.* → components)
3. **Theme System**: CSS variables + UnoCSS shortcuts in SlideShell.vue
4. **JSON Schema**: Reuse existing schema (no changes to content generation)
5. **Output Format**: Single .md file with `---` separators, Slidev CLI consumption
6. **Performance**: Jinja2 template caching + batch processing achieves <500ms target

No outstanding "NEEDS CLARIFICATION" items remain. Ready to proceed to Phase 1 (Design).
