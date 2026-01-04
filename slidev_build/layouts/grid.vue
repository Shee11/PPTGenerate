<!--
  grid.vue - Grid Layout for Cards/Metrics
  
  Purpose: Grid of cards, metrics, or other repeated content
  
  Props:
    - columns: Number of columns (2, 3, 4)
  
  Slots:
    - header: Optional header above grid
    - default: Grid items
    - footer: Optional footer below grid
-->
<template>
  <SlideShell :theme="theme" :header="header" :footer="slideFooter">
    <div class="grid-layout">
      <!-- Header section -->
      <div v-if="$slots.header" class="header-section">
        <slot name="header" />
      </div>
      
      <!-- Grid content -->
      <div class="grid-container" :style="gridStyle">
        <slot />
      </div>
      
      <!-- Footer section -->
      <div v-if="$slots.footer" class="footer-section">
        <slot name="footer" />
      </div>
    </div>
  </SlideShell>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import SlideShell from './SlideShell.vue'

const props = withDefaults(defineProps<{
  theme?: string
  header?: string
  slideFooter?: string
  columns?: 2 | 3 | 4
}>(), {
  theme: 'default',
  columns: 2
})

const gridStyle = computed(() => ({
  gridTemplateColumns: `repeat(${props.columns}, 1fr)`
}))
</script>

<style scoped>
.grid-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.header-section {
  margin-bottom: 32px;
  flex-shrink: 0;
}

.header-section :deep(h1),
.header-section :deep(h2) {
  font-size: 2rem;
  font-weight: 600;
  color: var(--c-text);
  margin: 0;
}

.grid-container {
  flex: 1;
  display: grid;
  gap: 24px;
  align-content: center;
}

.footer-section {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--c-border);
  flex-shrink: 0;
  font-size: 0.9375rem;
  color: var(--c-text-muted);
}
</style>
