<!--
  cards-grid.vue - Modern Card Grid Layout
  
  Purpose: Flexible grid of styled cards with hover effects
  Perfect for features, services, team members, or categorized content
  
  Props:
    - theme: Theme name (business, cyber, minimal, academic, creative, dark)
    - vibe: Vibe name (none, calm, dynamic, playful, professional, minimal, dramatic)
    - header: Header text
    - footer: Footer text
    - columns: Grid columns (2, 3, 4)
    - cardStyle: Card appearance (elevated, flat, outlined, glass)
  
  Slots:
    - title: Optional section title
    - card-1 to card-8: Individual card slots
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="cards-grid-layout" :class="[`cols-${columns}`, `style-${cardStyle}`, `vibe-${vibe}`]">
      <!-- Section title -->
      <div v-if="$slots.title" class="section-title">
        <slot name="title" />
      </div>
      
      <!-- Cards grid -->
      <div class="cards-container">
        <div 
          v-for="i in 8" 
          :key="i" 
          class="card-item"
          :style="cardTransform(i)"
          v-show="$slots[`card-${i}`]"
        >
          <div class="card-inner">
            <div class="card-shine"></div>
            <div class="card-content">
              <slot :name="`card-${i}`" />
            </div>
            <div class="card-accent"></div>
          </div>
        </div>
      </div>
      
      <!-- Background pattern -->
      <div class="grid-background">
        <div class="pattern-dots"></div>
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
  cardStyle?: 'elevated' | 'flat' | 'outlined' | 'glass'
}>(), {
  theme: 'business',
  vibe: 'none',
  columns: 3,
  cardStyle: 'elevated'
})

// Vibe configuration
const vibeConfig = computed(() => {
  const configs: Record<string, { rotation: number; translate: number; scale: number }> = {
    none: { rotation: 0, translate: 0, scale: 0 },
    calm: { rotation: 0.5, translate: 4, scale: 0.008 },
    dynamic: { rotation: 2, translate: 10, scale: 0.02 },
    playful: { rotation: 4, translate: 16, scale: 0.04 },
    professional: { rotation: 0.2, translate: 2, scale: 0.005 },
    minimal: { rotation: 0, translate: 0, scale: 0 },
    dramatic: { rotation: 2.5, translate: 12, scale: 0.025 }
  }
  return configs[props.vibe] || configs.none
})

const seededRandom = (seed: number) => {
  const x = Math.sin(seed * 9999) * 10000
  return x - Math.floor(x)
}

const cardTransform = (index: number) => {
  const config = vibeConfig.value
  const baseStyle = { '--card-index': index }
  
  if (config.rotation === 0 && config.translate === 0) {
    return baseStyle
  }
  
  const seed = index * 17
  const rotation = (seededRandom(seed) - 0.5) * 2 * config.rotation
  const translateX = (seededRandom(seed + 1) - 0.5) * 2 * config.translate
  const translateY = (seededRandom(seed + 2) - 0.5) * 2 * config.translate
  const scale = 1 + (seededRandom(seed + 3) - 0.5) * 2 * config.scale
  
  return {
    ...baseStyle,
    transform: `rotate(${rotation}deg) translate(${translateX}px, ${translateY}px) scale(${scale})`
  }
}
</script>

<style scoped>
.cards-grid-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  position: relative;
  padding: 0.5rem;
}

/* Section title */
.section-title {
  text-align: center;
}

.section-title :deep(h1),
.section-title :deep(h2) {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--c-text-main);
  margin: 0;
  font-family: var(--font-family);
}

.section-title :deep(p) {
  font-size: 1rem;
  color: var(--c-text-muted);
  margin: 0.5rem 0 0;
}

/* Cards container */
.cards-container {
  flex: 1;
  display: grid;
  gap: 1.25rem;
  align-content: center;
  position: relative;
  z-index: 10;
}

.cols-2 .cards-container { grid-template-columns: repeat(2, 1fr); }
.cols-3 .cards-container { grid-template-columns: repeat(3, 1fr); }
.cols-4 .cards-container { grid-template-columns: repeat(4, 1fr); }

/* Card item */
.card-item {
  transition: transform 0.3s ease;
}

.card-inner {
  height: 100%;
  min-height: 140px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.card-shine {
  position: absolute;
  top: -100%;
  left: -100%;
  width: 300%;
  height: 300%;
  background: linear-gradient(
    135deg,
    transparent 30%,
    rgba(255, 255, 255, 0.05) 50%,
    transparent 70%
  );
  transform: rotate(45deg);
  transition: all 0.6s ease;
  pointer-events: none;
}

.card-item:hover .card-shine {
  top: -50%;
  left: -50%;
}

.card-content {
  height: 100%;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

.card-content :deep(h3) {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--c-text-main);
  margin: 0 0 0.5rem;
}

.card-content :deep(h4) {
  font-size: 1rem;
  font-weight: 500;
  color: var(--c-primary);
  margin: 0 0 0.5rem;
}

.card-content :deep(p) {
  font-size: 0.875rem;
  color: var(--c-text-muted);
  line-height: 1.5;
  margin: 0;
  flex: 1;
}

.card-content :deep(ul) {
  margin: 0;
  padding-left: 1rem;
  font-size: 0.875rem;
}

.card-content :deep(li) {
  color: var(--c-text-muted);
  margin-bottom: 0.25rem;
}

.card-content :deep(.card-icon) {
  font-size: 2rem;
  margin-bottom: 0.75rem;
}

.card-accent {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(to right, var(--c-primary), var(--c-accent));
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.card-item:hover .card-accent {
  transform: scaleX(1);
}

/* Style variants */
.style-elevated .card-inner {
  background: var(--c-bg-surface);
  border-radius: 0.75rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.style-elevated .card-item:hover .card-inner {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

.style-flat .card-inner {
  background: var(--c-bg-surface);
  border-radius: 0.5rem;
}

.style-outlined .card-inner {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
}

.style-outlined .card-item:hover .card-inner {
  border-color: var(--c-primary);
  background: rgba(255, 255, 255, 0.02);
}

.style-glass .card-inner {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
}

.style-glass .card-item:hover .card-inner {
  background: rgba(255, 255, 255, 0.08);
}

/* Background pattern */
.grid-background {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.pattern-dots {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, var(--c-primary) 1px, transparent 1px);
  background-size: 30px 30px;
  opacity: 0.03;
}

/* Vibe variations */
.vibe-playful .card-inner {
  border-radius: 1.5rem;
}

.vibe-playful .card-item {
  animation: card-wobble 3s ease-in-out infinite;
  animation-delay: calc(var(--card-index) * 0.15s);
}

@keyframes card-wobble {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(1deg); }
  75% { transform: rotate(-1deg); }
}

.vibe-dramatic .card-accent {
  height: 5px;
}

.vibe-dramatic .card-item:hover .card-inner {
  transform: scale(1.03);
}

.vibe-minimal .card-accent,
.vibe-minimal .card-shine,
.vibe-minimal .grid-background {
  display: none;
}

.vibe-calm .pattern-dots {
  opacity: 0.02;
}

.vibe-professional .card-inner {
  border-radius: 0.25rem;
}

.vibe-professional .card-accent {
  height: 2px;
  background: var(--c-primary);
}

.vibe-dynamic .card-inner {
  transform-origin: center bottom;
}

.vibe-dynamic .card-item:hover .card-inner {
  transform: perspective(500px) rotateX(-5deg) translateY(-8px);
}
</style>
