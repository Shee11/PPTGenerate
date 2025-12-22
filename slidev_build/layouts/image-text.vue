<!--
  image-text.vue - Elegant Image + Text Split Layout
  
  Purpose: Professional image and text combination with multiple arrangement options
  Perfect for product showcases, team introductions, or visual storytelling
  
  Props:
    - theme: Theme name (business, cyber, minimal, academic, creative, dark)
    - vibe: Vibe name (none, calm, dynamic, playful, professional, minimal, dramatic)
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
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="3" y="3" width="18" height="18" rx="2"/>
                  <circle cx="8.5" cy="8.5" r="1.5"/>
                  <path d="M21 15l-5-5L5 21"/>
                </svg>
              </div>
            </slot>
          </div>
          <div v-if="$slots.caption" class="image-caption">
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
      
      <!-- Decorative elements -->
      <div class="layout-decorations">
        <div class="decoration-corner decoration-corner-tl"></div>
        <div class="decoration-corner decoration-corner-br"></div>
        <div class="decoration-line"></div>
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
  theme: 'business',
  vibe: 'none',
  imagePosition: 'left',
  imageSize: 'medium',
  imageStyle: 'rounded'
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
    dramatic: { rotation: 2, translate: 10, scale: 0.02 }
  }
  return configs[props.vibe] || configs.none
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
  padding: 0.5rem;
}

/* Position variants */
.position-left {
  grid-template-columns: var(--image-ratio) 1fr;
}

.position-right {
  grid-template-columns: 1fr var(--image-ratio);
}

.position-right .image-area {
  order: 2;
}

.position-top {
  grid-template-rows: var(--image-ratio) 1fr;
  grid-template-columns: 1fr;
}

.position-bottom {
  grid-template-rows: 1fr var(--image-ratio);
  grid-template-columns: 1fr;
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
  transition: transform 0.3s ease;
}

.image-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.image-frame {
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: var(--c-bg-surface);
}

.image-frame :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--c-text-muted);
  opacity: 0.3;
}

.image-placeholder svg {
  width: 80px;
  height: 80px;
}

.image-caption {
  padding: 0.75rem;
  text-align: center;
}

.image-caption :deep(p) {
  font-size: 0.875rem;
  color: var(--c-text-muted);
  font-style: italic;
  margin: 0;
}

/* Image style variants */
.image-rounded .image-frame {
  border-radius: 1rem;
}

.image-square .image-frame {
  border-radius: 0;
}

.image-circle .image-frame {
  border-radius: 50%;
  aspect-ratio: 1;
}

.image-blob .image-frame {
  border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
}

/* Content area */
.content-area {
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;
}

.content-wrapper {
  width: 100%;
}

.content-wrapper :deep(h1) {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--c-text-main);
  margin: 0 0 1rem;
  font-family: var(--font-family);
}

.content-wrapper :deep(h2) {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--c-primary);
  margin: 0 0 1rem;
}

.content-wrapper :deep(h3) {
  font-size: 1.25rem;
  font-weight: 500;
  color: var(--c-accent);
  margin: 0 0 0.75rem;
}

.content-wrapper :deep(p) {
  font-size: 1.125rem;
  color: var(--c-text-muted);
  line-height: 1.7;
  margin: 0 0 1rem;
}

.content-wrapper :deep(ul),
.content-wrapper :deep(ol) {
  margin: 0 0 1rem;
  padding-left: 1.5rem;
}

.content-wrapper :deep(li) {
  font-size: 1.125rem;
  color: var(--c-text-main);
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.content-wrapper :deep(li::marker) {
  color: var(--c-accent);
}

/* Decorative elements */
.layout-decorations {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.decoration-corner {
  position: absolute;
  width: 60px;
  height: 60px;
  border: 2px solid var(--c-primary);
  opacity: 0.1;
}

.decoration-corner-tl {
  top: 0;
  left: 0;
  border-right: none;
  border-bottom: none;
}

.decoration-corner-br {
  bottom: 0;
  right: 0;
  border-left: none;
  border-top: none;
}

.decoration-line {
  position: absolute;
  width: 100px;
  height: 3px;
  background: linear-gradient(to right, var(--c-accent), transparent);
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0.2;
}

/* Vibe variations */
.vibe-dramatic .image-frame {
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

.vibe-dramatic .decoration-corner {
  opacity: 0.3;
  border-width: 3px;
}

.vibe-playful .image-frame {
  transform: rotate(2deg);
  transition: transform 0.3s ease;
}

.vibe-playful .image-area:hover .image-frame {
  transform: rotate(-1deg) scale(1.02);
}

.vibe-playful .decoration-corner {
  border-radius: 50%;
  width: 40px;
  height: 40px;
  background: var(--c-accent);
  border: none;
  opacity: 0.2;
}

.vibe-minimal .layout-decorations {
  display: none;
}

.vibe-minimal .image-frame {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.vibe-calm .image-frame {
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.vibe-professional .image-frame {
  border: 2px solid var(--c-primary);
}

.vibe-professional .content-wrapper {
  border-left: 3px solid var(--c-primary);
  padding-left: 1.5rem;
}

.vibe-dynamic .image-frame {
  animation: subtle-float 4s ease-in-out infinite;
}

@keyframes subtle-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
</style>
