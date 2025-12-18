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
  padding: 3rem;
  background: linear-gradient(135deg, var(--c-bg-base) 0%, color-mix(in srgb, var(--c-bg-base) 97%, var(--slidev-theme-primary, #3b82f6)) 100%);
  color: var(--c-text-main);
  position: relative;
  overflow: hidden;
}

/* Decorative background pattern on left side */
.hero-split-layout::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 40%;
  background: 
    radial-gradient(circle at 30% 40%, rgba(59, 130, 246, 0.04) 0%, transparent 60%),
    repeating-linear-gradient(45deg, transparent, transparent 40px, rgba(59, 130, 246, 0.02) 40px, rgba(59, 130, 246, 0.02) 80px);
  pointer-events: none;
}

/* Decorative diagonal divider */
.hero-split-layout::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: calc(var(--split-left, 50%) - 2px);
  width: 4px;
  background: linear-gradient(180deg, 
    transparent 0%, 
    var(--slidev-theme-primary, #3b82f6) 20%,
    var(--slidev-theme-primary, #3b82f6) 80%,
    transparent 100%);
  opacity: 0.3;
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
  pointer-events: none;
}

.split-panel {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 2.5rem;
  overflow: auto;
  position: relative;
  z-index: 1;
}

.split-left {
  padding-right: 3rem;
  position: relative;
}

/* Subtle overlay on left panel */
.split-left::before {
  content: '';
  position: absolute;
  inset: -1rem;
  background: linear-gradient(120deg, 
    rgba(59, 130, 246, 0.02) 0%, 
    transparent 60%);
  border-radius: 20px;
  pointer-events: none;
}

.split-right {
  padding-left: 3rem;
}

/* Floating accent shapes */
.split-right::before {
  content: '';
  position: absolute;
  right: 5%;
  top: 10%;
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.08) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.split-right::after {
  content: '';
  position: absolute;
  right: 15%;
  bottom: 15%;
  width: 80px;
  height: 80px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.06) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}
</style>
