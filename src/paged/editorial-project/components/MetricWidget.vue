<!--
  MetricWidget.vue - Editorial Metric Widget
  
  Props:
    - value: Metric value
    - label: Metric label
    - sublabel: Optional sublabel
-->
<template>
  <div class="metric-widget">
    <span class="metric-value">{{ value }}</span>
    <span class="metric-label">{{ label }}</span>
    <span v-if="sublabel" class="metric-sublabel">{{ sublabel }}</span>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  value: string
  label: string
  sublabel?: string
}>(), {})
</script>

<style scoped>
.metric-widget {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  text-align: center;
}

.metric-value {
  font-family: var(--edit-font-display);
  font-size: 3rem;
  font-weight: 400;
  color: var(--edit-gold);
  line-height: 1;
}

.metric-label {
  font-family: var(--edit-font-accent);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--edit-text);
}

.metric-sublabel {
  font-family: var(--edit-font-body);
  font-size: 0.85rem;
  font-style: italic;
  color: var(--edit-text-light);
}
</style>
