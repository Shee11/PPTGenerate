<!--
  ChartWidget.vue - Handdrawn Chart Placeholder Component
  
  Props:
    - type: Chart type
    - title: Chart title
    - data: Chart data points
-->
<template>
  <div class="chart-widget" :class="`chart-${type}`">
    <div class="chart-paper">
      <!-- Grid background -->
      <div class="chart-grid"></div>
      
      <!-- Title -->
      <div v-if="title" class="chart-title">
        <span class="title-icon">📊</span>
        {{ title }}
      </div>
      
      <!-- Chart area -->
      <div class="chart-area">
        <slot>
          <!-- Default bar chart visualization -->
          <div v-if="type === 'bar'" class="bar-chart">
            <div 
              v-for="(item, i) in data" 
              :key="i" 
              class="bar-item"
              :style="{ '--bar-height': `${item.value}%`, '--bar-delay': `${i * 0.1}s` }"
            >
              <div class="bar" :class="`bar-${['pink', 'blue', 'green', 'yellow'][i % 4]}`"></div>
              <div class="bar-label">{{ item.label }}</div>
            </div>
          </div>
          
          <!-- Line chart placeholder -->
          <div v-else-if="type === 'line'" class="line-chart">
            <svg viewBox="0 0 200 100" class="line-svg">
              <path d="M10,80 Q50,60 80,40 T130,50 T180,20" fill="none" stroke="var(--hand-pink)" stroke-width="3"/>
              <circle v-for="(_, i) in 5" :key="i" :cx="10 + i * 42" :cy="[80, 60, 40, 50, 20][i]" r="5" fill="var(--hand-pink)"/>
            </svg>
          </div>
          
          <!-- Pie chart placeholder -->
          <div v-else-if="type === 'pie'" class="pie-chart">
            <div class="pie-circle">
              <div class="pie-segment segment-1"></div>
              <div class="pie-segment segment-2"></div>
              <div class="pie-segment segment-3"></div>
              <div class="pie-center">📈</div>
            </div>
          </div>
        </slot>
      </div>
      
      <!-- Legend -->
      <div v-if="data.length" class="chart-legend">
        <div v-for="(item, i) in data" :key="i" class="legend-item">
          <span class="legend-dot" :class="`dot-${['pink', 'blue', 'green', 'yellow'][i % 4]}`"></span>
          <span class="legend-text">{{ item.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface DataPoint {
  label: string
  value: number
}

withDefaults(defineProps<{
  type?: 'bar' | 'line' | 'pie'
  title?: string
  data?: DataPoint[]
}>(), {
  type: 'bar',
  data: () => []
})
</script>

<style scoped>
.chart-widget {
  width: 100%;
}

.chart-paper {
  position: relative;
  background: var(--hand-bg-cream);
  border: 2px solid var(--hand-text-light);
  border-radius: 8px;
  padding: 1.25rem;
  box-shadow: 3px 3px 0 var(--hand-shadow-color);
}

/* Grid */
.chart-grid {
  position: absolute;
  inset: 1.25rem;
  background-image: 
    linear-gradient(var(--hand-blue-light) 1px, transparent 1px),
    linear-gradient(90deg, var(--hand-blue-light) 1px, transparent 1px);
  background-size: 25px 25px;
  opacity: 0.5;
  pointer-events: none;
}

/* Title */
.chart-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--hand-font-display);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--hand-text-dark);
  margin-bottom: 1rem;
  position: relative;
  z-index: 2;
}

.title-icon {
  font-size: 1rem;
}

/* Chart area */
.chart-area {
  position: relative;
  z-index: 2;
  min-height: 150px;
}

/* Bar chart */
.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 150px;
  padding-top: 1rem;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.bar {
  width: 40px;
  height: var(--bar-height);
  border-radius: 4px 4px 0 0;
  animation: bar-grow 0.5s ease-out backwards;
  animation-delay: var(--bar-delay);
}

@keyframes bar-grow {
  from {
    height: 0;
  }
}

.bar-pink { background: var(--hand-pink); }
.bar-blue { background: var(--hand-blue); }
.bar-green { background: var(--hand-green); }
.bar-yellow { background: var(--hand-yellow-dark); }

.bar-label {
  font-family: var(--hand-font-handwriting);
  font-size: 0.8rem;
  color: var(--hand-text);
}

/* Line chart */
.line-chart {
  display: flex;
  justify-content: center;
}

.line-svg {
  width: 100%;
  max-width: 300px;
  height: 120px;
}

/* Pie chart */
.pie-chart {
  display: flex;
  justify-content: center;
}

.pie-circle {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: conic-gradient(
    var(--hand-pink) 0deg 120deg,
    var(--hand-blue) 120deg 220deg,
    var(--hand-green) 220deg 360deg
  );
  border: 3px solid var(--hand-text-light);
}

.pie-center {
  position: absolute;
  inset: 30%;
  background: var(--hand-bg-cream);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

/* Legend */
.chart-legend {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 1rem;
  flex-wrap: wrap;
  position: relative;
  z-index: 2;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.dot-pink { background: var(--hand-pink); }
.dot-blue { background: var(--hand-blue); }
.dot-green { background: var(--hand-green); }
.dot-yellow { background: var(--hand-yellow-dark); }

.legend-text {
  font-family: var(--hand-font-body);
  font-size: 0.8rem;
  color: var(--hand-text);
}
</style>
