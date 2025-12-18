<script setup lang="ts">
import { computed } from 'vue'

// Props from frontmatter
const props = defineProps<{
  ratio?: string
}>()

// Parse ratio parameter (e.g., "60-40", "50-50", "70-30")
const splitRatio = computed(() => {
  const ratio = props.ratio || '50-50'
  const parts = ratio.split('-').map(Number)
  
  if (parts.length === 2 && !parts.some(isNaN)) {
    const [left, right] = parts
    const total = left + right
    return {
      left: `${(left / total) * 100}%`,
      right: `${(right / total) * 100}%`
    }
  }
  
  // Default to 50-50 split
  return { left: '50%', right: '50%' }
})

const containerStyle = computed(() => ({
  display: 'flex',
  gap: '2rem'
}))
</script>

<template>
  <div class="hero-split-layout" :style="containerStyle">
    <!-- Left panel -->
    <div class="split-panel split-left" :style="{ width: splitRatio.left }">
      <slot name="left" />
    </div>
    
    <!-- Right panel -->
    <div class="split-panel split-right" :style="{ width: splitRatio.right }">
      <slot name="right" />
    </div>
  </div>
</template>

<style scoped>
.hero-split-layout {
  width: 100%;
  height: 100%;
  padding: 2rem;
  background-color: var(--c-bg-base);
  color: var(--c-text-main);
}

.split-panel {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 1.5rem;
  overflow: auto;
}

.split-left {
  border-right: 1px solid var(--border-theme);
  padding-right: 2rem;
}

.split-right {
  padding-left: 2rem;
}
</style>
