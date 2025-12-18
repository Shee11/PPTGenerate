# Quickstart Guide: Slidev Layout Engine

**Feature**: 001-slidev-engine  
**Audience**: Developers extending the Slidev layout system  
**Date**: 2024-12-18

## Overview

This guide shows how to:
1. Use the Slidev layout engine for content generation
2. Create custom Vue layouts
3. Add new themes
4. Extend widget-to-component mappings

## Prerequisites

- Python 3.11+ with project dependencies installed
- Node.js 18+ (for Slidev project)
- Familiarity with Vue 3 and Slidev basics

## Quick Start: Using the Slidev Engine

### 1. Generate Content with Slidev Layouts

```python
from src.layout.engine_registry import LayoutEngineRegistry
from src.generation.content.generator import ContentGenerator

# Switch to Slidev engine
LayoutEngineRegistry.set_active_engine("slidev")

# Generate content (LLM uses Slidev layout documentation)
generator = ContentGenerator()
slides_json = generator.generate(user_request="Create a Q4 revenue presentation")

# slides_json contains layout names, slot names, widget types from Slidev docs
```

### 2. Render to Slidev Markdown

```python
from src.render.slidev.markdown_renderer import SlidevRenderer

renderer = SlidevRenderer()

# Single slide
markdown = renderer.render(slides_json[0])
with open("slide.md", "w") as f:
    f.write(markdown)

# Multi-slide presentation
markdown = renderer.render(slides_json)
with open("presentation.md", "w") as f:
    f.write(markdown)
```

### 3. View in Slidev

```bash
# Install Slidev CLI (once)
npm install -g @slidev/cli

# Start dev server
slidev presentation.md

# Export to PDF
slidev build presentation.md --format pdf
```

---

## Extending the System

### Adding a New Layout

**Example**: Add "Three-Column" layout

#### Step 1: Create Vue Layout Component

```vue
<!-- slidev-project/layouts/three-column.vue -->
<template>
  <SlideShell :theme="$slidev.configs.theme">
    <div class="three-column" :style="{ gap: gap }">
      <div class="column"><slot name="left" /></div>
      <div class="column"><slot name="center" /></div>
      <div class="column"><slot name="right" /></div>
    </div>
  </SlideShell>
</template>

<script setup>
import { defineProps } from 'vue'
const props = defineProps({
  gap: { type: String, default: '24px' }
})
</script>

<style scoped>
.three-column {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  height: 100%;
}
.column {
  @apply bg-theme-elevated border-theme rounded-lg p-6 shadow-theme;
}
</style>
```

#### Step 2: Update Layout Documentation

```python
# src/layout/slidev/layout_engine.py
def get_layout_documentation(cls) -> str:
    return """
    ...existing layouts...
    
    4. Three Column (layout: "three-column")
       - Three equal-width columns
       - Slot names: 'left', 'center', 'right'
       - Parameters: gap (spacing between columns)
       - Best for: Side-by-side comparisons, triple metrics
    """
```

#### Step 3: Add to Data Model

Update `data-model.md`:

```markdown
| `three-column` | `three-column` | `left` → `::left::`, `center` → `::center::`, `right` → `::right::` |
```

#### Step 4: Test

```python
# Test slide JSON
slide = {
    "layout": "three-column",
    "parameters": {"gap": "32px"},
    "widgets": {
        "left": {"type": "Type.Heading", "parameters": {"text": "Column 1"}},
        "center": {"type": "Type.Heading", "parameters": {"text": "Column 2"}},
        "right": {"type": "Type.Heading", "parameters": {"text": "Column 3"}}
    }
}

# Render and verify
markdown = SlidevRenderer().render(slide)
assert "::left::" in markdown
assert "::center::" in markdown
assert "::right::" in markdown
```

---

### Adding a New Theme

**Example**: Add "Minimal" theme

#### Step 1: Define Theme Variables

```vue
<!-- slidev-project/components/SlideShell.vue -->
<script setup>
const THEMES = {
  // ...existing themes...
  minimal: {
    '--c-primary': '#000000',
    '--c-accent': '#6b7280',
    '--c-bg': '#fafafa',
    '--c-text': '#1f2937',
    '--c-text-muted': '#9ca3af',
    '--c-border': '#e5e7eb',
    '--c-success': '#059669',
    '--c-warning': '#d97706',
    '--c-danger': '#dc2626',
    '--font-main': 'system-ui, sans-serif',
    '--font-mono': 'monospace',
    '--shadow-sm': '0 1px 2px rgba(0,0,0,0.05)',
    '--shadow-md': '0 2px 4px rgba(0,0,0,0.1)',
  }
}
</script>
```

#### Step 2: Add Color-to-Theme Mapping

```python
# src/render/slidev/markdown_renderer.py
class SlidevRenderer:
    THEME_COLORS = {
        # ...existing mappings...
        '#000000': 'minimal',  # Black primary → minimal theme
    }
```

#### Step 3: Update Documentation

```python
# src/layout/slidev/layout_engine.py
def get_layout_documentation(cls) -> str:
    return """
    ...existing themes...
    
    3. Minimal Theme (theme: "minimal")
       - Colors: Light gray background (#fafafa), Black primary (#000000)
       - Typography: System font, clean and simple
       - Visual style: Minimal shadows, thin borders, lots of whitespace
       - Use for: Minimalist presentations, text-focused content
    """
```

---

### Adding a New Vue Component

**Example**: Add "Timeline" component for Data.Timeline widget

#### Step 1: Create Component

```vue
<!-- slidev-project/components/Timeline.vue -->
<template>
  <div class="timeline">
    <div v-for="(event, i) in events" :key="i" class="timeline-event">
      <div class="timeline-dot" />
      <div class="timeline-content">
        <h4 class="text-theme-primary">{{ event.title }}</h4>
        <p class="text-theme-muted text-sm">{{ event.date }}</p>
        <p class="text-theme-main">{{ event.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
const props = defineProps({
  events: { type: Array, required: true }
})
</script>

<style scoped>
.timeline {
  @apply relative pl-8;
}
.timeline-event {
  @apply relative pb-8;
}
.timeline-dot {
  @apply absolute left-0 top-2 w-3 h-3 rounded-full bg-theme-primary;
}
.timeline-content {
  @apply pl-6;
}
</style>
```

#### Step 2: Add Widget-to-Component Mapping

```python
# src/render/slidev/markdown_renderer.py
class SlidevRenderer:
    WIDGET_TO_COMPONENT = {
        # ...existing mappings...
        "Data.Timeline": "Timeline",
    }
    
    def _render_component(self, widget_type, parameters):
        if widget_type == "Data.Timeline":
            events = parameters.get("events", [])
            # Serialize events array to JSON for Vue prop
            events_json = json.dumps(events)
            return f'<Timeline :events="{events_json}" />'
```

#### Step 3: Register Widget Type

```python
# src/widgets/data.py (optional - for type safety)
class TimelineWidget(BaseWidget):
    type_name = "Data.Timeline"
    
    def __init__(self, events: List[Dict[str, str]]):
        self.events = events
    
    def render_data(self) -> dict:
        return {"events": self.events}
```

#### Step 4: Update Documentation

```python
# src/layout/slidev/layout_engine.py
def get_layout_documentation(cls) -> str:
    return """
    ...existing data widgets...
    
    - Data.Timeline → <Timeline :events="[...]" />
      - Displays chronological sequence of events
      - Parameters: events (array of {title, date, description} objects)
    """
```

---

## Development Workflow

### 1. Local Development Loop

```bash
# Terminal 1: Python backend
cd /path/to/project
python -m src.cli.uce_render generate --topic "Test presentation" --engine slidev

# Terminal 2: Slidev live reload
cd slidev-project
slidev output/slides.md
# Opens http://localhost:3030 with auto-reload
```

### 2. Testing Changes

```bash
# Run Python tests
pytest tests/integration/test_slidev_renderer.py

# Run Vue component tests (in slidev-project)
cd slidev-project
npm test

# Visual regression tests
npm run test:visual
```

### 3. Debugging Tips

**Python Renderer Issues**:
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

renderer = SlidevRenderer()
markdown = renderer.render(slide_json)
print(markdown)  # Inspect raw markdown output
```

**Slidev Rendering Issues**:
- Check browser console for Vue errors
- Inspect frontmatter parsing: `http://localhost:3030/__inspect__`
- Verify slot names match layout component

**Theme Not Applying**:
- Verify theme name in frontmatter matches SlideShell.vue keys
- Check CSS variable cascade (use browser DevTools)
- Ensure UnoCSS shortcuts compiled (`npm run build`)

---

## Common Patterns

### Pattern 1: Conditional Widget Rendering

```python
def _render_widget(self, widget_type, parameters):
    # Skip widgets with no content
    if not parameters.get("text") and not parameters.get("code"):
        return ""
    
    # Render based on type
    if widget_type.startswith("Type."):
        return self._render_typography(widget_type, parameters)
    # ...
```

### Pattern 2: Theme Inheritance

```vue
<!-- Child component inherits theme via CSS variables -->
<template>
  <div class="custom-component">
    <!-- Automatically uses --c-primary from parent SlideShell -->
    <h3 class="text-theme-primary">{{ title }}</h3>
  </div>
</template>
```

### Pattern 3: Layout Parameter Validation

```python
def _validate_parameters(self, layout, parameters):
    if layout == "smart-grid":
        cols = parameters.get("cols", 3)
        if cols < 2 or cols > 4:
            logging.warning(f"Invalid cols value {cols}, clamping to 2-4")
            parameters["cols"] = max(2, min(4, cols))
    return parameters
```

---

## Troubleshooting

### Issue: LLM generates invalid layout names

**Solution**: Update layout documentation with clearer examples

```python
# Be explicit about valid values
def get_layout_documentation(cls) -> str:
    return """
    IMPORTANT: Use EXACT layout names in quotes:
    - "smart-grid" (NOT "grid" or "smart_grid")
    - "hero-split" (NOT "split" or "hero")
    - "full-bleed" (NOT "fullbleed" or "full_bleed")
    """
```

### Issue: Components not rendering in Slidev

**Checklist**:
1. Component file exists in `slidev-project/components/`
2. Component name matches exactly (case-sensitive)
3. Component registered globally or imported in SlideShell.vue
4. Props passed correctly (`:prop=value` for non-strings)

### Issue: Theme switching slow (>100ms)

**Solution**: Reduce theme variable count, use CSS custom property inheritance

```vue
<!-- Bad: Redeclare all variables per component -->
<style scoped>
.component { color: var(--c-primary); }
</style>

<!-- Good: Inherit from parent -->
<style>
.component { color: var(--c-primary); }
</style>
```

---

## Best Practices

### 1. Keep Layouts Simple

- ✅ Max 5-6 slots per layout
- ✅ Semantic slot names (left/right, not slot1/slot2)
- ❌ Avoid nested layouts (complexity)

### 2. Use Semantic Theme Variables

- ✅ `var(--c-primary)` for brand color
- ✅ `var(--c-text)` for main text
- ❌ Hardcoded hex colors in components

### 3. Validate Widget Parameters

```python
# Extract with fallbacks
label = parameters.get("label", "Untitled")
value = parameters.get("value", "0")
variant = parameters.get("preset", {}).get("variant", "primary")
```

### 4. Document All Contracts

- Update `data-model.md` when adding layouts
- Update `contracts/` when changing interfaces
- Add examples to `research.md`

---

## Next Steps

- **Read**: `data-model.md` for complete transformation rules
- **Review**: `contracts/` for interface specifications
- **Explore**: Existing layouts in `src/layout/dummy/strategies/` for patterns
- **Experiment**: Create custom layout following "Adding a New Layout" steps above

## Questions?

- Check `research.md` for architectural decisions
- Review `spec.md` for requirements and success criteria
- See `plan.md` for overall implementation strategy
