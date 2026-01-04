<!--
  cards-grid.vue - Handdrawn Cards Grid Layout
  
  Slots:
    - title: Grid title
    - card1 through card6: Card content
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="cards-grid" :class="`vibe-${vibe}`">
      <!-- Title -->
      <div v-if="$slots.title" class="grid-title">
        <slot name="title" />
        <div class="title-underline">〰️〰️〰️</div>
      </div>
      
      <!-- Cards -->
      <div class="cards-container">
        <div 
          v-for="i in 6" 
          :key="i" 
          class="card"
          :class="`card-${['pink', 'blue', 'green', 'yellow', 'purple', 'orange'][i-1]}`"
          :style="{ '--card-index': i }"
        >
          <div class="card-tape"></div>
          <div class="card-content">
            <slot :name="`card${i}`">
              <span class="card-icon">{{ ['📝', '💡', '🎯', '⭐', '🎨', '🔮'][i-1] }}</span>
              <span class="placeholder">Card {{ i }}</span>
            </slot>
          </div>
          <div class="card-number">{{ i }}</div>
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
.cards-grid {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Title */
.grid-title {
  text-align: center;
  font-family: var(--hand-font-display);
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--hand-text-dark);
}

.title-underline {
  font-size: 1rem;
  opacity: 0.5;
}

/* Cards container */
.cards-container {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 1rem;
}

.card {
  position: relative;
  padding: 1rem;
  padding-top: 1.5rem;
  border-radius: 4px;
  box-shadow: 3px 3px 0 var(--hand-shadow-color);
  display: flex;
  flex-direction: column;
  animation: card-drop 0.4s ease-out backwards;
  animation-delay: calc(var(--card-index) * 0.08s);
}

@keyframes card-drop {
  from {
    opacity: 0;
    transform: translateY(-20px) rotate(0deg);
  }
}

/* Card colors */
.card-pink {
  background: var(--hand-pink-light);
  transform: rotate(-1deg);
}

.card-blue {
  background: var(--hand-blue-light);
  transform: rotate(0.5deg);
}

.card-green {
  background: var(--hand-green-light);
  transform: rotate(-0.5deg);
}

.card-yellow {
  background: var(--hand-yellow);
  transform: rotate(1deg);
}

.card-purple {
  background: var(--hand-purple-light);
  transform: rotate(-1.5deg);
}

.card-orange {
  background: var(--hand-orange-light);
  transform: rotate(0.5deg);
}

/* Card tape */
.card-tape {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%) rotate(-3deg);
  width: 40px;
  height: 15px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

/* Card content */
.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-icon {
  font-size: 1.5rem;
}

.card-content :deep(h3) {
  font-family: var(--hand-font-display);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--hand-text-dark);
  margin: 0;
}

.card-content :deep(p) {
  font-family: var(--hand-font-body);
  font-size: 0.85rem;
  line-height: 1.4;
  color: var(--hand-text);
  margin: 0;
}

/* Card number */
.card-number {
  position: absolute;
  bottom: 0.25rem;
  right: 0.5rem;
  font-family: var(--hand-font-display);
  font-size: 1.2rem;
  color: var(--hand-text-light);
  opacity: 0.3;
}

.placeholder {
  font-family: var(--hand-font-handwriting);
  color: var(--hand-text-light);
  font-size: 0.85rem;
}

/* Vibe modifiers */
.vibe-minimal .card {
  transform: none;
  box-shadow: none;
  background: var(--hand-bg-cream);
  border: 1px solid var(--hand-text-light);
}

.vibe-minimal .card-tape,
.vibe-minimal .card-number {
  display: none;
}

.vibe-playful .card:hover {
  transform: scale(1.05) rotate(0deg);
  z-index: 10;
}

.vibe-decorated .card::before {
  content: '✦';
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  font-size: 0.7rem;
  color: var(--hand-text-light);
}
</style>
