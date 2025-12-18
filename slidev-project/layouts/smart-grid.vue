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
  gap: 1.5rem;
  width: 100%;
  height: 100%;
  padding: 2rem;
  background-color: var(--c-bg-base);
  grid-template-rows: auto 1fr;
}

.grid-header {
  grid-column: 1 / -1; /* Span all columns */
  margin-bottom: 1rem;
  color: var(--c-text-main);
}

.grid-cell {
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--border-theme);
  overflow: auto;
  color: var(--c-text-main);
}
</style>
