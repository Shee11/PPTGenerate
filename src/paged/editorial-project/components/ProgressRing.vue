<!--
  ProgressRing.vue - Editorial Progress Ring Component
  
  Props:
    - value: Progress percentage (0-100)
    - label: Progress label
    - size: Ring size
-->
<template>
  <div class="progress-ring" :style="{ '--size': size }">
    <svg class="ring-svg" viewBox="0 0 100 100">
      <circle class="ring-bg" cx="50" cy="50" r="42" />
      <circle 
        class="ring-progress" 
        cx="50" cy="50" r="42"
        :style="{ '--progress': value }"
      />
    </svg>
    <div class="ring-content">
      <span class="ring-value">{{ value }}%</span>
      <span v-if="label" class="ring-label">{{ label }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  value: number
  label?: string
  size?: string
}>(), {
  value: 0,
  size: '120px'
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
  fill: none;
  stroke: var(--edit-border);
  stroke-width: 6;
}

.ring-progress {
  fill: none;
  stroke: var(--edit-gold);
  stroke-width: 6;
  stroke-linecap: round;
  stroke-dasharray: 264;
  stroke-dashoffset: calc(264 - (264 * var(--progress) / 100));
  transition: stroke-dashoffset 0.6s ease;
}

.ring-content {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.15rem;
}

.ring-value {
  font-family: var(--edit-font-display);
  font-size: 1.25rem;
  color: var(--edit-text-dark);
}

.ring-label {
  font-family: var(--edit-font-accent);
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--edit-text-light);
}
</style>
