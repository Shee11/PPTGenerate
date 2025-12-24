<!--
  smart-grid.vue - Editorial Responsive Grid Layout
  
  Slots:
    - header: Grid header
    - col1, col2, col3, col4: Column content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer" :dark="dark">
    <div class="smart-grid">
      <!-- Header -->
      <div v-if="$slots.header" class="grid-header">
        <slot name="header" />
        <div class="header-ornament">
          <span class="ornament-line"></span>
          <span class="ornament-diamond">◆</span>
          <span class="ornament-line"></span>
        </div>
      </div>
      
      <!-- Grid columns -->
      <div class="grid-columns">
        <div 
          v-for="i in 4" 
          :key="i" 
          class="grid-col"
          :style="{ '--col-index': i }"
        >
          <div class="col-content">
            <slot :name="`col${i}`">
              <span class="col-number">{{ String(i).padStart(2, '0') }}</span>
              <span class="placeholder">Column {{ i }}</span>
            </slot>
          </div>
          <div v-if="i < 4" class="col-divider"></div>
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
}>(), {
  theme: 'editorial',
  vibe: 'classic'
})
</script>

<style scoped>
.smart-grid {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Header */
.grid-header {
  text-align: center;
}

.grid-header :deep(h2) {
  font-family: var(--edit-font-display);
  font-size: 2.2rem;
  font-weight: 400;
  color: var(--edit-text-dark);
  margin-bottom: 1rem;
}

.header-ornament {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.ornament-line {
  width: 60px;
  height: 1px;
  background: var(--edit-gold);
}

.ornament-diamond {
  color: var(--edit-gold);
  font-size: 0.6rem;
}

/* Grid columns */
.grid-columns {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
}

.grid-col {
  position: relative;
  padding: 0 1.5rem;
  display: flex;
  flex-direction: column;
  animation: fade-in 0.5s ease-out backwards;
  animation-delay: calc(var(--col-index) * 0.1s);
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Column content */
.col-content {
  flex: 1;
}

.col-number {
  display: block;
  font-family: var(--edit-font-display);
  font-size: 2.5rem;
  color: var(--edit-gold);
  line-height: 1;
  margin-bottom: 1rem;
}

.col-content :deep(h3) {
  font-family: var(--edit-font-display);
  font-size: 1.3rem;
  font-weight: 500;
  color: var(--edit-text-dark);
  margin-bottom: 0.75rem;
}

.col-content :deep(p) {
  font-family: var(--edit-font-body);
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--edit-text);
}

/* Column divider */
.col-divider {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 1px;
  background: var(--edit-light);
}

.placeholder {
  font-family: var(--edit-font-accent);
  font-style: italic;
  color: var(--edit-text-light);
  font-size: 0.9rem;
}

/* Vibe: Modern */
.vibe-modern .col-number {
  color: var(--edit-charcoal);
}

.vibe-modern .ornament-line {
  background: var(--edit-charcoal);
}

.vibe-modern .ornament-diamond {
  color: var(--edit-charcoal);
}

/* Vibe: Luxe */
.vibe-luxe .col-divider {
  background: var(--edit-slate);
}
</style>
