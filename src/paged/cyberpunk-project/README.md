# Cyberpunk Slidev Project

A cyberpunk/neon-themed Slidev presentation template with futuristic aesthetics, glowing effects, and HUD-style UI elements.

## Design Language

### Colors
- **Cyan** (`#00FFFF`) - Primary accent, headings, interactive elements
- **Magenta** (`#FF00FF`) - Secondary accent, highlights
- **Yellow** (`#FFFF00`) - Warning/attention, VS elements
- **Pink** (`#FF0080`) - Tertiary accent
- **Green** (`#00FF41`) - Success states, status indicators

### Typography
- **Display**: Orbitron - Futuristic geometric sans-serif
- **Body**: Rajdhani - Tech-inspired readable font
- **Mono**: Share Tech Mono - Monospace for code/data

### Effects
- Neon glow on text and borders
- Scan lines overlay
- HUD-style corner frames
- Grid background patterns
- Glitch animations (vibe: glitch)

## Layouts

| Layout | Description | Slots |
|--------|-------------|-------|
| `SlideShell` | Base wrapper with HUD frame | default |
| `hero-split` | Two-panel hero layout | left, right |
| `smart-grid` | 4-column responsive grid | header, col1-4 |
| `info-boxes` | 2x2 information boxes | title, box1-4_title/content |
| `timeline` | Vertical timeline | title, item1-6 |
| `comparison` | Side-by-side comparison | title, left/right_title/content |
| `dashboard` | Widget dashboard grid | title, widget1-6 |
| `spotlight` | Hero with visual | badge, heading, description, visual |
| `full-bleed` | Full-screen background | background, overlay, caption |
| `quote-hero` | Large quote display | quote, author, context |
| `stats-showcase` | Statistics display | title, stat1-4 |
| `cards-grid` | 3x2 card grid | title, card1-6 |
| `feature-grid` | 2x2 feature blocks | title, feature1-4 |
| `two-cols-header` | Header + two columns | header, left, right |
| `image-text` | Image + text split | image, content |
| `magazine` | Magazine-style layout | headline, lead, col1-2, sidebar |

## Components

| Component | Description | Props |
|-----------|-------------|-------|
| `MetricWidget` | Metric display | value, label, trend, unit |
| `QuoteWidget` | Quote block | quote, author, source |
| `TableWidget` | Data table | headers, rows, highlight |
| `ChartWidget` | Simple charts | title, type, data |
| `IconBox` | Icon + text box | icon, title, description |
| `TimelineItem` | Timeline node | date, title, description, status |
| `ProgressRing` | Circular progress | value, label, size |
| `GradientText` | Gradient text | text, gradient, size, glow |

## Vibes

Control the visual intensity with the `vibe` prop:

- `minimal` - Clean, reduced effects
- `clean` - Light effects, professional
- `balanced` - Default, moderate effects
- `intense` - Strong glows and animations
- `glitch` - Glitch effects and distortion

## Usage

```yaml
---
layout: hero-split
vibe: intense
---

::left::
# WELCOME TO THE FUTURE

The digital frontier awaits

::right::
![Cyber City](/images/cyber.jpg)
```

## CSS Variables

```css
--cyber-cyan: #00FFFF;
--cyber-magenta: #FF00FF;
--cyber-yellow: #FFFF00;
--cyber-pink: #FF0080;
--cyber-green: #00FF41;
--cyber-bg: #0a0a12;
--cyber-text: #e0e0e0;
--cyber-text-dim: #666;
```
