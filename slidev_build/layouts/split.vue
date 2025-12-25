<!--
  split.vue - Two Column Split Layout
  
  Purpose: Two-column layout with configurable ratio
  Columns are horizontally left-aligned, vertically center-aligned
  
  Props:
    - ratio: Column ratio ('50-50', '40-60', '60-40')
  
  Slots:
    - header: Optional header above columns
    - left: Left column content
    - right: Right column content
-->
<template>
  <SlideShell :theme="theme" :header="header" :footer="footer">
    <div class="split-layout">
      <!-- Header section -->
      <div v-if="$slots.header" class="header-section">
        <slot name="header" />
      </div>
      
      <!-- Two columns -->
      <div class="columns-container">
        <div class="column column-left" :style="leftStyle">
          <slot name="left" />
        </div>
        <div class="column column-right" :style="rightStyle">
          <slot name="right" />
        </div>
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
  footer?: string
  ratio?: '50-50' | '40-60' | '60-40'
}>(), {
  theme: 'default',
  ratio: '50-50'
})

const ratioMap: Record<string, [number, number]> = {
  '50-50': [1, 1],
  '40-60': [2, 3],
  '60-40': [3, 2],
}

const leftStyle = computed(() => ({
  flex: ratioMap[props.ratio]?.[0] || 1
}))

const rightStyle = computed(() => ({
  flex: ratioMap[props.ratio]?.[1] || 1
}))
</script>

<style scoped>
.split-layout {
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

.columns-container {
  flex: 1;
  display: flex;
  gap: 48px;
  min-height: 0;
}

.column {
  display: flex;
  flex-direction: column;
  justify-content: center; /* Vertically center aligned */
  align-items: flex-start; /* Horizontally left aligned */
  min-width: 0;
}

.column :deep(h1),
.column :deep(h2),
.column :deep(h3) {
  margin-bottom: 16px;
}

.column :deep(ul),
.column :deep(ol) {
  margin: 0;
  padding-left: 1.5em;
}

.column :deep(li) {
  margin-bottom: 12px;
  line-height: 1.5;
}

.column :deep(p) {
  margin-bottom: 12px;
  line-height: 1.6;
}

.column :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}
</style>
