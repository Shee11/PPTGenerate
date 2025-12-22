<script setup lang="ts">
/**
 * Smart Grid Layout
 * 
 * A flexible grid layout with configurable columns (2-4).
 * Inherits from SlideShell for consistent header/footer/theme/vibe.
 * 
 * Frontmatter:
 *   layout: smart-grid
 *   cols: 3          # Number of columns (2-4)
 *   header: "..."    # Optional header text
 *   footer: "..."    # Optional footer text
 *   theme: dark-professional
 *   vibe: balanced
 */
import { computed, inject } from 'vue'
import SlideShell from './SlideShell.vue'

const props = defineProps<{
  cols?: number
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'decorative' | 'expressive'
}>()

// Get vibe from SlideShell injection or props
const injectedVibe = inject('vibe', computed(() => props.vibe || 'balanced'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'balanced')

// Clamp cols to valid range (2-4)
const columnCount = computed(() => {
  const cols = props.cols || 3
  return Math.max(2, Math.min(4, cols))
})

// Generate grid template columns
const gridStyle = computed(() => ({
  gridTemplateColumns: `repeat(${columnCount.value}, 1fr)`
}))

// Vibe class for grid-specific styling
const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="smart-grid" :class="vibeClass" :style="gridStyle">
      <!-- Full-width header spanning all columns -->
      <div class="grid-header">
        <slot name="header" />
      </div>
      
      <!-- Column slots -->
      <div v-if="columnCount >= 1" class="grid-cell">
        <slot name="col1" />
      </div>
      <div v-if="columnCount >= 2" class="grid-cell">
        <slot name="col2" />
      </div>
      <div v-if="columnCount >= 3" class="grid-cell">
        <slot name="col3" />
      </div>
      <div v-if="columnCount >= 4" class="grid-cell">
        <slot name="col4" />
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.smart-grid {
  display: grid;
  gap: 1.5rem;
  width: 100%;
  height: 100%;
  padding: 2rem;
  grid-template-rows: auto 1fr;
}

.grid-header {
  grid-column: 1 / -1;
  color: var(--theme-text);
  font-weight: 600;
  font-family: var(--font-heading);
}

.grid-header :deep(h1),
.grid-header :deep(h2),
.grid-header :deep(h3) {
  color: var(--theme-primary);
  margin: 0;
}

.grid-cell {
  padding: 1.5rem;
  border-radius: var(--radius-md);
  background: var(--theme-bg-surface);
  border: 1px solid var(--theme-border-subtle);
  overflow: hidden;
  color: var(--theme-text);
  box-shadow: var(--shadow-sm);
  position: relative;
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  gap: 0.75rem;
  padding: 1rem;
}

.vibe-minimal .grid-cell {
  padding: 1rem;
  border-radius: var(--radius-sm);
  box-shadow: none;
  border: 1px solid var(--theme-border);
  background: transparent;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  gap: 1rem;
  padding: 1.5rem;
}

.vibe-clean .grid-cell {
  padding: 1.25rem;
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
}

/* === VIBE: BALANCED (default) === */
/* Base styles above */

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  gap: 2rem;
  padding: 2.5rem;
}

.vibe-decorative .grid-cell {
  padding: 2rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: 2px solid transparent;
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-bg-surface) 95%, var(--theme-primary))
  );
}

/* Gradient border effect */
.vibe-decorative .grid-cell::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--radius-lg);
  padding: 2px;
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-accent));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0.3;
  pointer-events: none;
}

/* Slight rotations for visual interest */
.vibe-decorative .grid-cell:nth-child(2) {
  transform: rotate(-0.5deg);
}

.vibe-decorative .grid-cell:nth-child(3) {
  transform: rotate(0.5deg);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  gap: 2.5rem;
  padding: 3rem;
}

.vibe-expressive .grid-cell {
  padding: 2.5rem;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg), var(--shadow-glow);
  border: none;
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-bg-elevated) 80%, var(--theme-primary))
  );
}

/* More dramatic rotations */
.vibe-expressive .grid-cell:nth-child(2) {
  transform: rotate(-1.5deg) translateY(-4px);
}

.vibe-expressive .grid-cell:nth-child(3) {
  transform: rotate(1deg) translateY(4px);
}

.vibe-expressive .grid-cell:nth-child(4) {
  transform: rotate(-0.5deg);
}

.vibe-expressive .grid-cell:nth-child(5) {
  transform: rotate(0.75deg);
}

/* Asymmetric border radius */
.vibe-expressive .grid-cell:nth-child(even) {
  border-radius: var(--radius-xl) var(--radius-sm) var(--radius-xl) var(--radius-sm);
}

.vibe-expressive .grid-cell:nth-child(odd):not(:first-child) {
  border-radius: var(--radius-sm) var(--radius-xl) var(--radius-sm) var(--radius-xl);
}

/* Corner accent */
.vibe-expressive .grid-cell::after {
  content: '';
  position: absolute;
  top: -1px;
  right: -1px;
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, var(--theme-primary) 0%, transparent 70%);
  border-radius: 0 var(--radius-xl) 0 var(--radius-lg);
  opacity: 0.3;
}
</style>
