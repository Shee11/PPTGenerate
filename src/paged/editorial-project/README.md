# Editorial Project

A Slidev theme with a **Serif, Elegant, Photography** aesthetic. Inspired by high-end editorial magazines and luxury publications.

## Design Language

### Typography
- **Display Font**: Playfair Display - Elegant serif for headlines
- **Body Font**: Cormorant Garamond - Refined serif for body text  
- **Accent Font**: Source Serif 4 - Modern serif for captions and labels

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Black | `#1a1a1a` | Primary text |
| Charcoal | `#2d2d2d` | Secondary backgrounds |
| Gold | `#c9a962` | Accents, highlights |
| Navy | `#1e3a5f` | Alternative accent |
| Burgundy | `#722f37` | Warm accent |
| Cream | `#f8f6f3` | Background |
| White | `#ffffff` | Cards, surfaces |

### Visual Elements
- Thin hairline dividers
- Corner frame decorations
- Diamond ornaments (◆ ◇)
- Drop caps for magazine style
- Image frames with offset shadows

## Vibes

The editorial theme includes 4 vibes for different moods:

### Classic (default)
Gold accents with cream backgrounds. Elegant and timeless.

### Modern
Charcoal accents with minimal ornamentation. Clean and sophisticated.

### Luxe
Dark backgrounds with gold accents. High-end and dramatic.

### Warm
Burgundy and cream combination. Inviting and rich.

## Layouts

| Layout | Description |
|--------|-------------|
| `SlideShell` | Base wrapper with header/footer lines |
| `hero-split` | Text + image with elegant divider |
| `smart-grid` | 4-column numbered grid |
| `info-boxes` | 2x2 numbered card grid |
| `timeline` | Horizontal timeline with alternating events |
| `comparison` | Side-by-side with "vs" divider |
| `dashboard` | Metrics + chart + summary |
| `spotlight` | Centered featured content |
| `full-bleed` | Full-bleed photography with overlays |
| `quote-hero` | Large quote with attribution |
| `stats-showcase` | Statistics row display |
| `cards-grid` | 2-4 column card grid |
| `feature-grid` | 6-feature grid with icons |
| `two-cols-header` | Two columns with header |
| `image-text` | Image + text with frame option |
| `magazine` | Magazine layout with drop cap |
| `default` | Standard content layout |
| `cover` | Title page with corner frames |

## Components

| Component | Description |
|-----------|-------------|
| `MetricWidget` | Statistic with value + label |
| `QuoteWidget` | Pull quote with attribution |
| `TableWidget` | Elegant data table |
| `ChartWidget` | Chart placeholder |
| `IconBox` | Icon with title and description |
| `TimelineItem` | Single timeline event |
| `ProgressRing` | Circular progress indicator |
| `GradientText` | Text with gradient fills |

## Usage

```yaml
---
theme: editorial
layout: cover
vibe: classic
---

# Your Elegant Presentation

*A sophisticated story told beautifully*

---
layout: hero-split
---

::title::
## Chapter One

::content::
Begin your narrative with refined typography
and thoughtful design.

::image::
![Hero image](./image.jpg)

---
layout: quote-hero
vibe: luxe
---

::quote::
*Design is not just what it looks like—design is how it works.*

::author::
Steve Jobs

::context::
Apple Inc.
```

## Photography Integration

The editorial theme is optimized for photography:

- **full-bleed**: Full-screen images with overlay options
- **image-text**: Side-by-side with optional frames
- **Overlay modes**: `dark`, `light`, `gradient`, `none`
- **Frame effects**: Elegant double-border with gold accent

## Font Loading

Add to your Slidev setup:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;1,8..60,400&display=swap" rel="stylesheet">
```

## License

MIT License
