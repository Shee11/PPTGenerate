<!--
  stats-showcase.vue - Impressive Statistics Display Layout
  
  Purpose: Stunning display of key metrics with animated counters and visual impact
  Perfect for data highlights, KPIs, achievements, or impressive numbers
  
  Props:
    - theme: Theme name (business, cyber, minimal, academic, creative, dark)
    - vibe: Vibe name (none, calm, dynamic, playful, professional, minimal, dramatic)
    - header: Header text
    - footer: Footer text
    - columns: Number of stat columns (2, 3, 4)
    - style: Visual style (cards, minimal, gradient, neon)
  
  Slots:
    - title: Optional section title
    - stat-1 to stat-6: Individual stat slots
    - default: Fallback content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="stats-showcase-layout" :class="[`cols-${columns}`, `style-${displayStyle}`, `vibe-${vibe}`]">
      <!-- Section title -->
      <div v-if="$slots.title" class="section-title">
        <slot name="title" />
      </div>
      
      <!-- Stats grid -->
      <div class="stats-grid">
        <div 
          v-for="i in 6" 
          :key="i" 
          class="stat-item"
          :style="statTransform(i)"
          v-show="$slots[`stat-${i}`]"
        >
          <div class="stat-glow"></div>
          <div class="stat-content">
            <slot :name="`stat-${i}`" />
          </div>
          <div class="stat-underline"></div>
        </div>
      </div>
      
      <!-- Background effects -->
      <div class="stats-background">
        <div class="grid-lines">
          <div v-for="i in 5" :key="i" class="grid-line" :style="{ '--line-index': i }"></div>
        </div>
        <div class="glow-orbs">
          <div class="orb orb-1"></div>
          <div class="orb orb-2"></div>
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
  columns?: 2 | 3 | 4
  displayStyle?: 'cards' | 'minimal' | 'gradient' | 'neon'
}>(), {
  theme: 'business',
  vibe: 'none',
  columns: 3,
  displayStyle: 'cards'
})

// Vibe configuration
const vibeConfig = computed(() => {
  const configs: Record<string, { rotation: number; translate: number; scale: number; stagger: number }> = {
    none: { rotation: 0, translate: 0, scale: 0, stagger: 0 },
    calm: { rotation: 0.5, translate: 4, scale: 0.01, stagger: 0.05 },
    dynamic: { rotation: 2, translate: 10, scale: 0.02, stagger: 0.1 },
    playful: { rotation: 3, translate: 15, scale: 0.03, stagger: 0.15 },
    professional: { rotation: 0.3, translate: 2, scale: 0.005, stagger: 0.03 },
    minimal: { rotation: 0, translate: 0, scale: 0, stagger: 0 },
    dramatic: { rotation: 2, translate: 8, scale: 0.025, stagger: 0.08 }
  }
  return configs[props.vibe] || configs.none
})

const seededRandom = (seed: number) => {
  const x = Math.sin(seed * 9999) * 10000
  return x - Math.floor(x)
}

const statTransform = (index: number) => {
  const config = vibeConfig.value
  if (config.rotation === 0 && config.translate === 0) {
    return { '--stat-index': index }
  }
  
  const seed = index * 10
  const rotation = (seededRandom(seed) - 0.5) * 2 * config.rotation
  const translateX = (seededRandom(seed + 1) - 0.5) * 2 * config.translate
  const translateY = (seededRandom(seed + 2) - 0.5) * 2 * config.translate
  const scale = 1 + (seededRandom(seed + 3) - 0.5) * 2 * config.scale
  
  return {
    '--stat-index': index,
    transform: `rotate(${rotation}deg) translate(${translateX}px, ${translateY}px) scale(${scale})`
  }
}
</script>

<style scoped>
.stats-showcase-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 2rem;
  position: relative;
  padding: 1rem;
}

/* Section title */
.section-title {
  text-align: center;
  margin-bottom: 1rem;
}

.section-title :deep(h1),
.section-title :deep(h2) {
  font-size: 2rem;
  font-weight: 700;
  color: var(--c-text-main);
  margin: 0;
  font-family: var(--font-family);
}

.section-title :deep(p) {
  font-size: 1.125rem;
  color: var(--c-text-muted);
  margin: 0.5rem 0 0;
}

/* Stats grid */
.stats-grid {
  display: grid;
  gap: 1.5rem;
  position: relative;
  z-index: 10;
}

.cols-2 .stats-grid { grid-template-columns: repeat(2, 1fr); }
.cols-3 .stats-grid { grid-template-columns: repeat(3, 1fr); }
.cols-4 .stats-grid { grid-template-columns: repeat(4, 1fr); }

/* Stat item */
.stat-item {
  position: relative;
  padding: 1.5rem;
  text-align: center;
  transition: transform 0.3s ease;
}

.stat-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, var(--c-primary), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 1rem;
}

.stat-item:hover .stat-glow {
  opacity: 0.1;
}

.stat-content {
  position: relative;
  z-index: 1;
}

.stat-content :deep(.stat-value),
.stat-content :deep(h2) {
  font-size: 3.5rem;
  font-weight: 800;
  color: var(--c-primary);
  margin: 0;
  line-height: 1;
  font-family: var(--font-family);
}

.stat-content :deep(.stat-label),
.stat-content :deep(h3) {
  font-size: 1rem;
  font-weight: 500;
  color: var(--c-text-main);
  margin: 0.75rem 0 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-content :deep(.stat-detail),
.stat-content :deep(p) {
  font-size: 0.875rem;
  color: var(--c-text-muted);
  margin: 0.5rem 0 0;
}

.stat-underline {
  width: 40px;
  height: 3px;
  background: var(--c-accent);
  margin: 1rem auto 0;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.stat-item:hover .stat-underline {
  width: 60px;
}

/* Style variants */
.style-cards .stat-item {
  background: var(--c-bg-surface);
  border-radius: 1rem;
  box-shadow: var(--shadow-theme);
}

.style-cards .stat-glow {
  border-radius: 1rem;
}

.style-gradient .stat-item {
  background: linear-gradient(135deg, var(--c-bg-surface), rgba(255,255,255,0.02));
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.style-gradient .stat-content :deep(.stat-value),
.style-gradient .stat-content :deep(h2) {
  background: linear-gradient(135deg, var(--c-primary), var(--c-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.style-neon .stat-item {
  border: 1px solid var(--c-primary);
  border-radius: 0.5rem;
  background: transparent;
}

.style-neon .stat-content :deep(.stat-value),
.style-neon .stat-content :deep(h2) {
  text-shadow: 0 0 20px var(--c-primary), 0 0 40px var(--c-primary);
}

.style-neon .stat-underline {
  box-shadow: 0 0 10px var(--c-accent);
}

.style-minimal .stat-item {
  background: transparent;
  padding: 1rem;
}

.style-minimal .stat-underline {
  display: none;
}

.style-minimal .stat-glow {
  display: none;
}

/* Background effects */
.stats-background {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.grid-lines {
  position: absolute;
  inset: 0;
}

.grid-line {
  position: absolute;
  width: 100%;
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(255,255,255,0.03), transparent);
  top: calc(var(--line-index) * 20%);
}

.glow-orbs {
  position: absolute;
  inset: 0;
}

.orb {
  position: absolute;
  border-radius: 50%;
  background: var(--c-primary);
  opacity: 0.03;
  filter: blur(60px);
}

.orb-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  right: -50px;
}

.orb-2 {
  width: 250px;
  height: 250px;
  bottom: -100px;
  left: -50px;
  background: var(--c-accent);
}

/* Vibe variations */
.vibe-dramatic .stat-content :deep(.stat-value),
.vibe-dramatic .stat-content :deep(h2) {
  animation: value-glow 2s ease-in-out infinite;
}

@keyframes value-glow {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

.vibe-playful .stat-item {
  animation: stat-bounce 3s ease-in-out infinite;
  animation-delay: calc(var(--stat-index) * 0.2s);
}

@keyframes stat-bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.vibe-minimal .stats-background {
  display: none;
}

.vibe-calm .orb {
  animation: orb-float 6s ease-in-out infinite;
}

.vibe-calm .orb-2 {
  animation-delay: 3s;
}

@keyframes orb-float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(20px, -20px); }
}

.vibe-professional .stat-item {
  border-bottom: 2px solid var(--c-primary);
  border-radius: 0;
  padding-bottom: 1.5rem;
}

.vibe-professional .stat-underline {
  display: none;
}

.vibe-dynamic .stat-item {
  transform-origin: center bottom;
}
</style>
