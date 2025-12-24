<!--
  default.vue - Editorial Default Layout
  
  Slots:
    - default: General content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="default-layout">
      <slot>
        <span class="placeholder">Slide content...</span>
      </slot>
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
}>(), {
  theme: 'editorial',
  vibe: 'classic'
})
</script>

<style scoped>
.default-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 2rem;
}

/* Typography */
.default-layout :deep(h1) {
  font-family: var(--edit-font-display);
  font-size: 2.5rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  line-height: 1.2;
  margin: 0 0 1rem;
}

.default-layout :deep(h2) {
  font-family: var(--edit-font-display);
  font-size: 1.75rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0 0 0.75rem;
}

.default-layout :deep(h3) {
  font-family: var(--edit-font-display);
  font-size: 1.25rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0 0 0.5rem;
}

.default-layout :deep(p) {
  font-family: var(--edit-font-body);
  font-size: 1rem;
  line-height: 1.8;
  color: var(--edit-text);
  margin: 0 0 0.75rem;
}

.default-layout :deep(ul),
.default-layout :deep(ol) {
  font-family: var(--edit-font-body);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--edit-text);
  padding-left: 1.5rem;
  margin: 0 0 0.75rem;
}

.default-layout :deep(li) {
  margin-bottom: 0.5rem;
}

.default-layout :deep(li::marker) {
  color: var(--edit-gold);
}

.default-layout :deep(blockquote) {
  font-family: var(--edit-font-accent);
  font-style: italic;
  font-size: 1.1rem;
  color: var(--edit-text-dark);
  padding-left: 1.5rem;
  border-left: 2px solid var(--edit-gold);
  margin: 1rem 0;
}

.default-layout :deep(a) {
  color: var(--edit-gold);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s;
}

.default-layout :deep(a:hover) {
  border-bottom-color: var(--edit-gold);
}

.default-layout :deep(code) {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9em;
  background: var(--edit-light);
  padding: 0.2em 0.4em;
  border-radius: 2px;
}

.default-layout :deep(strong) {
  font-weight: 600;
  color: var(--edit-text-dark);
}

.default-layout :deep(em) {
  font-style: italic;
}

.placeholder {
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: var(--edit-text-light);
}

/* Vibe: Luxe */
.vibe-luxe .default-layout :deep(h1),
.vibe-luxe .default-layout :deep(h2),
.vibe-luxe .default-layout :deep(h3) {
  color: var(--edit-white);
}

.vibe-luxe .default-layout :deep(code) {
  background: rgba(255, 255, 255, 0.1);
}
</style>
