<!--
  MetricCard.vue - Business Metric Display Component
  
  Clean, professional metric/KPI card for business presentations.
  
  Props:
    - value: Main metric value
    - label: Metric label/title
    - icon: Icon emoji
    - trend: Trend direction (up, down, neutral)
    - trendValue: Trend percentage/value
    - variant: Card style (default, bordered, accent, minimal)
-->
<template>
  <div 
    class="metric-card"
    :class="[`variant-${variant}`]"
    :style="cardStyles"
  >
    <div class="card-header">
      <div v-if="icon" class="card-icon">{{ icon }}</div>
      <div v-if="trend !== 'neutral'" class="trend" :class="[`trend-${trend}`]">
        <span class="trend-arrow">{{ trend === 'up' ? '▲' : '▼' }}</span>
        <span v-if="trendValue" class="trend-value">{{ trendValue }}</span>
      </div>
    </div>
    
    <div class="card-value">
      <slot name="value">{{ value }}</slot>
    </div>
    
    <div class="card-label">
      <slot name="label">{{ label }}</slot>
    </div>
    
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  value?: string | number
  label?: string
  icon?: string
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: string
  variant?: 'default' | 'bordered' | 'accent' | 'minimal'
  color?: string
}>(), {
  trend: 'neutral',
  variant: 'default',
  color: 'var(--c-primary)'
})

const cardStyles = computed(() => ({
  '--card-accent': props.color
}))
</script>

<style scoped>
.metric-card {
  background: var(--c-bg-surface, #ffffff);
  border-radius: var(--radius-card, 8px);
  padding: 1.5rem;
  transition: all 0.2s ease;
  border: 1px solid var(--c-border, #e5e7eb);
}

.metric-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Variants */
.variant-bordered {
  border: 2px solid var(--c-primary, #0F4C81);
}

.variant-accent {
  border-left: 4px solid var(--card-accent, var(--c-primary, #0F4C81));
  background: linear-gradient(to right, 
    color-mix(in srgb, var(--c-primary, #0F4C81) 5%, transparent),
    transparent 30%);
}

.variant-minimal {
  background: transparent;
  border: none;
  padding: 1rem 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.card-icon {
  font-size: 1.75rem;
  opacity: 0.9;
}

.trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.trend-up {
  color: #16a34a;
  background: rgba(22, 163, 74, 0.1);
}

.trend-down {
  color: #dc2626;
  background: rgba(220, 38, 38, 0.1);
}

.trend-arrow {
  font-size: 0.7rem;
}

.card-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--c-text-primary, #1a1a1a);
  line-height: 1.1;
  margin-bottom: 0.5rem;
  font-family: var(--font-display, 'Inter', sans-serif);
}

.card-label {
  font-size: 0.9rem;
  color: var(--c-text-secondary, #6b7280);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 500;
}

.card-footer {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--c-border, #e5e7eb);
  font-size: 0.85rem;
  color: var(--c-text-secondary, #6b7280);
}
</style>
