# Slidev Layout Architecture

## Overview

This document defines the unified architecture for Slidev layouts, themes, and vibes.

## Core Concepts

### 1. Theme (Color & Typography)
**Purpose**: High-level style control for colors and typography.

```yaml
# Frontmatter
theme: dark-professional  # or: light-minimal, cyber-neon, warm-corporate
```

**Theme provides CSS variables:**
```css
/* Colors */
--theme-bg-base: #0f172a;
--theme-bg-surface: #1e293b;
--theme-primary: #3b82f6;
--theme-accent: #8b5cf6;
--theme-text: #f8fafc;
--theme-text-muted: #94a3b8;
--theme-success: #10b981;
--theme-warning: #f59e0b;
--theme-danger: #ef4444;
--theme-border: #334155;

/* Typography */
--font-body: 'Inter', sans-serif;
--font-heading: 'Inter', sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Effects */
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
--shadow-md: 0 4px 12px rgba(0,0,0,0.1);
--shadow-lg: 0 8px 24px rgba(0,0,0,0.15);
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 16px;
```

### 2. Vibe (Layout Density & Complexity)
**Purpose**: High-level style control for layout behavior, NOT animations.

```yaml
# Frontmatter
vibe: clean  # or: minimal, balanced, decorative, expressive
```

**Vibe levels (5 levels):**

| Vibe | Density | Decorations | Grid Variations | Use Case |
|------|---------|-------------|-----------------|----------|
| minimal | High density, tight spacing | None | Uniform grid | Data-heavy, technical |
| clean | Normal spacing | Subtle borders | Slight variations | Professional, corporate |
| balanced | Comfortable spacing | Light gradients, soft shadows | Moderate variations | General purpose |
| decorative | Generous spacing | Gradients, glows, patterns | Asymmetric, rotations | Creative, marketing |
| expressive | Maximum breathing room | Complex overlays, animations | Dramatic asymmetry | Artistic, keynote |

**Vibe affects layout CSS:**
```css
/* Example: smart-grid with vibe=minimal */
.smart-grid.vibe-minimal {
  gap: 0.75rem;
  padding: 1.5rem;
}
.smart-grid.vibe-minimal .grid-cell {
  border-radius: var(--radius-sm);
  box-shadow: none;
  transform: none; /* No rotations */
}

/* Example: smart-grid with vibe=expressive */
.smart-grid.vibe-expressive {
  gap: 2.5rem;
  padding: 3rem;
}
.smart-grid.vibe-expressive .grid-cell {
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}
.smart-grid.vibe-expressive .grid-cell:nth-child(odd) {
  transform: rotate(-2deg);
}
```

### 3. SlideShell (Base Component)
**Purpose**: Unified wrapper providing header, footer, theme context, and vibe classes.

```vue
<!-- SlideShell.vue -->
<template>
  <div class="slide-shell" :class="[themeClass, vibeClass]" :style="themeVars">
    <header v-if="header" class="slide-header">{{ header }}</header>
    
    <main class="slide-content">
      <slot />
    </main>
    
    <footer v-if="footer" class="slide-footer">{{ footer }}</footer>
  </div>
</template>
```

### 4. Layouts Inherit SlideShell
All custom layouts wrap their content in SlideShell:

```vue
<!-- smart-grid.vue -->
<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="smart-grid" :class="vibeClass">
      <slot name="header" />
      <div class="grid-cell"><slot name="col1" /></div>
      <div class="grid-cell"><slot name="col2" /></div>
      <!-- ... -->
    </div>
  </SlideShell>
</template>
```

## Frontmatter Schema

```yaml
---
layout: smart-grid
theme: dark-professional   # Colors & typography
vibe: balanced            # Layout density & complexity
header: "Section Title"   # Optional header text
footer: "Page 1 of 10"   # Optional footer text
cols: 3                   # Layout-specific params
---
```

## Implementation Files

### Components
- `SlideShell.vue` - Base shell with header/footer/theme/vibe
- `MetricWidget.vue` - Respects theme colors
- `ChartWidget.vue` - Respects theme colors
- `QuoteWidget.vue` - Respects theme colors
- `TableWidget.vue` - Respects theme colors

### Layouts (all inherit SlideShell)
- `smart-grid.vue` - Grid with variable columns
- `hero-split.vue` - Two-panel split layout
- `timeline.vue` - Vertical timeline
- `comparison.vue` - Before/after comparison
- `dashboard.vue` - Metrics dashboard
- `feature-grid.vue` - Feature showcase
- `full-bleed.vue` - Edge-to-edge content
- `two-cols-header.vue` - Two columns with header

## Theme Presets

### dark-professional (default)
```css
--theme-bg-base: #0f172a;
--theme-bg-surface: #1e293b;
--theme-primary: #3b82f6;
--theme-text: #f8fafc;
```

### light-minimal
```css
--theme-bg-base: #ffffff;
--theme-bg-surface: #f8fafc;
--theme-primary: #2563eb;
--theme-text: #0f172a;
```

### cyber-neon
```css
--theme-bg-base: #050505;
--theme-bg-surface: #0a0a0a;
--theme-primary: #00ffa3;
--theme-text: #e2e8f0;
```

### warm-corporate
```css
--theme-bg-base: #fffbeb;
--theme-bg-surface: #fef3c7;
--theme-primary: #d97706;
--theme-text: #1c1917;
```

## Migration Notes

1. Remove `background` from frontmatter - use `theme` instead
2. Remove animation-based vibe values (particles, waves) - use CSS-based vibes
3. All layouts now receive consistent header/footer from SlideShell
4. Theme and vibe are passed via frontmatter, rendered via CSS classes
