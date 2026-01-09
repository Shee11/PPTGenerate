# Data Model: Extended Chart Types

**Feature**: 003-extended-chart-types  
**Version**: 1.0.0

## Entity Definitions

### 1. ChartType Enum

**Description**: Enumeration of all supported chart types  
**Location**: `src/paged/render/react/types/chart.ts`

| Value | Display Name | Description |
|-------|--------------|-------------|
| `area` | Area Chart | Filled line for cumulative trends |
| `bar` | Bar Chart | Vertical bars for comparison |
| `barStats` | Bar Stats | Horizontal bars with stats/labels |
| `bubble` | Bubble Chart | Scatter with size dimension |
| `doughnut` | Doughnut Chart | Pie with center hole |
| `pie` | Pie Chart | Proportional segments |
| `line` | Line Chart | Trend lines (existing) |
| `polarArea` | Polar Area | Radial segments |
| `radar` | Radar Chart | Multi-axis polygon |

### 2. ChartDataPoint (Extended)

**Description**: Base data structure for chart data points  
**Location**: `src/paged/render/react/types/chart.ts`

```typescript
interface ChartDataPoint {
  label: string;           // Required: Display label
  value: number;           // Required: Primary value
  color?: string;          // Optional: Override color
  
  // Cluster chart extensions
  before?: number;         // Optional: "Before" value
  after?: number;          // Optional: "After" value
  
  // Bubble chart extensions
  x?: number;              // Optional: X coordinate
  y?: number;              // Optional: Y coordinate
  size?: number;           // Optional: Bubble size
}
```

### 3. ChartSelectionContext

**Description**: Context provided to LLM for chart type selection  
**Location**: `src/generation/content/chart_selector.py`

| Field | Type | Description |
|-------|------|-------------|
| `data` | `List[Dict]` | The raw data points |
| `description` | `str` | Human description of data |
| `slide_context` | `str` | Surrounding slide content |
| `suggested_type` | `Optional[str]` | Hint from author |

### 4. ChartSelectionResult

**Description**: Result from LLM chart type selection  
**Location**: `src/generation/content/chart_selector.py`

| Field | Type | Description |
|-------|------|-------------|
| `chart_type` | `str` | Selected chart type |
| `confidence` | `float` | Confidence score 0-1 |
| `reasoning` | `str` | Explanation for selection |

---

## Relationships

```
ChartBlock (MDX)
    ├── type: ChartType
    ├── data: ChartDataPoint[]
    └── options?: ChartOptions

ChartSelectionContext
    ├── data → ChartDataPoint[]
    └── result → ChartSelectionResult
```

---

## State Transitions

### Chart Type Selection Flow

```
START
  ↓
[Content Generation]
  ↓
Has explicit chart_type? ─── YES ──→ Use specified type
  │ NO
  ↓
[Chart Selector LLM Call]
  ↓
Confidence > 0.7? ─── YES ──→ Use selected type
  │ NO
  ↓
Use "bar" (default fallback)
  ↓
END → Chart type assigned
```

---

## Validation Rules

### ChartDataPoint Validation

| Rule | Field(s) | Condition |
|------|----------|-----------|
| V-001 | `value` | Must be numeric, not NaN |
| V-002 | `label` | Must be non-empty string |
| V-003 | `x`, `y` (bubble) | Required together if bubble chart |
| V-004 | `size` (bubble) | Must be positive if specified |
| V-005 | `before`, `after` | Must be numeric if specified |

### ChartType Validation

| Rule | Condition |
|------|-----------|
| V-010 | Must be one of defined enum values |
| V-011 | If `bubble`, data must have x, y, size fields |
| V-012 | If `radar`, data should have 3+ points |
