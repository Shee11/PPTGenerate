<!--
  spotlight.vue - Cinematic Spotlight Layout
  
  Purpose: Dramatic center-focused layout with radial gradient spotlight effect
  Perfect for key announcements, featured content, or dramatic reveals
  
  Props:
    - theme: Theme name (business, cyber, minimal, academic, creative, dark)
    - vibe: Vibe name (none, calm, dynamic, playful, professional, minimal, dramatic)
    - header: Header text
    - footer: Footer text
    - spotlightColor: Spotlight gradient color (default: primary color)
    - intensity: Spotlight intensity (soft, medium, strong)
  
  Slots:
    - default: Main content in spotlight
    - subtitle: Secondary text below main content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="spotlight-layout" :class="[`intensity-${intensity}`, `vibe-${vibe}`]">
      <!-- Spotlight effect layer -->
      <div class="spotlight-effect" :style="spotlightStyle"></div>
      
      <!-- Ambient particles for dynamic vibes -->
      <div v-if="showParticles" class="particles">
        <div v-for="i in 12" :key="i" class="particle" :style="particleStyle(i)"></div>
      </div>
      
      <!-- Main content area -->
      <div class="content-wrapper" :style="contentTransform">
        <div class="main-content">
          <slot />
        </div>
        <div v-if="$slots.subtitle" class="subtitle-content">
          <slot name="subtitle" />
        </div>
      </div>
      
      <!-- Decorative rings -->
      <div class="decorative-rings">
        <div class="ring ring-1"></div>
        <div class="ring ring-2"></div>
        <div class="ring ring-3"></div>
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
  spotlightColor?: string
  intensity?: 'soft' | 'medium' | 'strong'
}>(), {
  theme: 'business',
  vibe: 'none',
  intensity: 'medium'
})

// Spotlight gradient style
const spotlightStyle = computed(() => {
  const color = props.spotlightColor || 'var(--c-primary)'
  const intensityMap = {
    soft: { size: '60%', opacity: 0.15 },
    medium: { size: '50%', opacity: 0.25 },
    strong: { size: '40%', opacity: 0.4 }
  }
  const config = intensityMap[props.intensity]
  
  return {
    background: `radial-gradient(ellipse ${config.size} ${config.size} at center, ${color}, transparent)`,
    opacity: config.opacity
  }
})

// Show particles for dynamic/playful vibes
const showParticles = computed(() => 
  ['dynamic', 'playful', 'dramatic'].includes(props.vibe)
)

// Particle animation styles
const particleStyle = (index: number) => {
  const angle = (index / 12) * 360
  const distance = 35 + (index % 3) * 10
  const delay = index * 0.2
  const duration = 3 + (index % 2)
  
  return {
    '--angle': `${angle}deg`,
    '--distance': `${distance}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`
  }
}

// Vibe-based content transform
const seededRandom = (seed: number) => {
  const x = Math.sin(seed * 9999) * 10000
  return x - Math.floor(x)
}

const contentTransform = computed(() => {
  const vibeConfig: Record<string, { rotation: number; translate: number }> = {
    none: { rotation: 0, translate: 0 },
    calm: { rotation: 0.5, translate: 3 },
    dynamic: { rotation: 2, translate: 8 },
    playful: { rotation: 3, translate: 12 },
    professional: { rotation: 0.2, translate: 1 },
    minimal: { rotation: 0, translate: 0 },
    dramatic: { rotation: 1.5, translate: 6 }
  }
  
  const config = vibeConfig[props.vibe] || vibeConfig.none
  if (config.rotation === 0 && config.translate === 0) return {}
  
  const rotation = (seededRandom(42) - 0.5) * 2 * config.rotation
  const translateY = (seededRandom(43) - 0.5) * 2 * config.translate
  
  return {
    transform: `rotate(${rotation}deg) translateY(${translateY}px)`
  }
})
</script>

<style scoped>
.spotlight-layout {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

/* Spotlight effect */
.spotlight-effect {
  position: absolute;
  inset: -20%;
  pointer-events: none;
  transition: opacity 0.5s ease;
}

/* Particles */
.particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: var(--c-primary);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  opacity: 0.6;
  animation: particle-float 3s ease-in-out infinite;
}

@keyframes particle-float {
  0%, 100% {
    transform: translate(-50%, -50%) rotate(var(--angle)) translateX(var(--distance)) scale(1);
    opacity: 0.6;
  }
  50% {
    transform: translate(-50%, -50%) rotate(var(--angle)) translateX(calc(var(--distance) + 5%)) scale(1.5);
    opacity: 1;
  }
}

/* Content wrapper */
.content-wrapper {
  position: relative;
  z-index: 10;
  text-align: center;
  max-width: 80%;
  transition: transform 0.3s ease;
}

.main-content {
  margin-bottom: 1.5rem;
}

.main-content :deep(h1) {
  font-size: 4rem;
  font-weight: 800;
  color: var(--c-text-main);
  margin: 0;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  font-family: var(--font-family);
}

.main-content :deep(h2) {
  font-size: 2.5rem;
  font-weight: 600;
  color: var(--c-primary);
  margin: 0.5rem 0 0;
}

.main-content :deep(p) {
  font-size: 1.5rem;
  color: var(--c-text-muted);
  margin: 1rem 0 0;
  line-height: 1.6;
}

.subtitle-content {
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.subtitle-content :deep(p) {
  font-size: 1.125rem;
  color: var(--c-text-muted);
  margin: 0;
  font-style: italic;
}

/* Decorative rings */
.decorative-rings {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 1px solid var(--c-primary);
  border-radius: 50%;
  opacity: 0.1;
}

.ring-1 {
  width: 120%;
  height: 120%;
  animation: ring-pulse 4s ease-in-out infinite;
}

.ring-2 {
  width: 140%;
  height: 140%;
  animation: ring-pulse 4s ease-in-out infinite 0.5s;
}

.ring-3 {
  width: 160%;
  height: 160%;
  animation: ring-pulse 4s ease-in-out infinite 1s;
}

@keyframes ring-pulse {
  0%, 100% { opacity: 0.05; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 0.15; transform: translate(-50%, -50%) scale(1.02); }
}

/* Intensity variations */
.intensity-soft .ring { opacity: 0.05; }
.intensity-strong .ring { opacity: 0.2; }
.intensity-strong .spotlight-effect { filter: blur(40px); }

/* Vibe variations */
.vibe-dramatic .ring {
  border-width: 2px;
  animation-duration: 2s;
}

.vibe-playful .particle {
  width: 6px;
  height: 6px;
  background: var(--c-accent);
}

.vibe-minimal .decorative-rings,
.vibe-minimal .particles {
  display: none;
}

.vibe-calm .spotlight-effect {
  filter: blur(60px);
}
</style>
