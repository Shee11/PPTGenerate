# Layout Validation and Refinement System

## Overview

The layout validation and refinement system automatically detects quality issues in generated layouts and provides instant feedback to the LLM for correction through an iterative refinement loop.

## Architecture

### Components

1. **LayoutValidator** (`src/layout/validation.py`)
   - Validates RenderableLayout objects
   - Detects 4 categories of issues
   - Returns structured LayoutIssue objects

2. **Refinement Loop** (`src/generation/content/generator.py`)
   - `refine_layout_with_validation()`: Main refinement orchestration
   - `_generate_refinement()`: LLM call with validation feedback
   - Uses `render_refinement_prompt()` for active slides (not draft)
   - Iterates up to `maxiter` times (default: 3)

3. **CLI Integration** (`cli/uce_render.py`)
   - `--maxiter` option to control refinement iterations
   - Automatic validation after LLM generation
   - Re-renders after each refinement

## Validation Categories

### 1. Color Contrast
**Detection**: Compares foreground and background colors using RGB distance
**Threshold**: 0.15 (15% similarity maximum)
**Example Issue**:
```
[WARNING] color_contrast: Low contrast: foreground '#333333' and background '#444444' 
are too similar in widget 'title'
Suggestion: Increase contrast for widget 'title': use darker text on light backgrounds 
or lighter text on dark backgrounds. Consider using theme accent colors.
```

### 2. Content Density
**Detection**: Calculates ratio of widget area to total slide area
**Threshold**: 30% minimum coverage
**Example Issue**:
```
[WARNING] content_density: Low content density (18.5%): slide appears empty with only 1 
widgets covering 18.5% of space
Suggestion: Add more content widgets or use a layout strategy with fewer, larger slots. 
Current strategy 'Bento.Standard' may not be optimal for this amount of content.
```

### 3. Widget Overlap
**Detection**: Checks for intersecting widget bounds (indicates text overflow)
**Threshold**: 2px tolerance
**Example Issue**:
```
[ERROR] overlap: Widgets 'title' and 'subtitle' overlap by 60000px - likely due to 
content overflow
Suggestion: Reduce text length in widgets 'title' and/or 'subtitle'. Content is too 
long for assigned space. Cut text by 30-50% or use shorter words.
```

### 4. Style Consistency
**Detection**: Groups widgets by type and compares presets
**Threshold**: All widgets of same type should have matching presets
**Example Issue**:
```
[WARNING] style_consistency: Inconsistent presets for display widgets: ['metric1', 'metric2']
Suggestion: Use consistent visual presets for all display widgets on same slide. Either 
apply same preset to all, or use 'set_preset' for global consistency.
```

## Refinement Workflow

```
1. Generate initial layout with LLM
   ↓
2. Render to RenderableLayout
   ↓
3. Validate (LayoutValidator.validate)
   ↓
4. Issues found? → Format feedback for LLM
   ↓
5. Call LLM with feedback + original prompt
   ↓
6. Apply refinement patch
   ↓
7. Re-render and validate again
   ↓
8. Repeat up to maxiter times or until no issues
```

## LLM Feedback Format

When issues are detected, they are formatted into actionable feedback for the LLM:

```
**LAYOUT VALIDATION ISSUES DETECTED**

Found 2 issue(s) that need correction:

1. [ERROR] overlap
   Problem: Widgets 'title' and 'subtitle' overlap by 150px
   Affected: title, subtitle
   Fix: Reduce text length in widgets by 40-50%

2. [WARNING] color_contrast
   Problem: Low contrast: foreground '#333' and background '#444'
   Affected: title
   Fix: Increase contrast using theme accent colors


**REQUIRED ACTION**:
Generate a new patch that addresses these issues. Focus on:
- SHORTEN TEXT in overlapping widgets by 40-60%
- ADJUST COLORS to improve contrast (use theme variables)
```

## Usage

### CLI

```bash
# Enable refinement with default maxiter=3
python -m cli --source input.txt --output result.html

# Custom refinement iterations
python -m cli --source input.txt --output result.html --maxiter 5

# Disable refinement
python -m cli --source input.txt --output result.html --maxiter 0
```

### Programmatic

```python
from src.generation.content.generator import refine_layout_with_validation
from src.layout.validation import LayoutValidator

# Validate a single layout
issues = LayoutValidator.validate(renderable_layout)

# Run refinement loop
refined_slides = refine_layout_with_validation(
    slides=slides,
    rendered_layouts=renderables,
    atoms=atoms,
    user_instruction="Create slides",
    config=config,
    maxiter=3
)
```

## Test Results

All validation checks working correctly:

✅ **Color Contrast**: Detects #333/#444 as too similar (84% similarity)
✅ **Content Density**: Detects 18.5% coverage as sparse (30% minimum)
✅ **Widget Overlap**: Detects 60000px overlap from bounds intersection
✅ **Style Consistency**: Detects different presets on same widget type

## Configuration

### Validation Thresholds

Located in `src/layout/validation.py`:

```python
COLOR_SIMILARITY_THRESHOLD = 0.15  # Max 15% color similarity
MIN_CONTENT_DENSITY = 0.3          # Min 30% slide coverage
OVERLAP_TOLERANCE = 2              # 2px acceptable overlap
```

### Refinement Settings

CLI option:
- `--maxiter <n>`: Maximum refinement iterations (default: 3)
- Set to 0 to disable refinement

## Benefits

1. **Self-Correcting**: Automatically fixes common layout issues
2. **Quality Assurance**: Ensures minimum standards for:
   - Readability (color contrast)
   - Content density
   - Layout integrity (no overlaps)
   - Visual consistency
3. **Learning Loop**: LLM improves through specific, actionable feedback
4. **Configurable**: Adjust iteration limit based on quality needs

## Future Enhancements

- [ ] Font size validation (minimum readability thresholds)
- [ ] Image quality checks (resolution, aspect ratio)
- [ ] Accessibility scoring (WCAG compliance)
- [ ] Layout balance (weight distribution)
- [ ] Animation performance (frame budget)
