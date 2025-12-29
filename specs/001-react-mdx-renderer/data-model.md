# Data Model: React MDX Presentation Renderer

**Date**: 2025-12-25  
**Feature**: 001-react-mdx-renderer  
**Status**: Complete

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Presentation                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ id: string                                                           │    │
│  │ meta: Meta                                                           │    │
│  │ constitution: Constitution                                           │    │
│  │ themes: Map<string, Theme>                                           │    │
│  │ active_theme_id: string                                              │    │
│  │ slides: Slide[]                                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ 1:N
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                  Slide                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ id: string                                                           │    │
│  │ rank: number                                                         │    │
│  │ layout: LayoutType                                                   │    │
│  │ widgets: Map<SlotName, Widget>                                       │    │
│  │ parameters: SlideParameters                                          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ 1:N
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                  Widget                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ type: WidgetType                                                     │    │
│  │ parameters: WidgetParameters                                         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Entities

### 1. Presentation (Root)

The top-level container representing a complete slide deck.

```typescript
interface Presentation {
  meta: {
    id: string;
    created_at: string;      // ISO 8601
    updated_at: string;      // ISO 8601
    version: string;
  };
  
  source?: {
    path: string;
    content_hash: string;
    content_type: string;
  };
  
  constitution: {
    tone: 'professional' | 'casual' | 'academic' | 'playful';
    target_slides: number;
    style_rules: string[];
    selected_theme: string;
    selected_vibe: VibeType;
  };
  
  themes: Record<string, Theme>;
  active_theme_id: string;
  project: string;           // 'react-mdx'
  
  slides: Slide[];
}
```

**Relationships**:
- Contains 1:N `Slide` entities
- References 1:N `Theme` entities (one active)

---

### 2. Slide

A single page in the presentation with layout and content.

```typescript
interface Slide {
  id: string;                // e.g., "slide_01_cover"
  rank: number;              // Display order (1-based)
  state: 'active' | 'draft' | 'archived';
  
  // Content metadata
  story: string;             // Brief description
  atoms: string[];           // Source fact IDs
  density: 'minimal' | 'moderate' | 'dense';
  visual_design: string;     // Layout description
  
  // Layout & content
  layout: LayoutType;
  widgets: Record<SlotName, Widget>;
  
  // Styling
  parameters: {
    theme: string;
    vibe: VibeType;
    background?: string;     // Optional override
  };
}

type LayoutType = 
  | 'cover'
  | 'split'
  | 'stacked'
  | 'grid'
  | 'full-bleed'
  | 'timeline'
  | 'dashboard'
  | 'quote-hero'
  | 'spotlight';

type SlotName = 
  | 'title'
  | 'subtitle'
  | 'left'
  | 'right'
  | 'content'
  | 'header'
  | 'footer'
  | 'note'
  | 'stat1' | 'stat2' | 'stat3'
  | 'chart'
  | 'quote'
  | 'attribution';
```

**Relationships**:
- Belongs to 1 `Presentation`
- Contains 1:N `Widget` entities (keyed by slot name)

---

### 3. Widget

A content element that renders in a specific layout slot.

```typescript
interface Widget {
  type: WidgetType;
  parameters: WidgetParameters;
}

// Widget types (matching existing state.json)
type WidgetType =
  // Typography (L3 atoms)
  | 'Type.Display'
  | 'Type.Heading'
  | 'Type.Body'
  | 'Type.Caption'
  | 'Type.Note'
  
  // Lists & Content (L2 blocks)
  | 'Type.List'
  | 'Type.Quote'
  | 'Type.Image'
  
  // Data Visualization (L2 blocks)
  | 'Type.Metric'
  | 'Type.BigNumber'
  | 'Type.Chart'
  | 'Type.Table';

// Parameters vary by type
type WidgetParameters = 
  | TextParameters
  | ListParameters
  | ImageParameters
  | MetricParameters
  | ChartParameters
  | TableParameters;

interface TextParameters {
  text: string;
  level?: 1 | 2 | 3 | 4 | 5 | 6;  // For headings
}

interface ListParameters {
  items: string[];
  ordered?: boolean;
}

interface ImageParameters {
  src: string;
  alt: string;
  caption?: string;
}

interface MetricParameters {
  value: string;
  label: string;
  change?: number;
  changeLabel?: string;
}

interface ChartParameters {
  chartType: 'bar' | 'line' | 'pie' | 'donut';
  title?: string;
  data: {
    labels: string[];
    values: number[];
  };
}

interface TableParameters {
  columns: string[];
  rows: string[][];
  showHeader?: boolean;
}
```

**Relationships**:
- Belongs to 1 `Slide` (in a named slot)
- Maps to 1 React component (L2 or L3)

---

### 4. Theme

Visual styling configuration using CSS custom properties.

```typescript
interface Theme {
  id: string;                // e.g., "business"
  name: string;              // Display name
  
  colors: {
    // Backgrounds
    bgBase: string;          // Main background
    bgSurface: string;       // Cards, panels
    bgElevated: string;      // Elevated surfaces
    
    // Accents
    primary: string;         // Primary brand color
    accent: string;          // Secondary accent
    success: string;
    warning: string;
    danger: string;
    
    // Text
    text: string;            // Primary text
    textMuted: string;       // Secondary text
    textDim: string;         // Tertiary text
    
    // Borders
    border: string;
    borderSubtle: string;
  };
  
  typography: {
    fontBody: string;        // Font stack for body text
    fontHeading: string;     // Font stack for headings
    fontMono: string;        // Font stack for code
  };
  
  effects: {
    // Shadows
    shadowSm: string;
    shadowMd: string;
    shadowLg: string;
    shadowGlow: string;
    
    // Border radius
    radiusSm: string;
    radiusMd: string;
    radiusLg: string;
    radiusXl: string;
  };
}
```

**Relationships**:
- Referenced by `Presentation` (collection)
- Applied to `Slide` via parameters.theme

---

### 5. Vibe

Density/complexity modifier applied to layouts.

```typescript
type VibeType = 'minimal' | 'clean' | 'balanced' | 'decorative' | 'expressive';

interface VibeConfig {
  padding: string;           // CSS padding value
  fontSize: string;          // Base font size
  borderWidth: string;       // Border thickness
  decorations: boolean;      // Gradients, glows, etc.
  uppercase: boolean;        // Uppercase headings
}

const VIBE_CONFIGS: Record<VibeType, VibeConfig> = {
  minimal: {
    padding: '1rem',
    fontSize: '0.65rem',
    borderWidth: '0',
    decorations: false,
    uppercase: false,
  },
  clean: {
    padding: '1.5rem',
    fontSize: '0.7rem',
    borderWidth: '1px',
    decorations: false,
    uppercase: false,
  },
  balanced: {
    padding: '2rem',
    fontSize: '0.75rem',
    borderWidth: '1px',
    decorations: false,
    uppercase: false,
  },
  decorative: {
    padding: '2.5rem',
    fontSize: '0.8rem',
    borderWidth: '2px',
    decorations: true,
    uppercase: false,
  },
  expressive: {
    padding: '3rem',
    fontSize: '0.875rem',
    borderWidth: '3px',
    decorations: true,
    uppercase: true,
  },
};
```

**Relationships**:
- Applied to `Slide` via parameters.vibe
- Modifies visual output of all components

---

## Component Layer Mapping

### L1: Layouts (Page Structure)

| LayoutType | React Component | Slots |
|------------|-----------------|-------|
| `cover` | `LayoutCover` | title, subtitle, footer |
| `split` | `LayoutSplit` | left, right, header |
| `stacked` | `LayoutGrid` | header, content, footer |
| `grid` | `LayoutGrid` | col1, col2, col3, col4 |
| `full-bleed` | `LayoutFullBleed` | content, overlay |
| `timeline` | `LayoutTimeline` | header, step1-4 |
| `dashboard` | `LayoutDashboard` | header, metric1-4, chart |

### L2: Blocks (Content Grouping)

| WidgetType | React Component | Primary Props |
|------------|-----------------|---------------|
| `Type.List` | `SmartList` | items, ordered |
| `Type.Quote` | `QuoteBlock` | text, author, attribution |
| `Type.Image` | `ImageBlock` | src, alt, caption |
| `Type.Metric` | `MetricGroup` | metrics[] |
| `Type.Chart` | `ChartBar/Line/Pie` | data, title |
| `Type.Table` | `TableData` | columns, rows |

### L3: Atoms (Typography)

| WidgetType | React Component | Primary Props |
|------------|-----------------|---------------|
| `Type.Display` | `Heading` | level=1 |
| `Type.Heading` | `Heading` | level |
| `Type.Body` | `Text` | variant="default" |
| `Type.Caption` | `Text` | variant="caption" |
| `Type.Note` | `Callout` | intent="info" |

---

## Validation Rules

### Slide Validation

1. **Layout required**: Every slide must have a `layout` field
2. **Widget types**: All widget types must be from allowed list
3. **Slot names**: Slots must match layout's expected slots
4. **Theme reference**: `parameters.theme` must exist in presentation's themes

### Widget Validation

1. **Required parameters**: Each widget type has required parameters
2. **Type coercion**: Numbers must be numbers, strings must be strings
3. **Array items**: List items and chart data must be non-empty

### Theme Validation

1. **Color format**: All colors must be valid CSS (hex, rgb, hsl)
2. **Font stacks**: Font families must be quoted if multi-word
3. **Required fields**: All color and typography fields must be present

---

## State Transitions

```
                    ┌─────────────────┐
                    │  state.json     │
                    │  (Input)        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Validation     │
                    │  (L0 Check)     │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
           ┌───────────────┐  ┌───────────────┐
           │  Valid MDX    │  │  Error Report │
           │  Generation   │  │  (Line nums)  │
           └───────┬───────┘  └───────────────┘
                   │
                   ▼
           ┌───────────────┐
           │  .mdx Files   │
           │  (Per slide)  │
           └───────┬───────┘
                   │
                   ▼
           ┌───────────────┐
           │  Next.js      │
           │  Build        │
           └───────┬───────┘
                   │
                   ▼
           ┌───────────────┐
           │  Static HTML  │
           │  (Output)     │
           └───────────────┘
```

---

## Example: Complete Slide Entity

```json
{
  "id": "slide_03_metrics",
  "rank": 3,
  "state": "active",
  "story": "Show key business metrics",
  "atoms": ["metric_001", "metric_002"],
  "density": "dense",
  "visual_design": "Dashboard layout with metrics and chart",
  "layout": "dashboard",
  "widgets": {
    "header": {
      "type": "Type.Heading",
      "parameters": {
        "text": "Q4 Performance Metrics",
        "level": 2
      }
    },
    "stat1": {
      "type": "Type.Metric",
      "parameters": {
        "value": "$2.4M",
        "label": "Revenue",
        "change": 12,
        "changeLabel": "vs Q3"
      }
    },
    "stat2": {
      "type": "Type.Metric",
      "parameters": {
        "value": "89%",
        "label": "Customer Satisfaction"
      }
    },
    "chart": {
      "type": "Type.Chart",
      "parameters": {
        "chartType": "bar",
        "title": "Monthly Revenue",
        "data": {
          "labels": ["Oct", "Nov", "Dec"],
          "values": [750000, 820000, 830000]
        }
      }
    }
  },
  "parameters": {
    "theme": "business",
    "vibe": "balanced"
  }
}
```

**Generated MDX**:
```mdx
<LayoutDashboard>
  <LayoutDashboard.Header>
    <Heading level={2}>Q4 Performance Metrics</Heading>
  </LayoutDashboard.Header>
  
  <LayoutDashboard.Stat1>
    <MetricGroup metrics={[{value: "$2.4M", label: "Revenue", change: 12, changeLabel: "vs Q3"}]} />
  </LayoutDashboard.Stat1>
  
  <LayoutDashboard.Stat2>
    <MetricGroup metrics={[{value: "89%", label: "Customer Satisfaction"}]} />
  </LayoutDashboard.Stat2>
  
  <LayoutDashboard.Chart>
    <ChartBar 
      title="Monthly Revenue"
      data={[
        {label: "Oct", value: 750000},
        {label: "Nov", value: 820000},
        {label: "Dec", value: 830000}
      ]}
    />
  </LayoutDashboard.Chart>
</LayoutDashboard>
```
