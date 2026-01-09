# Quickstart: Extended Chart Types

## Overview

This feature adds 8 chart types and intelligent LLM-based chart selection.

## Quick Test

### 1. New Chart Components

After implementation, test each chart type in MDX:

```mdx
<ChartArea data={[{label: "Q1", value: 100}, {label: "Q2", value: 150}]} />
<ChartBubble data={[{label: "A", x: 10, y: 20, size: 30}]} />
<ChartPolar data={[{label: "North", value: 40}, {label: "East", value: 60}]} />
<ChartRadar data={[{label: "Speed", value: 80}, {label: "Power", value: 70}]} />
<BarStats data={[{label: "Item A", value: 95}, {label: "Item B", value: 87}]} />
```

### 2. Auto Chart Selection

When no chart type is specified in content, the LLM will automatically select based on data patterns:

| Data Pattern | Auto-Selected Chart |
|--------------|---------------------|
| Time-series data | Area or Line |
| Category comparison | Bar |
| Percentages summing to 100% | Pie/Doughnut |
| 3D data (x, y, size) | Bubble |
| Multi-attribute comparison | Radar |

### 3. Run Tests

```bash
# Run chart component tests (from src/paged/render/react directory)
cd src/paged/render/react
npm run test -- Chart

# Run chart selector tests (from repo root)
pytest tests/test_chart_selector.py -v

# Or run all Python tests
pytest tests/ -v -k "chart"
```

## File Locations

| File | Purpose |
|------|---------|
| `src/paged/render/react/components/blocks/ChartArea.tsx` | Area chart component |
| `src/paged/render/react/components/blocks/ChartBubble.tsx` | Bubble chart component |
| `src/paged/render/react/components/blocks/ChartPolar.tsx` | Polar area component |
| `src/paged/render/react/components/blocks/ChartRadar.tsx` | Radar chart component |
| `src/paged/render/react/components/blocks/BarStats.tsx` | Horizontal bar stats |
| `src/generation/content/chart_selector.py` | LLM chart selection |

## Dependencies

No new dependencies required - uses existing:
- `recharts` (npm)
- `openai` (pip) - for LLM selection
