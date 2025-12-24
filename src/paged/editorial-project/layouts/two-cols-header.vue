<!--
  two-cols-header.vue - Editorial Two Columns with Header Layout
  
  Slots:
    - title: Section title header
    - left: Left column content
    - right: Right column content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="two-cols-header">
      <!-- Header section -->
      <div v-if="$slots.title" class="cols-header">
        <div class="header-rule"></div>
        <slot name="title" />
      </div>
      
      <!-- Two columns -->
      <div class="cols-container" :class="`ratio-${ratio}`">
        <div class="col col-left">
          <slot name="left">
            <span class="placeholder">Left column content</span>
          </slot>
        </div>
        
        <div class="col-divider">
          <div class="divider-line"></div>
        </div>
        
        <div class="col col-right">
          <slot name="right">
            <span class="placeholder">Right column content</span>
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
  ratio?: '50-50' | '60-40' | '40-60'
}>(), {
  theme: 'editorial',
  vibe: 'classic',
  ratio: '50-50'
})
</script>

<style scoped>
.two-cols-header {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2rem;
}

/* Header */
.cols-header {
  text-align: center;
}

.header-rule {
  width: 100px;
  height: 1px;
  background: var(--edit-gold);
  margin: 0 auto 1.5rem;
}

.cols-header :deep(h1) {
  font-family: var(--edit-font-display);
  font-size: 2rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0;
}

.cols-header :deep(p) {
  font-family: var(--edit-font-accent);
  font-size: 1rem;
  font-style: italic;
  color: var(--edit-text-light);
  margin-top: 0.5rem;
}

/* Columns container */
.cols-container {
  display: flex;
  gap: 2rem;
  flex: 1;
}

.ratio-50-50 .col-left,
.ratio-50-50 .col-right {
  flex: 1;
}

.ratio-60-40 .col-left { flex: 3; }
.ratio-60-40 .col-right { flex: 2; }

.ratio-40-60 .col-left { flex: 2; }
.ratio-40-60 .col-right { flex: 3; }

/* Column styling */
.col {
  display: flex;
  flex-direction: column;
}

.col :deep(h2) {
  font-family: var(--edit-font-display);
  font-size: 1.5rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0 0 1rem;
}

.col :deep(h3) {
  font-family: var(--edit-font-display);
  font-size: 1.25rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0 0 0.75rem;
}

.col :deep(p) {
  font-family: var(--edit-font-body);
  font-size: 1rem;
  line-height: 1.7;
  color: var(--edit-text);
  margin: 0 0 0.75rem;
}

.col :deep(ul),
.col :deep(ol) {
  font-family: var(--edit-font-body);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--edit-text);
  margin: 0;
  padding-left: 1.25rem;
}

.col :deep(li) {
  margin-bottom: 0.5rem;
}

/* Divider */
.col-divider {
  display: flex;
  align-items: center;
  padding: 0 0.5rem;
}

.divider-line {
  width: 1px;
  height: 100%;
  background: var(--edit-border);
}

.placeholder {
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: var(--edit-text-light);
}

/* Vibe: Modern */
.vibe-modern .header-rule {
  background: var(--edit-charcoal);
}

.vibe-modern .divider-line {
  background: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .cols-header :deep(h1) {
  color: var(--edit-white);
}

.vibe-luxe .col :deep(h2),
.vibe-luxe .col :deep(h3) {
  color: var(--edit-white);
}

.vibe-luxe .divider-line {
  background: rgba(201, 169, 98, 0.3);
}
</style>
