# Research: Extended Chart Types with Intelligent Selection

**Feature**: 003-extended-chart-types  
**Date**: 2025-12-31

## 1. Recharts Capabilities

### Decision
Use Recharts for all 8 chart types.

### Rationale
- Already a dependency in the project (see `package.json`)
- Consistent API across all chart types
- Good React integration with TypeScript support
- Supports all required chart types natively:
  - AreaChart ✅
  - BarChart ✅ (vertical and horizontal via `layout` prop)
  - ScatterChart ✅ (for bubble charts with `ZAxis` for size)
  - PieChart ✅ (pie and doughnut via `innerRadius`)
  - RadarChart ✅
  - RadialBarChart ✅ (for polar area)

### Alternatives Rejected
- **Chart.js**: Requires react-chartjs-2 wrapper, different API patterns
- **D3.js**: Too low-level, requires manual SVG management
- **Victory**: Less popular, fewer examples, different patterns from existing code

### Evidence
Existing components already use Recharts:
- `ChartBar.tsx` uses `BarChart`, `Bar`, `XAxis`, `YAxis`
- `ChartLine.tsx` uses `LineChart`, `Line`
- `ChartPie.tsx` uses `PieChart`, `Pie`, `Cell`

---

## 2. Data Format Patterns

### Decision
Extend existing `ChartDataPoint` type with optional fields for specialized charts.

### Rationale
- Maintains backward compatibility with existing charts
- Single source of truth for chart data types
- TypeScript type safety with optional fields

### Data Format Specification

```typescript
// Base format (existing)
interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
}

// Extended for bubble charts
interface BubbleDataPoint extends ChartDataPoint {
  x: number;
  y: number;
  size: number;
}

// Extended for clustered bar (existing)
interface ClusteredDataPoint extends ChartDataPoint {
  before?: number;
  after?: number;
}

// Radar uses base format - each point is an axis
// Polar uses base format - each point is a segment
// Area uses base format - sequential points
```

### Alternatives Rejected
- Separate types per chart: Increases complexity, harder to switch chart types
- Generic `any[]`: Loses type safety

---

## 3. LLM Chart Selection Strategy

### Decision
Integrate chart selection during MDX generation in `layout_generator.py`.

### Rationale
- LLM already generates MDX content
- Can analyze atom data and visual hints in context
- Natural integration point without new pipeline stages

### Selection Rules

| Data Pattern | Chart Type | Confidence |
|--------------|------------|------------|
| Time-series (dates/months in labels) | `area` or `line` | High |
| Categorical comparison (products, regions) | `bar` | High |
| Proportions summing to ~100% | `pie` or `doughnut` | High |
| 3D data (x, y, size present) | `bubble` | High |
| Multivariate (4+ attributes per item) | `radar` | High |
| Cyclical/periodic (hours, days, months) | `polarArea` | Medium |
| Rankings/sorted comparisons | `barStats` (horizontal) | Medium |
| Unknown pattern | `bar` (fallback) | Low |

### Integration Point
```python
# In layout_generator.py
def generate_slide_mdx(slide, atoms):
    for atom in atoms:
        if atom.visual == "chart" and not atom.chart_type:
            selection = select_chart_type(atom.data, atom.description)
            atom.chart_type = selection.chart_type
    # Continue with MDX generation...
```

### Alternatives Rejected
- Separate chart selection phase: Adds complexity, requires state passing
- Rule-based only (no LLM): Less flexible, can't understand context
- Client-side selection: Too late, loses LLM context

---

## 4. Visual Styling Research

### Earthy Color Palette

Based on the spec requirement for "soft, organic" styling:

```css
:root {
  /* Primary chart colors - warm earthy tones */
  --chart-color-1: #8B7355;  /* Terracotta brown */
  --chart-color-2: #9CAF88;  /* Sage green */
  --chart-color-3: #D4A574;  /* Sand/tan */
  --chart-color-4: #7C9082;  /* Muted teal */
  --chart-color-5: #C4A77D;  /* Warm gold */
  --chart-color-6: #A69076;  /* Dusty rose-brown */
  
  /* Soft styling */
  --chart-border-radius: 8px;
  --chart-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  --chart-fill-opacity: 0.7;
}
```

### Styling Patterns
- Rounded corners on all containers (`border-radius: 8px`)
- Soft drop shadows (subtle, not harsh)
- Gradient fills for area charts
- Translucent bubbles for bubble charts
- Smooth curves (monotone interpolation) for line/area charts
