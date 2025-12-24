<!--
  MetricWidget.vue - Handdrawn Metric Display Component
  
  Props:
    - value: The metric value
    - label: Metric label
    - change: Optional change indicator
    - color: Color variant (pink, blue, green, yellow)
-->
<template>
  <div class="metric-widget" :class="`metric-${color}`">
    <div class="metric-value">
      <slot name="value">{{ value }}</slot>
    </div>
    <div class="metric-label">
      <slot name="label">{{ label }}</slot>
    </div>
    <div v-if="change" class="metric-change" :class="{ negative: change.startsWith('-') }">
      {{ change }}
    </div>
    <div class="metric-doodle">{{ ['📈', '📊', '📉', '💹'][Math.floor(Math.random() * 4)] }}</div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  value?: string | number
  label?: string
  change?: string
  color?: 'pink' | 'blue' | 'green' | 'yellow'
}>(), {
  value: '0',
  label: 'Metric',
  color: 'pink'
})
</script>

<style scoped>
.metric-widget {
  position: relative;
  padding: 1.25rem;
  border-radius: 8px;
  border: 2px solid;
  text-align: center;
  box-shadow: 3px 3px 0 var(--hand-shadow-color);
}

.metric-pink {
  border-color: var(--hand-pink);
  background: var(--hand-pink-light);
  transform: rotate(-1deg);
}

.metric-blue {
  border-color: var(--hand-blue);
  background: var(--hand-blue-light);
  transform: rotate(0.5deg);
}

.metric-green {
  border-color: var(--hand-green);
  background: var(--hand-green-light);
  transform: rotate(-0.5deg);
}

.metric-yellow {
  border-color: var(--hand-yellow-dark);
  background: var(--hand-yellow);
  transform: rotate(1deg);
}

.metric-value {
  font-family: var(--hand-font-display);
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--hand-text-dark);
  line-height: 1;
}

.metric-label {
  font-family: var(--hand-font-handwriting);
  font-size: 1rem;
  color: var(--hand-text);
  margin-top: 0.25rem;
}

.metric-change {
  font-family: var(--hand-font-body);
  font-size: 0.85rem;
  color: var(--hand-green);
  margin-top: 0.25rem;
}

.metric-change.negative {
  color: var(--hand-pink);
}

.metric-doodle {
  position: absolute;
  top: -8px;
  right: -8px;
  font-size: 1rem;
}
</style>
