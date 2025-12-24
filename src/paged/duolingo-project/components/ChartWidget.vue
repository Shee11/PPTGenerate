<template>
  <div class="chart-widget" :class="chartType">
    <div v-if="title" class="chart-title">
      <span class="title-icon">{{ titleIcon }}</span>
      {{ title }}
    </div>
    <div class="chart-container">
      <!-- Bar Chart -->
      <div v-if="chartType === 'bar'" class="bar-chart">
        <div 
          v-for="(item, index) in data" 
          :key="index" 
          class="bar-item"
          :style="{ '--bar-index': index }"
        >
          <div class="bar-label">{{ item.label }}</div>
          <div class="bar-track">
            <div 
              class="bar-fill" 
              :style="{ 
                width: `${item.value}%`, 
                backgroundColor: item.color || duoColors[index % duoColors.length] 
              }"
            >
            </div>
            <span class="bar-value">{{ item.value }}{{ unit }}</span>
          </div>
        </div>
      </div>

      <!-- Line Chart -->
      <div v-else-if="chartType === 'line'" class="line-chart">
        <svg :viewBox="`0 0 ${width} ${height}`" class="line-svg">
          <!-- Grid lines -->
          <g class="grid-lines">
            <line v-for="i in 4" :key="i" 
              :x1="0" 
              :y1="height * i / 5" 
              :x2="width" 
              :y2="height * i / 5" 
              stroke="#E5E5E5" 
              stroke-width="1"
              stroke-dasharray="4,4"
            />
          </g>
          
          <!-- Area fill -->
          <path
            :d="areaPath"
            :fill="`url(#gradient-${chartId})`"
            opacity="0.3"
          />
          
          <!-- Line -->
          <polyline
            :points="linePoints"
            fill="none"
            :stroke="color || duoColors[0]"
            stroke-width="4"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          
          <!-- Data points -->
          <g v-for="(point, index) in points" :key="index">
            <circle
              :cx="point.x"
              :cy="point.y"
              r="8"
              fill="white"
              :stroke="color || duoColors[0]"
              stroke-width="4"
              class="data-point"
              :style="{ '--point-index': index }"
            />
          </g>
          
          <!-- Gradient definition -->
          <defs>
            <linearGradient :id="`gradient-${chartId}`" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" :stop-color="color || duoColors[0]" />
              <stop offset="100%" stop-color="white" />
            </linearGradient>
          </defs>
        </svg>
        <div class="line-labels">
          <span v-for="(item, index) in data" :key="index" class="line-label">
            {{ item.label }}
          </span>
        </div>
      </div>

      <!-- Pie/Donut Chart -->
      <div v-else-if="chartType === 'pie' || chartType === 'donut'" class="pie-chart">
        <div class="pie-wrapper">
          <svg viewBox="0 0 200 200" class="pie-svg">
            <circle
              v-for="(segment, index) in pieSegments"
              :key="index"
              cx="100"
              cy="100"
              :r="chartType === 'donut' ? 60 : 80"
              fill="transparent"
              :stroke="segment.color"
              :stroke-width="chartType === 'donut' ? 35 : 80"
              :stroke-dasharray="`${segment.length} ${circumference - segment.length}`"
              :stroke-dashoffset="`${-segment.offset}`"
              transform="rotate(-90 100 100)"
              class="pie-segment"
              :style="{ '--segment-index': index }"
            />
          </svg>
          <div v-if="chartType === 'donut'" class="donut-center">
            <span class="donut-icon">🎯</span>
            <span class="donut-total">{{ total }}{{ unit }}</span>
          </div>
        </div>
        <div class="pie-legend">
          <div 
            v-for="(item, index) in data" 
            :key="index" 
            class="legend-item"
            :style="{ '--legend-index': index }"
          >
            <span class="legend-color" :style="{ backgroundColor: item.color || duoColors[index % duoColors.length] }"></span>
            <span class="legend-text">{{ item.label }}</span>
            <span class="legend-value">{{ item.value }}{{ unit }}</span>
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

// Duolingo color palette
const duoColors = ['#58CC02', '#1CB0F6', '#FF9600', '#CE82FF', '#FF4B4B', '#2DBBC4']

// Unique chart ID
const chartId = computed(() => Math.random().toString(36).substr(2, 9))

// Chart type icons
const titleIcon = computed(() => {
  const icons = {
    bar: '📊',
    line: '📈',
    pie: '🥧',
    donut: '🍩',
  }
  return icons[props.chartType] || '📊'
})

// Total for donut center
const total = computed(() => {
  return props.data.reduce((sum, item) => sum + item.value, 0)
})

// Line chart calculations
const points = computed(() => {
  if (props.chartType !== 'line' || !props.data.length) return []
  const maxValue = Math.max(...props.data.map(d => d.value))
  const padding = 20
  const availableWidth = props.width - padding * 2
  const availableHeight = props.height - padding * 2
  const step = availableWidth / (props.data.length - 1)
  
  return props.data.map((item, i) => ({
    x: padding + i * step,
    y: padding + availableHeight - (item.value / maxValue) * availableHeight,
  }))
})

const linePoints = computed(() => {
  return points.value.map(p => `${p.x},${p.y}`).join(' ')
})

const areaPath = computed(() => {
  if (!points.value.length) return ''
  const pts = points.value
  const startX = pts[0].x
  const endX = pts[pts.length - 1].x
  const bottom = props.height - 20
  
  return `M ${startX},${bottom} L ${linePoints.value} L ${endX},${bottom} Z`
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
      color: item.color || duoColors[index % duoColors.length],
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
  background: white;
  border-radius: 20px;
  height: 100%;
  box-shadow: 
    0 4px 0 var(--duo-green-dark, #46a302),
    0 8px 20px rgba(88, 204, 2, 0.15);
  border: 3px solid var(--duo-green, #58CC02);
  position: relative;
}

.chart-title {
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 1.25rem;
  color: var(--duo-text, #4B4B4B);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.title-icon {
  font-size: 1.5rem;
}

.chart-container {
  height: calc(100% - 3rem);
}

/* Bar Chart */
.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
  justify-content: center;
}

.bar-item {
  animation: bar-enter 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
  animation-delay: calc(var(--bar-index) * 0.1s);
}

@keyframes bar-enter {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
}

.bar-label {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--duo-gray-dark, #777);
  margin-bottom: 0.35rem;
}

.bar-track {
  height: 28px;
  background: var(--duo-gray-light, #F7F7F7);
  border-radius: 14px;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
}

.bar-fill {
  height: 100%;
  border-radius: 14px;
  transition: width 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
}

.bar-value {
  position: absolute;
  right: 0.75rem;
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
  font-size: 0.875rem;
  font-weight: 800;
  color: var(--duo-text, #4B4B4B);
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

.data-point {
  animation: point-pop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
  animation-delay: calc(var(--point-index) * 0.1s + 0.3s);
}

@keyframes point-pop {
  from {
    r: 0;
  }
}

.line-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 0.75rem;
  padding: 0 20px;
}

.line-label {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--duo-gray-dark, #777);
}

/* Pie/Donut Chart */
.pie-chart {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  height: 100%;
}

.pie-wrapper {
  position: relative;
  width: 160px;
  height: 160px;
  flex-shrink: 0;
}

.pie-svg {
  width: 100%;
  height: 100%;
}

.pie-segment {
  animation: segment-draw 0.6s ease-out backwards;
  animation-delay: calc(var(--segment-index) * 0.15s);
}

@keyframes segment-draw {
  from {
    stroke-dasharray: 0 1000;
  }
}

.donut-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.donut-icon {
  font-size: 1.5rem;
  display: block;
}

.donut-total {
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--duo-text, #4B4B4B);
}

.pie-legend {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  animation: legend-enter 0.3s ease-out backwards;
  animation-delay: calc(var(--legend-index) * 0.1s + 0.4s);
}

@keyframes legend-enter {
  from {
    opacity: 0;
    transform: translateX(10px);
  }
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  flex-shrink: 0;
}

.legend-text {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--duo-text, #4B4B4B);
  flex: 1;
}

.legend-value {
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
  font-size: 0.9rem;
  font-weight: 800;
  color: var(--duo-text, #4B4B4B);
}
</style>
