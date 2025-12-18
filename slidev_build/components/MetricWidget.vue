<template>
  <div class="metric-widget" :class="variant">
    <div class="metric-icon" v-if="icon">
      <component :is="iconComponent" />
    </div>
    <div class="metric-content">
      <div class="metric-label">{{ label }}</div>
      <div class="metric-value">{{ value }}</div>
      <div v-if="change !== undefined" class="metric-change" :class="changeClass">
        <span class="change-icon">{{ change > 0 ? '↑' : '↓' }}</span>
        <span class="change-value">{{ Math.abs(change) }}%</span>
        <span v-if="changeLabel" class="change-label">{{ changeLabel }}</span>
      </div>
      <div v-if="subtitle" class="metric-subtitle">{{ subtitle }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    required: true,
  },
  change: Number, // Percentage change (positive or negative)
  changeLabel: String, // e.g., "vs last month"
  subtitle: String,
  icon: String, // trend-up, trend-down, users, dollar, chart
  variant: {
    type: String,
    default: 'default', // default, compact, large, card
  },
})

const changeClass = computed(() => {
  if (props.change === undefined) return ''
  return props.change > 0 ? 'positive' : 'negative'
})

const iconComponent = computed(() => {
  const icons = {
    'trend-up': TrendUpIcon,
    'trend-down': TrendDownIcon,
    'users': UsersIcon,
    'dollar': DollarIcon,
    'chart': ChartIcon,
  }
  return icons[props.icon] || null
})
</script>

<style scoped>
.metric-widget {
  padding: 2rem;
  background: linear-gradient(145deg,
    color-mix(in srgb, var(--c-bg-base) 98%, white) 0%,
    color-mix(in srgb, var(--c-bg-base) 95%, white) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  height: 100%;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.06),
    0 1px 3px rgba(0, 0, 0, 0.08);
  border: 1px solid color-mix(in srgb, white 10%, transparent);
  position: relative;
  overflow: hidden;
}

/* Corner accent */
.metric-widget::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 60px;
  height: 60px;
  background: radial-gradient(circle at top right,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 8%, transparent) 0%,
    transparent 70%);
  pointer-events: none;
}

.metric-icon {
  width: 3.5rem;
  height: 3.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg,
    var(--slidev-theme-primary, #3b82f6) 0%,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 80%, #8b5cf6) 100%);
  border-radius: 12px;
  color: white;
  flex-shrink: 0;
  box-shadow: 
    0 4px 12px rgba(59, 130, 246, 0.3),
    inset 0 -2px 4px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  position: relative;
}

/* Glow around icon */
.metric-icon::after {
  content: '';
  position: absolute;
  inset: -6px;
  border-radius: 16px;
  background: radial-gradient(circle,
    rgba(59, 130, 246, 0.2) 0%,
    transparent 70%);
  z-index: -1;
}

.metric-content {
  flex: 1;
  position: relative;
}

.metric-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.6);
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg,
    var(--slidev-theme-text, #1f2937) 0%,
    color-mix(in srgb, var(--slidev-theme-text, #1f2937) 80%, var(--slidev-theme-primary, #3b82f6)) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 0.75rem;
}

.metric-change {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.95rem;
  font-weight: 600;
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  width: fit-content;
}

.metric-change.positive {
  color: #10b981;
  background: linear-gradient(135deg,
    rgba(16, 185, 129, 0.1) 0%,
    rgba(16, 185, 129, 0.05) 100%);
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.15);
}

.metric-change.negative {
  color: #ef4444;
  background: linear-gradient(135deg,
    rgba(239, 68, 68, 0.1) 0%,
    rgba(239, 68, 68, 0.05) 100%);
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.15);
}

.change-icon {
  font-size: 1.2rem;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.change-label {
  margin-left: 0.35rem;
  font-weight: 400;
  color: rgba(0, 0, 0, 0.5);
}

.metric-subtitle {
  margin-top: 0.75rem;
  font-size: 0.85rem;
  color: rgba(0, 0, 0, 0.5);
}

/* Variants */
.compact {
  padding: 1.25rem;
}

.compact .metric-value {
  font-size: 2rem;
}

.compact .metric-icon {
  width: 3rem;
  height: 3rem;
}

.large {
  padding: 2.5rem;
}

.large .metric-value {
  font-size: 3.5rem;
}

.large .metric-icon {
  width: 4.5rem;
  height: 4.5rem;
}

.card {
  background: linear-gradient(145deg,
    white 0%,
    color-mix(in srgb, white 98%, var(--slidev-theme-primary, #3b82f6)) 100%);
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.08),
    0 8px 24px rgba(0, 0, 0, 0.05);
}
</style>

<!-- Icon Components (inline for simplicity) -->
<template id="trend-up-icon">
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
  </svg>
</template>

<script>
const TrendUpIcon = {
  template: '#trend-up-icon'
}

const TrendDownIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
  </svg>`
}

const UsersIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
  </svg>`
}

const DollarIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>`
}

const ChartIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
  </svg>`
}
</script>
