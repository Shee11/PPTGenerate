<!--
  cards-grid.vue - Duolingo Style Card Grid Layout
  
  Purpose: Flexible grid of styled cards with Duolingo's playful design
  Perfect for features, services, or categorized content
  
  Slots: title, card-1 to card-8 (EXACTLY same as slidev-project - note the hyphen!)
  Parameters: columns: 2 | 3 | 4, cardStyle: "elevated" | "flat" | "outlined" | "glass"
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="cards-grid-layout" :class="[`cols-${columns}`, `style-${cardStyle}`, `vibe-${vibe}`]">
      <!-- Section title -->
      <div v-if="$slots.title" class="section-title">
        <slot name="title" />
      </div>
      
      <!-- Cards grid -->
      <div class="cards-container">
        <div 
          v-for="i in 8" 
          :key="i" 
          class="card-item"
          v-show="$slots[`card-${i}`]"
          :style="{ '--card-color': cardColors[(i-1) % cardColors.length] }"
        >
          <div class="card-inner">
            <div class="card-accent"></div>
            <div class="card-content">
              <slot :name="`card-${i}`" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<script setup lang="ts">
import SlideShell from './SlideShell.vue'

const props = withDefaults(defineProps<{
  theme?: string
  vibe?: string
  header?: string
  footer?: string
  columns?: 2 | 3 | 4
  cardStyle?: 'elevated' | 'flat' | 'outlined' | 'glass'
}>(), {
  theme: 'duolingo',
  vibe: 'playful',
  columns: 3,
  cardStyle: 'elevated'
})

// Duolingo accent colors for cards
const cardColors = ['#58CC02', '#1CB0F6', '#FF9600', '#CE82FF', '#FF4B4B', '#FFC800', '#58CC02', '#1CB0F6']
</script>

<style scoped>
.cards-grid-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  position: relative;
  padding: 1.5rem;
}

.section-title {
  text-align: center;
  flex-shrink: 0;
}

.section-title :deep(h1),
.section-title :deep(h2),
.section-title :deep(h3) {
  margin: 0;
  color: var(--theme-text);
  font-weight: 800;
}

.cards-container {
  flex: 1;
  display: grid;
  gap: 1rem;
  align-content: start;
}

.cols-2 .cards-container { grid-template-columns: repeat(2, 1fr); }
.cols-3 .cards-container { grid-template-columns: repeat(3, 1fr); }
.cols-4 .cards-container { grid-template-columns: repeat(4, 1fr); }

.card-item {
  position: relative;
}

.card-inner {
  background: var(--theme-bg-card);
  border: 2px solid var(--theme-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card-accent {
  height: 6px;
  background: var(--card-color, var(--theme-primary));
  flex-shrink: 0;
}

.card-content {
  padding: 1.25rem;
  flex: 1;
}

.card-content :deep(h1),
.card-content :deep(h2),
.card-content :deep(h3),
.card-content :deep(h4) {
  color: var(--card-color, var(--theme-primary));
  font-weight: 700;
  margin: 0 0 0.75rem 0;
  font-size: 1.1rem;
}

.card-content :deep(p) {
  color: var(--theme-text-muted);
  margin: 0;
  line-height: 1.5;
  font-size: 0.95rem;
}

/* Card style variations */
.style-flat .card-inner {
  box-shadow: none;
  border-color: var(--theme-border);
}

.style-outlined .card-inner {
  background: transparent;
  border-width: 2px;
  border-color: var(--card-color, var(--theme-primary));
  box-shadow: none;
}

.style-outlined .card-accent {
  display: none;
}

.style-glass .card-inner {
  background: color-mix(in srgb, var(--theme-bg-card) 80%, transparent);
  backdrop-filter: blur(8px);
  border-color: color-mix(in srgb, var(--card-color) 30%, var(--theme-border));
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
  gap: 1rem;
}

.vibe-minimal .cards-container {
  gap: 0.75rem;
}

.vibe-minimal .card-inner {
  border-radius: var(--radius-sm);
  border-width: 1px;
  box-shadow: none;
}

.vibe-minimal .card-accent {
  height: 3px;
}

.vibe-minimal .card-content {
  padding: 1rem;
}

/* === VIBE: CLEAN === */
.vibe-clean .card-inner {
  border-width: 1px;
  box-shadow: 0 1px 0 var(--theme-border);
}

.vibe-clean .card-accent {
  height: 4px;
}

/* === VIBE: PLAYFUL === */
.vibe-playful .card-inner {
  border-radius: var(--radius-xl);
  border-width: 3px;
  border-color: var(--card-color, var(--theme-primary));
  box-shadow: 0 4px 0 color-mix(in srgb, var(--card-color, var(--theme-primary)) 40%, transparent);
}

.vibe-playful .card-accent {
  height: 0;
  display: none;
}

.vibe-playful .card-inner {
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--card-color) 8%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.vibe-playful .card-item:nth-child(odd) {
  transform: rotate(-0.5deg);
}

.vibe-playful .card-item:nth-child(even) {
  transform: rotate(0.5deg);
}

.vibe-playful .card-content {
  padding: 1.5rem;
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 2rem;
  gap: 2rem;
}

.vibe-expressive .cards-container {
  gap: 1.5rem;
}

.vibe-expressive .card-inner {
  border-radius: var(--radius-xl);
  border-width: 4px;
  border-color: var(--card-color, var(--theme-primary));
  box-shadow: 0 6px 0 color-mix(in srgb, var(--card-color, var(--theme-primary)) 50%, transparent);
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--card-color) 12%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.vibe-expressive .card-accent {
  display: none;
}

.vibe-expressive .card-item:nth-child(odd) {
  transform: rotate(-1deg);
}

.vibe-expressive .card-item:nth-child(even) {
  transform: rotate(1deg);
}

.vibe-expressive .card-content {
  padding: 1.75rem;
}

.vibe-expressive .card-content :deep(h1),
.vibe-expressive .card-content :deep(h2),
.vibe-expressive .card-content :deep(h3),
.vibe-expressive .card-content :deep(h4) {
  font-size: 1.3rem;
}
</style>
