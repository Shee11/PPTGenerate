# Quickstart: MDX Direct Output

## Overview

MDX Direct Output allows LLMs to generate React MDX markup directly instead of JSON widget definitions. This eliminates the JSON-to-MDX conversion step in the rendering pipeline.

## Enabling MDX Output

Set project type to `react-mdx`:

```python
from src.generation.content.generator import generate_slides

slides = generate_slides(
    atoms=atoms,
    user_instruction="Create a pitch deck",
    project="react-mdx"  # Enable MDX output
)
```

## State Format

With MDX output, slides are stored with an `mdx` field:

```json
{
  "slides": [
    {
      "id": "slide_01",
      "rank": 1,
      "story": "HOOK",
      "atoms": ["stat_001"],
      "mdx": "<LayoutCover><Heading level={1}>Hello World</Heading></LayoutCover>"
    }
  ]
}
```

## Writing MDX Content

### Layout Structure

Every slide starts with a Layout component:

```mdx
<LayoutSplit ratio="2:1">
  <Left>
    <!-- Left content -->
  </Left>
  <Right>
    <!-- Right content -->
  </Right>
</LayoutSplit>
```

### Available Layouts

| Layout | Use Case |
|--------|----------|
| `<LayoutCover>` | Title slides, section breaks |
| `<LayoutSplit ratio="1:1\|2:1\|1:2">` | Two-column content |
| `<LayoutStacked>` | Vertical content flow |
| `<LayoutGrid cols={2\|3\|4}>` | Multi-column grid |
| `<LayoutFullBleed image="...">` | Background image |
| `<LayoutDashboard>` | KPI dashboards |
| `<LayoutTimeline>` | Chronological content |

### Content Components

```mdx
<!-- Metrics -->
<BigNum id="stat_001" value="42%" label="Growth"/>
<MetricGroup id="metrics_001" cols={3}>
  <Metric value="$1M" label="Revenue"/>
</MetricGroup>

<!-- Lists -->
<SmartList id="list_001" items={["Point 1", "Point 2"]}/>

<!-- Charts -->
<ChartBar id="chart_001" data={[{name: "Q1", value: 100}]}/>

<!-- Text -->
<Heading level={1}>Title</Heading>
<Text>Body content</Text>
```

## Refinement with Patches

To update specific elements, use Patch format:

```xml
<Patch id="stat_001">
  <BigNum value="95%" label="Updated Growth"/>
</Patch>
```

The patch system finds the element with `id="stat_001"` and replaces it.

## ID Requirements

All patchable elements MUST have `id` attributes:

```mdx
<!-- ✅ Correct: Has ID for patching -->
<BigNum id="stat_001" value="42%"/>

<!-- ❌ Wrong: No ID, cannot be patched -->
<BigNum value="42%"/>
```

## Comparison: JSON vs MDX

### JSON Mode (slidev)
```json
{
  "layout": "split",
  "widgets": {
    "Left": {"type": "Type.Heading", "parameters": {"text": "Title"}},
    "Right": {"type": "Data.BigNum", "parameters": {"value": "42%"}}
  }
}
```

### MDX Mode (react-mdx)
```mdx
<LayoutSplit ratio="1:1">
  <Left><Heading>Title</Heading></Left>
  <Right><BigNum id="stat_001" value="42%"/></Right>
</LayoutSplit>
```

## Benefits

1. **Natural syntax**: LLMs understand JSX/HTML from training data
2. **No conversion**: MDX renders directly without transformation
3. **Human editable**: Designers can modify MDX manually
4. **Targeted patches**: Update specific elements without regenerating
