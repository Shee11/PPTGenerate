<!--
  ProgressRing.vue - Handdrawn Progress Ring Component
  
  Props:
    - value: Progress value (0-100)
    - label: Center label
    - color: Color variant
-->
<template>
  <div class="progress-ring" :class="`ring-${color}`">
    <svg class="ring-svg" viewBox="0 0 100 100">
      <!-- Background circle -->
      <circle
        class="ring-bg"
        cx="50"
        cy="50"
        r="40"
        fill="none"
        stroke-width="8"
      />
      <!-- Progress circle with sketchy effect -->
      <circle
        class="ring-progress"
        cx="50"
        cy="50"
        r="40"
        fill="none"
        stroke-width="8"
        stroke-linecap="round"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="offset"
      />
      <!-- Decorative dots -->
      <circle v-for="i in 8" :key="i" 
        :cx="50 + 40 * Math.cos((i * 45 - 90) * Math.PI / 180)"
        :cy="50 + 40 * Math.sin((i * 45 - 90) * Math.PI / 180)"
        r="2"
        class="ring-dot"
      />
    </svg>
    
    <!-- Center content -->
    <div class="ring-center">
      <div class="ring-value">{{ value }}%</div>
      <div v-if="label" class="ring-label">{{ label }}</div>
    </div>
    
    <!-- Doodle -->
    <div class="ring-deco">✨</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  value?: number
  label?: string
  color?: 'pink' | 'blue' | 'green' | 'yellow'
}>(), {
  value: 75,
  color: 'pink'
})

const circumference = computed(() => 2 * Math.PI * 40)
const offset = computed(() => circumference.value - (props.value / 100) * circumference.value)
</script>

<style scoped>
.progress-ring {
  position: relative;
  width: 120px;
  height: 120px;
}

.ring-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.ring-bg {
  stroke: var(--hand-bg-cream);
}

.ring-progress {
  transition: stroke-dashoffset 0.5s ease-out;
}

.ring-pink .ring-progress { stroke: var(--hand-pink); }
.ring-blue .ring-progress { stroke: var(--hand-blue); }
.ring-green .ring-progress { stroke: var(--hand-green); }
.ring-yellow .ring-progress { stroke: var(--hand-yellow-dark); }

.ring-dot {
  fill: var(--hand-text-light);
  opacity: 0.3;
}

/* Center */
.ring-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.ring-value {
  font-family: var(--hand-font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--hand-text-dark);
  line-height: 1;
}

.ring-label {
  font-family: var(--hand-font-handwriting);
  font-size: 0.75rem;
  color: var(--hand-text);
  margin-top: 0.15rem;
}

/* Deco */
.ring-deco {
  position: absolute;
  top: -5px;
  right: -5px;
  font-size: 1rem;
}
</style>
