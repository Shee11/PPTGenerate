<!--
  ProgressRing.vue - Circular Progress Ring Component
  
  Beautiful circular progress indicator with customizable appearance.
  Perfect for showing completion, scores, or percentages.
  
  Props:
    - value: Progress value (0-100)
    - size: Ring diameter in px
    - strokeWidth: Ring thickness
    - color: Progress color
    - backgroundColor: Track color
    - label: Center label text
    - showValue: Show percentage in center
    - animated: Animate on mount
-->
<template>
  <div class="progress-ring" :style="ringStyles">
    <svg :width="size" :height="size" viewBox="0 0 100 100">
      <!-- Background circle -->
      <circle
        class="ring-background"
        cx="50"
        cy="50"
        :r="radius"
        fill="none"
        :stroke="backgroundColor"
        :stroke-width="strokeWidth"
      />
      <!-- Progress circle -->
      <circle
        class="ring-progress"
        cx="50"
        cy="50"
        :r="radius"
        fill="none"
        :stroke="color"
        :stroke-width="strokeWidth"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="dashOffset"
        stroke-linecap="round"
        transform="rotate(-90 50 50)"
      />
    </svg>
    <!-- Center content -->
    <div class="ring-center">
      <span v-if="showValue" class="ring-value">{{ Math.round(animatedValue) }}%</span>
      <span v-if="label" class="ring-label">{{ label }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, watch } from 'vue'

const props = withDefaults(defineProps<{
  value: number
  size?: number
  strokeWidth?: number
  color?: string
  backgroundColor?: string
  label?: string
  showValue?: boolean
  animated?: boolean
}>(), {
  size: 120,
  strokeWidth: 8,
  color: 'var(--c-primary)',
  backgroundColor: 'rgba(255, 255, 255, 0.1)',
  showValue: true,
  animated: true
})

const animatedValue = ref(0)

const radius = computed(() => 50 - props.strokeWidth / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)

const dashOffset = computed(() => {
  const progress = Math.min(Math.max(animatedValue.value, 0), 100)
  return circumference.value * (1 - progress / 100)
})

const ringStyles = computed(() => ({
  '--ring-size': `${props.size}px`,
  '--ring-color': props.color
}))

const animateProgress = () => {
  if (!props.animated) {
    animatedValue.value = props.value
    return
  }
  
  const duration = 1500
  const startTime = performance.now()
  const startValue = animatedValue.value
  const endValue = props.value
  
  const animate = (currentTime: number) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)
    const easeOut = 1 - Math.pow(1 - progress, 3)
    
    animatedValue.value = startValue + (endValue - startValue) * easeOut
    
    if (progress < 1) {
      requestAnimationFrame(animate)
    }
  }
  
  requestAnimationFrame(animate)
}

onMounted(() => {
  animateProgress()
})

watch(() => props.value, () => {
  animateProgress()
})
</script>

<style scoped>
.progress-ring {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: var(--ring-size);
  height: var(--ring-size);
}

.progress-ring svg {
  position: absolute;
  top: 0;
  left: 0;
}

.ring-background {
  opacity: 0.3;
}

.ring-progress {
  transition: stroke-dashoffset 0.3s ease;
  filter: drop-shadow(0 0 6px var(--ring-color));
}

.ring-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  z-index: 1;
}

.ring-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--c-text-main);
  line-height: 1;
}

.ring-label {
  font-size: 0.75rem;
  color: var(--c-text-muted);
  margin-top: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
</style>
