<!--
  feature-grid.vue - Editorial Feature Grid Layout
  
  Slots:
    - title: Section title
    - features: Feature items (grid of 4-6)
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="feature-grid">
      <!-- Title -->
      <div v-if="$slots.title" class="feature-header">
        <div class="header-decor">
          <span class="decor-line"></span>
          <span class="decor-diamond">◇</span>
          <span class="decor-line"></span>
        </div>
        <slot name="title" />
      </div>
      
      <!-- Features grid -->
      <div class="features-container">
        <slot name="features">
          <div class="feature-item">
            <span class="feature-icon">✦</span>
            <h3>Feature Title</h3>
            <p>Feature description goes here.</p>
          </div>
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
}>(), {
  theme: 'editorial',
  vibe: 'classic'
})
</script>

<style scoped>
.feature-grid {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2rem;
}

/* Header */
.feature-header {
  text-align: center;
}

.header-decor {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.decor-line {
  width: 50px;
  height: 1px;
  background: var(--edit-gold);
}

.decor-diamond {
  color: var(--edit-gold);
  font-size: 0.75rem;
}

.feature-header :deep(h1),
.feature-header :deep(h2) {
  font-family: var(--edit-font-display);
  font-size: 2rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0;
}

.feature-header :deep(p) {
  font-family: var(--edit-font-body);
  font-size: 1rem;
  color: var(--edit-text-light);
  margin-top: 0.5rem;
}

/* Features container */
.features-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  flex: 1;
  align-content: center;
}

/* Feature item */
.features-container :deep(.feature-item) {
  text-align: center;
  padding: 1.5rem;
}

.features-container :deep(.feature-icon) {
  font-size: 1.5rem;
  color: var(--edit-gold);
  display: block;
  margin-bottom: 1rem;
}

.features-container :deep(.feature-item h3) {
  font-family: var(--edit-font-display);
  font-size: 1.2rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0 0 0.5rem;
}

.features-container :deep(.feature-item p) {
  font-family: var(--edit-font-body);
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--edit-text);
  margin: 0;
}

.features-container :deep(.feature-divider) {
  width: 30px;
  height: 1px;
  background: var(--edit-border);
  margin: 0.75rem auto;
}

.feature-item {
  text-align: center;
}

.feature-icon {
  color: var(--edit-gold);
  font-size: 1.25rem;
}

/* Vibe: Modern */
.vibe-modern .header-decor {
  display: none;
}

.vibe-modern .features-container :deep(.feature-icon) {
  color: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .feature-header :deep(h1),
.vibe-luxe .feature-header :deep(h2) {
  color: var(--edit-white);
}

.vibe-luxe .features-container :deep(.feature-item h3) {
  color: var(--edit-white);
}

/* Vibe: Warm */
.vibe-warm .decor-line {
  background: var(--edit-burgundy);
}

.vibe-warm .features-container :deep(.feature-icon) {
  color: var(--edit-burgundy);
}
</style>
