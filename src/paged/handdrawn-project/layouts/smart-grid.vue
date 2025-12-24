<!--
  smart-grid.vue - Handdrawn Responsive Grid Layout
  
  Slots:
    - header: Grid header
    - col1, col2, col3, col4: Column content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="smart-grid" :class="`vibe-${vibe}`">
      <!-- Header -->
      <div v-if="$slots.header" class="grid-header">
        <span class="header-star">★</span>
        <slot name="header" />
        <span class="header-star">★</span>
      </div>
      
      <!-- Grid columns -->
      <div class="grid-columns">
        <div 
          v-for="i in 4" 
          :key="i" 
          class="grid-col"
          :class="[`col-${i}`, `sticky-${['yellow', 'pink', 'blue', 'green'][i-1]}`]"
          :style="{ '--col-index': i }"
        >
          <div class="col-pin">📌</div>
          <div class="col-content">
            <slot :name="`col${i}`">
              <span class="placeholder">✏️ Column {{ i }}</span>
            </slot>
          </div>
          <div class="col-number">{{ i }}</div>
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
}>(), {
  theme: 'handdrawn',
  vibe: 'cozy'
})
</script>

<style scoped>
.smart-grid {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Header */
.grid-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-family: var(--hand-font-display);
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--hand-text-dark);
}

.header-star {
  color: var(--hand-yellow-dark);
  font-size: 1.2rem;
}

/* Grid columns */
.grid-columns {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
}

.grid-col {
  position: relative;
  padding: 1.25rem;
  padding-top: 1.75rem;
  border-radius: 3px;
  box-shadow: 3px 3px 0 var(--hand-shadow-color);
  animation: col-drop 0.4s ease-out backwards;
  animation-delay: calc(var(--col-index) * 0.1s);
}

@keyframes col-drop {
  from {
    opacity: 0;
    transform: translateY(-20px) rotate(0deg);
  }
}

.sticky-yellow {
  background: var(--hand-yellow);
  transform: rotate(-1deg);
}

.sticky-pink {
  background: var(--hand-pink-light);
  transform: rotate(1deg);
}

.sticky-blue {
  background: var(--hand-blue-light);
  transform: rotate(-0.5deg);
}

.sticky-green {
  background: var(--hand-green-light);
  transform: rotate(1.5deg);
}

/* Pin */
.col-pin {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1.2rem;
}

/* Column content */
.col-content :deep(h3) {
  font-family: var(--hand-font-display);
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--hand-text-dark);
  margin-bottom: 0.5rem;
}

.col-content :deep(p) {
  font-family: var(--hand-font-body);
  font-size: 0.95rem;
  line-height: 1.5;
  color: var(--hand-text);
}

/* Column number */
.col-number {
  position: absolute;
  bottom: 0.5rem;
  right: 0.75rem;
  font-family: var(--hand-font-display);
  font-size: 1.5rem;
  color: var(--hand-text-light);
  opacity: 0.3;
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: 0.9rem;
}

/* Vibe modifiers */
.vibe-minimal .col-pin,
.vibe-minimal .col-number {
  display: none;
}

.vibe-minimal .grid-col {
  background: var(--hand-bg-cream);
  transform: none;
}

.vibe-playful .grid-col:hover {
  transform: scale(1.02) rotate(0deg);
  box-shadow: 5px 5px 0 var(--hand-shadow-color);
}

.vibe-decorated .col-pin {
  font-size: 1.5rem;
}
</style>
