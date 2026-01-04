<template>
  <div class="metric-widget" :class="variant">
    <div class="metric-icon" v-if="icon">
      <span class="icon-emoji">{{ iconEmoji }}</span>
    </div>
    <div class="metric-content">
      <div class="metric-label">{{ label }}</div>
      <div class="metric-value">{{ value }}</div>
      <div v-if="change !== undefined" class="metric-change" :class="changeClass">
        <span class="change-icon">{{ change > 0 ? '📈' : '📉' }}</span>
        <span class="change-value">{{ Math.abs(change) }}%</span>
        <span v-if="changeLabel" class="change-label">{{ changeLabel }}</span>
      </div>
      <div v-if="subtitle" class="metric-subtitle">{{ subtitle }}</div>
    </div>
    <div class="metric-decoration">
      <span class="decoration-star" v-for="i in stars" :key="i">⭐</span>
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
  icon: String, // trend-up, trend-down, users, dollar, chart, streak, xp, gem
  variant: {
    type: String,
    default: 'default', // default, compact, large, card
  },
  accentColor: {
    type: String,
    default: 'green', // green, blue, orange, purple
  },
})

const changeClass = computed(() => {
  if (props.change === undefined) return ''
  return props.change > 0 ? 'positive' : 'negative'
})

const iconEmoji = computed(() => {
  const icons = {
    'trend-up': '📈',
    'trend-down': '📉',
    'users': '👥',
    'dollar': '💰',
    'chart': '📊',
    'streak': '🔥',
    'xp': '⚡',
    'gem': '💎',
    'crown': '👑',
    'heart': '❤️',
    'target': '🎯',
  }
  return icons[props.icon] || '📊'
})

const stars = computed(() => {
  // Show stars based on value (if numeric)
  const numValue = parseFloat(props.value)
  if (isNaN(numValue)) return 0
  if (numValue >= 1000) return 3
  if (numValue >= 100) return 2
  if (numValue >= 10) return 1
  return 0
})
</script>

<style scoped>
.metric-widget {
  padding: 1.5rem;
  background: white;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  height: 100%;
  box-shadow: 
    0 4px 0 var(--duo-green-dark, #46a302),
    0 8px 20px rgba(88, 204, 2, 0.15);
  border: 3px solid var(--duo-green, #58CC02);
  position: relative;
  overflow: hidden;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.metric-widget:hover {
  transform: translateY(-2px);
}

/* Accent color variants */
.metric-widget[data-accent="blue"] {
  border-color: var(--duo-blue, #1CB0F6);
  box-shadow: 
    0 4px 0 var(--duo-blue-dark, #1899D6),
    0 8px 20px rgba(28, 176, 246, 0.15);
}

.metric-widget[data-accent="orange"] {
  border-color: var(--duo-orange, #FF9600);
  box-shadow: 
    0 4px 0 #E68600,
    0 8px 20px rgba(255, 150, 0, 0.15);
}

.metric-widget[data-accent="purple"] {
  border-color: var(--duo-purple, #CE82FF);
  box-shadow: 
    0 4px 0 #B86EE6,
    0 8px 20px rgba(206, 130, 255, 0.15);
}

.metric-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: var(--duo-gray-light, #F7F7F7);
  border-radius: 12px;
  flex-shrink: 0;
}

.icon-emoji {
  font-size: 2rem;
}

.metric-content {
  flex: 1;
  min-width: 0;
}

.metric-label {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--duo-gray-dark, #777);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.metric-value {
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
  font-size: 2.25rem;
  font-weight: 800;
  color: var(--duo-text, #4B4B4B);
  line-height: 1.1;
}

.metric-change {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  margin-top: 0.5rem;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 0.8rem;
  font-weight: 700;
}

.metric-change.positive {
  background: rgba(88, 204, 2, 0.15);
  color: var(--duo-green-dark, #46a302);
}

.metric-change.negative {
  background: rgba(255, 75, 75, 0.15);
  color: var(--duo-red, #FF4B4B);
}

.change-icon {
  font-size: 0.9rem;
}

.change-value {
  font-weight: 800;
}

.change-label {
  opacity: 0.8;
  font-weight: 600;
}

.metric-subtitle {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 0.8rem;
  color: var(--duo-gray, #AFAFAF);
  margin-top: 0.35rem;
  font-weight: 600;
}

.metric-decoration {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  display: flex;
  gap: 0.15rem;
}

.decoration-star {
  font-size: 1rem;
  opacity: 0.6;
  animation: star-twinkle 2s ease-in-out infinite;
}

.decoration-star:nth-child(2) { animation-delay: 0.3s; }
.decoration-star:nth-child(3) { animation-delay: 0.6s; }

@keyframes star-twinkle {
  0%, 100% { transform: scale(1); opacity: 0.6; }
  50% { transform: scale(1.2); opacity: 1; }
}

/* Variant: compact */
.metric-widget.compact {
  padding: 1rem;
  gap: 1rem;
}

.metric-widget.compact .metric-icon {
  width: 44px;
  height: 44px;
}

.metric-widget.compact .icon-emoji {
  font-size: 1.5rem;
}

.metric-widget.compact .metric-value {
  font-size: 1.5rem;
}

.metric-widget.compact .metric-decoration {
  display: none;
}

/* Variant: large */
.metric-widget.large {
  padding: 2rem;
  flex-direction: column;
  text-align: center;
}

.metric-widget.large .metric-icon {
  width: 72px;
  height: 72px;
}

.metric-widget.large .icon-emoji {
  font-size: 2.5rem;
}

.metric-widget.large .metric-value {
  font-size: 3rem;
}

/* Variant: card */
.metric-widget.card {
  flex-direction: column;
  text-align: center;
  padding: 2rem;
  border-width: 4px;
}

.metric-widget.card .metric-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--duo-green, #58CC02) 0%, var(--duo-blue, #1CB0F6) 100%);
}

.metric-widget.card .icon-emoji {
  font-size: 2.5rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}

.metric-widget.card .metric-value {
  font-size: 2.5rem;
  background: linear-gradient(135deg, var(--duo-green, #58CC02) 0%, var(--duo-blue, #1CB0F6) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
