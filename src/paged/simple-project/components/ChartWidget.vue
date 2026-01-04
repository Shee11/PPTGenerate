<!--
  ChartWidget.vue - Simple Chart Display
  
  Props:
    - chartType: 'bar' | 'line' | 'pie'
    - title: Chart title
    - data: Chart data
-->
<template>
  <div class="chart-widget">
    <div v-if="title" class="chart-title">{{ title }}</div>
    <div class="chart-container">
      <!-- Bar Chart -->
      <div v-if="chartType === 'bar'" class="bar-chart">
        <div 
          v-for="(item, index) in normalizedData" 
          :key="index" 
          class="bar-item"
        >
          <div class="bar-label">{{ item.label }}</div>
          <div class="bar-track">
            <div 
              class="bar-fill" 
              :style="{ width: `${item.percent}%` }"
            >
              <span class="bar-value">{{ item.value }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Line Chart -->
      <div v-else-if="chartType === 'line'" class="line-chart">
        <svg :viewBox="`0 0 400 200`" class="line-svg">
          <polyline
            :points="linePoints"
            fill="none"
            stroke="var(--c-primary)"
            stroke-width="3"
          />
          <circle
            v-for="(point, index) in points"
            :key="index"
            :cx="point.x"
            :cy="point.y"
            r="5"
            fill="var(--c-primary)"
          />
        </svg>
        <div class="line-labels">
          <span v-for="(item, index) in data.labels" :key="index" class="line-label">
            {{ item }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface ChartData {
  labels: string[]
  values: number[]
}

const props = withDefaults(defineProps<{
  chartType?: 'bar' | 'line' | 'pie'
  title?: string
  data: ChartData
}>(), {
  chartType: 'bar'
})

const maxValue = computed(() => Math.max(...props.data.values))

const normalizedData = computed(() => {
  return props.data.labels.map((label, index) => ({
    label,
    value: props.data.values[index],
    percent: (props.data.values[index] / maxValue.value) * 100
  }))
})

// Line chart points
const points = computed(() => {
  const width = 400
  const height = 200
  const padding = 40
  const max = maxValue.value
  
  return props.data.values.map((value, index) => ({
    x: padding + (index / (props.data.values.length - 1)) * (width - padding * 2),
    y: height - padding - (value / max) * (height - padding * 2)
  }))
})

const linePoints = computed(() => {
  return points.value.map(p => `${p.x},${p.y}`).join(' ')
})
</script>

<style scoped>
.chart-widget {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chart-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--c-text);
}

.chart-container {
  flex: 1;
}

/* Bar Chart */
.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.bar-label {
  font-size: 0.875rem;
  color: var(--c-text-muted);
}

.bar-track {
  height: 32px;
  background: var(--c-bg-surface);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: var(--c-primary);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 8px;
  min-width: 40px;
  transition: width 0.3s ease;
}

.bar-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--c-bg-base);
}

/* Line Chart */
.line-chart {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.line-svg {
  width: 100%;
  height: auto;
}

.line-labels {
  display: flex;
  justify-content: space-between;
  padding: 0 40px;
}

.line-label {
  font-size: 0.75rem;
  color: var(--c-text-dim);
}
</style>
