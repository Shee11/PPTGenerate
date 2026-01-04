<!--
  dashboard.vue - Editorial Dashboard Layout
  
  Slots:
    - title: Dashboard title
    - metric1, metric2, metric3, metric4: Metric widgets
    - chart: Main chart area
    - summary: Summary section
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="dashboard">
      <!-- Title -->
      <div v-if="$slots.title" class="dashboard-title">
        <slot name="title" />
      </div>
      
      <!-- Metrics row -->
      <div class="metrics-row">
        <div 
          v-for="i in 4" 
          :key="i" 
          class="metric-card"
          :style="{ '--metric-index': i }"
        >
          <slot :name="`metric${i}`">
            <div class="metric-value">—</div>
            <div class="metric-label">Metric {{ i }}</div>
          </slot>
        </div>
      </div>
      
      <!-- Main content -->
      <div class="dashboard-main">
        <!-- Chart area -->
        <div class="chart-area">
          <slot name="chart">
            <div class="chart-placeholder">
              <span>Chart Area</span>
            </div>
          </slot>
        </div>
        
        <!-- Summary -->
        <div class="summary-area">
          <div class="summary-header">Summary</div>
          <div class="summary-divider"></div>
          <div class="summary-content">
            <slot name="summary">
              <span class="placeholder">Summary notes...</span>
            </slot>
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
  dark?: boolean
}>(), {
  theme: 'editorial',
  vibe: 'classic'
})
</script>

<style scoped>
.dashboard {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Title */
.dashboard-title {
  font-family: var(--edit-font-display);
  font-size: 1.6rem;
  font-weight: 400;
  color: var(--edit-text-dark);
}

/* Metrics row */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.metric-card {
  text-align: center;
  padding: 1rem;
  border: 1px solid var(--edit-light);
  animation: fade-in 0.4s ease-out backwards;
  animation-delay: calc(var(--metric-index) * 0.1s);
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.metric-card :deep(.metric-value),
.metric-value {
  font-family: var(--edit-font-display);
  font-size: 2rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  line-height: 1;
}

.metric-card :deep(.metric-label),
.metric-label {
  font-family: var(--edit-font-accent);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--edit-text-light);
  margin-top: 0.5rem;
}

.metric-card :deep(.metric-change) {
  font-family: var(--edit-font-body);
  font-size: 0.85rem;
  color: var(--edit-sage);
  margin-top: 0.25rem;
}

/* Main content */
.dashboard-main {
  flex: 1;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}

/* Chart area */
.chart-area {
  border: 1px solid var(--edit-light);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: var(--edit-text-light);
}

/* Summary area */
.summary-area {
  padding: 1.5rem;
  background: var(--edit-cream);
}

.summary-header {
  font-family: var(--edit-font-display);
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--edit-text-dark);
  margin-bottom: 0.75rem;
}

.summary-divider {
  width: 30px;
  height: 1px;
  background: var(--edit-gold);
  margin-bottom: 0.75rem;
}

.summary-content {
  font-family: var(--edit-font-body);
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--edit-text);
}

.placeholder {
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: var(--edit-text-light);
  font-size: 0.9rem;
}

/* Vibe: Modern */
.vibe-modern .metric-card {
  border-color: var(--edit-charcoal);
}

.vibe-modern .summary-area {
  background: var(--edit-white);
  border: 1px solid var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .metric-card {
  background: var(--edit-charcoal);
  border-color: var(--edit-slate);
}

.vibe-luxe .chart-area {
  background: var(--edit-charcoal);
  border-color: var(--edit-slate);
}

.vibe-luxe .summary-area {
  background: var(--edit-slate);
}
</style>
