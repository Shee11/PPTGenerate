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
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  height: 100%;
}

.metric-icon {
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--slidev-theme-primary, #3b82f6);
  border-radius: 0.5rem;
  color: white;
  flex-shrink: 0;
}

.metric-content {
  flex: 1;
}

.metric-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.6);
  margin-bottom: 0.5rem;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--slidev-theme-text, #1f2937);
  line-height: 1;
  margin-bottom: 0.5rem;
}

.metric-change {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.9rem;
  font-weight: 600;
}

.metric-change.positive {
  color: #10b981;
}

.metric-change.negative {
  color: #ef4444;
}

.change-icon {
  font-size: 1.1rem;
}

.change-label {
  margin-left: 0.25rem;
  font-weight: 400;
  color: rgba(0, 0, 0, 0.5);
}

.metric-subtitle {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: rgba(0, 0, 0, 0.5);
}

/* Variants */
.compact {
  padding: 1rem;
}

.compact .metric-value {
  font-size: 2rem;
}

.compact .metric-icon {
  width: 2.5rem;
  height: 2.5rem;
}

.large {
  padding: 2rem;
}

.large .metric-value {
  font-size: 3.5rem;
}

.large .metric-icon {
  width: 4rem;
  height: 4rem;
}

.card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.card:hover {
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
  transition: all 0.2s;
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
