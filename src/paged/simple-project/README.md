# Simple Project - Slidev Layouts & Widgets

A clean, minimal Slidev project with simple layouts and reusable widget components.

## Layouts

| Layout | Description | Slots |
|--------|-------------|-------|
| `cover` | Title slide with centered content | `default`, `subtitle`, `footer` |
| `split` | Two-column layout (left-aligned, vertically centered) | `header`, `left`, `right` |
| `centered` | Single centered content area | `header`, `default`, `supporting` |
| `stacked` | Vertical sections (primary above, secondary below) | `header`, `primary`, `secondary` |
| `grid` | Grid layout for cards/metrics | `header`, `default`, `footer` |

### Split Layout Props
- `ratio`: Column ratio - `'50-50'` (default), `'40-60'`, `'60-40'`

### Grid Layout Props
- `columns`: Number of columns - `2` (default), `3`, `4`

## Widgets (Components)

| Widget | Type | Description |
|--------|------|-------------|
| `DisplayWidget` | `Type.Display` | Large display text for titles |
| `HeadingWidget` | `Type.Heading` | Section/slide title (h1-h4) |
| `BodyWidget` | `Type.Body` | Body text block |
| `CaptionWidget` | `Type.Caption` | Small caption text |
| `ListWidget` | `Type.List` | Styled list with optional header |
| `ImageWidget` | `Type.Image` | Image with optional caption |
| `ChartWidget` | `Type.Chart` | Bar/line charts |
| `MetricWidget` | `Type.Metric` | KPI/metric card |
| `BigNumberWidget` | `Type.BigNumber` | Large focal number |
| `QuoteWidget` | `Type.Quote` | Quote/vision statement |
| `CardWidget` | `Type.Card` | Generic card with icon, title, text |
| `NoteWidget` | `Type.Note` | Summary/insight callout |

## Usage Example

```vue
---
layout: split
ratio: '60-40'
---

::header::
# Slide Title

::left::
<ListWidget 
  header="Key Points"
  :items="['Point one', 'Point two', 'Point three']"
/>

::right::
<ImageWidget 
  src="https://example.com/image.jpg"
  alt="Description"
/>
```

## Styling

All components use CSS variables from `SlideShell.vue`:

- `--c-bg-base` - Base background
- `--c-bg-surface` - Surface/card background
- `--c-primary` - Primary accent color
- `--c-accent` - Secondary accent color
- `--c-text` - Main text color
- `--c-text-muted` - Muted text color
- `--c-text-dim` - Dim text color
- `--c-border` - Border color
- `--font-heading` - Heading font family
- `--font-body` - Body font family

## Themes

Available themes (passed via `theme` prop):
- `default` - Dark blue professional
- `light` - Clean white/light
- `dark` - Pure dark with cyan accent
