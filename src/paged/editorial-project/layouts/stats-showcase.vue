<!--
  stats-showcase.vue - Editorial Statistics Showcase Layout
  
  Slots:
    - title: Section title
    - stats: Statistics items (4 recommended)
    - footer: Footer note
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="stats-showcase">
      <!-- Title section -->
      <div v-if="$slots.title" class="showcase-header">
        <div class="header-line"></div>
        <slot name="title" />
      </div>
      
      <!-- Stats row -->
      <div class="stats-row">
        <slot name="stats">
          <div class="stat-item">
            <span class="stat-value">100%</span>
            <span class="stat-label">Sample Stat</span>
          </div>
        </slot>
      </div>
      
      <!-- Footer -->
      <div v-if="$slots.footer" class="showcase-footer">
        <div class="footer-line"></div>
        <slot name="footer" />
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
}>(), {
  theme: 'editorial',
  vibe: 'classic'
})
</script>

<style scoped>
.stats-showcase {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3rem;
  padding: 2rem;
}

/* Header */
.showcase-header {
  text-align: center;
}

.header-line {
  width: 80px;
  height: 1px;
  background: var(--edit-gold);
  margin: 0 auto 1.5rem;
}

.showcase-header :deep(h1),
.showcase-header :deep(h2) {
  font-family: var(--edit-font-display);
  font-size: 2rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0;
}

.showcase-header :deep(p) {
  font-family: var(--edit-font-accent);
  font-style: italic;
  font-size: 1rem;
  color: var(--edit-text-light);
  margin-top: 0.5rem;
}

/* Stats row */
.stats-row {
  display: flex;
  gap: 4rem;
  justify-content: center;
  flex-wrap: wrap;
}

.stats-row :deep(.stat-item) {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  min-width: 140px;
}

.stats-row :deep(.stat-value) {
  font-family: var(--edit-font-display);
  font-size: 3.5rem;
  font-weight: 400;
  color: var(--edit-gold);
  line-height: 1;
}

.stats-row :deep(.stat-label) {
  font-family: var(--edit-font-accent);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--edit-text);
  text-align: center;
}

.stats-row :deep(.stat-sublabel) {
  font-family: var(--edit-font-body);
  font-size: 0.85rem;
  font-style: italic;
  color: var(--edit-text-light);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.stat-value {
  font-family: var(--edit-font-display);
  font-size: 3rem;
  color: var(--edit-gold);
}

.stat-label {
  font-family: var(--edit-font-accent);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--edit-text);
}

/* Footer */
.showcase-footer {
  text-align: center;
}

.footer-line {
  width: 60px;
  height: 1px;
  background: var(--edit-border);
  margin: 0 auto 1rem;
}

.showcase-footer :deep(p) {
  font-family: var(--edit-font-body);
  font-size: 0.9rem;
  color: var(--edit-text-light);
  font-style: italic;
}

/* Vibe: Modern */
.vibe-modern .header-line,
.vibe-modern .footer-line {
  background: var(--edit-charcoal);
}

.vibe-modern .stats-row :deep(.stat-value) {
  color: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .showcase-header :deep(h1),
.vibe-luxe .showcase-header :deep(h2) {
  color: var(--edit-white);
}
</style>
