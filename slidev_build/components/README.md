# Slidev Custom Components

This directory contains reusable Vue components for Slidev presentations.

## Available Components

### ChartWidget

Data visualization component supporting bar, line, pie, and donut charts.

**Props:**
- `chartType`: `'bar' | 'line' | 'pie' | 'donut'` (default: 'bar')
- `title`: Chart title (optional)
- `data`: Array of `{ label: string, value: number, color?: string }`
- `unit`: Unit suffix (default: '%')
- `color`: Primary color for line charts
- `width`, `height`: Dimensions for line charts (default: 400x200)

**Usage:**
```vue
<ChartWidget
  chartType="bar"
  title="Quarterly Growth"
  :data="[
    { label: 'Q1', value: 85, color: '#3b82f6' },
    { label: 'Q2', value: 92, color: '#10b981' },
    { label: 'Q3', value: 78, color: '#f59e0b' },
    { label: 'Q4', value: 95, color: '#8b5cf6' }
  ]"
/>
```

---

### TableWidget

Data table component with multiple formatting options.

**Props:**
- `title`: Table title (optional)
- `variant`: `'default' | 'striped' | 'bordered' | 'minimal'` (default: 'default')
- `showHeader`: Show table header (default: true)
- `columns`: Array of column definitions
  - `key`: Data key
  - `label`: Column label
  - `align`: `'left' | 'center' | 'right'` (default: 'left')
  - `format`: `'text' | 'badge' | 'number' | 'percent' | 'change'` (default: 'text')
- `rows`: Array of data objects

**Column Formats:**
- `text`: Plain text
- `badge`: Colored badge (use `_variant` suffix for color: success, warning, error, info)
- `number`: Formatted number with thousands separator
- `percent`: Percentage display
- `change`: Up/down indicator with color coding

**Usage:**
```vue
<TableWidget
  title="Sales Performance"
  variant="striped"
  :columns="[
    { key: 'product', label: 'Product', align: 'left' },
    { key: 'sales', label: 'Sales', align: 'right', format: 'number' },
    { key: 'change', label: 'Change', align: 'right', format: 'change' },
    { key: 'status', label: 'Status', align: 'center', format: 'badge' }
  ]"
  :rows="[
    { product: 'Widget A', sales: 12500, change: 15.2, status: 'Active', status_variant: 'success' },
    { product: 'Widget B', sales: 8300, change: -3.5, status: 'Pending', status_variant: 'warning' }
  ]"
/>
```

---

### QuoteWidget

Quote/testimonial display component with multiple style variants.

**Props:**
- `text`: Quote text (required)
- `author`: Author name (optional)
- `attribution`: Role, company, or context (optional)
- `variant`: `'default' | 'minimal' | 'boxed' | 'accent' | 'large'` (default: 'default')
- `showIcon`: Show quotation mark icon (default: true)

**Variants:**
- `default`: Standard quote with icon
- `minimal`: Clean, borderless style
- `boxed`: Quote in colored box
- `accent`: Full-color background
- `large`: Larger text sizes

**Usage:**
```vue
<QuoteWidget
  text="This solution transformed our workflow and saved us countless hours every week."
  author="Jane Smith"
  attribution="CTO, Tech Corp"
  variant="accent"
/>
```

---

### MetricWidget

KPI/metric display component with trend indicators.

**Props:**
- `label`: Metric label (required)
- `value`: Metric value - string or number (required)
- `change`: Percentage change (optional)
- `changeLabel`: Change context, e.g., "vs last month" (optional)
- `subtitle`: Additional context (optional)
- `icon`: `'trend-up' | 'trend-down' | 'users' | 'dollar' | 'chart'` (optional)
- `variant`: `'default' | 'compact' | 'large' | 'card'` (default: 'default')

**Variants:**
- `default`: Standard metric card
- `compact`: Smaller padding and font sizes
- `large`: Larger value display
- `card`: White card with shadow and hover effect

**Usage:**
```vue
<MetricWidget
  label="Total Revenue"
  value="$2.3M"
  :change="18.5"
  changeLabel="vs last quarter"
  subtitle="Exceeds Q4 target by 12%"
  icon="dollar"
  variant="card"
/>
```

---

## Theme Integration

All components automatically use Slidev theme colors via CSS variables:

- `--slidev-theme-primary`: Primary brand color
- `--slidev-theme-background`: Background color
- `--slidev-theme-text`: Text color

These are injected by the markdown renderer based on the generated theme.

---

## Importing Components

Components are automatically available in all slides. No import needed.

Just use them directly in your markdown:

```md
---
layout: smart-grid
---

::header::
# Dashboard

::col1::
<MetricWidget label="Users" value="12.5K" :change="23" icon="users" />

::col2::
<MetricWidget label="Revenue" value="$1.2M" :change="15" icon="dollar" />

::col3::
<ChartWidget chartType="line" :data="[...]" />
```

---

## Development

### File Structure
```
slidev_build/
├── components/
│   ├── ChartWidget.vue
│   ├── TableWidget.vue
│   ├── QuoteWidget.vue
│   ├── MetricWidget.vue
│   └── README.md (this file)
└── layouts/
    ├── smart-grid.vue
    ├── hero-split.vue
    └── ...
```

### Adding New Components

1. Create `.vue` file in `components/` directory
2. Use Vue 3 Composition API (`<script setup>`)
3. Include scoped styles using Tailwind CSS classes
4. Reference theme CSS variables for colors
5. Update `layout_engine.py` documentation
6. Add usage example to this README

---

## Notes

- All components use Vue 3 Composition API
- Styling uses Tailwind CSS utility classes and scoped CSS
- Icons use inline SVG for zero dependencies
- Components are responsive by default
- Theme colors applied via CSS custom properties
