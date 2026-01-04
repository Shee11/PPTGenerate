<!--
  full-bleed.vue - Editorial Full Bleed Photography Layout
  
  Slots:
    - background: Background image
    - content: Overlay content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :dark="true">
    <div class="full-bleed" :class="`overlay-${overlay}`">
      <!-- Background image -->
      <div class="bleed-bg">
        <slot name="background">
          <div class="bg-placeholder"></div>
        </slot>
      </div>
      
      <!-- Overlay -->
      <div class="bleed-overlay"></div>
      
      <!-- Content -->
      <div class="bleed-content" :class="`position-${contentPosition}`">
        <div class="content-inner">
          <slot name="content">
            <span class="placeholder">Content overlay</span>
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
  overlay?: 'dark' | 'light' | 'gradient' | 'none'
  contentPosition?: 'center' | 'bottom' | 'left' | 'right'
}>(), {
  theme: 'editorial',
  vibe: 'classic',
  overlay: 'gradient',
  contentPosition: 'center'
})
</script>

<style scoped>
.full-bleed {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

/* Background */
.bleed-bg {
  position: absolute;
  inset: 0;
}

.bleed-bg :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.bg-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--edit-charcoal) 0%, var(--edit-slate) 100%);
}

/* Overlay */
.bleed-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.overlay-dark .bleed-overlay {
  background: rgba(0, 0, 0, 0.5);
}

.overlay-light .bleed-overlay {
  background: rgba(255, 255, 255, 0.3);
}

.overlay-gradient .bleed-overlay {
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7) 0%, transparent 60%);
}

.overlay-none .bleed-overlay {
  display: none;
}

/* Content */
.bleed-content {
  position: absolute;
  inset: 0;
  display: flex;
  padding: 3rem;
  z-index: 2;
}

.position-center {
  align-items: center;
  justify-content: center;
  text-align: center;
}

.position-bottom {
  align-items: flex-end;
  justify-content: center;
  text-align: center;
}

.position-left {
  align-items: center;
  justify-content: flex-start;
}

.position-right {
  align-items: center;
  justify-content: flex-end;
}

.content-inner {
  max-width: 700px;
}

.content-inner :deep(h1) {
  font-family: var(--edit-font-display);
  font-size: 3.5rem;
  font-weight: 400;
  color: var(--edit-white);
  line-height: 1.15;
  margin-bottom: 1rem;
}

.content-inner :deep(h2) {
  font-family: var(--edit-font-display);
  font-size: 2rem;
  font-weight: 400;
  color: var(--edit-white);
  margin-bottom: 0.75rem;
}

.content-inner :deep(p) {
  font-family: var(--edit-font-body);
  font-size: 1.2rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.9);
}

.content-inner :deep(.category) {
  font-family: var(--edit-font-accent);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--edit-gold);
  margin-bottom: 1rem;
}

.placeholder {
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: rgba(255, 255, 255, 0.7);
}
</style>
