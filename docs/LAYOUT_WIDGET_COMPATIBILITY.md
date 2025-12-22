# Layout-Widget Compatibility System

## Problem
Widgets don't always fit well in their assigned layout slots. For example:
- **Quote widgets** (100-250 chars) placed in narrow grid columns → text overflow, poor readability
- **Tables** placed in split layouts → cramped, unreadable
- **Long body text** in timeline steps → overflow

## Root Cause
The LLM selects layouts based on visual_design intent but doesn't validate that widget types are compatible with slot dimensions.

## Solution: Three-Tier Approach

### 1. **Prevention** (Primary): LLM Prompt Guidance ✅ IMPLEMENTED
**File**: `src/generation/content/prompts.py`

Added comprehensive layout-widget compatibility rules to slide generation prompt:

```
**LAYOUT-WIDGET COMPATIBILITY** (CRITICAL):
⚠️ Quote widgets need WIDE space - quotes are typically 100-250 characters:
  ✅ GOOD: QuoteWidget in full-bleed, hero-split (right), center, default
  ❌ BAD: QuoteWidget in smart-grid columns (too narrow!)

⚠️ Grid columns are NARROW - only short content:
  ✅ GOOD: Heading (2-5 words), Body (5-10 words), MetricWidget  
  ❌ BAD: Quote, Table, Code in grids

**Layout Selection Checklist**:
1. Quote? → MUST use full-bleed/hero-split/center
2. Table? → MUST use full-bleed/default
3. 3-4 metrics? → Use smart-grid with MetricWidgets
4. Using smart-grid? → ALL widgets SHORT (NO quotes!)
```

**Impact**: LLM will now avoid placing quotes in grids

### 2. **Detection** (Validation): Automated Checker ✅ IMPLEMENTED
**Files**: 
- `src/layout/slidev/layout_validator.py` - Validation logic
- `src/layout/slidev/validate_slides.py` - CLI tool

**Features**:
- Validates widget types against slot constraints
- Checks content length vs slot width
- Suggests better layouts when mismatches detected

**Usage**:
```bash
# Check for issues
python -m src.layout.slidev.validate_slides output/debug_content.json

# Auto-fix issues
python -m src.layout.slidev.validate_slides output/debug_content.json --fix
```

**Example Output**:
```
❌ Slide 3 (slide_3): smart-grid layout
  Widgets:
    • col4: QuoteWidget (150 chars)
  Issues:
    ⚠️ QuoteWidget in smart-grid.col4 (too narrow)
  💡 Suggested: full-bleed, hero-split, center
```

### 3. **Correction** (Runtime): Widget Adaptation 🔄 TODO
**Approach**: CSS-based responsive widgets

For widgets that don't fit, apply adaptive styling:

```css
/* Quote widget in narrow slot - reduce font size, remove icon */
.grid-cell .quote-widget {
  font-size: 0.9rem;  /* Smaller than default 1.2rem */
  padding: 1rem;      /* Reduced padding */
}

.grid-cell .quote-widget .quote-icon {
  display: none;      /* Hide decorative icon */
}
```

**Implementation Plan** (Future):
1. Add `data-slot-width` attribute to slot containers
2. Widgets detect slot width via CSS container queries
3. Apply adaptive styles automatically

## Constraint Definitions

### Widget Space Requirements
| Widget Type    | Width Required | Typical Chars |
|----------------|----------------|---------------|
| **QuoteWidget**| wide (>600px)  | 100-250       |
| **TableWidget**| wide (>800px)  | 200-400       |
| **Type.Code**  | wide (>700px)  | 200-500       |
| **MetricWidget**| narrow (200px)| 20-50         |
| **Type.Body**  | medium (400px) | 100-300       |
| **Type.Heading**| medium (300px)| 30-60         |

### Layout Slot Widths
| Layout        | Slot Name | Width    | Max Chars |
|---------------|-----------|----------|-----------|
| smart-grid    | col1-4    | narrow   | 150       |
| hero-split    | left      | medium   | 200       |
| hero-split    | right     | medium   | 300       |
| timeline      | step1-6   | narrow   | 100       |
| full-bleed    | default   | full     | 500       |
| default       | default   | full     | 400       |

## Recommendations

### For Quote-Heavy Slides
✅ **Best Layouts**:
1. `full-bleed` - Quote takes entire slide with dramatic styling
2. `hero-split` (right slot) - Quote on right, context on left
3. `center` - Centered quote with minimal distractions
4. `default` - Standard single-column layout

❌ **Avoid**:
- `smart-grid` (columns too narrow)
- `timeline` (steps too narrow)
- `feature-grid` (boxes too small)

### For Multi-Metric Slides
✅ **Best Layouts**:
1. `smart-grid` (3-4 cols) - Perfect for MetricWidgets
2. `dashboard` - Designed for metrics display
3. `feature-grid` - Card-based metric display

### For Tables/Code
✅ **Best Layouts**:
1. `full-bleed` - Maximum width for content
2. `default` - Standard single-column
3. `two-cols` - Code left, explanation right

## Testing

Run validator on generated slides:
```bash
# Generate slides
python -m cli.uce_render --source data/context/career_talk.txt \\
  --user-instruction "Create presentation" \\
  --layout-engine slidev \\
  --output output/test.html

# Validate
python -m src.layout.slidev.validate_slides output/debug_content.json
```

Expected: 0 layout-widget compatibility issues

## Success Metrics

1. **Prevention Rate**: % of slides generated without compatibility issues
   - Target: >90% (LLM follows compatibility rules)
   
2. **Detection Accuracy**: % of issues correctly identified by validator
   - Target: 100% (comprehensive rule coverage)
   
3. **User Experience**: No visible text overflow or cramped layouts
   - Target: Professional appearance on all slides

## Integration Points

### Current Implementation
- ✅ Prompt guidance added to `_build_slide_generation_system_prompt()`
- ✅ Validator available via CLI
- ✅ Constraint definitions in `layout_validator.py`

### Future Enhancements
1. **Auto-validation in pipeline**: Run validator after slide generation, before rendering
2. **Auto-fix mode**: Automatically switch layouts when issues detected
3. **Widget adaptation**: CSS container queries for responsive widget sizing
4. **Layout hints in UI**: Show compatibility warnings in real-time
