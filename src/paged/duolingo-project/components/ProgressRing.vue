<!--
  ProgressRing.vue - Duolingo Styled Circular Progress Ring
  
  Playful circular progress indicator with Duolingo styling.
  Perfect for showing XP, completion, streaks, or percentages.
  
  Props:
    - value: Progress value (0-100)
    - size: Ring diameter in px
    - strokeWidth: Ring thickness
    - color: Color theme (green, blue, orange, purple)
    - label: Center label text
    - showValue: Show percentage in center
    - animated: Animate on mount
    - icon: Center icon emoji
-->
<template>
  <div class="progress-ring" :class="`color-${color}`" :style="ringStyles">
    <svg :width="size" :height="size" viewBox="0 0 100 100">
      <!-- Background circle -->
      <circle
        class="ring-background"
        cx="50"
        cy="50"
        :r="radius"
        fill="none"
        :stroke-width="strokeWidth"
      />
      <!-- Progress circle -->
      <circle
        class="ring-progress"
        cx="50"
        cy="50"
        :r="radius"
        fill="none"
        :stroke-width="strokeWidth"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="dashOffset"
        stroke-linecap="round"
        transform="rotate(-90 50 50)"
      />
    </svg>
    <!-- Center content -->
    <div class="ring-center">
      <span v-if="icon" class="ring-icon">{{ icon }}</span>
      <span v-if="showValue && !icon" class="ring-value">{{ Math.round(animatedValue) }}%</span>
      <span v-if="label" class="ring-label">{{ label }}</span>
    </div>
    <!-- Celebration particles -->
    <div v-if="animatedValue >= 100" class="celebration">
      <span v-for="i in 6" :key="i" class="particle" :style="{ '--particle-index': i }">✨</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, watch } from 'vue'

const props = withDefaults(defineProps<{
  value: number
  size?: number
  strokeWidth?: number
  color?: 'green' | 'blue' | 'orange' | 'purple'
  label?: string
  showValue?: boolean
  animated?: boolean
  icon?: string
}>(), {
  size: 120,
  strokeWidth: 10,
  color: 'green',
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
  '--ring-size': `${props.size}px`
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
    
    // Easing function (ease-out-bounce feel)
    const eased = 1 - Math.pow(1 - progress, 3)
    
    animatedValue.value = startValue + (endValue - startValue) * eased
    
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
  font-family: var(--duo-font, 'Nunito', sans-serif);
}

.progress-ring svg {
  transform: rotate(0);
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
}

/* Background ring */
.ring-background {
  stroke: var(--duo-gray-light, #E5E5E5);
}

/* Progress ring */
.ring-progress {
  transition: stroke-dashoffset 0.3s ease;
}

/* Color variants */
.color-green .ring-progress {
  stroke: var(--duo-green, #58CC02);
  filter: drop-shadow(0 0 8px rgba(88, 204, 2, 0.4));
}

.color-blue .ring-progress {
  stroke: var(--duo-blue, #1CB0F6);
  filter: drop-shadow(0 0 8px rgba(28, 176, 246, 0.4));
}

.color-orange .ring-progress {
  stroke: var(--duo-orange, #FF9600);
  filter: drop-shadow(0 0 8px rgba(255, 150, 0, 0.4));
}

.color-purple .ring-progress {
  stroke: var(--duo-purple, #CE82FF);
  filter: drop-shadow(0 0 8px rgba(206, 130, 255, 0.4));
}

/* Center content */
.ring-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.15rem;
}

.ring-icon {
  font-size: 2rem;
  line-height: 1;
  animation: icon-bounce 2s ease-in-out infinite;
}

@keyframes icon-bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.ring-value {
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
  font-size: calc(var(--ring-size) * 0.2);
  font-weight: 800;
  color: var(--duo-text, #4B4B4B);
  line-height: 1;
}

.ring-label {
  font-size: calc(var(--ring-size) * 0.1);
  font-weight: 700;
  color: var(--duo-gray-dark, #777);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Celebration particles */
.celebration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  top: 50%;
  left: 50%;
  font-size: 1rem;
  animation: particle-burst 1s ease-out forwards;
  animation-delay: calc(var(--particle-index) * 0.1s);
}

@keyframes particle-burst {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 1;
  }
  100% {
    transform: translate(
      calc(-50% + cos(var(--particle-index) * 60deg) * 60px),
      calc(-50% + sin(var(--particle-index) * 60deg) * 60px)
    ) scale(1);
    opacity: 0;
  }
}

.particle:nth-child(1) { --angle: 0deg; }
.particle:nth-child(2) { --angle: 60deg; }
.particle:nth-child(3) { --angle: 120deg; }
.particle:nth-child(4) { --angle: 180deg; }
.particle:nth-child(5) { --angle: 240deg; }
.particle:nth-child(6) { --angle: 300deg; }

/* Color-specific value colors */
.color-green .ring-value {
  color: var(--duo-green-dark, #46a302);
}

.color-blue .ring-value {
  color: var(--duo-blue-dark, #1899D6);
}

.color-orange .ring-value {
  color: #E68600;
}

.color-purple .ring-value {
  color: #B86EE6;
}
</style>
