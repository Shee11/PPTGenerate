<!--
  ChartWidget.vue - Business Chart Component
  
  Clean, professional chart component for data visualization.
  Supports bar, line, pie, and donut charts.
  
  Props:
    - chartType: Type of chart (bar, line, pie, donut)
    - title: Chart title
    - data: Array of data points
    - unit: Unit suffix for values
-->
<template>
  <div class="chart-widget" :class="chartType">
    <div v-if="title" class="chart-title">{{ title }}</div>
    <div class="chart-container">
      <!-- Bar Chart -->
      <div v-if="chartType === 'bar'" class="bar-chart">
        <div v-for="(item, index) in data" :key="index" class="bar-item">
          <div class="bar-label">{{ item.label }}</div>
          <div class="bar-track">
            <div 
              class="bar-fill" 
              :style="{ width: `${item.value}%`, backgroundColor: item.color || 'var(--c-primary, #0F4C81)' }"
            >
              <span class="bar-value">{{ item.value }}{{ unit }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Line Chart -->
      <div v-else-if="chartType === 'line'" class="line-chart">
        <svg :viewBox="`0 0 ${width} ${height}`" class="line-svg">
          <polyline
            :points="linePoints"
            fill="none"
            :stroke="color || 'var(--c-primary, #0F4C81)'"
            stroke-width="2"
          />
          <circle
            v-for="(point, index) in points"
            :key="index"
            :cx="point.x"
            :cy="point.y"
            r="4"
            :fill="color || 'var(--c-primary, #0F4C81)'"
          />
        </svg>
        <div class="line-labels">
          <span v-for="(item, index) in data" :key="index" class="line-label">
            {{ item.label }}
          </span>
        </div>
      </div>

      <!-- Pie/Donut Chart -->
      <div v-else-if="chartType === 'pie' || chartType === 'donut'" class="pie-chart">
        <svg :viewBox="`0 0 200 200`" class="pie-svg">
          <circle
            v-for="(segment, index) in pieSegments"
            :key="index"
            :cx="100"
            :cy="100"
            :r="chartType === 'donut' ? 60 : 80"
            fill="transparent"
            :stroke="segment.color"
            :stroke-width="chartType === 'donut' ? 30 : 80"
            :stroke-dasharray="`${segment.length} ${circumference - segment.length}`"
            :stroke-dashoffset="`${-segment.offset}`"
            :transform="`rotate(-90 100 100)`"
          />
        </svg>
        <div class="pie-legend">
          <div v-for="(item, index) in data" :key="index" class="legend-item">
            <span class="legend-color" :style="{ backgroundColor: item.color }"></span>
            <span class="legend-text">{{ item.label }}: {{ item.value }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  chartType: {
    type: String,
    default: 'bar',
  },
  title: String,
  data: {
    type: Array,
    default: () => [],
  },
  unit: {
    type: String,
    default: '%',
  },
  color: String,
  width: {
    type: Number,
    default: 400,
  },
  height: {
    type: Number,
    default: 200,
  },
})

// Line chart calculations
const points = computed(() => {
  if (!props.data.length) return []
  const maxValue = Math.max(...props.data.map(d => d.value))
  const padding = 20
  const usableWidth = props.width - padding * 2
  const usableHeight = props.height - padding * 2
  
  return props.data.map((item, index) => ({
    x: padding + (usableWidth / (props.data.length - 1 || 1)) * index,
    y: padding + usableHeight - (item.value / maxValue) * usableHeight
  }))
})

const linePoints = computed(() => {
  return points.value.map(p => `${p.x},${p.y}`).join(' ')
})

// Pie chart calculations
const circumference = computed(() => 2 * Math.PI * (props.chartType === 'donut' ? 60 : 80))

const pieSegments = computed(() => {
  const total = props.data.reduce((sum, item) => sum + item.value, 0)
  let offset = 0
  
  return props.data.map((item, index) => {
    const length = (item.value / total) * circumference.value
    const segment = {
      color: item.color || getDefaultColor(index),
      length,
      offset
    }
    offset += length
    return segment
  })
})

const getDefaultColor = (index) => {
  const colors = ['#0F4C81', '#E67E22', '#27AE60', '#9B59B6', '#34495E']
  return colors[index % colors.length]
}
</script>

<style scoped>
.chart-widget {
  background: var(--c-bg-surface, #ffffff);
  border-radius: var(--radius-card, 8px);
  padding: 1.5rem;
  border: 1px solid var(--c-border, #e5e7eb);
  height: 100%;
}

.chart-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--c-text-primary, #1a1a1a);
  margin-bottom: 1.25rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.chart-container {
  height: calc(100% - 2.5rem);
}

/* Bar Chart */
.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.bar-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.bar-label {
  font-size: 0.85rem;
  color: var(--c-text-secondary, #6b7280);
  font-weight: 500;
}

.bar-track {
  height: 28px;
  background: var(--c-bg-muted, #f3f4f6);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 0.75rem;
  transition: width 0.6s ease;
  min-width: fit-content;
  border-radius: 4px;
}

.bar-value {
  font-size: 0.8rem;
  font-weight: 600;
  color: white;
}

/* Line Chart */
.line-chart {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.line-svg {
  flex: 1;
  width: 100%;
}

.line-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
}

.line-label {
  font-size: 0.75rem;
  color: var(--c-text-secondary, #6b7280);
}

/* Pie Chart */
.pie-chart {
  display: flex;
  align-items: center;
  gap: 2rem;
  height: 100%;
}

.pie-svg {
  width: 150px;
  height: 150px;
  flex-shrink: 0;
}

.pie-legend {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  flex-shrink: 0;
}

.legend-text {
  font-size: 0.85rem;
  color: var(--c-text-secondary, #6b7280);
}
</style>
