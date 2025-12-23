<!--
  quote-hero.vue - Dramatic Quote Display Layout
  
  Purpose: Stunning quote display with large typography and attribution
  Perfect for testimonials, key quotes, or impactful statements
  
  Props:
    - theme: Theme name (business, cyber, minimal, academic, creative, dark)
    - vibe: Vibe name (none, calm, dynamic, playful, professional, minimal, dramatic)
    - header: Header text
    - footer: Footer text
    - quoteStyle: Visual style (classic, modern, editorial, bold)
  
  Slots:
    - quote: The quote text
    - author: Quote attribution/author
    - context: Additional context (title, company, etc.)
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="quote-hero-layout" :class="[`style-${quoteStyle}`, `vibe-${vibe}`]">
      <!-- Decorative quote marks -->
      <div class="quote-marks">
        <span class="quote-mark quote-mark-open">"</span>
        <span class="quote-mark quote-mark-close">"</span>
      </div>
      
      <!-- Main quote content -->
      <div class="quote-wrapper" :style="quoteTransform">
        <blockquote class="quote-text">
          <slot name="quote" />
        </blockquote>
        
        <!-- Attribution -->
        <div v-if="$slots.author || $slots.context" class="quote-attribution">
          <div class="attribution-line"></div>
          <div class="author-wrapper">
            <div v-if="$slots.author" class="author-name">
              <slot name="author" />
            </div>
            <div v-if="$slots.context" class="author-context">
              <slot name="context" />
            </div>
          </div>
        </div>
      </div>
      
      <!-- Background decorations -->
      <div class="quote-decorations">
        <div class="decoration decoration-1"></div>
        <div class="decoration decoration-2"></div>
        <div class="decoration decoration-3"></div>
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
  quoteStyle?: 'classic' | 'modern' | 'editorial' | 'bold'
}>(), {
  theme: 'business',
  vibe: 'none',
  quoteStyle: 'modern'
})

// Vibe configuration
const vibeConfig = computed(() => {
  const configs: Record<string, { rotation: number; translate: number; scale: number }> = {
    none: { rotation: 0, translate: 0, scale: 0 },
    calm: { rotation: 0.5, translate: 5, scale: 0.01 },
    dynamic: { rotation: 2, translate: 12, scale: 0.02 },
    playful: { rotation: 3, translate: 18, scale: 0.03 },
    professional: { rotation: 0.3, translate: 3, scale: 0.005 },
    minimal: { rotation: 0, translate: 0, scale: 0 },
    dramatic: { rotation: 2.5, translate: 15, scale: 0.025 }
  }
  return configs[props.vibe] || configs.none
})

const seededRandom = (seed: number) => {
  const x = Math.sin(seed * 9999) * 10000
  return x - Math.floor(x)
}

const quoteTransform = computed(() => {
  const config = vibeConfig.value
  if (config.rotation === 0 && config.translate === 0) return {}
  
  const rotation = (seededRandom(50) - 0.5) * config.rotation
  const translateY = (seededRandom(51) - 0.5) * config.translate
  const scale = 1 + (seededRandom(52) - 0.5) * config.scale
  
  return {
    transform: `rotate(${rotation}deg) translateY(${translateY}px) scale(${scale})`
  }
})
</script>

<style scoped>
.quote-hero-layout {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 2rem;
}

/* Quote marks */
.quote-marks {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.quote-mark {
  position: absolute;
  font-size: 15rem;
  font-family: Georgia, serif;
  color: var(--c-primary);
  opacity: 0.08;
  line-height: 1;
}

.quote-mark-open {
  top: 0;
  left: 2rem;
}

.quote-mark-close {
  bottom: 0;
  right: 2rem;
  transform: rotate(180deg);
}

/* Quote wrapper */
.quote-wrapper {
  max-width: 85%;
  text-align: center;
  position: relative;
  z-index: 10;
  transition: transform 0.3s ease;
}

/* Quote text */
.quote-text {
  margin: 0;
  padding: 0;
}

.quote-text :deep(p) {
  font-size: 2.5rem;
  font-weight: 400;
  color: var(--c-text-main);
  line-height: 1.4;
  margin: 0;
  font-family: var(--font-family);
}

/* Attribution */
.quote-attribution {
  margin-top: 2.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.attribution-line {
  width: 60px;
  height: 3px;
  background: linear-gradient(to right, transparent, var(--c-primary), transparent);
  border-radius: 2px;
}

.author-wrapper {
  text-align: center;
}

.author-name :deep(p),
.author-name :deep(span) {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--c-primary);
  margin: 0;
}

.author-context :deep(p),
.author-context :deep(span) {
  font-size: 1rem;
  color: var(--c-text-muted);
  margin: 0.25rem 0 0;
  font-style: italic;
}

/* Background decorations */
.quote-decorations {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.decoration {
  position: absolute;
  border-radius: 50%;
  background: var(--c-primary);
  opacity: 0.03;
}

.decoration-1 {
  width: 400px;
  height: 400px;
  top: -150px;
  right: -100px;
}

.decoration-2 {
  width: 300px;
  height: 300px;
  bottom: -100px;
  left: -50px;
}

.decoration-3 {
  width: 200px;
  height: 200px;
  top: 50%;
  left: 10%;
  background: var(--c-accent);
}

/* Style variants */
.style-classic .quote-text :deep(p) {
  font-family: Georgia, 'Times New Roman', serif;
  font-style: italic;
  font-size: 2.25rem;
}

.style-classic .quote-mark {
  opacity: 0.15;
}

.style-bold .quote-text :deep(p) {
  font-size: 3.5rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.style-bold .quote-mark {
  display: none;
}

.style-bold .attribution-line {
  width: 100px;
  height: 5px;
  background: var(--c-primary);
}

.style-editorial .quote-text :deep(p) {
  font-size: 2rem;
  font-weight: 300;
  letter-spacing: 0.03em;
  line-height: 1.6;
}

.style-editorial .quote-mark-open {
  font-size: 8rem;
  top: 15%;
  left: 5%;
  opacity: 0.2;
  color: var(--c-accent);
}

.style-editorial .quote-mark-close {
  display: none;
}

.style-modern .quote-wrapper {
  background: var(--c-bg-surface);
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: var(--shadow-theme);
}

/* Vibe variations */
.vibe-dramatic .quote-mark {
  opacity: 0.2;
  animation: quote-pulse 3s ease-in-out infinite;
}

@keyframes quote-pulse {
  0%, 100% { opacity: 0.1; transform: scale(1); }
  50% { opacity: 0.25; transform: scale(1.05); }
}

.vibe-dramatic .quote-mark-close {
  animation-delay: 1.5s;
}

.vibe-playful .decoration {
  animation: float 4s ease-in-out infinite;
}

.vibe-playful .decoration-2 {
  animation-delay: 1s;
}

.vibe-playful .decoration-3 {
  animation-delay: 2s;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.vibe-minimal .quote-marks,
.vibe-minimal .quote-decorations {
  display: none;
}

.vibe-minimal .attribution-line {
  background: var(--c-text-muted);
  opacity: 0.3;
}

.vibe-calm .quote-wrapper {
  background: linear-gradient(135deg, rgba(255,255,255,0.02), transparent);
  padding: 2rem;
  border-radius: 0.5rem;
}

.vibe-professional .quote-wrapper {
  border-left: 4px solid var(--c-primary);
  padding-left: 2rem;
  text-align: left;
}

.vibe-professional .quote-attribution {
  align-items: flex-start;
}

.vibe-professional .attribution-line {
  display: none;
}
</style>
