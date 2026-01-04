<script setup lang="ts">
/**
 * Dashboard Layout - Duolingo Style
 * 
 * Metrics dashboard with 4 metric cards and a chart area.
 * Features Duolingo's gamified stat display style.
 * 
 * Slots: title, metric1, metric2, metric3, metric4, chart (EXACTLY same as slidev-project)
 */
import { computed, inject } from 'vue'
import SlideShell from './SlideShell.vue'

const props = defineProps<{
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'playful' | 'expressive'
}>()

const injectedVibe = inject('vibe', computed(() => props.vibe || 'playful'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'playful')
const vibeClass = computed(() => `vibe-${currentVibe.value}`)

// Duolingo stat colors
const metricColors = ['#58CC02', '#1CB0F6', '#FF9600', '#CE82FF']
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="dashboard" :class="vibeClass">
      <header v-if="$slots.title" class="dashboard-title">
        <slot name="title" />
      </header>
      
      <div class="dashboard-grid">
        <div v-if="$slots.metric1" class="metric-card" :style="{ '--metric-color': metricColors[0] }">
          <div class="metric-icon">🎯</div>
          <slot name="metric1" />
        </div>
        <div v-if="$slots.metric2" class="metric-card" :style="{ '--metric-color': metricColors[1] }">
          <div class="metric-icon">⚡</div>
          <slot name="metric2" />
        </div>
        <div v-if="$slots.metric3" class="metric-card" :style="{ '--metric-color': metricColors[2] }">
          <div class="metric-icon">🔥</div>
          <slot name="metric3" />
        </div>
        <div v-if="$slots.metric4" class="metric-card" :style="{ '--metric-color': metricColors[3] }">
          <div class="metric-icon">💎</div>
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
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.dashboard-title {
  text-align: center;
  font-weight: 800;
  color: var(--theme-text);
}

.dashboard-title :deep(h1),
.dashboard-title :deep(h2),
.dashboard-title :deep(h3) {
  color: var(--theme-text);
  margin: 0;
  font-weight: 800;
}

.dashboard-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: auto 1fr;
  gap: 1rem;
}

.metric-card {
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  background: var(--theme-bg-card);
  border: 2px solid var(--theme-border);
  box-shadow: var(--shadow-card);
  color: var(--theme-text);
  position: relative;
  overflow: hidden;
}

/* Colored top accent */
.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--metric-color, var(--theme-primary));
}

.metric-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.metric-card :deep(h1),
.metric-card :deep(h2),
.metric-card :deep(h3),
.metric-card :deep(.big-num) {
  color: var(--metric-color, var(--theme-primary));
  font-weight: 800;
  font-size: 2.5rem;
  margin: 0;
  line-height: 1;
}

.metric-card :deep(p),
.metric-card :deep(.label) {
  color: var(--theme-text-muted);
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0.5rem 0 0 0;
}

.chart-area {
  grid-column: 1 / -1;
  background: var(--theme-bg-card);
  border: 2px solid var(--theme-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
  gap: 0.75rem;
}

.vibe-minimal .dashboard-grid {
  gap: 0.75rem;
}

.vibe-minimal .metric-card {
  border-radius: var(--radius-sm);
  border-width: 1px;
  padding: 1rem;
  box-shadow: none;
}

.vibe-minimal .metric-card::before {
  height: 2px;
}

.vibe-minimal .metric-icon {
  font-size: 1rem;
}

.vibe-minimal .metric-card :deep(h1),
.vibe-minimal .metric-card :deep(h2),
.vibe-minimal .metric-card :deep(h3),
.vibe-minimal .metric-card :deep(.big-num) {
  font-size: 1.75rem;
}

.vibe-minimal .chart-area {
  border-radius: var(--radius-sm);
  border-width: 1px;
  box-shadow: none;
  padding: 1rem;
}

/* === VIBE: CLEAN === */
.vibe-clean .metric-card {
  border-width: 1px;
  box-shadow: 0 1px 0 var(--theme-border);
}

.vibe-clean .metric-card::before {
  height: 3px;
}

.vibe-clean .chart-area {
  border-width: 1px;
  box-shadow: 0 1px 0 var(--theme-border);
}

/* === VIBE: PLAYFUL === */
.vibe-playful .metric-card {
  border-radius: var(--radius-xl);
  border-width: 3px;
  border-color: var(--metric-color, var(--theme-primary));
  box-shadow: 0 4px 0 color-mix(in srgb, var(--metric-color, var(--theme-primary)) 40%, transparent);
}

.vibe-playful .metric-card::before {
  height: 0;
  display: none;
}

.vibe-playful .metric-card {
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--metric-color) 10%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.vibe-playful .metric-icon {
  font-size: 2rem;
  margin-bottom: 0.75rem;
}

.vibe-playful .metric-card :deep(h1),
.vibe-playful .metric-card :deep(h2),
.vibe-playful .metric-card :deep(h3),
.vibe-playful .metric-card :deep(.big-num) {
  font-size: 3rem;
}

.vibe-playful .chart-area {
  border-radius: var(--radius-xl);
  border-width: 3px;
  border-color: var(--theme-primary);
  box-shadow: 0 4px 0 color-mix(in srgb, var(--theme-primary) 30%, transparent);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 2rem;
  gap: 1.5rem;
}

.vibe-expressive .dashboard-grid {
  gap: 1.5rem;
}

.vibe-expressive .metric-card {
  border-radius: var(--radius-xl);
  border-width: 4px;
  border-color: var(--metric-color, var(--theme-primary));
  box-shadow: 0 6px 0 color-mix(in srgb, var(--metric-color, var(--theme-primary)) 50%, transparent);
  padding: 1.75rem;
}

.vibe-expressive .metric-card::before {
  display: none;
}

.vibe-expressive .metric-card {
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--metric-color) 15%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.vibe-expressive .metric-icon {
  font-size: 2.5rem;
}

.vibe-expressive .metric-card :deep(h1),
.vibe-expressive .metric-card :deep(h2),
.vibe-expressive .metric-card :deep(h3),
.vibe-expressive .metric-card :deep(.big-num) {
  font-size: 3.5rem;
}

.vibe-expressive .chart-area {
  border-radius: var(--radius-xl);
  border-width: 4px;
  border-color: var(--theme-accent);
  box-shadow: 0 6px 0 color-mix(in srgb, var(--theme-accent) 40%, transparent);
}
</style>
