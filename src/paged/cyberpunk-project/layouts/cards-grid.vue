<!--
  cards-grid.vue - Cyberpunk Cards Grid Layout
  
  Slots:
    - title: Section title
    - card1 through card6: Individual cards
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="cards-grid-layout" :class="`vibe-${vibe}`">
      <!-- Title -->
      <div v-if="$slots.title" class="section-title">
        <span class="title-marker">//</span>
        <slot name="title" />
      </div>
      
      <!-- Cards grid -->
      <div class="cards-container">
        <div 
          v-for="i in 6" 
          :key="i" 
          class="card"
          :class="`card-${i}`"
          :style="{ '--card-index': i }"
        >
          <div class="card-border">
            <div class="border-animate"></div>
          </div>
          <div class="card-inner">
            <div class="card-header">
              <span class="card-id">{{ String(i).padStart(2, '0') }}</span>
            </div>
            <div class="card-content">
              <slot :name="`card${i}`">
                <span class="placeholder">// CARD_{{ i }}</span>
              </slot>
            </div>
          </div>
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
  theme: 'cyberpunk',
  vibe: 'balanced'
})
</script>

<style scoped>
.cards-grid-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Title */
.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-family: var(--cyber-font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  letter-spacing: 3px;
}

.title-marker {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-magenta, #FF00FF);
  text-shadow: 0 0 10px var(--cyber-magenta-glow);
}

/* Cards container */
.cards-container {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 1.25rem;
}

.card {
  position: relative;
  background: rgba(18, 18, 26, 0.85);
  animation: card-enter 0.5s ease-out backwards;
  animation-delay: calc(var(--card-index) * 0.1s);
  overflow: hidden;
}

@keyframes card-enter {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
}

/* Card border animation */
.card-border {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.border-animate {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, 
    var(--cyber-cyan, #00FFFF), 
    var(--cyber-magenta, #FF00FF), 
    var(--cyber-cyan, #00FFFF)
  );
  background-size: 200% 100%;
  padding: 1px;
  -webkit-mask: 
    linear-gradient(#fff 0 0) content-box, 
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0.5;
}

.card:hover .border-animate {
  opacity: 1;
  animation: border-flow 2s linear infinite;
}

@keyframes border-flow {
  from { background-position: 0% 0%; }
  to { background-position: 200% 0%; }
}

/* Card inner */
.card-inner {
  position: relative;
  z-index: 5;
  height: 100%;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
}

.card-header {
  margin-bottom: 0.75rem;
}

.card-id {
  font-family: var(--cyber-font-mono);
  font-size: 0.7rem;
  color: var(--cyber-cyan, #00FFFF);
  background: rgba(0, 255, 255, 0.1);
  padding: 0.2rem 0.5rem;
  border: 1px solid rgba(0, 255, 255, 0.3);
}

/* Card content */
.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-content :deep(h3) {
  font-family: var(--cyber-font-display);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.card-content :deep(p) {
  font-family: var(--cyber-font-body);
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--cyber-text, #e0e0e0);
}

.card-content :deep(.icon) {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  filter: drop-shadow(0 0 10px var(--cyber-cyan-glow));
}

.placeholder {
  font-family: var(--cyber-font-mono);
  color: var(--cyber-text-dim);
  font-size: 0.8rem;
}

/* Alternating card accents */
.card-1 { --card-accent: var(--cyber-cyan, #00FFFF); }
.card-2 { --card-accent: var(--cyber-magenta, #FF00FF); }
.card-3 { --card-accent: var(--cyber-yellow, #FFFF00); }
.card-4 { --card-accent: var(--cyber-pink, #FF0080); }
.card-5 { --card-accent: var(--cyber-green, #00FF41); }
.card-6 { --card-accent: var(--cyber-cyan, #00FFFF); }

/* Vibe modifiers */
.vibe-minimal .card-border,
.vibe-minimal .card-header {
  display: none;
}

.vibe-minimal .card {
  border: 1px solid rgba(0, 255, 255, 0.2);
}

.vibe-intense .border-animate {
  opacity: 0.8;
  animation: border-flow 3s linear infinite;
}

.vibe-glitch .card:nth-child(odd) {
  animation: card-enter 0.5s ease-out backwards, card-glitch 5s ease-in-out infinite;
}

@keyframes card-glitch {
  0%, 100% { transform: translate(0); }
  20% { transform: translate(-1px, 0); }
  40% { transform: translate(1px, 0); }
  60% { transform: translate(0); }
}
</style>
