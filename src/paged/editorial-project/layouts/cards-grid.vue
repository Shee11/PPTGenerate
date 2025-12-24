<!--
  cards-grid.vue - Editorial Cards Grid Layout
  
  Slots:
    - title: Section title
    - cards: Grid cards (3 recommended)
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="cards-grid">
      <!-- Title -->
      <div v-if="$slots.title" class="grid-header">
        <slot name="title" />
        <div class="header-ornament">✦</div>
      </div>
      
      <!-- Cards -->
      <div class="grid-container" :class="`cols-${columns}`">
        <slot name="cards">
          <div class="card-item">
            <span class="card-number">01</span>
            <h3>Card Title</h3>
            <p>Card description goes here.</p>
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
  columns?: 2 | 3 | 4
}>(), {
  theme: 'editorial',
  vibe: 'classic',
  columns: 3
})
</script>

<style scoped>
.cards-grid {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2rem;
}

/* Header */
.grid-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.grid-header :deep(h1),
.grid-header :deep(h2) {
  font-family: var(--edit-font-display);
  font-size: 2rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0;
}

.header-ornament {
  color: var(--edit-gold);
  font-size: 0.7rem;
}

/* Grid */
.grid-container {
  display: grid;
  gap: 1.5rem;
  flex: 1;
}

.cols-2 { grid-template-columns: repeat(2, 1fr); }
.cols-3 { grid-template-columns: repeat(3, 1fr); }
.cols-4 { grid-template-columns: repeat(4, 1fr); }

/* Card styles */
.grid-container :deep(.card-item) {
  background: var(--edit-white);
  border: 1px solid var(--edit-border);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  transition: all 0.3s ease;
}

.grid-container :deep(.card-item:hover) {
  border-color: var(--edit-gold);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.grid-container :deep(.card-number) {
  font-family: var(--edit-font-display);
  font-size: 2rem;
  color: var(--edit-gold);
  line-height: 1;
}

.grid-container :deep(.card-item h3) {
  font-family: var(--edit-font-display);
  font-size: 1.25rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin: 0;
}

.grid-container :deep(.card-item p) {
  font-family: var(--edit-font-body);
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--edit-text);
  margin: 0;
}

.grid-container :deep(.card-icon) {
  font-size: 1.5rem;
  color: var(--edit-gold);
  margin-bottom: 0.5rem;
}

.grid-container :deep(.card-image) {
  width: 100%;
  height: 120px;
  object-fit: cover;
  margin-bottom: 0.5rem;
}

.card-item {
  background: var(--edit-white);
  border: 1px solid var(--edit-border);
  padding: 1.5rem;
}

.card-number {
  font-family: var(--edit-font-display);
  font-size: 1.5rem;
  color: var(--edit-gold);
}

/* Vibe: Modern */
.vibe-modern .header-ornament {
  display: none;
}

.vibe-modern .grid-container :deep(.card-item) {
  border-color: var(--edit-charcoal);
}

.vibe-modern .grid-container :deep(.card-number) {
  color: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .grid-container :deep(.card-item) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(201, 169, 98, 0.3);
}

.vibe-luxe .grid-container :deep(.card-item h3) {
  color: var(--edit-white);
}
</style>
