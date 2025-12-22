<!--
  AnimatedCounter.vue - Animated Number Counter Component
  
  Displays numbers with a counting animation effect.
  Great for statistics, metrics, achievements.
  
  Props:
    - value: Target number to count to
    - prefix: Text before number (e.g., "$")
    - suffix: Text after number (e.g., "%", "K")
    - duration: Animation duration in ms
    - decimals: Number of decimal places
    - label: Label text below number
    - color: Number color
-->
<template>
  <div class="animated-counter" :style="counterStyles">
    <div class="counter-value">
      <span v-if="prefix" class="prefix">{{ prefix }}</span>
      <span class="number">{{ displayValue }}</span>
      <span v-if="suffix" class="suffix">{{ suffix }}</span>
    </div>
    <div v-if="label" class="counter-label">{{ label }}</div>
    <div class="counter-underline"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'

const props = withDefaults(defineProps<{
  value: number
  prefix?: string
  suffix?: string
  duration?: number
  decimals?: number
  label?: string
  color?: string
}>(), {
  duration: 2000,
  decimals: 0,
  color: 'var(--c-primary)'
})

const currentValue = ref(0)

const displayValue = computed(() => {
  return currentValue.value.toFixed(props.decimals)
})

const counterStyles = computed(() => ({
  '--counter-color': props.color
}))

const animateCounter = () => {
  const startTime = performance.now()
  const startValue = 0
  const endValue = props.value
  
  const animate = (currentTime: number) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / props.duration, 1)
    
    // Easing function (ease-out)
    const easeOut = 1 - Math.pow(1 - progress, 3)
    
    currentValue.value = startValue + (endValue - startValue) * easeOut
    
    if (progress < 1) {
      requestAnimationFrame(animate)
    } else {
      currentValue.value = endValue
    }
  }
  
  requestAnimationFrame(animate)
}

onMounted(() => {
  animateCounter()
})

watch(() => props.value, () => {
  animateCounter()
})
</script>

<style scoped>
.animated-counter {
  text-align: center;
  padding: 1rem;
}

.counter-value {
  font-size: 3rem;
  font-weight: 800;
  color: var(--counter-color);
  line-height: 1;
  font-family: var(--font-family);
}

.prefix,
.suffix {
  font-size: 0.6em;
  font-weight: 600;
  opacity: 0.8;
}

.prefix {
  margin-right: 0.1em;
}

.suffix {
  margin-left: 0.1em;
}

.counter-label {
  font-size: 1rem;
  color: var(--c-text-muted);
  margin-top: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.counter-underline {
  width: 40px;
  height: 3px;
  background: var(--counter-color);
  margin: 0.75rem auto 0;
  border-radius: 2px;
  opacity: 0.6;
}
</style>
