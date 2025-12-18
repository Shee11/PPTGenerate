<script setup lang="ts">
import { computed } from 'vue'

// Props from frontmatter
const props = defineProps<{
  cols?: number
}>()

// Clamp cols to valid range (2-4)
const columnCount = computed(() => {
  const cols = props.cols || 3
  return Math.max(2, Math.min(4, cols))
})

// Generate grid template columns based on cols parameter
const gridStyle = computed(() => ({
  '--cols': columnCount.value,
  gridTemplateColumns: `repeat(${columnCount.value}, 1fr)`
}))
</script>

<template>
  <div class="smart-grid-layout" :style="gridStyle">
    <!-- Full-width header spanning all columns -->
    <div class="grid-header">
      <slot name="header" />
    </div>
    
    <!-- Column slots (only render up to cols count) -->
    <div v-if="columnCount >= 1" class="grid-cell bg-theme-surface border-theme shadow-theme">
      <slot name="col1" />
    </div>
    <div v-if="columnCount >= 2" class="grid-cell bg-theme-surface border-theme shadow-theme">
      <slot name="col2" />
    </div>
    <div v-if="columnCount >= 3" class="grid-cell bg-theme-surface border-theme shadow-theme">
      <slot name="col3" />
    </div>
    <div v-if="columnCount >= 4" class="grid-cell bg-theme-surface border-theme shadow-theme">
      <slot name="col4" />
    </div>
  </div>
</template>

<style scoped>
.smart-grid-layout {
  display: grid;
  gap: 2rem;
  width: 100%;
  height: 100%;
  padding: 3rem;
  background: linear-gradient(135deg, var(--c-bg-base) 0%, color-mix(in srgb, var(--c-bg-base) 95%, var(--slidev-theme-primary, #3b82f6)) 100%);
  grid-template-rows: auto 1fr;
  position: relative;
}

/* Decorative background mesh */
.smart-grid-layout::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 20% 30%, rgba(59, 130, 246, 0.03) 0%, transparent 50%),
              radial-gradient(circle at 80% 70%, rgba(139, 92, 246, 0.03) 0%, transparent 50%);
  pointer-events: none;
}

.grid-header {
  grid-column: 1 / -1;
  margin-bottom: 1.5rem;
  color: var(--c-text-main);
  font-weight: 600;
  position: relative;
  z-index: 1;
}

.grid-cell {
  padding: 2rem;
  border-radius: 12px;
  background: linear-gradient(145deg, 
    color-mix(in srgb, var(--c-bg-base) 98%, white) 0%, 
    color-mix(in srgb, var(--c-bg-base) 96%, white) 100%);
  border: 2px solid transparent;
  background-clip: padding-box;
  position: relative;
  overflow: auto;
  color: var(--c-text-main);
  box-shadow: 
    0 1px 3px rgba(0, 0, 0, 0.05),
    0 4px 12px rgba(0, 0, 0, 0.08),
    0 8px 24px rgba(0, 0, 0, 0.06);
  transition: transform 0.3s ease;
}

/* nth-child variations - break the grid monotony */
.grid-cell:nth-child(2) {
  transform: rotate(-1deg);
}

.grid-cell:nth-child(3) {
  transform: rotate(1deg) translateY(-5px);
}

.grid-cell:nth-child(4) {
  transform: rotate(-0.5deg) translateY(5px);
  border-radius: 16px 4px 16px 4px;
}

.grid-cell:nth-child(5) {
  transform: rotate(0.5deg);
  border-radius: 4px 16px 4px 16px;
}

/* Different aspect ratios for visual interest */
.grid-cell:nth-child(even) {
  padding: 2.5rem 2rem;
}

.grid-cell:nth-child(3n) {
  padding: 1.75rem 2.25rem;
}

/* Gradient border effect */
.grid-cell::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 12px;
  padding: 2px;
  background: linear-gradient(135deg, 
    var(--slidev-theme-primary, #3b82f6) 0%, 
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 70%, #8b5cf6) 50%,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 40%, transparent) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0.4;
  pointer-events: none;
}

/* Corner accent decorations */
.grid-cell::after {
  content: '';
  position: absolute;
  top: -1px;
  right: -1px;
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, var(--slidev-theme-primary, #3b82f6) 0%, transparent 70%);
  border-radius: 0 12px 0 12px;
  opacity: 0.15;
}

/* Position-based accent colors */
.grid-cell:nth-child(2)::before {
  background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
}

.grid-cell:nth-child(3)::before {
  background: linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%);
}

.grid-cell:nth-child(4)::before {
  background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%);
}

.grid-cell:nth-child(5)::before {
  background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
}
</style>
