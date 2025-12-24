<!--
  ChartWidget.vue - Editorial Chart Widget Placeholder
  
  Props:
    - title: Chart title
    - type: Chart type (bar, line, pie)
    - height: Chart height
-->
<template>
  <div class="chart-widget">
    <h4 v-if="title" class="chart-title">{{ title }}</h4>
    <div class="chart-area" :style="{ height: height }">
      <div class="chart-placeholder">
        <span class="chart-icon">📊</span>
        <span class="chart-label">{{ type }} chart</span>
      </div>
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title?: string
  type?: 'bar' | 'line' | 'pie' | 'area'
  height?: string
}>(), {
  type: 'bar',
  height: '200px'
})
</script>

<style scoped>
.chart-widget {
  width: 100%;
}

.chart-title {
  font-family: var(--edit-font-display);
  font-size: 1rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0 0 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--edit-border);
}

.chart-area {
  position: relative;
  background: var(--edit-white);
  border: 1px solid var(--edit-border);
  border-radius: 2px;
  overflow: hidden;
}

.chart-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, var(--edit-light) 0%, var(--edit-white) 100%);
}

.chart-icon {
  font-size: 2rem;
  opacity: 0.5;
}

.chart-label {
  font-family: var(--edit-font-accent);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--edit-text-light);
}

/* Hide placeholder when slot has content */
.chart-area:has(> :not(.chart-placeholder)) .chart-placeholder {
  display: none;
}
</style>
