<!--
  dashboard.vue - Handdrawn Dashboard Layout
  
  Slots:
    - title: Dashboard title
    - metric1, metric2, metric3, metric4: Metric widgets
    - chart: Main chart area
    - summary: Summary section
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="dashboard" :class="`vibe-${vibe}`">
      <!-- Title -->
      <div v-if="$slots.title" class="dashboard-title">
        <span class="title-icon">📊</span>
        <slot name="title" />
      </div>
      
      <!-- Metrics row -->
      <div class="metrics-row">
        <div 
          v-for="i in 4" 
          :key="i" 
          class="metric-card"
          :class="`metric-${['pink', 'blue', 'green', 'yellow'][i-1]}`"
          :style="{ '--metric-index': i }"
        >
          <slot :name="`metric${i}`">
            <span class="placeholder">📈 Metric {{ i }}</span>
          </slot>
        </div>
      </div>
      
      <!-- Main content -->
      <div class="dashboard-main">
        <!-- Chart area -->
        <div class="chart-area">
          <div class="chart-paper">
            <div class="chart-grid"></div>
            <div class="chart-content">
              <slot name="chart">
                <span class="placeholder">📉 Chart goes here</span>
              </slot>
            </div>
          </div>
        </div>
        
        <!-- Summary -->
        <div class="summary-area">
          <div class="summary-note">
            <div class="note-tape"></div>
            <div class="note-content">
              <slot name="summary">
                <span class="placeholder">📝 Summary notes...</span>
              </slot>
            </div>
          </div>
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<script setup lang="ts">
import SlideShell from './SlideShell.vue'

withDefaults(defineProps<{
  theme?: string
  vibe?: string
  header?: string
  footer?: string
}>(), {
  theme: 'handdrawn',
  vibe: 'cozy'
})
</script>

<style scoped>
.dashboard {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Title */
.dashboard-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-family: var(--hand-font-display);
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--hand-text-dark);
}

.title-icon {
  font-size: 1.3rem;
}

/* Metrics row */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.metric-card {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 2px solid;
  text-align: center;
  animation: metric-pop 0.3s ease-out backwards;
  animation-delay: calc(var(--metric-index) * 0.1s);
}

@keyframes metric-pop {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
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

.metric-card :deep(.metric-value) {
  font-family: var(--hand-font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--hand-text-dark);
}

.metric-card :deep(.metric-label) {
  font-family: var(--hand-font-body);
  font-size: 0.8rem;
  color: var(--hand-text);
}

/* Main content */
.dashboard-main {
  flex: 1;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1rem;
}

/* Chart area */
.chart-area {
  display: flex;
}

.chart-paper {
  flex: 1;
  background: var(--hand-bg-cream);
  border: 2px solid var(--hand-text-light);
  border-radius: 8px;
  position: relative;
  overflow: hidden;
}

.chart-grid {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(var(--hand-blue-light) 1px, transparent 1px),
    linear-gradient(90deg, var(--hand-blue-light) 1px, transparent 1px);
  background-size: 30px 30px;
  opacity: 0.5;
}

.chart-content {
  position: relative;
  z-index: 2;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

/* Summary area */
.summary-area {
  display: flex;
}

.summary-note {
  flex: 1;
  background: var(--hand-yellow);
  padding: 1rem;
  padding-top: 1.5rem;
  position: relative;
  box-shadow: 3px 3px 0 var(--hand-shadow-color);
  transform: rotate(1deg);
}

.note-tape {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%) rotate(-3deg);
  width: 60px;
  height: 20px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.note-content {
  font-family: var(--hand-font-handwriting);
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--hand-text-dark);
}

.note-content :deep(h4) {
  font-family: var(--hand-font-display);
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.note-content :deep(ul) {
  list-style: none;
  padding: 0;
}

.note-content :deep(li) {
  padding-left: 1.25rem;
  position: relative;
}

.note-content :deep(li::before) {
  content: '•';
  position: absolute;
  left: 0.25rem;
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: 0.9rem;
}

/* Vibe modifiers */
.vibe-minimal .metric-card {
  transform: none;
  background: var(--hand-bg-cream);
  border-width: 1px;
}

.vibe-minimal .summary-note {
  transform: none;
  box-shadow: none;
  background: var(--hand-bg-cream);
  border: 1px solid var(--hand-text-light);
}

.vibe-minimal .note-tape {
  display: none;
}

.vibe-playful .metric-card:hover {
  transform: scale(1.05) rotate(0deg);
}

.vibe-decorated .chart-paper::before {
  content: '📈';
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 1.2rem;
  z-index: 3;
}
</style>
