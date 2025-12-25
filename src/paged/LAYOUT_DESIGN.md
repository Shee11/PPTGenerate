# Slidev Project Layout & Widget Design

This document summarizes the layout system, widgets, and theme architecture used in the `slidev-project` under `src/paged/`.

## Architecture Overview

```
src/paged/slidev-project/
├── layouts/           # Vue layout components (16 layouts)
│   └── SlideShell.vue # Base wrapper for all layouts
├── components/        # Reusable widget components (19 widgets)
├── styles/
│   └── index.css      # Global styles
├── package.json
└── uno.config.ts
```

## SlideShell - The Base Wrapper

All layouts inherit from `SlideShell.vue`, which provides:

1. **Consistent Header/Footer** - Renders header/footer from frontmatter
2. **Theme CSS Variables** - Applies theme presets via CSS custom properties
3. **Vibe Class Propagation** - Controls layout density/complexity

```vue
<SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
  <YourLayoutContent />
</SlideShell>
```

---

## Layouts (16 Total)

| Layout | Slots | Description |
|--------|-------|-------------|
| `smart-grid` | header, col1, col2, col3, col4 | Flexible grid (2-4 columns) |
| `hero-split` | left, right | Two-panel split with configurable ratio |
| `two-cols-header` | header, left, right | Two columns with full-width header |
| `full-bleed` | content | Full-screen background with content overlay |
| `feature-grid` | header, feature1-4 | 2x2 feature boxes |
| `comparison` | header, left, right | Side-by-side comparison |
| `timeline` | header, step1-4 | Horizontal timeline with steps |
| `dashboard` | header, metric1-4, chart | Metrics dashboard layout |
| `spotlight` | highlight, context | Hero content with supporting context |
| `magazine` | header, featured, sidebar | Editorial magazine layout |
| `quote-hero` | quote, attribution | Large quote with attribution |
| `stats-showcase` | header, stat1-3, context | Statistics showcase |
| `image-text` | image, content | Image with text content |
| `cards-grid` | header, card1-4 | Grid of cards |
| `info-boxes` | header, box1-3 | Information boxes |

### Layout Parameters (Frontmatter)

```yaml
---
layout: smart-grid
cols: 3              # Grid columns (2-4)
ratio: "60-40"       # Split ratio for hero-split
header: "Section"    # Optional header text
footer: "Page 1"     # Optional footer text
theme: business      # Theme preset name
vibe: balanced       # Density control
---
```

---

## Themes (7 Presets + 4 Legacy)

Each theme defines CSS custom properties for consistent styling:

### Primary Themes

| Theme | Background | Primary | Accent | Use Case |
|-------|------------|---------|--------|----------|
| `business` | `#0f172a` (dark blue) | `#3b82f6` (blue) | `#8b5cf6` (purple) | Professional corporate |
| `cyber` | `#050505` (black) | `#00ffa3` (neon green) | `#00d4ff` (cyan) | Tech/futuristic |
| `minimal` | `#ffffff` (white) | `#18181b` (black) | `#3b82f6` (blue) | Clean, modern |
| `academic` | `#fefce8` (cream) | `#854d0e` (brown) | `#b45309` (amber) | Scholarly, formal |
| `creative` | `#fdf4ff` (pink) | `#a21caf` (magenta) | `#c026d3` (fuchsia) | Vibrant, artistic |
| `duolingo` | `#ffffff` (white) | `#58CC02` (green) | `#1CB0F6` (blue) | Playful, gamified |
| `dark` | `#09090b` (black) | `#a78bfa` (violet) | `#c4b5fd` (lavender) | Modern dark mode |

### Theme CSS Variables

```css
/* Background layers */
--theme-bg-base      /* Main background */
--theme-bg-surface   /* Cards, panels */
--theme-bg-elevated  /* Elevated surfaces */

/* Colors */
--theme-primary      /* Primary accent */
--theme-accent       /* Secondary accent */
--theme-success      /* Success state */
--theme-warning      /* Warning state */
--theme-danger       /* Error state */

/* Text */
--theme-text         /* Primary text */
--theme-text-muted   /* Secondary text */
--theme-text-dim     /* Tertiary text */

/* Borders */
--theme-border       /* Primary border */
--theme-border-subtle/* Subtle border */

/* Typography */
--font-body          /* Body text font */
--font-heading       /* Heading font */
--font-mono          /* Monospace font */

/* Effects */
--shadow-sm/md/lg    /* Shadow sizes */
--shadow-glow        /* Glow effect */
--radius-sm/md/lg/xl /* Border radius */
```

### Automatic Contrast Adjustment

SlideShell automatically adjusts text colors when background overrides create contrast issues:
- Light backgrounds with dark themes → switches to dark text
- Dark backgrounds with light themes → switches to light text

---

## Vibes (5 Density Levels)

Vibes control the visual density and complexity of layouts:

| Vibe | Padding | Font Size | Style |
|------|---------|-----------|-------|
| `minimal` | Tight | 0.65rem | No borders, no frills |
| `clean` | Subtle | 0.7rem | Professional, subtle |
| `balanced` | Default | 0.75rem | Comfortable (default) |
| `decorative` | More | 0.8rem | Gradient borders |
| `expressive` | Maximum | 0.875rem | Bold, uppercase, shadows |

```yaml
---
vibe: balanced  # Options: minimal, clean, balanced, decorative, expressive
---
```

---

## Widgets (19 Components)

### Data Visualization

| Widget | Props | Description |
|--------|-------|-------------|
| `MetricWidget` | label, value, change, changeLabel, subtitle, icon, variant | KPI metric with trend |
| `ChartWidget` | chartType, title, data, unit, color | Bar/line/pie/donut charts |
| `TableWidget` | title, columns, rows, variant, showHeader | Data tables |
| `AnimatedCounter` | value, duration | Animated number counter |
| `ProgressRing` | value, size, color | Circular progress indicator |
| `MetricCard` | (similar to MetricWidget) | Card-styled metric |

### Typography & Content

| Widget | Props | Description |
|--------|-------|-------------|
| `QuoteWidget` | text, author, attribution, variant, showIcon | Blockquote with attribution |
| `GradientText` | text, gradient | Text with gradient fill |
| `RetroTerminal` | text, prompt | Terminal-style text display |

### Decorative

| Widget | Props | Description |
|--------|-------|-------------|
| `GlassCard` | - | Glassmorphism card container |
| `GlassPanel` | - | Frosted glass panel |
| `GlowCard` | - | Card with glow effect |
| `HolographicCard` | - | Iridescent holographic card |
| `PolaroidCard` | - | Polaroid-style photo card |
| `NeonFrame` | - | Neon-bordered frame |
| `IconBox` | icon, label | Icon with label |
| `FloatingBadge` | text | Floating badge/tag |
| `TimelineItem` | title, description, date | Timeline entry |

### Widget Usage in Markdown

Widgets are rendered via Vue components in slot content:

```markdown
::stat1::
<MetricWidget label="Revenue" value="$2.4M" :change="12" changeLabel="vs last month" />

::chart::
<ChartWidget chartType="bar" title="Sales" :data='[{"label":"Q1","value":75}]' />
```

---

## Rendering Pipeline

### Markdown Renderer (`markdown_renderer.py`)

The `SlidevRenderer` converts slide JSON to Slidev markdown:

1. **Frontmatter Generation** - Creates YAML with layout, theme, vibe, parameters
2. **Widget Rendering** - Dispatches to type-specific renderers:
   - `Type.*` → Typography (heading, body, list, quote, image, caption, etc.)
   - `Data.*` → Data widgets (BigNum, Metric, Table, Chart)
   - Vue components → Direct component tags

### Widget Type Mapping

```python
# Typography widgets → Markdown
Type.Display  → plain text
Type.Heading  → # heading (with level)
Type.Body     → paragraph
Type.Caption  → *italic text*
Type.List     → - bullet list
Type.Quote    → > blockquote
Type.Image    → ![alt](src)
Type.Metric   → ## value + label
Type.BigNumber → ## value + label
Type.Note     → > **Note:** text
Type.Chart    → 📊 placeholder

# Data widgets → Markdown
Data.BigNum   → ## value + label
Data.Metric   → ### value + label
Data.Table    → | markdown table |
Data.Chart    → 📊 placeholder

# Vue components → Direct tags
TableWidget   → <TableWidget ... />
ChartWidget   → <ChartWidget ... />
MetricWidget  → <MetricWidget ... />
QuoteWidget   → <QuoteWidget ... />
```

---

## Project Selection

Multiple project styles are available via the `--project` CLI flag:

| Project | Directory | Style |
|---------|-----------|-------|
| `slidev` (default) | `slidev-project` | Professional gradients, glassmorphism |
| `duolingo` | `duolingo-project` | Playful, chunky, bright colors |
| `cyberpunk` | `cyberpunk-project` | Neon, HUD frames, glitch effects |
| `handdrawn` | `handdrawn-project` | Sketchy, hand-drawn aesthetic |
| `editorial` | `editorial-project` | Magazine/editorial typography |
| `business` | `business-project` | Corporate professional |
| `simple` | `simple-project` | Clean, minimal layouts |

```bash
# CLI usage
python -m cli.uce_render --render state.json -o output.html --project simple
```

---

## State.json Widget Schema

Widgets in state.json follow this structure:

```json
{
  "widgets": {
    "title": {
      "type": "Type.Heading",
      "parameters": {
        "text": "Slide Title",
        "level": 1
      }
    },
    "left": {
      "type": "Type.Image",
      "parameters": {
        "src": "https://example.com/image.jpg",
        "alt": "Description"
      }
    },
    "right": {
      "type": "Type.List",
      "parameters": {
        "items": ["Point 1", "Point 2", "Point 3"]
      }
    }
  }
}
```

---

## Best Practices

1. **Use SlideShell** - Always wrap layouts in SlideShell for consistency
2. **Theme Presets** - Use predefined themes; they handle contrast automatically
3. **Vibes for Density** - Use vibes instead of custom padding/sizing
4. **Named Slots** - Use semantic slot names (title, left, right, content)
5. **Widget Types** - Prefer `Type.*` for content, `Data.*` for visualizations
6. **Background Override** - Use `background` in frontmatter for per-slide changes
