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
              :style="{ width: `${item.value}%`, backgroundColor: item.color || 'var(--slidev-theme-primary, #3b82f6)' }"
            >
              <span class="bar-value">{{ item.value }}{{ unit }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Line Chart (Simple) -->
      <div v-else-if="chartType === 'line'" class="line-chart">
        <svg :viewBox="`0 0 ${width} ${height}`" class="line-svg">
          <polyline
            :points="linePoints"
            fill="none"
            :stroke="color || 'var(--slidev-theme-primary, #3b82f6)'"
            stroke-width="3"
          />
          <circle
            v-for="(point, index) in points"
            :key="index"
            :cx="point.x"
            :cy="point.y"
            r="5"
            :fill="color || 'var(--slidev-theme-primary, #3b82f6)'"
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
            :stroke-width="chartType === 'donut' ? 40 : 80"
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
    default: 'bar', // bar, line, pie, donut
  },
  title: String,
  data: {
    type: Array,
    default: () => [],
    // Format: [{ label: 'Q1', value: 75, color: '#3b82f6' }, ...]
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
  if (props.chartType !== 'line' || !props.data.length) return []
  const maxValue = Math.max(...props.data.map(d => d.value))
  const step = props.width / (props.data.length - 1)
  return props.data.map((item, i) => ({
    x: i * step,
    y: props.height - (item.value / maxValue) * props.height * 0.8,
  }))
})

const linePoints = computed(() => {
  return points.value.map(p => `${p.x},${p.y}`).join(' ')
})

// Pie chart calculations
const circumference = computed(() => 2 * Math.PI * (props.chartType === 'donut' ? 60 : 80))

const pieSegments = computed(() => {
  if (!props.data.length) return []
  const total = props.data.reduce((sum, item) => sum + item.value, 0)
  let offset = 0
  return props.data.map((item, index) => {
    const percentage = item.value / total
    const length = percentage * circumference.value
    const segment = {
      color: item.color || `hsl(${index * 360 / props.data.length}, 70%, 60%)`,
      length,
      offset,
    }
    offset += length
    return segment
  })
})
</script>

<style scoped>
.chart-widget {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  height: 100%;
}

.chart-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--slidev-theme-text, #1f2937);
}

.chart-container {
  height: calc(100% - 2rem);
}

/* Bar Chart */
.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  height: 100%;
  justify-content: space-around;
}

.bar-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.bar-label {
  min-width: 4rem;
  font-weight: 500;
  font-size: 0.9rem;
}

.bar-track {
  flex: 1;
  height: 2rem;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 0.25rem;
  overflow: hidden;
  position: relative;
}

.bar-fill {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 0.5rem;
  transition: width 0.5s ease;
  border-radius: 0.25rem;
}

.bar-value {
  color: white;
  font-weight: 600;
  font-size: 0.85rem;
}

/* Line Chart */
.line-chart {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.line-svg {
  flex: 1;
  width: 100%;
}

.line-labels {
  display: flex;
  justify-content: space-around;
  margin-top: 0.5rem;
  font-size: 0.85rem;
}

/* Pie Chart */
.pie-chart {
  display: flex;
  align-items: center;
  gap: 2rem;
  height: 100%;
}

.pie-svg {
  width: 200px;
  height: 200px;
}

.pie-legend {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.legend-color {
  width: 1rem;
  height: 1rem;
  border-radius: 0.25rem;
}
</style>
