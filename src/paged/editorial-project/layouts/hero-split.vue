<!--
  hero-split.vue - Editorial Hero Split Layout
  
  Slots:
    - left: Left panel content
    - right: Right panel content (often image)
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="hero-split" :class="`split-${imagePosition}`">
      <!-- Text side -->
      <div class="split-text">
        <div class="text-inner">
          <slot name="left">
            <span class="placeholder">Editorial content</span>
          </slot>
        </div>
      </div>
      
      <!-- Divider -->
      <div class="split-divider">
        <div class="divider-line"></div>
      </div>
      
      <!-- Image side -->
      <div class="split-image">
        <div class="image-inner">
          <slot name="right">
            <div class="image-placeholder">
              <span>Image</span>
            </div>
          </slot>
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<script setup lang="ts">
import SlideShell from './SlideShell.vue'

withDefaults(defineProps<{
  theme?: string
  vibe?: string
  header?: string
  footer?: string
  dark?: boolean
  imagePosition?: 'left' | 'right'
}>(), {
  theme: 'editorial',
  vibe: 'classic',
  imagePosition: 'right'
})
</script>

<style scoped>
.hero-split {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 2rem;
  align-items: center;
}

.split-left {
  direction: rtl;
}

.split-left > * {
  direction: ltr;
}

/* Text side */
.split-text {
  display: flex;
  align-items: center;
}

.text-inner {
  width: 100%;
}

.text-inner :deep(h1) {
  font-family: var(--edit-font-display);
  font-size: 2.8rem;
  font-weight: 400;
  line-height: 1.15;
  color: var(--edit-text-dark);
  margin-bottom: 1rem;
}

.text-inner :deep(h2) {
  font-family: var(--edit-font-display);
  font-size: 1.8rem;
  font-weight: 400;
  color: var(--edit-text);
  margin-bottom: 0.75rem;
}

.text-inner :deep(p) {
  font-family: var(--edit-font-body);
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--edit-text);
  margin-bottom: 1rem;
}

.text-inner :deep(.category) {
  font-family: var(--edit-font-accent);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--edit-gold);
  margin-bottom: 1rem;
}

/* Divider */
.split-divider {
  display: flex;
  align-items: center;
  padding: 2rem 0;
}

.divider-line {
  width: 1px;
  height: 100%;
  max-height: 300px;
  background: var(--edit-light);
}

/* Image side */
.split-image {
  height: 100%;
  display: flex;
  align-items: center;
}

.image-inner {
  width: 100%;
  height: 100%;
  max-height: 400px;
}

.image-inner :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 300px;
  background: var(--edit-cream);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: var(--edit-text-light);
}

.placeholder {
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: var(--edit-text-light);
}

/* Vibe: Modern */
.vibe-modern .divider-line {
  background: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .text-inner :deep(h1) {
  color: var(--edit-white);
}

.vibe-luxe .divider-line {
  background: var(--edit-gold);
}
</style>
