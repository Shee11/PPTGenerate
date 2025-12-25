# Business Project Components

Professional, corporate-styled Vue components for business presentations.

## Available Components

### Data Display
- **MetricCard** - KPI/metric display with trend indicators
- **ChartWidget** - Bar, line, pie, and donut charts
- **TableWidget** - Professional data tables with formatting
- **StatNumber** - Large stat number with prefix/suffix

### Content
- **QuoteWidget** - Testimonial/quote display
- **IconBox** - Icon with label for features/services
- **CardContainer** - Flexible card wrapper
- **ListItem** - Styled list items with bullets/icons
- **TimelineItem** - Timeline/roadmap entries
- **ProgressBar** - Progress/completion bars

## Usage

Components are auto-imported in Slidev. Use directly in your slides:

```vue
<MetricCard 
  value="$2.4M" 
  label="Revenue" 
  icon="💰" 
  trend="up" 
  trendValue="+12%"
/>

<ChartWidget 
  chartType="bar" 
  title="Sales by Region"
  :data="[
    { label: 'North', value: 75, color: '#0F4C81' },
    { label: 'South', value: 60, color: '#E67E22' },
  ]"
/>

<TableWidget
  title="Performance"
  :columns="[
    { key: 'name', label: 'Product', align: 'left' },
    { key: 'revenue', label: 'Revenue', format: 'currency' },
    { key: 'growth', label: 'Growth', format: 'change' },
  ]"
  :rows="[
    { name: 'Product A', revenue: 125000, growth: 15 },
    { name: 'Product B', revenue: 98000, growth: -5 },
  ]"
/>
```

## Component Variants

### MetricCard
- `default` - Standard card with subtle background
- `bordered` - Primary color border
- `accent` - Left accent bar with gradient
- `minimal` - No background, compact

### TableWidget
- `default` - Clean lines
- `striped` - Alternating row colors
- `bordered` - All borders visible
- `minimal` - No container styling

### QuoteWidget
- `default` - Left border accent
- `boxed` - Contained with top accent
- `minimal` - No background
- `accent` - Gradient background
- `large` - Larger text

## Theme Integration

Components use CSS variables from the business theme:
- `--c-primary` - Primary brand color
- `--c-bg-surface` - Card backgrounds
- `--c-text-primary` - Main text color
- `--c-text-secondary` - Muted text
- `--c-border` - Border color
