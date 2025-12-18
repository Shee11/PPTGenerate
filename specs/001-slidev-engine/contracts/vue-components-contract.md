# Contract: Vue Components

**Purpose**: Define props interfaces and behavior contracts for Slidev Vue components  
**Location**: Slidev project (separate from Python backend)  
**Language**: TypeScript/Vue 3

## Component Interfaces

### MetricCard.vue

**Purpose**: Display labeled numeric metrics with variant styling

**Props Interface**:

```typescript
interface MetricCardProps {
  label: string;        // Metric name (e.g., "Revenue", "Users")
  value: string;        // Metric value (e.g., "$5.2M", "1,234")
  variant?: 'primary' | 'success' | 'danger';  // Color theme (default: 'primary')
}
```

**Requirements**:
- ✅ FR-021: Accept label, value, variant props
- ✅ FR-022: Display label in uppercase with muted color, value in large mono font

**Visual Contract**:
- Label: 12px font, uppercase, muted color (gray-500)
- Value: 48px font, monospace, variant color (primary/success/danger)
- Layout: Vertical stack (label on top, value below)
- Spacing: 8px gap between label and value

**Theme Integration**:
- Variant colors reference CSS variables:
  - `primary` → `var(--c-primary)`
  - `success` → `var(--c-success, #10b981)`
  - `danger` → `var(--c-danger, #ef4444)`
- Respects theme switching (business ↔ cyber)

**Usage in Markdown**:
```markdown
<MetricCard label="Revenue" value="$5.2M" variant="primary" />
```

**Test Contract**:
- Renders with all props combinations
- Label always uppercase in DOM
- Variant changes color (verify via computed styles)
- No props → renders empty (graceful degradation)

---

### StatusBadge.vue

**Purpose**: Display status indicators with color-coded visual feedback

**Props Interface**:

```typescript
interface StatusBadgeProps {
  status: 'success' | 'warning' | 'error';  // Status type
  text: string;                              // Status message
}
```

**Requirements**:
- ✅ FR-023: Accept status and text props

**Visual Contract**:
- Badge: Inline-block, rounded pill shape
- Text: 14px font, status color (white on cyber theme, dark on business)
- Background: Status color with opacity
  - `success` → green background
  - `warning` → yellow/orange background
  - `error` → red background
- Glow effect on cyber theme (box-shadow with neon colors)

**Theme Integration**:
- Status colors reference CSS variables:
  - `success` → `var(--c-success)`
  - `warning` → `var(--c-warning)`
  - `error` → `var(--c-danger)`
- Cyber theme adds glow shadow (e.g., `box-shadow: 0 0 10px var(--c-success)`)

**Usage in Markdown**:
```markdown
<StatusBadge status="warning" text="High CPU" />
```

**Test Contract**:
- All status values render with correct color
- Glow effect appears only on cyber theme
- Text properly escaped (handles special chars)

---

### ProgressBar.vue

**Purpose**: Display progress/percentage indicators

**Props Interface**:

```typescript
interface ProgressBarProps {
  label?: string;       // Optional label (e.g., "CPU Usage")
  value: number;        // Current value (0-100)
  max?: number;         // Maximum value (default: 100)
  status?: 'success' | 'warning' | 'error';  // Auto-derive if omitted
}
```

**Requirements**:
- Progress bar with percentage fill
- Color changes based on value thresholds or explicit status

**Visual Contract**:
- Container: Full-width bar, 8px height, rounded
- Fill: Percentage-based width, animated transition
- Label: Above bar if provided, 12px font
- Colors:
  - <30% → error (red)
  - 30-70% → warning (yellow)
  - >70% → success (green)
  - Override with explicit `status` prop

**Theme Integration**:
- Background: `var(--c-bg-elevated)` (light gray on business, dark gray on cyber)
- Fill: Status color (`var(--c-success)`, `var(--c-warning)`, `var(--c-danger)`)

**Usage in Markdown**:
```markdown
<ProgressBar label="CPU Usage" :value="85" status="warning" />
```

**Test Contract**:
- Value 0 → 0% width
- Value 100 → 100% width
- Value changes trigger smooth transition (CSS animation)
- Status auto-derived correctly based on thresholds

---

## Layout Components

### SlideShell.vue

**Purpose**: Wrapper component that injects theme CSS variables and renders header/footer

**Props Interface**:

```typescript
interface SlideShellProps {
  theme?: 'business' | 'cyber';  // Theme name from frontmatter (default: 'business')
}
```

**Requirements**:
- ✅ FR-024: Inject theme CSS variables, render header/footer, wrap slot content

**Theme Variables**:

```typescript
const THEMES = {
  business: {
    '--c-primary': '#2563eb',
    '--c-accent': '#f59e0b',
    '--c-bg': '#ffffff',
    '--c-text': '#0f172a',
    '--c-text-muted': '#64748b',
    '--c-border': '#e2e8f0',
    '--c-success': '#10b981',
    '--c-warning': '#f59e0b',
    '--c-danger': '#ef4444',
    '--font-main': 'Inter, sans-serif',
    '--font-mono': 'Fira Code, monospace',
    '--shadow-sm': '0 1px 2px rgba(0,0,0,0.05)',
    '--shadow-md': '0 4px 6px rgba(0,0,0,0.1)',
  },
  cyber: {
    '--c-primary': '#00ffa3',
    '--c-accent': '#ff006e',
    '--c-bg': '#050505',
    '--c-text': '#e2e8f0',
    '--c-text-muted': '#94a3b8',
    '--c-border': '#1e293b',
    '--c-success': '#00ffa3',
    '--c-warning': '#ffd60a',
    '--c-danger': '#ff006e',
    '--font-main': 'Orbitron, monospace',
    '--font-mono': 'Fira Code, monospace',
    '--shadow-sm': '0 0 10px rgba(0,255,163,0.3)',
    '--shadow-md': '0 0 20px rgba(0,255,163,0.5)',
  }
}
```

**Visual Contract**:
- Applies CSS variables to root element (`:style="themeVars"`)
- Renders default slot (slide content)
- Optional header/footer from frontmatter (if provided)
- Cyber theme adds grid pattern overlay (CSS pseudo-element)

**Test Contract**:
- Theme switching updates CSS variables (<100ms, SC-002)
- All descendant components can reference `var(--c-primary)`
- Grid overlay visible only on cyber theme

---

### SmartGrid.vue

**Purpose**: Column-based grid layout with dynamic column count

**Props Interface**:

```typescript
interface SmartGridProps {
  cols?: number;    // Number of columns (default: 3, range: 2-4)
  gap?: string;     // Grid gap (default: '24px')
}
```

**Requirements**:
- ✅ FR-017: Accept cols parameter (2-4), generate CSS grid
- ✅ FR-018: Provide header slot spanning full width
- ✅ FR-019: Provide col1-colN slots
- ✅ FR-020: Grid cells have rounded borders, theme-based background

**Layout Contract**:
- Header: Full-width row (grid-column: 1 / -1)
- Columns: Equal-width grid (grid-template-columns: repeat(cols, 1fr))
- Gap: Configurable spacing between cells
- Cell styling: Rounded corners (8px), theme background, theme shadow

**Slot Structure**:
```vue
<template>
  <div class="smart-grid" :style="gridStyle">
    <div class="grid-header"><slot name="header" /></div>
    <div class="grid-col"><slot name="col1" /></div>
    <div class="grid-col"><slot name="col2" /></div>
    <div class="grid-col" v-if="cols >= 3"><slot name="col3" /></div>
    <div class="grid-col" v-if="cols >= 4"><slot name="col4" /></div>
  </div>
</template>
```

**Test Contract**:
- `cols: 2` renders 2 columns
- `cols: 4` renders 4 columns
- Header spans full width regardless of cols
- Gap parameter affects CSS grid-gap

---

### HeroSplit.vue

**Purpose**: Two-panel layout with left/right content areas

**Props Interface**:

```typescript
interface HeroSplitProps {
  ratio?: string;   // Split ratio (default: '50-50', options: '60-40', '40-60', '70-30', '30-70')
}
```

**Layout Contract**:
- Two columns with configurable width ratio
- Ratio "60-40" → left 60%, right 40%
- Responsive breakpoints (stack on mobile)

**Slot Structure**:
```vue
<template>
  <div class="hero-split" :style="splitStyle">
    <div class="split-left"><slot name="left" /></div>
    <div class="split-right"><slot name="right" /></div>
  </div>
</template>
```

---

### FullBleed.vue

**Purpose**: Single full-screen content area

**Props Interface**:

```typescript
interface FullBleedProps {
  align?: 'top' | 'center' | 'bottom';  // Vertical alignment (default: 'center')
}
```

**Layout Contract**:
- 100% viewport width/height
- Content vertically aligned per prop
- No margins/padding (true full bleed)

**Slot Structure**:
```vue
<template>
  <div class="full-bleed" :class="`align-${align}`">
    <slot />  <!-- Default unnamed slot -->
  </div>
</template>
```

---

## UnoCSS Shortcuts

**Location**: `uno.config.ts` in Slidev project

**Required Shortcuts**:

```typescript
export default defineConfig({
  shortcuts: {
    // Background
    'bg-theme-base': 'bg-[var(--c-bg)]',
    'bg-theme-elevated': 'bg-[var(--c-bg-elevated,#f8fafc)]',
    
    // Text
    'text-theme-main': 'text-[var(--c-text)]',
    'text-theme-muted': 'text-[var(--c-text-muted)]',
    'text-theme-primary': 'text-[var(--c-primary)]',
    
    // Border
    'border-theme': 'border-[var(--c-border)]',
    
    // Shadow
    'shadow-theme': 'shadow-[var(--shadow-md)]',
    'shadow-theme-sm': 'shadow-[var(--shadow-sm)]',
    
    // Typography
    'font-theme': 'font-[var(--font-main)]',
    'font-mono-theme': 'font-[var(--font-mono)]',
  }
})
```

**Requirements**:
- ✅ FR-015: Provide semantic class names for theme properties
- ✅ FR-016: All components reference CSS variables, not hardcoded colors

**Test Contract**:
- Classes apply correct CSS variable values
- Values change with theme switching

---

## Acceptance Criteria

**Per Component**:
- [ ] Props interface defined and type-safe
- [ ] Visual contract documented (sizes, colors, spacing)
- [ ] Theme integration verified (CSS variables used)
- [ ] Slots properly named and functional
- [ ] UnoCSS shortcuts applied where appropriate
- [ ] Renders correctly in both business and cyber themes
- [ ] Component tests pass (props, slots, styling)

**Integration**:
- [ ] All components importable in Slidev markdown
- [ ] Theme switching affects all components (<100ms)
- [ ] Components work together in same slide
- [ ] No prop conflicts or naming collisions

---

## Change Impact

Adding new component requires:
1. Define props interface (TypeScript)
2. Document visual contract (sizes, colors)
3. Implement with CSS variable references
4. Add to widget-to-component mapping in renderer
5. Update `data-model.md` transformation rules
6. Create component tests
