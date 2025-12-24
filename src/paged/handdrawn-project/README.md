# Handdrawn Slidev Project

A **sketchy, pastel, friendly** presentation theme for Slidev with hand-drawn aesthetics.

## Design Language

### Color Palette
- **Pastel Pink**: `#FFB5BA` - Primary accent
- **Pastel Blue**: `#A8D8EA` - Secondary accent
- **Pastel Green**: `#B5EAD7` - Success/positive
- **Pastel Yellow**: `#FFEAA7` - Highlight/notes
- **Pastel Purple**: `#DCD6F7` - Accent
- **Pastel Orange**: `#FFD8BE` - Warm accent
- **Cream**: `#FFF9F0` - Background
- **Dark Text**: `#2D3436` - Primary text

### Typography
- **Display**: `Caveat` - Hand-written headers
- **Handwriting**: `Patrick Hand` - Notes and annotations
- **Body**: `Nunito` - Readable body text

### Visual Elements
- **Sketchy borders** - Organic, imperfect shapes
- **Sticky notes** - Post-it style containers
- **Paper textures** - Notebook lines, cream paper
- **Tape decorations** - Masking tape effects
- **Doodles** - Emoji decorations (✿★♪♥🌸)
- **Corner folds** - Paper curl effects
- **Paper clips & pushpins** - Attachment decorations

## Vibes

Each layout supports 4 vibes via the `vibe` prop:

| Vibe | Description |
|------|-------------|
| `playful` | More rotations, hover animations, bouncy effects |
| `cozy` | Balanced decorations, warm sticky notes |
| `minimal` | Clean, reduced decorations, flat styling |
| `decorated` | Maximum doodles, sparkles, stickers |

## Layouts (16)

| Layout | Description | Key Slots |
|--------|-------------|-----------|
| `SlideShell` | Base wrapper with paper texture | `default` |
| `default` | Simple content layout | `default` |
| `cover` | Title slide with decorative frame | `title`, `subtitle`, `author` |
| `hero-split` | Two-panel sticky notes | `left`, `right` |
| `smart-grid` | 4-column pinned notes | `header`, `col1-4` |
| `info-boxes` | 4 info boxes with icons | `title`, `box1-4_title/content` |
| `timeline` | Horizontal event timeline | `title`, `event1-4_title/content` |
| `comparison` | VS comparison layout | `title`, `left/right_title/content` |
| `dashboard` | Metrics + chart + notes | `title`, `metric1-4`, `chart`, `summary` |
| `spotlight` | Centered featured content | `title`, `main`, `caption` |
| `full-bleed` | Background with overlay card | `background`, `content` |
| `quote-hero` | Large quote on notebook | `quote`, `author`, `context` |
| `stats-showcase` | 3 stat cards with pins | `title`, `stat1-3`, `footer` |
| `cards-grid` | 6-card grid with tape | `title`, `card1-6` |
| `feature-grid` | 4 feature boxes | `title`, `feature1-4` |
| `two-cols-header` | Header + 2 columns | `header`, `left`, `right` |
| `image-text` | Photo frame + notebook | `image`, `content` |
| `magazine` | Headline + main + sidebar | `headline`, `main`, `sidebar`, `footer` |

## Components (8)

| Component | Props | Description |
|-----------|-------|-------------|
| `MetricWidget` | `value`, `label`, `change`, `color` | Stat display on sticky |
| `QuoteWidget` | `quote`, `author`, `color` | Quote with marks |
| `TableWidget` | `headers`, `rows` | Paper table with clip |
| `ChartWidget` | `type`, `title`, `data` | Chart on grid paper |
| `IconBox` | `icon`, `title`, `color` | Icon + content box |
| `TimelineItem` | `title`, `date`, `icon`, `position`, `color` | Single timeline event |
| `ProgressRing` | `value`, `label`, `color` | Circular progress |
| `GradientText` | `variant`, `size` | Styled text effects |

## Usage

```vue
<template>
  <hero-split vibe="cozy">
    <template #left>
      <h1>Hello! 👋</h1>
      <p>Welcome to my presentation</p>
    </template>
    <template #right>
      <MetricWidget value="98%" label="Happiness" color="pink" />
    </template>
  </hero-split>
</template>
```

## CSS Classes

Utility classes available in `styles/index.css`:

```css
/* Borders */
.sketchy-border       /* Hand-drawn border effect */

/* Sticky Notes */
.sticky-note          /* Default yellow */
.sticky-pink          /* Pink variant */
.sticky-blue          /* Blue variant */
.sticky-green         /* Green variant */

/* Effects */
.marker-highlight     /* Yellow marker effect */
.marker-pink         /* Pink marker */
.tape                /* Masking tape decoration */
.doodle-underline    /* Wavy underline */
.notebook-bg         /* Lined notebook background */

/* Checkboxes */
.hand-checkbox       /* Hand-drawn checkbox */
.hand-checkbox.checked

/* Animations */
.wobble              /* Gentle wobble */
.bounce-in           /* Bouncy entrance */
```

## Project Selection

In `state.json`, set:
```json
{
  "project": "handdrawn"
}
```

## Font Setup

Add to your HTML or slides config:
```html
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&family=Patrick+Hand&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
```
