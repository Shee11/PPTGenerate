<!--
  MetricWidget.vue - Cyberpunk Metric Display Widget
  
  Props:
    - value: The metric value
    - label: Description label
    - trend: Optional trend indicator (up/down/neutral)
    - unit: Optional unit suffix
-->
<template>
  <div class="metric-widget" :class="[`trend-${trend}`]">
    <div class="metric-glow"></div>
    <div class="metric-value">
      <span class="value-text">{{ value }}</span>
      <span v-if="unit" class="value-unit">{{ unit }}</span>
    </div>
    <div class="metric-label">{{ label }}</div>
    <div v-if="trend && trend !== 'neutral'" class="metric-trend">
      <span class="trend-icon">{{ trend === 'up' ? '▲' : '▼' }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  value: string | number
  label: string
  trend?: 'up' | 'down' | 'neutral'
  unit?: string
}>(), {
  trend: 'neutral'
})
</script>

<style scoped>
.metric-widget {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 1.5rem;
  background: rgba(18, 18, 26, 0.8);
  border: 1px solid rgba(0, 255, 255, 0.2);
  overflow: hidden;
}

.metric-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--cyber-cyan, #00FFFF);
  box-shadow: 0 0 20px var(--cyber-cyan-glow);
}

.metric-value {
  display: flex;
  align-items: baseline;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}

.value-text {
  font-family: var(--cyber-font-display);
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-shadow: 0 0 20px var(--cyber-cyan-glow);
  line-height: 1;
}

.value-unit {
  font-family: var(--cyber-font-mono);
  font-size: 1rem;
  color: var(--cyber-text-dim);
}

.metric-label {
  font-family: var(--cyber-font-mono);
  font-size: 0.8rem;
  color: var(--cyber-text, #e0e0e0);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.metric-trend {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
}

.trend-icon {
  font-size: 0.8rem;
}

/* Trend modifiers */
.trend-up .metric-glow {
  background: var(--cyber-green, #00FF41);
  box-shadow: 0 0 20px var(--cyber-green-glow);
}

.trend-up .value-text {
  color: var(--cyber-green, #00FF41);
  text-shadow: 0 0 20px var(--cyber-green-glow);
}

.trend-up .trend-icon {
  color: var(--cyber-green, #00FF41);
}

.trend-down .metric-glow {
  background: var(--cyber-pink, #FF0080);
  box-shadow: 0 0 20px var(--cyber-pink-glow);
}

.trend-down .value-text {
  color: var(--cyber-pink, #FF0080);
  text-shadow: 0 0 20px var(--cyber-pink-glow);
}

.trend-down .trend-icon {
  color: var(--cyber-pink, #FF0080);
}
</style>
