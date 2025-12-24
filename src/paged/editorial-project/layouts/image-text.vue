<!--
  image-text.vue - Editorial Image and Text Layout
  
  Slots:
    - image: Image content
    - content: Text content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="image-text" :class="[`layout-${imagePosition}`, { 'framed': frameImage }]">
      <!-- Image side -->
      <div class="image-side">
        <div class="image-frame">
          <slot name="image">
            <div class="image-placeholder"></div>
          </slot>
        </div>
        <div v-if="$slots.caption" class="image-caption">
          <slot name="caption" />
        </div>
      </div>
      
      <!-- Text side -->
      <div class="text-side">
        <slot name="content">
          <span class="placeholder">Text content here...</span>
        </slot>
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
  frameImage?: boolean
}>(), {
  theme: 'editorial',
  vibe: 'classic',
  imagePosition: 'left',
  frameImage: true
})
</script>

<style scoped>
.image-text {
  height: 100%;
  display: flex;
  gap: 3rem;
  padding: 2rem;
}

/* Layout variants */
.layout-left {
  flex-direction: row;
}

.layout-right {
  flex-direction: row-reverse;
}

/* Image side */
.image-side {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem;
}

.image-frame {
  position: relative;
}

.framed .image-frame {
  padding: 8px;
  border: 1px solid var(--edit-border);
}

.framed .image-frame::before {
  content: '';
  position: absolute;
  top: 4px;
  left: 4px;
  right: -4px;
  bottom: -4px;
  border: 1px solid var(--edit-gold);
  opacity: 0.5;
  pointer-events: none;
}

.image-frame :deep(img) {
  width: 100%;
  height: auto;
  max-height: 400px;
  object-fit: cover;
  display: block;
}

.image-placeholder {
  width: 100%;
  height: 300px;
  background: linear-gradient(135deg, var(--edit-light) 0%, var(--edit-muted) 100%);
}

.image-caption {
  font-family: var(--edit-font-accent);
  font-size: 0.85rem;
  font-style: italic;
  color: var(--edit-text-light);
  padding-left: 8px;
  border-left: 2px solid var(--edit-gold);
}

/* Text side */
.text-side {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.text-side :deep(h1) {
  font-family: var(--edit-font-display);
  font-size: 2.25rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  line-height: 1.25;
  margin: 0 0 1rem;
}

.text-side :deep(h2) {
  font-family: var(--edit-font-display);
  font-size: 1.5rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0 0 0.75rem;
}

.text-side :deep(.category) {
  font-family: var(--edit-font-accent);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--edit-gold);
  margin-bottom: 1rem;
}

.text-side :deep(p) {
  font-family: var(--edit-font-body);
  font-size: 1rem;
  line-height: 1.8;
  color: var(--edit-text);
  margin: 0 0 0.75rem;
}

.text-side :deep(p.lead) {
  font-size: 1.15rem;
  color: var(--edit-text-dark);
}

.text-side :deep(blockquote) {
  font-family: var(--edit-font-accent);
  font-style: italic;
  font-size: 1.1rem;
  color: var(--edit-text-dark);
  padding-left: 1.5rem;
  border-left: 2px solid var(--edit-gold);
  margin: 1rem 0;
}

.placeholder {
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: var(--edit-text-light);
}

/* Vibe: Modern */
.vibe-modern.framed .image-frame {
  border-color: var(--edit-charcoal);
}

.vibe-modern.framed .image-frame::before {
  display: none;
}

.vibe-modern .image-caption {
  border-color: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .text-side :deep(h1),
.vibe-luxe .text-side :deep(h2) {
  color: var(--edit-white);
}

.vibe-luxe.framed .image-frame {
  border-color: rgba(201, 169, 98, 0.3);
}
</style>
