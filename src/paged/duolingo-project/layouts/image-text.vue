<!--
  image-text.vue - Duolingo Image + Text Split Layout
  
  Purpose: Playful image and text combination with colorful Duolingo styling
  Perfect for product showcases, character introductions, or visual storytelling
  
  Props:
    - theme: Theme name (default: duolingo)
    - vibe: Vibe modifier (minimal, clean, balanced, playful, expressive)
    - header: Header text
    - footer: Footer text
    - imagePosition: Image placement (left, right, top, bottom)
    - imageSize: Image area ratio (small, medium, large)
    - imageStyle: Image presentation (rounded, square, circle, blob)
  
  Slots:
    - image: Image content area
    - content: Text content area
    - caption: Optional image caption
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="image-text-layout" :class="[
      `position-${imagePosition}`,
      `size-${imageSize}`,
      `image-${imageStyle}`,
      `vibe-${vibe}`
    ]">
      <!-- Image area -->
      <div class="image-area" :style="imageTransform">
        <div class="image-wrapper">
          <div class="image-frame">
            <slot name="image">
              <div class="image-placeholder">
                <span class="placeholder-icon">🖼️</span>
                <span class="placeholder-text">Add image</span>
              </div>
            </slot>
          </div>
          <div v-if="$slots.caption" class="image-caption">
            <span class="caption-icon">📸</span>
            <slot name="caption" />
          </div>
        </div>
      </div>
      
      <!-- Content area -->
      <div class="content-area" :style="contentTransform">
        <div class="content-wrapper">
          <slot name="content">
            <p>Add your content here</p>
          </slot>
        </div>
      </div>
      
      <!-- Duolingo decorative elements -->
      <div class="layout-decorations">
        <div class="decoration-owl">🦉</div>
        <div class="decoration-dots">
          <span v-for="i in 5" :key="i" class="dot" :style="{ '--dot-index': i }"></span>
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
  imagePosition?: 'left' | 'right' | 'top' | 'bottom'
  imageSize?: 'small' | 'medium' | 'large'
  imageStyle?: 'rounded' | 'square' | 'circle' | 'blob'
}>(), {
  theme: 'duolingo',
  vibe: 'balanced',
  imagePosition: 'left',
  imageSize: 'medium',
  imageStyle: 'rounded'
})

// Vibe configuration - Duolingo playful values
const vibeConfig = computed(() => {
  const configs: Record<string, { rotation: number; translate: number; scale: number }> = {
    minimal: { rotation: 0, translate: 0, scale: 0 },
    clean: { rotation: 0.5, translate: 4, scale: 0.01 },
    balanced: { rotation: 1, translate: 8, scale: 0.02 },
    playful: { rotation: 2.5, translate: 15, scale: 0.03 },
    expressive: { rotation: 4, translate: 20, scale: 0.04 }
  }
  return configs[props.vibe] || configs.balanced
})

const seededRandom = (seed: number) => {
  const x = Math.sin(seed * 9999) * 10000
  return x - Math.floor(x)
}

const imageTransform = computed(() => {
  const config = vibeConfig.value
  if (config.rotation === 0 && config.translate === 0) return {}
  
  const rotation = (seededRandom(100) - 0.5) * config.rotation
  const translateX = (seededRandom(101) - 0.5) * config.translate
  const translateY = (seededRandom(102) - 0.5) * config.translate
  
  return {
    transform: `rotate(${rotation}deg) translate(${translateX}px, ${translateY}px)`
  }
})

const contentTransform = computed(() => {
  const config = vibeConfig.value
  if (config.rotation === 0 && config.translate === 0) return {}
  
  const rotation = (seededRandom(200) - 0.5) * config.rotation * 0.5
  const translateY = (seededRandom(201) - 0.5) * config.translate * 0.5
  
  return {
    transform: `rotate(${rotation}deg) translateY(${translateY}px)`
  }
})
</script>

<style scoped>
.image-text-layout {
  height: 100%;
  display: grid;
  gap: 2rem;
  position: relative;
  padding: 1rem;
}

/* Position variants */
.position-left {
  grid-template-columns: var(--image-ratio, 45%) 1fr;
}

.position-right {
  grid-template-columns: 1fr var(--image-ratio, 45%);
}

.position-right .image-area {
  order: 2;
}

.position-right .content-area {
  order: 1;
}

.position-top {
  grid-template-columns: 1fr;
  grid-template-rows: var(--image-ratio, 45%) 1fr;
}

.position-bottom {
  grid-template-columns: 1fr;
  grid-template-rows: 1fr var(--image-ratio, 45%);
}

.position-bottom .image-area {
  order: 2;
}

/* Size variants */
.size-small { --image-ratio: 35%; }
.size-medium { --image-ratio: 45%; }
.size-large { --image-ratio: 55%; }

/* Image area */
.image-area {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.image-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.image-frame {
  flex: 1;
  background: white;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 
    0 4px 0 var(--duo-green-dark, #46a302),
    0 8px 20px rgba(88, 204, 2, 0.2);
  border: 3px solid var(--duo-green, #58CC02);
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-frame :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: var(--duo-gray, #AFAFAF);
  padding: 2rem;
}

.placeholder-icon {
  font-size: 3rem;
  opacity: 0.6;
}

.placeholder-text {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 1rem;
  font-weight: 700;
}

/* Image style variants */
.image-rounded .image-frame {
  border-radius: 24px;
}

.image-square .image-frame {
  border-radius: 8px;
}

.image-circle .image-frame {
  border-radius: 50%;
  aspect-ratio: 1;
  max-width: min(100%, 100%);
}

.image-blob .image-frame {
  border-radius: 60% 40% 50% 50% / 50% 50% 40% 60%;
  animation: blob-morph 8s ease-in-out infinite;
}

@keyframes blob-morph {
  0%, 100% { border-radius: 60% 40% 50% 50% / 50% 50% 40% 60%; }
  25% { border-radius: 50% 60% 40% 50% / 40% 50% 60% 50%; }
  50% { border-radius: 40% 50% 60% 50% / 60% 40% 50% 50%; }
  75% { border-radius: 50% 50% 50% 60% / 50% 60% 40% 40%; }
}

/* Caption */
.image-caption {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--duo-gray-dark, #777);
  background: var(--duo-gray-light, #F7F7F7);
  padding: 0.5rem 1rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.caption-icon {
  font-size: 1rem;
}

/* Content area */
.content-area {
  display: flex;
  align-items: center;
  padding: 1rem;
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.content-wrapper {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 
    0 4px 0 var(--duo-blue-dark, #1899D6),
    0 8px 20px rgba(28, 176, 246, 0.15);
  border: 3px solid var(--duo-blue, #1CB0F6);
  width: 100%;
}

.content-wrapper :deep(h1),
.content-wrapper :deep(h2),
.content-wrapper :deep(h3) {
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
  font-weight: 800;
  color: var(--duo-text, #4B4B4B);
  margin-bottom: 1rem;
}

.content-wrapper :deep(h1) { font-size: 2.5rem; }
.content-wrapper :deep(h2) { font-size: 2rem; }
.content-wrapper :deep(h3) { font-size: 1.5rem; }

.content-wrapper :deep(p) {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 1.125rem;
  line-height: 1.7;
  color: var(--duo-text, #4B4B4B);
  margin-bottom: 0.75rem;
}

.content-wrapper :deep(ul),
.content-wrapper :deep(ol) {
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}

.content-wrapper :deep(li) {
  font-family: var(--duo-font, 'Nunito', sans-serif);
  font-size: 1.125rem;
  line-height: 1.6;
  color: var(--duo-text, #4B4B4B);
  margin-bottom: 0.5rem;
}

/* Decorative elements */
.layout-decorations {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: -1;
}

.decoration-owl {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  font-size: 2rem;
  opacity: 0.3;
  animation: owl-bounce 2s ease-in-out infinite;
}

@keyframes owl-bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.decoration-dots {
  position: absolute;
  top: 2rem;
  right: 2rem;
  display: flex;
  gap: 0.5rem;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--duo-green, #58CC02);
  opacity: 0.3;
  animation: dot-pulse 1.5s ease-in-out infinite;
  animation-delay: calc(var(--dot-index) * 0.15s);
}

@keyframes dot-pulse {
  0%, 100% { transform: scale(1); opacity: 0.3; }
  50% { transform: scale(1.2); opacity: 0.6; }
}

/* Vibe modifiers */
.vibe-minimal .layout-decorations {
  display: none;
}

.vibe-clean .decoration-owl {
  display: none;
}

.vibe-playful .decoration-owl {
  opacity: 0.5;
  font-size: 2.5rem;
}

.vibe-expressive .decoration-owl {
  opacity: 0.7;
  font-size: 3rem;
}

.vibe-expressive .dot {
  width: 12px;
  height: 12px;
}
</style>
