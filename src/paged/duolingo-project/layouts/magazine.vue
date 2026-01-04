<!--
  magazine.vue - Duolingo Editorial Magazine Layout
  
  Purpose: Playful editorial design with Duolingo's colorful styling
  Features large featured area with sidebar content strips
  
  Props:
    - theme: Theme name (default: duolingo)
    - vibe: Vibe modifier (minimal, clean, balanced, playful, expressive)
    - header: Header text
    - footer: Footer text
    - variant: Layout variant (left-feature, right-feature, center-feature)
  
  Slots:
    - feature: Main featured content (large area)
    - sidebar: Sidebar content strips
    - caption: Optional caption for featured content
    - strip-1, strip-2, strip-3: Individual sidebar strips
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="magazine-layout" :class="[`variant-${variant}`, `vibe-${vibe}`]">
      <!-- Feature area -->
      <div class="feature-area" :style="featureTransform">
        <div class="feature-content">
          <slot name="feature">
            <div class="placeholder">
              <span class="placeholder-icon">⭐</span>
              <span class="placeholder-text">Featured Content</span>
            </div>
          </slot>
        </div>
        <div v-if="$slots.caption" class="feature-caption">
          <slot name="caption" />
        </div>
      </div>
      
      <!-- Sidebar strips -->
      <div class="sidebar-area" :style="sidebarTransform">
        <div 
          class="sidebar-strip" 
          v-for="i in 3" 
          :key="i" 
          :style="stripStyle(i)"
          :class="`strip-${i}`"
        >
          <slot :name="`strip-${i}`">
            <slot name="sidebar" v-if="i === 1" />
          </slot>
        </div>
      </div>
      
      <!-- Duolingo decorative elements -->
      <div class="magazine-decor">
        <div class="decor-badge">📖</div>
        <div class="decor-streak">
          <span v-for="i in 3" :key="i" class="streak-flame" :style="{ '--flame-index': i }">🔥</span>
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
  variant?: 'left-feature' | 'right-feature' | 'center-feature'
}>(), {
  theme: 'duolingo',
  vibe: 'balanced',
  variant: 'left-feature'
})

// Duolingo accent colors for strips
const stripColors = ['#58CC02', '#1CB0F6', '#FF9600']

// Vibe configuration
const vibeConfig = computed(() => {
  const configs: Record<string, { rotation: number; translate: number; skew: number }> = {
    minimal: { rotation: 0, translate: 0, skew: 0 },
    clean: { rotation: 0.3, translate: 4, skew: 0 },
    balanced: { rotation: 0.8, translate: 8, skew: 0.5 },
    playful: { rotation: 2, translate: 15, skew: 2 },
    expressive: { rotation: 3, translate: 20, skew: 3 }
  }
  return configs[props.vibe] || configs.balanced
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
  const color = stripColors[index - 1] || stripColors[0]
  
  return {
    '--strip-delay': `${delay}s`,
    '--strip-color': color,
    '--strip-shadow': color + '40',
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
  padding: 1rem;
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

.variant-center-feature .sidebar-area {
  display: contents;
}

/* Feature area */
.feature-area {
  background: white;
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 
    0 6px 0 var(--duo-green-dark, #46a302),
    0 12px 30px rgba(88, 204, 2, 0.2);
  border: 4px solid var(--duo-green, #58CC02);
  display: flex;
  flex-direction: column;
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.feature-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.feature-content :deep(h1),
.feature-content :deep(h2) {
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
  font-weight: 800;
  color: var(--duo-text, #4B4B4B);
  margin-bottom: 1rem;
}

.feature-content :deep(h1) { font-size: 2.5rem; }
.feature-content :deep(h2) { font-size: 2rem; }

.feature-content :deep(p) {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 1.25rem;
  line-height: 1.7;
  color: var(--duo-text, #4B4B4B);
}

.feature-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 16px;
}

.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: var(--duo-gray, #AFAFAF);
  padding: 3rem;
}

.placeholder-icon {
  font-size: 4rem;
  opacity: 0.5;
}

.placeholder-text {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 1.25rem;
  font-weight: 700;
}

.feature-caption {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 2px dashed var(--duo-gray-light, #E5E5E5);
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--duo-gray-dark, #777);
}

/* Sidebar area */
.sidebar-area {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.sidebar-strip {
  flex: 1;
  background: white;
  border-radius: 16px;
  padding: 1.25rem;
  border-left: 5px solid var(--strip-color, var(--duo-blue, #1CB0F6));
  box-shadow: 
    0 4px 0 var(--strip-shadow, rgba(28, 176, 246, 0.3)),
    0 8px 16px var(--strip-shadow, rgba(28, 176, 246, 0.1));
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  animation: strip-enter 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
  animation-delay: var(--strip-delay, 0s);
}

@keyframes strip-enter {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
}

.sidebar-strip:hover {
  transform: translateX(-4px) scale(1.02);
}

.sidebar-strip :deep(h3),
.sidebar-strip :deep(h4) {
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
  font-weight: 800;
  color: var(--duo-text, #4B4B4B);
  margin-bottom: 0.5rem;
}

.sidebar-strip :deep(h3) { font-size: 1.25rem; }
.sidebar-strip :deep(h4) { font-size: 1rem; }

.sidebar-strip :deep(p) {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 0.95rem;
  line-height: 1.5;
  color: var(--duo-text, #4B4B4B);
}

/* Individual strip colors */
.strip-1 {
  --strip-color: var(--duo-green, #58CC02);
  --strip-shadow: rgba(88, 204, 2, 0.25);
}

.strip-2 {
  --strip-color: var(--duo-blue, #1CB0F6);
  --strip-shadow: rgba(28, 176, 246, 0.25);
}

.strip-3 {
  --strip-color: var(--duo-orange, #FF9600);
  --strip-shadow: rgba(255, 150, 0, 0.25);
}

/* Decorative elements */
.magazine-decor {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: -1;
}

.decor-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  font-size: 2rem;
  opacity: 0.3;
  animation: badge-float 3s ease-in-out infinite;
}

@keyframes badge-float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(5deg); }
}

.decor-streak {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  display: flex;
  gap: 0.25rem;
}

.streak-flame {
  font-size: 1.5rem;
  opacity: 0.3;
  animation: flame-dance 1s ease-in-out infinite;
  animation-delay: calc(var(--flame-index) * 0.15s);
}

@keyframes flame-dance {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-5px) scale(1.1); }
}

/* Vibe modifiers */
.vibe-minimal .magazine-decor {
  display: none;
}

.vibe-minimal .sidebar-strip {
  border-left-width: 3px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.vibe-clean .magazine-decor {
  opacity: 0.2;
}

.vibe-playful .streak-flame {
  opacity: 0.5;
  font-size: 2rem;
}

.vibe-expressive .decor-badge {
  opacity: 0.5;
  font-size: 2.5rem;
}

.vibe-expressive .streak-flame {
  opacity: 0.6;
  font-size: 2.5rem;
}
</style>
