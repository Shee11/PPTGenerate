<script setup lang="ts">
/**
 * Dashboard Layout
 * 
 * Metrics dashboard with 4 metric cards and a chart area.
 * Inherits from SlideShell for consistent header/footer/theme/vibe.
 * 
 * Frontmatter:
 *   layout: dashboard
 *   header: "..."    # Optional header text
 *   footer: "..."    # Optional footer text
 *   theme: dark-professional
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

// Get vibe from SlideShell injection or props
const injectedVibe = inject('vibe', computed(() => props.vibe || 'balanced'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'balanced')

// Vibe class
const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="dashboard" :class="vibeClass">
      <header v-if="$slots.title" class="dashboard-title">
        <slot name="title" />
      </header>
      
      <div class="dashboard-grid">
        <div v-if="$slots.metric1" class="metric-card large">
          <slot name="metric1" />
        </div>
        <div v-if="$slots.metric2" class="metric-card large">
          <slot name="metric2" />
        </div>
        <div v-if="$slots.metric3" class="metric-card small">
          <slot name="metric3" />
        </div>
        <div v-if="$slots.metric4" class="metric-card small">
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
  text-align: center;
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
  grid-template-rows: auto auto 1fr;
  gap: 1rem;
}

.metric-card {
  border-radius: var(--radius-md);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: var(--theme-bg-surface);
  border: 1px solid var(--theme-border-subtle);
  color: var(--theme-text);
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
}

/* Accent bar at top */
.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--theme-primary);
}

.metric-card:nth-child(2)::before {
  background: var(--theme-accent);
}

.metric-card:nth-child(3)::before {
  background: var(--theme-success);
}

.metric-card:nth-child(4)::before {
  background: var(--theme-warning);
}

.metric-card.large {
  grid-column: span 2;
}

.metric-card.small {
  grid-column: span 1;
}

.chart-area {
  grid-column: span 4;
  border-radius: var(--radius-md);
  padding: 1.5rem;
  background: var(--theme-bg-surface);
  border: 1px solid var(--theme-border-subtle);
  color: var(--theme-text);
  box-shadow: var(--shadow-sm);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
}

.vibe-minimal .dashboard-grid {
  gap: 0.5rem;
}

.vibe-minimal .metric-card {
  padding: 0.75rem;
  border-radius: var(--radius-sm);
  background: transparent;
  border: 1px solid var(--theme-border);
  box-shadow: none;
}

.vibe-minimal .metric-card::before {
  height: 2px;
}

.vibe-minimal .chart-area {
  padding: 1rem;
  border-radius: var(--radius-sm);
  background: transparent;
  border: 1px solid var(--theme-border);
  box-shadow: none;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  padding: 1.5rem;
}

.vibe-clean .dashboard-grid {
  gap: 0.75rem;
}

.vibe-clean .metric-card {
  padding: 1rem;
  border-radius: var(--radius-sm);
}

.vibe-clean .chart-area {
  padding: 1.25rem;
  border-radius: var(--radius-sm);
}

/* === VIBE: BALANCED (default) === */
/* Base styles above */

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  padding: 2.5rem;
}

.vibe-decorative .dashboard-grid {
  gap: 1.5rem;
}

.vibe-decorative .metric-card {
  padding: 1.75rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-bg-elevated) 50%, var(--theme-bg-surface))
  );
  border: none;
}

.vibe-decorative .metric-card::before {
  height: 4px;
  box-shadow: 0 2px 8px color-mix(in srgb, var(--theme-primary) 50%, transparent);
}

/* Corner decoration */
.vibe-decorative .metric-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 40px;
  height: 40px;
  background: radial-gradient(
    circle at bottom right,
    color-mix(in srgb, var(--theme-primary) 10%, transparent) 0%,
    transparent 70%
  );
}

.vibe-decorative .chart-area {
  padding: 2rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-bg-elevated) 50%, var(--theme-bg-surface))
  );
  border: none;
}

.vibe-decorative .chart-area::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--theme-success), var(--theme-primary));
  box-shadow: 0 2px 8px color-mix(in srgb, var(--theme-success) 50%, transparent);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 3rem;
}

.vibe-expressive .dashboard-grid {
  gap: 2rem;
}

.vibe-expressive .metric-card {
  padding: 2rem;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg), var(--shadow-glow);
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-bg-elevated) 70%, var(--theme-primary))
  );
  border: none;
  backdrop-filter: blur(10px);
}

.vibe-expressive .metric-card::before {
  height: 6px;
  background: linear-gradient(90deg, var(--theme-primary), var(--theme-accent));
  box-shadow: 0 2px 12px color-mix(in srgb, var(--theme-primary) 60%, transparent);
}

.vibe-expressive .metric-card::after {
  content: '';
  position: absolute;
  bottom: -10%;
  right: -10%;
  width: 80px;
  height: 80px;
  background: radial-gradient(
    circle,
    color-mix(in srgb, var(--theme-primary) 15%, transparent) 0%,
    transparent 70%
  );
  border-radius: 50%;
}

.vibe-expressive .chart-area {
  padding: 2.5rem;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg), var(--shadow-glow);
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-bg-elevated) 70%, var(--theme-success))
  );
  border: none;
  backdrop-filter: blur(10px);
  position: relative;
}

.vibe-expressive .chart-area::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, var(--theme-success), var(--theme-primary), var(--theme-accent));
  box-shadow: 0 2px 12px color-mix(in srgb, var(--theme-success) 60%, transparent);
  border-radius: var(--radius-xl) var(--radius-xl) 0 0;
}
</style>
