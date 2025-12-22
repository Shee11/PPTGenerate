<!--
  magazine.vue - Editorial Magazine Layout
  
  Purpose: Asymmetric editorial design inspired by magazine spreads
  Features large featured area with sidebar content strips
  
  Props:
    - theme: Theme name (business, cyber, minimal, academic, creative, dark)
    - vibe: Vibe name (none, calm, dynamic, playful, professional, minimal, dramatic)
    - header: Header text
    - footer: Footer text
    - variant: Layout variant (left-feature, right-feature, center-feature)
  
  Slots:
    - feature: Main featured content (large area)
    - sidebar: Sidebar content strips
    - caption: Optional caption for featured content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="magazine-layout" :class="[`variant-${variant}`, `vibe-${vibe}`]">
      <!-- Feature area -->
      <div class="feature-area" :style="featureTransform">
        <div class="feature-content">
          <slot name="feature">
            <div class="placeholder">Featured Content</div>
          </slot>
        </div>
        <div v-if="$slots.caption" class="feature-caption">
          <slot name="caption" />
        </div>
      </div>
      
      <!-- Sidebar strips -->
      <div class="sidebar-area" :style="sidebarTransform">
        <div class="sidebar-strip" v-for="i in 3" :key="i" :style="stripStyle(i)">
          <slot :name="`strip-${i}`">
            <slot name="sidebar" v-if="i === 1" />
          </slot>
        </div>
      </div>
      
      <!-- Decorative elements -->
      <div class="magazine-decor">
        <div class="decor-line decor-line-1"></div>
        <div class="decor-line decor-line-2"></div>
        <div class="decor-accent"></div>
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
  variant?: 'left-feature' | 'right-feature' | 'center-feature'
}>(), {
  theme: 'business',
  vibe: 'none',
  variant: 'left-feature'
})

// Vibe configuration
const vibeConfig = computed(() => {
  const configs: Record<string, { rotation: number; translate: number; skew: number }> = {
    none: { rotation: 0, translate: 0, skew: 0 },
    calm: { rotation: 0.3, translate: 4, skew: 0 },
    dynamic: { rotation: 1.5, translate: 10, skew: 1 },
    playful: { rotation: 2, translate: 15, skew: 2 },
    professional: { rotation: 0.2, translate: 2, skew: 0 },
    minimal: { rotation: 0, translate: 0, skew: 0 },
    dramatic: { rotation: 2.5, translate: 12, skew: 1.5 }
  }
  return configs[props.vibe] || configs.none
})

const seededRandom = (seed: number) => {
  const x = Math.sin(seed * 9999) * 10000
  return x - Math.floor(x)
}

const featureTransform = computed(() => {
  const config = vibeConfig.value
  if (config.rotation === 0 && config.translate === 0) return {}
  
  const rotation = (seededRandom(10) - 0.5) * config.rotation
  const translateX = (seededRandom(11) - 0.5) * config.translate
  const translateY = (seededRandom(12) - 0.5) * config.translate
  
  return {
    transform: `rotate(${rotation}deg) translate(${translateX}px, ${translateY}px)`
  }
})

const sidebarTransform = computed(() => {
  const config = vibeConfig.value
  if (config.rotation === 0 && config.skew === 0) return {}
  
  const skew = (seededRandom(20) - 0.5) * config.skew
  
  return {
    transform: `skewY(${skew}deg)`
  }
})

const stripStyle = (index: number) => {
  const config = vibeConfig.value
  const delay = index * 0.1
  const translateX = (seededRandom(30 + index) - 0.5) * config.translate * 0.5
  
  return {
    '--strip-delay': `${delay}s`,
    transform: config.translate > 0 ? `translateX(${translateX}px)` : undefined
  }
}
</script>

<style scoped>
.magazine-layout {
  height: 100%;
  display: grid;
  gap: 1.5rem;
  position: relative;
  padding: 0.5rem;
}

/* Layout variants */
.variant-left-feature {
  grid-template-columns: 2fr 1fr;
}

.variant-right-feature {
  grid-template-columns: 1fr 2fr;
}

.variant-right-feature .feature-area {
  order: 2;
}

.variant-right-feature .sidebar-area {
  order: 1;
}

.variant-center-feature {
  grid-template-columns: 1fr 2fr 1fr;
}

.variant-center-feature .feature-area {
  order: 2;
}

/* Feature area */
.feature-area {
  display: flex;
  flex-direction: column;
  position: relative;
  transition: transform 0.3s ease;
}

.feature-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: var(--c-bg-surface);
  border-radius: 0.75rem;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

.feature-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, var(--c-primary), var(--c-accent));
}

.feature-content :deep(h1) {
  font-size: 3rem;
  font-weight: 800;
  color: var(--c-text-main);
  margin: 0 0 1rem;
  line-height: 1.1;
  font-family: var(--font-family);
}

.feature-content :deep(h2) {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--c-primary);
  margin: 0 0 1rem;
}

.feature-content :deep(p) {
  font-size: 1.25rem;
  color: var(--c-text-muted);
  line-height: 1.7;
  margin: 0;
}

.feature-caption {
  margin-top: 0.75rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 0.25rem;
}

.feature-caption :deep(p) {
  font-size: 0.875rem;
  color: var(--c-text-muted);
  font-style: italic;
  margin: 0;
}

/* Sidebar area */
.sidebar-area {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  transition: transform 0.3s ease;
}

.sidebar-strip {
  flex: 1;
  background: var(--c-bg-surface);
  border-radius: 0.5rem;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease;
  transition-delay: var(--strip-delay, 0s);
}

.sidebar-strip::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 1rem;
  right: 1rem;
  height: 2px;
  background: linear-gradient(to right, var(--c-primary), transparent);
}

.sidebar-strip:last-child::after {
  display: none;
}

.sidebar-strip :deep(h3) {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--c-primary);
  margin: 0 0 0.5rem;
}

.sidebar-strip :deep(p) {
  font-size: 0.9rem;
  color: var(--c-text-muted);
  margin: 0;
  line-height: 1.5;
}

.sidebar-strip :deep(ul) {
  margin: 0;
  padding-left: 1.25rem;
}

.sidebar-strip :deep(li) {
  font-size: 0.9rem;
  color: var(--c-text-muted);
  margin-bottom: 0.25rem;
}

/* Decorative elements */
.magazine-decor {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.decor-line {
  position: absolute;
  background: var(--c-primary);
  opacity: 0.1;
}

.decor-line-1 {
  width: 100%;
  height: 1px;
  top: 20%;
  transform: rotate(-2deg);
}

.decor-line-2 {
  width: 1px;
  height: 100%;
  right: 35%;
  transform: rotate(2deg);
}

.decor-accent {
  position: absolute;
  width: 80px;
  height: 80px;
  border: 2px solid var(--c-accent);
  border-radius: 50%;
  top: -20px;
  right: -20px;
  opacity: 0.15;
}

/* Vibe variations */
.vibe-dramatic .feature-content::before {
  width: 8px;
}

.vibe-dramatic .sidebar-strip {
  border-left: 3px solid var(--c-accent);
}

.vibe-playful .feature-content {
  border-radius: 1.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.vibe-playful .sidebar-strip {
  border-radius: 1rem;
}

.vibe-minimal .magazine-decor {
  display: none;
}

.vibe-minimal .feature-content::before {
  display: none;
}

.vibe-calm .feature-content,
.vibe-calm .sidebar-strip {
  background: linear-gradient(135deg, var(--c-bg-surface), rgba(255, 255, 255, 0.02));
}

.vibe-professional .feature-content {
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.placeholder {
  color: var(--c-text-muted);
  font-style: italic;
}
</style>
