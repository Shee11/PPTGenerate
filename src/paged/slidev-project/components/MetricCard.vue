<!--
  MetricCard.vue - Styled Metric Display Component
  
  Beautiful metric/KPI card with icon, value, and trend.
  Perfect for dashboards, stats displays, or highlights.
  
  Props:
    - value: Main metric value
    - label: Metric label/title
    - icon: Icon emoji
    - trend: Trend direction (up, down, neutral)
    - trendValue: Trend percentage/value
    - variant: Card style (default, minimal, accent, gradient)
    - color: Accent color
-->
<template>
  <div 
    class="metric-card"
    :class="[`variant-${variant}`]"
    :style="cardStyles"
  >
    <div class="card-glow"></div>
    
    <div class="card-header">
      <div v-if="icon" class="card-icon">{{ icon }}</div>
      <div v-if="trend !== 'neutral'" class="trend" :class="[`trend-${trend}`]">
        <span class="trend-arrow">{{ trend === 'up' ? '↑' : '↓' }}</span>
        <span v-if="trendValue" class="trend-value">{{ trendValue }}</span>
      </div>
    </div>
    
    <div class="card-value">
      <slot name="value">{{ value }}</slot>
    </div>
    
    <div class="card-label">
      <slot name="label">{{ label }}</slot>
    </div>
    
    <div class="card-footer">
      <slot name="footer" />
    </div>
    
    <div class="card-accent-line"></div>
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
  variant?: 'default' | 'minimal' | 'accent' | 'gradient'
  color?: string
}>(), {
  trend: 'neutral',
  variant: 'default',
  color: 'var(--c-primary)'
})

const cardStyles = computed(() => ({
  '--card-color': props.color
}))
</script>

<style scoped>
.metric-card {
  position: relative;
  background: var(--c-bg-surface);
  border-radius: 0.75rem;
  padding: 1.25rem;
  transition: all 0.3s ease;
  overflow: hidden;
}

.metric-card:hover {
  transform: translateY(-2px);
}

/* Glow effect */
.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 60%;
  background: linear-gradient(to bottom, var(--card-color), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.metric-card:hover .card-glow {
  opacity: 0.05;
}

/* Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.card-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
}

.trend-up {
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.trend-down {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.trend-arrow {
  font-weight: 700;
}

/* Value */
.card-value {
  font-size: 2rem;
  font-weight: 800;
  color: var(--c-text-main);
  line-height: 1;
  margin-bottom: 0.5rem;
  font-family: var(--font-family);
}

/* Label */
.card-label {
  font-size: 0.875rem;
  color: var(--c-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Footer */
.card-footer {
  margin-top: 0.75rem;
}

.card-footer:empty {
  display: none;
}

.card-footer :deep(p) {
  font-size: 0.75rem;
  color: var(--c-text-muted);
  margin: 0;
}

/* Accent line */
.card-accent-line {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(to right, var(--card-color), transparent);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.metric-card:hover .card-accent-line {
  transform: scaleX(1);
}

/* Variants */
.variant-minimal {
  background: transparent;
  padding: 1rem;
}

.variant-minimal .card-glow {
  display: none;
}

.variant-minimal .card-accent-line {
  display: none;
}

.variant-accent {
  border-left: 4px solid var(--card-color);
  border-radius: 0 0.75rem 0.75rem 0;
}

.variant-accent .card-accent-line {
  display: none;
}

.variant-gradient {
  background: linear-gradient(135deg, var(--c-bg-surface), rgba(255,255,255,0.02));
}

.variant-gradient .card-value {
  background: linear-gradient(135deg, var(--card-color), var(--c-accent, var(--card-color)));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
