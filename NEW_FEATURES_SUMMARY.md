# New Features Summary

## Comparison Widget (Type.Comparison)

### Implementation
- **File**: `src/widgets/comparison.py`
- **Widget Type**: `Type.Comparison`
- **Minimum Size**: M (medium)
- **Template**: `src/render/templates/widgets/comparison.html.j2`

### Parameters
- `left_title`: Title for left column
- `left_items`: List of bullet points for left column
- `right_title`: Title for right column
- `right_items`: List of bullet points for right column
- `left_color`: CSS color for left title (default: red #ef4444)
- `right_color`: CSS color for right title (default: green #22c55e)
- `bottom_note`: Optional note displayed below both columns

### Features
- Side-by-side two-column grid layout
- Custom colored titles for each column
- Bullet lists with custom styling
- Optional bottom note section
- Responsive measurement based on content

### Usage Example
```json
{
  "type": "Type.Comparison",
  "parameters": {
    "left_title": "From Building...",
    "left_items": [
      "Writing every function from scratch",
      "Stitching together APIs manually"
    ],
    "right_title": "To Composing...",
    "right_items": [
      "Describing what you want in plain language",
      "Letting AI generate boilerplate code"
    ],
    "left_color": "#EF4444",
    "right_color": "#10B981",
    "bottom_note": "We shift from micro-optimization to macro-orchestration."
  }
}
```

## Bento.VerticalStack Layout

### Implementation
- **File**: `src/layout/strategies/bento.py` (lines 290-368)
- **Strategy Name**: `Bento.VerticalStack`
- **Template**: `src/render/templates/layouts/bento.html.j2`

### Slots
- `stage_1`: Size M
- `stage_2`: Size M
- `stage_3`: Size M
- `stage_4`: Size M

### Features
- Horizontal pipeline layout
- 3-5 stages supported (dynamically sized)
- Equal-width stages
- Arrow separators between stages
- Perfect for process flows, pipelines, transformation sequences

### Layout Behavior
- Stages are arranged horizontally in a row
- Each stage gets equal width: `content_width / num_stages`
- Arrows (`→`) are rendered between stages
- CSS Flexbox layout with space-between alignment

### Usage Example
```json
{
  "strategy": "Bento.VerticalStack",
  "widgets": {
    "stage_1": {
      "type": "Type.Heading",
      "parameters": {"text": "Collect Data", "level": 3}
    },
    "stage_2": {
      "type": "Type.Heading",
      "parameters": {"text": "Train Model", "level": 3}
    },
    "stage_3": {
      "type": "Type.Heading",
      "parameters": {"text": "Tune Parameters", "level": 3}
    },
    "stage_4": {
      "type": "Type.Heading",
      "parameters": {"text": "Deploy", "level": 3}
    }
  }
}
```

## Additional Changes

### Default Widget Styles (CLI Enhancement)
- **File**: `cli/uce_render.py` (lines 508-527)
- Added automatic default widget styles injection when config doesn't provide them
- Prevents "No style defined for widget type" errors
- Supports all widget types: Type.Display, Type.Heading, Type.Body, Type.Caption, Type.Quote, Type.List, Type.Comparison, Data.BigNum, Data.Metric, Data.Table, Data.Chart

### Prompts Update
- **File**: `src/generation/content/prompts.py`
- Added Type.Comparison widget guidance for LLM content generation
- Added Bento.VerticalStack layout recommendation for process flows
- Removed deprecated Comparison.TwoColumn layout references

### CSS Styling
- **File**: `src/render/templates/base.html.j2`
- Added comprehensive CSS for comparison widget:
  - `.widget-comparison` container
  - `.comparison-grid` - two-column grid
  - `.comparison-column` - column styling
  - `.comparison-title` - colored titles
  - `.comparison-list` - custom bullet styling
  - `.comparison-note` - bottom note styling

### Widget Dispatcher
- **File**: `src/render/templates/widgets/_widget_content.html.j2`
- Updated routing to check Type.Comparison before generic Type.* pattern
- Ensures comparison.html.j2 template is used for Type.Comparison widgets

## Testing

### Test File
- **File**: `data/test_new_features.json`
- Contains two slides:
  1. Comparison widget test using Bento.HeroLeft layout
  2. VerticalStack layout test with 4-stage pipeline

### Output
- **File**: `output/test_new_features.html`
- Successfully generates HTML with both features
- Comparison widget renders with grid layout, colored titles, and bottom note
- VerticalStack renders with horizontal pipeline and arrow separators

## Files Modified

1. `src/widgets/comparison.py` - NEW
2. `src/render/templates/widgets/comparison.html.j2` - NEW
3. `src/widgets/__init__.py` - Added ComparisonWidget import
4. `src/layout/strategies/bento.py` - Added BentoVerticalStackStrategy
5. `src/render/templates/layouts/bento.html.j2` - Added VerticalStack rendering
6. `src/layout/layout_engine.py` - Registered BentoVerticalStackStrategy
7. `src/generation/content/prompts.py` - Updated widget/layout guidance
8. `src/render/templates/base.html.j2` - Added comparison widget CSS
9. `src/render/templates/widgets/_widget_content.html.j2` - Fixed widget routing
10. `cli/uce_render.py` - Added default widget styles, fixed Patch import bug
11. `data/test_new_features.json` - NEW test configuration

## Reference
- Baseline Page 4: Two-column comparison grid with colored headers
- Baseline Page 3: Horizontal pipeline flow with equal-width stages
