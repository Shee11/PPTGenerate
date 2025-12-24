# Duolingo-Project

A Duolingo-inspired presentation theme for Slidev with playful, gamified styling.

## Features

- 🦉 **Duolingo Design System**: Chunky rounded corners, bottom-shadows, bright colors
- 🎨 **Color Palette**: Green (#58CC02), Blue (#1CB0F6), Orange (#FF9600), Purple (#CE82FF)
- 🔤 **Typography**: Nunito font family with extra-bold weights
- ⭐ **Playful Animations**: Bouncy transitions, particle effects, hover interactions
- 🎮 **Gamified Elements**: XP, streaks, gems, progress indicators

## Installation

This project is used as a source for the `SlidevRenderer`. To use it:

```python
from src.paged.render.slidev.markdown_renderer import SlidevRenderer

# Use Duolingo styling
renderer = SlidevRenderer(project="duolingo")

# Or use default Slidev styling
renderer = SlidevRenderer(project="slidev")  # or just SlidevRenderer()
```

## Layouts

All layouts have **exactly the same slots** as `slidev-project` for API compatibility:

| Layout | Slots | Description |
|--------|-------|-------------|
| `SlideShell.vue` | `default`, `header`, `footer` | Base wrapper with theme |
| `hero-split.vue` | `left`, `right` | Two-column hero layout |
| `smart-grid.vue` | `header`, `col1-4` | Responsive 4-column grid |
| `info-boxes.vue` | `title`, `box1_title/content` - `box4_title/content` | Info box cards |
| `timeline.vue` | `title`, `step1-5` | Vertical timeline |
| `comparison.vue` | `title`, `beforeLabel`, `before`, `afterLabel`, `after` | Before/after comparison |
| `dashboard.vue` | `title`, `metric1-4`, `chart` | Dashboard with metrics |
| `spotlight.vue` | `default`, `subtitle` | Centered spotlight content |
| `full-bleed.vue` | `default` | Full-width content |
| `quote-hero.vue` | `quote`, `author`, `context` | Large quote display |
| `stats-showcase.vue` | `title`, `stat-1` - `stat-6` | Statistics grid |
| `cards-grid.vue` | `title`, `card-1` - `card-8` | Flexible card grid |
| `feature-grid.vue` | `title`, `feature1-6` | Feature showcase |
| `two-cols-header.vue` | `header`, `left`, `right` | Two columns with header |
| `image-text.vue` | `image`, `content`, `caption` | Image + text split |
| `magazine.vue` | `feature`, `sidebar`, `caption`, `strip-1/2/3` | Magazine editorial |

## Components

| Component | Props | Description |
|-----------|-------|-------------|
| `MetricWidget.vue` | `label`, `value`, `change`, `icon`, `variant` | Gamified metric display |
| `QuoteWidget.vue` | `text`, `author`, `attribution`, `variant` | Speech bubble quote |
| `TableWidget.vue` | `title`, `columns`, `rows`, `variant` | Colorful data table |
| `ChartWidget.vue` | `chartType`, `title`, `data`, `unit` | Animated charts |
| `IconBox.vue` | `icon`, `size`, `variant`, `color` | Styled icon container |
| `TimelineItem.vue` | `title`, `subtitle`, `markerIcon`, `markerColor` | Timeline entry |
| `ProgressRing.vue` | `value`, `size`, `color`, `label`, `icon` | Circular progress |
| `GradientText.vue` | `gradient`, `animated`, `weight` | Gradient text effect |

## Vibe System

Each layout supports a `vibe` prop with these options:

- `minimal`: Clean, no decorations
- `clean`: Subtle styling
- `balanced`: Default Duolingo feel
- `playful`: More animations and color
- `expressive`: Maximum playfulness

## Color Themes

Accent colors available throughout:

- **Green** (`#58CC02`): Success, XP, progress
- **Blue** (`#1CB0F6`): Info, gems, links
- **Orange** (`#FF9600`): Streaks, warnings
- **Purple** (`#CE82FF`): Premium, achievements
- **Red** (`#FF4B4B`): Errors, hearts

## File Structure

```
duolingo-project/
├── package.json          # NPM dependencies
├── README.md             # This file
├── layouts/              # Vue layout components
│   ├── SlideShell.vue    # Base wrapper
│   ├── hero-split.vue
│   ├── smart-grid.vue
│   └── ...
├── components/           # Vue widget components
│   ├── MetricWidget.vue
│   ├── QuoteWidget.vue
│   └── ...
└── styles/
    └── index.css         # Global Duolingo styles
```

## Usage Example

```markdown
---
layout: hero-split
theme: duolingo
vibe: playful
---

::left::
# Learn Today! 🦉

<ProgressRing :value="75" color="green" icon="⚡" label="XP" />

::right::
<MetricWidget 
  label="Daily Streak" 
  value="42" 
  icon="streak"
  :change="5"
/>
```

## License

Part of the UCE Render project.
