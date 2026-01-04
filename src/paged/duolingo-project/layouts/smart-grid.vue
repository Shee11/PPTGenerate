<script setup lang="ts">
/**
 * Smart Grid Layout - Duolingo Style
 * 
 * Flexible grid layout with configurable columns (2-4).
 * Features Duolingo's card-based design with colorful accents.
 * 
 * Slots: header, col1, col2, col3, col4 (EXACTLY these names - same as slidev-project)
 * Parameters: cols: 2 | 3 | 4
 */
import { computed, inject } from 'vue'
import SlideShell from './SlideShell.vue'

const props = defineProps<{
  cols?: number
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'playful' | 'expressive'
}>()

const injectedVibe = inject('vibe', computed(() => props.vibe || 'playful'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'playful')

const columnCount = computed(() => {
  const cols = props.cols || 3
  return Math.max(2, Math.min(4, cols))
})

const gridStyle = computed(() => ({
  gridTemplateColumns: `repeat(${columnCount.value}, 1fr)`
}))

const vibeClass = computed(() => `vibe-${currentVibe.value}`)

// Duolingo-style accent colors for each column
const colColors = ['#58CC02', '#1CB0F6', '#FF9600', '#CE82FF']
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="smart-grid" :class="vibeClass">
      <!-- Full-width header -->
      <div class="grid-header">
        <slot name="header" />
      </div>
      
      <!-- Grid container -->
      <div class="grid-container" :style="gridStyle">
        <div v-if="columnCount >= 1" class="grid-cell" :style="{ '--accent-color': colColors[0] }">
          <div class="cell-accent"></div>
          <div class="cell-content">
            <slot name="col1" />
          </div>
        </div>
        <div v-if="columnCount >= 2" class="grid-cell" :style="{ '--accent-color': colColors[1] }">
          <div class="cell-accent"></div>
          <div class="cell-content">
            <slot name="col2" />
          </div>
        </div>
        <div v-if="columnCount >= 3" class="grid-cell" :style="{ '--accent-color': colColors[2] }">
          <div class="cell-accent"></div>
          <div class="cell-content">
            <slot name="col3" />
          </div>
        </div>
        <div v-if="columnCount >= 4" class="grid-cell" :style="{ '--accent-color': colColors[3] }">
          <div class="cell-accent"></div>
          <div class="cell-content">
            <slot name="col4" />
          </div>
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.smart-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
  height: 100%;
  padding: 1.5rem;
}

.grid-header {
  color: var(--theme-text);
  font-weight: 800;
  font-family: var(--font-heading);
  text-align: center;
}

.grid-header :deep(h1),
.grid-header :deep(h2),
.grid-header :deep(h3) {
  color: var(--theme-text);
  margin: 0;
  font-weight: 800;
}

.grid-header :deep(h1) {
  font-size: 2rem;
}

.grid-container {
  flex: 1;
  display: grid;
  gap: 1rem;
  min-height: 0;
}

.grid-cell {
  background: var(--theme-bg-card);
  border-radius: var(--radius-lg);
  border: 2px solid var(--theme-border);
  box-shadow: var(--shadow-card);
  overflow: hidden;
  color: var(--theme-text);
  position: relative;
  display: flex;
  flex-direction: column;
}

.cell-accent {
  height: 6px;
  background: var(--accent-color, var(--theme-primary));
  flex-shrink: 0;
}

.cell-content {
  padding: 1.5rem;
  flex: 1;
}

.cell-content :deep(h1),
.cell-content :deep(h2),
.cell-content :deep(h3),
.cell-content :deep(h4) {
  color: var(--accent-color, var(--theme-primary));
  font-weight: 700;
  margin-bottom: 0.75rem;
}

.cell-content :deep(p) {
  color: var(--theme-text-muted);
  line-height: 1.6;
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  gap: 1rem;
  padding: 1rem;
}

.vibe-minimal .grid-container {
  gap: 0.75rem;
}

.vibe-minimal .grid-cell {
  border-radius: var(--radius-sm);
  box-shadow: none;
  border: 1px solid var(--theme-border);
}

.vibe-minimal .cell-accent {
  height: 3px;
}

.vibe-minimal .cell-content {
  padding: 1rem;
}

/* === VIBE: CLEAN === */
.vibe-clean .grid-cell {
  border-width: 1px;
  box-shadow: 0 1px 0 var(--theme-border);
}

.vibe-clean .cell-accent {
  height: 4px;
}

/* === VIBE: PLAYFUL === */
.vibe-playful .grid-cell {
  border-radius: var(--radius-xl);
  border-width: 3px;
  border-color: var(--accent-color, var(--theme-primary));
  transform: rotate(-0.5deg);
}

.vibe-playful .grid-cell:nth-child(even) {
  transform: rotate(0.5deg);
}

.vibe-playful .cell-accent {
  height: 8px;
}

.vibe-playful .cell-content {
  padding: 1.75rem;
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 2rem;
  gap: 2rem;
}

.vibe-expressive .grid-container {
  gap: 1.5rem;
}

.vibe-expressive .grid-cell {
  border-radius: var(--radius-xl);
  border-width: 4px;
  border-color: var(--accent-color, var(--theme-primary));
  box-shadow: 0 6px 0 color-mix(in srgb, var(--accent-color, var(--theme-primary)) 60%, transparent);
}

.vibe-expressive .cell-accent {
  height: 0;
  display: none;
}

.vibe-expressive .grid-cell {
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--accent-color) 10%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.vibe-expressive .cell-content {
  padding: 2rem;
}

.vibe-expressive .grid-header :deep(h1),
.vibe-expressive .grid-header :deep(h2) {
  font-size: 2.5rem;
  background: linear-gradient(90deg, var(--theme-primary), var(--theme-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
