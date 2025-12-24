<!--
  ProgressRing.vue - Cyberpunk Progress Ring Widget
  
  Props:
    - value: Current value (0-100)
    - label: Progress label
    - size: Ring size in pixels
-->
<template>
  <div class="progress-ring" :style="{ '--size': `${size}px` }">
    <svg class="ring-svg" :viewBox="`0 0 ${size} ${size}`">
      <!-- Background ring -->
      <circle 
        class="ring-bg"
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        :stroke-width="strokeWidth"
      />
      <!-- Progress ring -->
      <circle 
        class="ring-progress"
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        :stroke-width="strokeWidth"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="progressOffset"
        stroke-linecap="round"
      />
      <!-- Glow ring -->
      <circle 
        class="ring-glow"
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        :stroke-width="strokeWidth + 4"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="progressOffset"
        stroke-linecap="round"
      />
    </svg>
    <div class="ring-content">
      <span class="ring-value">{{ value }}%</span>
      <span v-if="label" class="ring-label">{{ label }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  value: number
  label?: string
  size?: number
}>(), {
  size: 120
})

const strokeWidth = 8
const radius = computed(() => (props.size - strokeWidth) / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)
const progressOffset = computed(() => {
  const progress = Math.max(0, Math.min(100, props.value)) / 100
  return circumference.value * (1 - progress)
})
</script>

<style scoped>
.progress-ring {
  position: relative;
  width: var(--size);
  height: var(--size);
}

.ring-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.ring-bg {
  stroke: rgba(0, 255, 255, 0.1);
}

.ring-progress {
  stroke: url(#ring-gradient);
  stroke: var(--cyber-cyan, #00FFFF);
  filter: drop-shadow(0 0 5px var(--cyber-cyan-glow));
  transition: stroke-dashoffset 0.5s ease-out;
}

.ring-glow {
  stroke: var(--cyber-cyan, #00FFFF);
  opacity: 0.3;
  filter: blur(4px);
}

.ring-content {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.ring-value {
  font-family: var(--cyber-font-display);
  font-size: calc(var(--size) * 0.2);
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-shadow: 0 0 15px var(--cyber-cyan-glow);
  line-height: 1;
}

.ring-label {
  font-family: var(--cyber-font-mono);
  font-size: calc(var(--size) * 0.08);
  color: var(--cyber-text-dim);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 0.25rem;
}
</style>
