<script setup lang="ts">
/**
 * Dashboard Layout - Business Project
 * 
 * Metrics dashboard with 4 metric cards and a chart area.
 * 
 * Slots:
 *   - title: Dashboard title
 *   - metric1, metric2, metric3, metric4: Metric cards
 *   - chart: Main chart/visualization area
 * 
 * Frontmatter:
 *   layout: dashboard
 *   header: "..."
 *   footer: "..."
 *   theme: business_professional
 *   vibe: balanced
 */
import { computed, inject } from 'vue'
import SlideShell from './SlideShell.vue'

const props = defineProps<{
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'decorative' | 'expressive'
}>()

const injectedVibe = inject('vibe', computed(() => props.vibe || 'balanced'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'balanced')
const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="dashboard" :class="vibeClass">
      <header v-if="$slots.title" class="dashboard-title">
        <slot name="title" />
      </header>
      
      <div class="dashboard-grid">
        <div v-if="$slots.metric1" class="metric-card metric-1">
          <slot name="metric1" />
        </div>
        <div v-if="$slots.metric2" class="metric-card metric-2">
          <slot name="metric2" />
        </div>
        <div v-if="$slots.metric3" class="metric-card metric-3">
          <slot name="metric3" />
        </div>
        <div v-if="$slots.metric4" class="metric-card metric-4">
          <slot name="metric4" />
        </div>
        <div v-if="$slots.chart" class="chart-area">
          <slot name="chart" />
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.dashboard {
  height: 100%;
  width: 100%;
  padding: 2rem;
  display: flex;
  flex-direction: column;
}

.dashboard-title {
  margin-bottom: 1.5rem;
  text-align: left;
  font-weight: 600;
  color: var(--theme-text);
}

.dashboard-title :deep(h1),
.dashboard-title :deep(h2),
.dashboard-title :deep(h3) {
  color: var(--theme-primary);
  margin: 0;
}

.dashboard-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: auto 1fr;
  gap: 1rem;
}

.metric-card {
  border-radius: var(--radius-md);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  background: var(--theme-bg-surface);
  border: 1px solid var(--theme-border);
  color: var(--theme-text);
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
}

/* Accent bar at top with different colors */
.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}

.metric-1::before { background: var(--theme-primary); }
.metric-2::before { background: var(--theme-accent); }
.metric-3::before { background: var(--theme-success); }
.metric-4::before { background: var(--theme-warning); }

.metric-card :deep(h3),
.metric-card :deep(h4) {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--theme-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0 0 0.5rem 0;
}

.metric-card :deep(p) {
  font-size: 2rem;
  font-weight: 700;
  color: var(--theme-text);
  margin: 0;
  line-height: 1.2;
}

.chart-area {
  grid-column: span 4;
  border-radius: var(--radius-md);
  padding: 1.5rem;
  background: var(--theme-bg-surface);
  border: 1px solid var(--theme-border);
  color: var(--theme-text);
  box-shadow: var(--shadow-sm);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1.5rem;
}

.vibe-minimal .dashboard-grid {
  gap: 0.75rem;
}

.vibe-minimal .metric-card {
  padding: 1rem;
  border-radius: var(--radius-sm);
  box-shadow: none;
}

.vibe-minimal .metric-card::before {
  height: 2px;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  padding: 1.75rem;
}

.vibe-clean .dashboard-grid {
  gap: 1rem;
}

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  padding: 2.5rem;
}

.vibe-decorative .dashboard-grid {
  gap: 1.25rem;
}

.vibe-decorative .metric-card {
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: none;
}

.vibe-decorative .metric-card::before {
  height: 4px;
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 3rem;
}

.vibe-expressive .dashboard-grid {
  gap: 1.5rem;
}

.vibe-expressive .metric-card {
  padding: 2rem;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    var(--theme-bg-elevated)
  );
}

.vibe-expressive .metric-card::before {
  height: 5px;
  background: linear-gradient(90deg, var(--theme-primary), var(--theme-accent));
}

.vibe-expressive .metric-card :deep(p) {
  font-size: 2.5rem;
}
</style>
