<!--
  MetricWidget.vue - Metric/KPI Display
  
  Props:
    - value: Metric value
    - label: Metric label
    - description: Optional description
    - icon: Optional icon
-->
<template>
  <div class="metric-widget">
    <div v-if="icon" class="metric-icon">{{ icon }}</div>
    <div class="metric-value">{{ value }}</div>
    <div class="metric-label">{{ label }}</div>
    <div v-if="description" class="metric-description">{{ description }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  value: string | number
  label: string
  description?: string
  icon?: string
}>()
</script>

<style scoped>
.metric-widget {
  background: var(--c-bg-surface);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 8px;
}

.metric-icon {
  font-size: 1.5rem;
  margin-bottom: 4px;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--c-primary);
  line-height: 1;
}

.metric-label {
  font-size: 1rem;
  font-weight: 600;
  color: var(--c-text);
}

.metric-description {
  font-size: 0.875rem;
  color: var(--c-text-muted);
  line-height: 1.4;
}
</style>
