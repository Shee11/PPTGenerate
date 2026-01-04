<!--
  ChartWidget.vue - Cyberpunk Chart Display Widget
  
  Props:
    - title: Chart title
    - type: Chart type (bar, line, pie)
    - data: Chart data points
-->
<template>
  <div class="chart-widget">
    <div class="chart-header">
      <span class="chart-icon">[#]</span>
      <span class="chart-title">{{ title }}</span>
    </div>
    <div class="chart-container" :class="`chart-${type}`">
      <!-- Bar chart -->
      <div v-if="type === 'bar'" class="bar-chart">
        <div 
          v-for="(item, i) in data" 
          :key="i" 
          class="bar-item"
          :style="{ '--bar-height': `${item.value}%`, '--bar-index': i }"
        >
          <div class="bar-fill"></div>
          <span class="bar-label">{{ item.label }}</span>
          <span class="bar-value">{{ item.value }}</span>
        </div>
      </div>
      
      <!-- Line chart (simplified) -->
      <div v-if="type === 'line'" class="line-chart">
        <svg viewBox="0 0 200 100" class="line-svg">
          <path 
            :d="linePath" 
            class="line-path"
            fill="none"
            stroke-width="2"
          />
          <circle 
            v-for="(point, i) in linePoints" 
            :key="i"
            :cx="point.x"
            :cy="point.y"
            r="4"
            class="line-point"
          />
        </svg>
      </div>
      
      <!-- Placeholder for pie -->
      <div v-if="type === 'pie'" class="pie-chart">
        <div class="pie-placeholder">// PIE_CHART</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface DataPoint {
  label: string
  value: number
}

const props = withDefaults(defineProps<{
  title: string
  type?: 'bar' | 'line' | 'pie'
  data: DataPoint[]
}>(), {
  type: 'bar'
})

const linePoints = computed(() => {
  const maxVal = Math.max(...props.data.map(d => d.value))
  return props.data.map((d, i) => ({
    x: (i / (props.data.length - 1)) * 180 + 10,
    y: 90 - (d.value / maxVal) * 80
  }))
})

const linePath = computed(() => {
  return linePoints.value
    .map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`)
    .join(' ')
})
</script>

<style scoped>
.chart-widget {
  background: rgba(18, 18, 26, 0.8);
  border: 1px solid rgba(0, 255, 255, 0.2);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chart-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.chart-icon {
  font-family: var(--cyber-font-mono);
  font-size: 0.85rem;
  color: var(--cyber-magenta, #FF00FF);
  text-shadow: 0 0 5px var(--cyber-magenta-glow);
}

.chart-title {
  font-family: var(--cyber-font-display);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.chart-container {
  flex: 1;
  min-height: 120px;
}

/* Bar chart */
.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 100%;
  padding-top: 1.5rem;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  flex: 1;
  max-width: 60px;
  position: relative;
}

.bar-fill {
  width: 80%;
  height: var(--bar-height);
  background: linear-gradient(180deg, var(--cyber-cyan, #00FFFF), var(--cyber-magenta, #FF00FF));
  box-shadow: 0 0 15px var(--cyber-cyan-glow);
  animation: bar-grow 0.6s ease-out backwards;
  animation-delay: calc(var(--bar-index) * 0.1s);
}

@keyframes bar-grow {
  from { height: 0; }
}

.bar-label {
  font-family: var(--cyber-font-mono);
  font-size: 0.65rem;
  color: var(--cyber-text-dim);
  text-transform: uppercase;
}

.bar-value {
  position: absolute;
  top: 0;
  font-family: var(--cyber-font-mono);
  font-size: 0.7rem;
  color: var(--cyber-cyan, #00FFFF);
}

/* Line chart */
.line-chart {
  height: 100%;
  padding: 0.5rem;
}

.line-svg {
  width: 100%;
  height: 100%;
}

.line-path {
  stroke: var(--cyber-cyan, #00FFFF);
  filter: drop-shadow(0 0 5px var(--cyber-cyan-glow));
}

.line-point {
  fill: var(--cyber-magenta, #FF00FF);
  filter: drop-shadow(0 0 5px var(--cyber-magenta-glow));
}

/* Pie chart placeholder */
.pie-chart {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.pie-placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 0.8rem;
}
</style>
