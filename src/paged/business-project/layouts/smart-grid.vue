<script setup lang="ts">
/**
 * Smart Grid Layout - Business Project
 * 
 * Flexible grid layout with configurable columns (2-4).
 * 
 * Slots:
 *   - header: Full-width header
 *   - col1, col2, col3, col4: Column content
 * 
 * Frontmatter:
 *   layout: smart-grid
 *   cols: 3          # Number of columns (2-4)
 *   header: "..."
 *   footer: "..."
 *   theme: business_professional
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

const injectedVibe = inject('vibe', computed(() => props.vibe || 'balanced'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'balanced')

// Clamp cols to valid range (2-4)
const columnCount = computed(() => {
  const cols = props.cols || 3
  return Math.max(2, Math.min(4, cols))
})

const gridStyle = computed(() => ({
  gridTemplateColumns: `repeat(${columnCount.value}, 1fr)`
}))

const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="smart-grid" :class="vibeClass" :style="gridStyle">
      <div class="grid-header">
        <slot name="header" />
      </div>
      
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
  border: 1px solid var(--theme-border);
  overflow: hidden;
  color: var(--theme-text);
  box-shadow: var(--shadow-sm);
  position: relative;
}

.grid-cell :deep(h3),
.grid-cell :deep(h4) {
  color: var(--theme-primary);
  font-family: var(--font-heading);
  margin-top: 0;
  margin-bottom: 0.75rem;
}

.grid-cell :deep(ul),
.grid-cell :deep(ol) {
  padding-left: 1.25rem;
  margin: 0;
}

.grid-cell :deep(li) {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

/* Cell accent bar */
.grid-cell::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--theme-primary);
}

.grid-cell:nth-child(3)::before {
  background: var(--theme-accent);
}

.grid-cell:nth-child(4)::before {
  background: var(--theme-success);
}

.grid-cell:nth-child(5)::before {
  background: var(--theme-warning);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  gap: 1rem;
  padding: 1.5rem;
}

.vibe-minimal .grid-cell {
  padding: 1rem;
  border-radius: var(--radius-sm);
  box-shadow: none;
  border: 1px solid var(--theme-border);
  background: transparent;
}

.vibe-minimal .grid-cell::before {
  display: none;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  gap: 1.25rem;
  padding: 1.75rem;
}

.vibe-clean .grid-cell {
  padding: 1.25rem;
  border-radius: var(--radius-sm);
}

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  gap: 2rem;
  padding: 2.5rem;
}

.vibe-decorative .grid-cell {
  padding: 1.75rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: none;
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-bg-surface) 95%, var(--theme-primary))
  );
}

.vibe-decorative .grid-cell::before {
  height: 4px;
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  gap: 2.5rem;
  padding: 3rem;
}

.vibe-expressive .grid-cell {
  padding: 2rem;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  border: 2px solid transparent;
  background: var(--theme-bg-surface);
}

.vibe-expressive .grid-cell:hover {
  border-color: var(--theme-primary);
}

.vibe-expressive .grid-cell::before {
  height: 5px;
  background: linear-gradient(90deg, var(--theme-primary), var(--theme-accent));
}
</style>
