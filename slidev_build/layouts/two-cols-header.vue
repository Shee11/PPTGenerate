<!--
  two-cols-header.vue - Two Column Layout with Header
  
  Purpose: Two-column content layout with prominent header section
  
  Props:
    - theme: Theme name (business, cyber, minimal, academic, creative, dark)
    - vibe: Vibe name (none, calm, dynamic, playful, professional, minimal, dramatic)
    - header: Header text (passed to SlideShell)
    - footer: Footer text (passed to SlideShell)
    - ratio: Column ratio ('50-50', '40-60', '60-40', '30-70', '70-30')
  
  Slots:
    - header: Main title/header content
    - left: Left column content
    - right: Right column content
    - default: Fallback content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="two-cols-header-layout">
      <!-- Main title from ::header:: slot -->
      <div class="header-section" :style="headerTransform">
        <slot name="header">
          <h1>Two Columns</h1>
        </slot>
      </div>

      <!-- Two columns content -->
      <div class="columns-container" :style="containerStyle">
        <div 
          class="column column-left" 
          :style="{ ...leftColumnStyle, ...vibeTransform(0) }"
        >
          <slot name="left">
            <slot />
          </slot>
        </div>
        <div 
          class="column column-right" 
          :style="{ ...rightColumnStyle, ...vibeTransform(1) }"
        >
          <slot name="right" />
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import SlideShell from './SlideShell.vue'

const props = withDefaults(defineProps<{
  theme?: string
  vibe?: string
  header?: string
  footer?: string
  ratio?: string
}>(), {
  theme: 'business',
  vibe: 'none',
  ratio: '50-50'
})

// Parse ratio into flex values
const ratioValues = computed(() => {
  const ratioMap: Record<string, [number, number]> = {
    '50-50': [1, 1],
    '40-60': [2, 3],
    '60-40': [3, 2],
    '30-70': [3, 7],
    '70-30': [7, 3]
  }
  return ratioMap[props.ratio] || [1, 1]
})

const leftColumnStyle = computed(() => ({
  flex: ratioValues.value[0]
}))

const rightColumnStyle = computed(() => ({
  flex: ratioValues.value[1]
}))

// Vibe configuration
const vibeConfig = computed(() => {
  const configs: Record<string, { rotation: number; translate: number; scale: number }> = {
    none: { rotation: 0, translate: 0, scale: 0 },
    calm: { rotation: 0.3, translate: 2, scale: 0.005 },
    dynamic: { rotation: 1.5, translate: 8, scale: 0.02 },
    playful: { rotation: 2.5, translate: 12, scale: 0.03 },
    professional: { rotation: 0.2, translate: 1, scale: 0.003 },
    minimal: { rotation: 0, translate: 0, scale: 0 },
    dramatic: { rotation: 2, translate: 10, scale: 0.025 }
  }
  return configs[props.vibe] || configs.none
})

// Seeded random for consistent vibe effects
const seededRandom = (seed: number) => {
  const x = Math.sin(seed * 9999) * 10000
  return x - Math.floor(x)
}

// Generate vibe-based transform for columns
const vibeTransform = (index: number) => {
  const config = vibeConfig.value
  if (config.rotation === 0 && config.translate === 0) {
    return {}
  }
  
  const seed = index + 1
  const rotation = (seededRandom(seed) - 0.5) * 2 * config.rotation
  const translateX = (seededRandom(seed + 10) - 0.5) * 2 * config.translate
  const translateY = (seededRandom(seed + 20) - 0.5) * 2 * config.translate
  const scale = 1 + (seededRandom(seed + 30) - 0.5) * 2 * config.scale
  
  return {
    transform: `rotate(${rotation}deg) translate(${translateX}px, ${translateY}px) scale(${scale})`
  }
}

// Header transform for vibe
const headerTransform = computed(() => {
  const config = vibeConfig.value
  if (config.rotation === 0 && config.translate === 0) {
    return {}
  }
  
  const rotation = (seededRandom(100) - 0.5) * config.rotation * 0.5
  const translateY = (seededRandom(110) - 0.5) * config.translate * 0.5
  
  return {
    transform: `rotate(${rotation}deg) translateY(${translateY}px)`
  }
})

// Container gap based on vibe
const containerStyle = computed(() => {
  const gapMap: Record<string, string> = {
    none: '2rem',
    calm: '2.5rem',
    dynamic: '1.5rem',
    playful: '3rem',
    professional: '2rem',
    minimal: '3rem',
    dramatic: '1rem'
  }
  return {
    gap: gapMap[props.vibe] || '2rem'
  }
})
</script>

<style scoped>
.two-cols-header-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.header-section {
  text-align: center;
  padding: 0.5rem 0;
  transition: transform 0.3s ease;
}

.header-section :deep(h1) {
  color: var(--c-primary);
  margin: 0;
  font-size: 2.25rem;
  font-weight: 700;
  font-family: var(--font-family);
}

.header-section :deep(h2) {
  color: var(--c-text-muted);
  margin: 0.5rem 0 0;
  font-size: 1.25rem;
  font-weight: 400;
}

.columns-container {
  flex: 1;
  display: flex;
  min-height: 0;
  transition: gap 0.3s ease;
}

.column {
  display: flex;
  flex-direction: column;
  min-width: 0;
  transition: transform 0.3s ease;
}

.column :deep(h3) {
  color: var(--c-primary);
  margin: 0 0 1rem;
  font-size: 1.5rem;
  font-weight: 600;
  font-family: var(--font-family);
}

.column :deep(h4) {
  color: var(--c-accent);
  margin: 0 0 0.75rem;
  font-size: 1.125rem;
  font-weight: 500;
}

.column :deep(p) {
  color: var(--c-text-main);
  margin: 0 0 1rem;
  line-height: 1.6;
}

.column :deep(ul),
.column :deep(ol) {
  color: var(--c-text-main);
  margin: 0 0 1rem;
  padding-left: 1.5rem;
}

.column :deep(li) {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.column :deep(li::marker) {
  color: var(--c-accent);
}

/* Vibe-specific column styles */
.vibe-playful .column {
  background: var(--c-bg-surface);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: var(--shadow-theme);
}

.vibe-dramatic .column-left {
  border-right: 3px solid var(--c-primary);
  padding-right: 1.5rem;
}

.vibe-dynamic .columns-container {
  align-items: flex-start;
}

.vibe-dynamic .column-right {
  margin-top: 2rem;
}

.vibe-minimal .column {
  padding: 0 1rem;
}

.vibe-professional .header-section {
  border-bottom: 2px solid var(--c-primary);
  padding-bottom: 1rem;
  margin-bottom: 0.5rem;
}

.vibe-calm .columns-container {
  background: var(--c-bg-surface);
  border-radius: 0.5rem;
  padding: 1.5rem;
}
</style>
