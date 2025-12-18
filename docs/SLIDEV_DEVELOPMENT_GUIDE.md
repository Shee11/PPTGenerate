# Slidev Layout Engine - Development Guide

## Overview

The Slidev layout engine integrates Slidev presentation framework with the UCE rendering system, enabling AI-generated presentations with custom Vue components and layouts.

## Architecture

### Directory Structure

```
gggg/
├── slidev-project/          # SOURCE (version controlled)
│   ├── layouts/             # Custom Vue layout components
│   │   ├── smart-grid.vue
│   │   ├── hero-split.vue
│   │   ├── full-bleed.vue
│   │   ├── feature-grid.vue
│   │   ├── comparison.vue
│   │   ├── timeline.vue
│   │   └── dashboard.vue
│   ├── components/          # Custom Vue widget components
│   │   ├── ChartWidget.vue
│   │   ├── TableWidget.vue
│   │   ├── QuoteWidget.vue
│   │   ├── MetricWidget.vue
│   │   └── README.md
│   └── package.json         # Slidev dependencies
│
├── slidev_build/            # BUILD (temporary, gitignored)
│   └── [auto-generated on each render]
│
└── src/
    ├── layout/slidev/
    │   ├── layout_engine.py      # Documentation for LLM
    │   └── markdown_renderer.py  # Markdown/HTML generator
    └── render/slidev/
        └── markdown_renderer.py  # (copy of above)
```

### Key Concepts

**slidev-project/** (Source Directory)
- **Purpose**: Single source of truth for all Slidev code
- **Version Control**: Committed to git
- **Contents**: Vue components, package.json, configuration
- **Usage**: Edit files here to add/modify layouts and widgets

**slidev_build/** (Build Directory)
- **Purpose**: Temporary workspace for Slidev build process
- **Lifecycle**: Created fresh on each render, deleted after
- **Contents**: Copy of slidev-project + generated slides.md
- **Usage**: Never edit files here - they'll be overwritten

## Three-Phase Generation Pipeline

### Phase 1: Storyline Generation

**Input**: Extracted atoms (facts/concepts from source content)

**Process**: LLM creates narrative structure with abstract visual design

**Output**: Draft slides with:
- `story`: Narrative description (1-2 sentences)
- `atoms`: References to relevant facts (2-5 IDs)
- `density`: Information density (minimal/moderate/dense)
- `visual_design`: Abstract design intent (hierarchical/split/grid/timeline/etc.)

**Example**:
```json
{
  "id": "slide_2",
  "rank": 2,
  "state": "draft",
  "story": "Contrast old accuracy-focused workflow with modern speed-first approach",
  "atoms": ["atom_005", "atom_012"],
  "density": "minimal",
  "visual_design": "split"
}
```

### Phase 2: Slide Generation (Parallel)

**Input**: Each draft slide + related atoms

**Process**: LLM reads layout documentation and:
1. Matches `visual_design` to available layouts
2. Selects best-fit layout (e.g., "split" → "comparison" or "hero-split")
3. Populates layout slots with appropriate widgets

**Output**: Active slide with:
- `layout`: Concrete layout name (e.g., "hero-split")
- `widgets`: Populated content for each slot
- `header`/`footer`: Optional global elements

**Example**:
```json
{
  "id": "slide_2",
  "rank": 2,
  "state": "active",
  "layout": "comparison",
  "visual_design": "split",
  "widgets": {
    "before": {"type": "Type.Body", "parameters": {"text": "Old: Weeks tuning models"}},
    "after": {"type": "Type.Body", "parameters": {"text": "New: Hours with prompts"}}
  }
}
```

### Phase 3: Rendering

**Input**: Active slides with populated widgets

**Process**:
1. Copy slidev-project/ → slidev_build/
2. Generate slides.md in Slidev markdown format
3. Run `npm run build` to create static HTML
4. Copy dist/ folder to output location

**Output**: Standalone HTML presentation

## Adding New Layouts

### 1. Create Vue Layout Component

Create `slidev-project/layouts/your-layout.vue`:

```vue
<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  // Define parameters
  columns: {
    type: Number,
    default: 3
  }
})
</script>

<template>
  <div class="your-layout">
    <!-- Define slots -->
    <div class="slot-header">
      <slot name="header" />
    </div>
    <div class="slot-content">
      <slot name="content" />
    </div>
  </div>
</template>

<style scoped>
.your-layout {
  display: grid;
  grid-template-rows: auto 1fr;
  height: 100%;
}
/* Add Tailwind or custom CSS */
</style>
```

### 2. Document the Layout

Update `src/layout/slidev/layout_engine.py` in `get_layout_documentation()`:

```python
N. your-layout (Your Layout Name)
   - Brief description of purpose
   - Slot names: 'header', 'content', 'footer'
   - Parameters: columns (integer, 2-4)
   - Best for: Specific use cases
   - Visual: How it looks
   - Design characteristics: hierarchical, balanced, modern
   
   Example JSON:
   {
     "layout": "your-layout",
     "parameters": {"columns": 3},
     "widgets": {
       "header": {"type": "Type.Heading", "parameters": {"text": "Title"}},
       "content": {"type": "Type.Body", "parameters": {"text": "Content"}}
     }
   }
```

### 3. Test the Layout

```bash
python -m cli.uce_render \
  --source data/context/career_talk.txt \
  --user-instruction "Create presentation with hierarchical structure" \
  --layout-engine slidev \
  --output output/test.html \
  --verbose
```

The LLM should automatically discover and use your layout when `visual_design` matches your documented characteristics.

## Adding New Widgets

### 1. Create Vue Component

Create `slidev-project/components/YourWidget.vue`:

```vue
<script setup lang="ts">
const props = defineProps({
  title: String,
  value: Number,
  color: {
    type: String,
    default: '#3b82f6'
  }
})
</script>

<template>
  <div class="your-widget" :style="{ borderColor: color }">
    <h3>{{ title }}</h3>
    <div class="value">{{ value }}</div>
  </div>
</template>

<style scoped>
.your-widget {
  border: 2px solid;
  padding: 1rem;
  border-radius: 0.5rem;
}
.value {
  font-size: 2rem;
  font-weight: bold;
}
</style>
```

### 2. Document the Widget

Update `src/layout/slidev/layout_engine.py`:

```python
N. <YourWidget> - Brief description
   Usage in markdown:
   ```vue
   <YourWidget
     title="Widget Title"
     :value="42"
     color="#ff0000"
   />
   ```
   
   Props:
   - title (string): Widget title
   - value (number): Numeric value to display
   - color (string): Border color (hex)
   
   Use cases: When to use this widget
   Design characteristics: data-focused, visual-emphasis, etc.
```

### 3. Map Widget Type

In `src/render/slidev/markdown_renderer.py`, add to `_widget_to_vue_component()`:

```python
def _widget_to_vue_component(self, widget_type: str, params: dict) -> str:
    if widget_type == "Custom.YourWidget":
        return f"""<YourWidget
  title="{params.get('title', 'Default Title')}"
  :value="{params.get('value', 0)}"
  color="{params.get('color', '#3b82f6')}"
/>"""
    # ... existing mappings
```

## Visual Design System

### Abstract Design Principles

The LLM uses abstract visual design language in the storyline phase:

- **hierarchical**: Top-down information flow, clear priority
- **symmetrical**: Balanced, stable, formal
- **asymmetrical**: Dynamic, modern, creative tension
- **split**: Compare/contrast, dual concepts
- **grid**: Organized data, multiple equal items
- **timeline**: Sequential progression, chronological
- **full-canvas**: Immersive, bold statement

### Layout Matching Process

1. Storyline LLM assigns `visual_design` based on content intent
2. Slide generation LLM reads layout documentation
3. LLM matches design characteristics to available layouts
4. LLM selects best-fit layout and populates slots

**Example Matching**:
- `visual_design: "split"` → could match:
  - `hero-split` (split, asymmetrical, comparison)
  - `comparison` (split, symmetrical, contrast)
  - `two-cols` (split, symmetrical)

The LLM chooses based on context and widget requirements.

## Debugging Tips

### Check Phase Outputs

After rendering, examine debug files in `output/`:

```bash
# Phase 1: Check visual_design values
Get-Content output/debug_phase1_storyline.json

# Phase 2: Check layout selection
Get-Content output/debug_phase2_patches.json

# Phase 3: Check final active slides
Get-Content output/debug_phase3_final.json
```

### Verify Layout Documentation

Ensure your layout documentation includes:
- ✓ Design characteristics keywords
- ✓ All slot names documented
- ✓ Parameter types and defaults
- ✓ Complete JSON example

### Test Layout Matching

```python
# In Python REPL
from src.layout.engine_registry import LayoutEngineRegistry
LayoutEngineRegistry.set_active_engine("slidev")
engine = LayoutEngineRegistry.get_active_engine()
print(engine.get_layout_documentation())
```

### Common Issues

**Issue**: LLM always chooses same layout
- **Fix**: Add more diverse design characteristics to documentation
- **Fix**: Ensure visual_design variety in storyline phase

**Issue**: "Slot not found" error
- **Fix**: Check slot names in documentation match Vue template
- **Fix**: Verify LLM example JSON uses correct slot names

**Issue**: Widget not rendering
- **Fix**: Check component is in slidev-project/components/
- **Fix**: Verify _widget_to_vue_component mapping exists
- **Fix**: Check Vue component prop types match parameters

## Performance Optimization

### Caching

The system caches LLM responses in `.uce_cache/`:

```bash
# Clear cache to force fresh generation
Remove-Item -Recurse -Force .uce_cache
```

### Parallel Slide Generation

Phase 2 runs in parallel (default: 5 workers):

```python
# Adjust in src/generation/content/generator.py
slide_patches = _generate_slides_parallel(
    draft_slides, atoms, user_instruction, config, 
    intent_guidance, max_workers=10  # Increase for faster generation
)
```

### Build Performance

Slidev builds can be slow for large presentations:

```bash
# In slidev-project/package.json, use production build:
"build": "slidev build --base ./ --out dist"
```

## Best Practices

### Layout Design

1. **Keep slots semantic**: Use meaningful names (`hero`, `content`) not generic (`slot1`, `slot2`)
2. **Provide parameters**: Make layouts flexible with sensible defaults
3. **Document use cases**: Help LLM understand when to use each layout
4. **Add design keywords**: Include multiple characteristic words for better matching

### Widget Design

1. **Single responsibility**: Each widget should do one thing well
2. **Prop validation**: Use TypeScript types or prop validators
3. **Flexible styling**: Support theme colors via CSS variables
4. **Responsive**: Test at different slide sizes

### Documentation Quality

1. **Be specific**: Clear descriptions help LLM make better choices
2. **Show examples**: Include complete JSON examples
3. **Update together**: When changing code, update documentation
4. **Test matching**: Verify LLM can find your layouts with expected visual_design values

## Architecture Decisions

### Why Two Directories?

- **Separation of concerns**: Source code vs build artifacts
- **Clean builds**: Fresh build directory ensures no stale files
- **Version control**: Only source code tracked in git
- **Development workflow**: Edit in one place, build happens automatically

### Why Documentation-Driven?

- **No hardcoded mappings**: Flexible, extensible system
- **LLM-native**: Documentation is the API for AI
- **Self-documenting**: Code + docs stay in sync
- **Layout-engine agnostic**: Prompts work with any engine

### Why Abstract Visual Design?

- **Intent-based**: Describes what, not how
- **Future-proof**: New layouts can match existing intents
- **Maintainable**: No brittle name-based mappings
- **Intelligent**: LLM uses context to choose best match

## Related Documentation

- `slidev-project/components/README.md`: Widget component reference
- `src/layout/slidev/layout_engine.py`: Layout documentation source
- `src/render/slidev/markdown_renderer.py`: Rendering implementation
- `LAYOUT_ENGINE_REFACTOR_PLAN.md`: Historical refactoring notes

## Troubleshooting

### Build Fails

```bash
# Check Node.js version (requires 18+)
node --version

# Reinstall dependencies
cd slidev-project
rm -rf node_modules package-lock.json
npm install

# Test Slidev directly
npm run dev  # Should start dev server
```

### Layouts Not Copying

Check `src/render/slidev/markdown_renderer.py`:

```python
def _copy_layouts_and_components(self, source_dir: Path):
    # Verify source_dir points to slidev-project/
    # Check layouts_src and components_src paths
```

### LLM Not Finding Layouts

Verify layout documentation is being injected:

```python
# In prompts.py _build_slide_generation_system_prompt()
layout_docs = active_engine.get_layout_documentation()
# Should contain your layout with design characteristics
```

## Contributing

When adding features:

1. Update source files in `slidev-project/`
2. Update documentation in `layout_engine.py`
3. Add tests if applicable
4. Update this guide with new patterns
5. Test end-to-end generation
