<!--
  stats-showcase.vue - Handdrawn Stats Showcase Layout
  
  Slots:
    - title: Section title
    - stat1, stat2, stat3: Stat items
    - footer: Footer note
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="stats-showcase" :class="`vibe-${vibe}`">
      <!-- Title -->
      <div v-if="$slots.title" class="stats-title">
        <span class="title-star">⭐</span>
        <slot name="title" />
        <span class="title-star">⭐</span>
      </div>
      
      <!-- Stats grid -->
      <div class="stats-grid">
        <div 
          v-for="i in 3" 
          :key="i" 
          class="stat-card"
          :class="`stat-${['pink', 'blue', 'green'][i-1]}`"
          :style="{ '--stat-index': i }"
        >
          <!-- Pushpin -->
          <div class="stat-pin">📌</div>
          
          <div class="stat-content">
            <slot :name="`stat${i}`">
              <div class="stat-value">{{ ['42', '87%', '∞'][i-1] }}</div>
              <div class="stat-label">Stat {{ i }}</div>
            </slot>
          </div>
          
          <!-- Decorative corner -->
          <div class="stat-corner">✦</div>
        </div>
      </div>
      
      <!-- Footer note -->
      <div v-if="$slots.footer" class="stats-footer">
        <div class="footer-note">
          <slot name="footer" />
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
.stats-showcase {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Title */
.stats-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-family: var(--hand-font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--hand-text-dark);
}

.title-star {
  font-size: 1.5rem;
  color: var(--hand-yellow-dark);
}

/* Stats grid */
.stats-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  align-items: center;
}

.stat-card {
  position: relative;
  padding: 2rem;
  padding-top: 2.5rem;
  border-radius: 8px;
  border: 3px solid;
  text-align: center;
  box-shadow: 4px 4px 0 var(--hand-shadow-color);
  animation: stat-pop 0.4s ease-out backwards;
  animation-delay: calc(var(--stat-index) * 0.15s);
}

@keyframes stat-pop {
  from {
    opacity: 0;
    transform: scale(0.8) rotate(0deg);
  }
}

.stat-pink {
  border-color: var(--hand-pink);
  background: var(--hand-pink-light);
  transform: rotate(-2deg);
}

.stat-blue {
  border-color: var(--hand-blue);
  background: var(--hand-blue-light);
  transform: rotate(1deg);
}

.stat-green {
  border-color: var(--hand-green);
  background: var(--hand-green-light);
  transform: rotate(-1deg);
}

/* Pin */
.stat-pin {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1.5rem;
}

/* Stat content */
.stat-content :deep(.stat-value),
.stat-value {
  font-family: var(--hand-font-display);
  font-size: 3.5rem;
  font-weight: 700;
  color: var(--hand-text-dark);
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-content :deep(.stat-label),
.stat-label {
  font-family: var(--hand-font-handwriting);
  font-size: 1.2rem;
  color: var(--hand-text);
}

.stat-content :deep(.stat-change) {
  font-family: var(--hand-font-body);
  font-size: 0.9rem;
  color: var(--hand-green);
  margin-top: 0.25rem;
}

.stat-content :deep(.stat-change.negative) {
  color: var(--hand-pink);
}

/* Corner decoration */
.stat-corner {
  position: absolute;
  bottom: 0.5rem;
  right: 0.75rem;
  font-size: 0.8rem;
  color: var(--hand-text-light);
  opacity: 0.5;
}

/* Footer */
.stats-footer {
  text-align: center;
}

.footer-note {
  display: inline-block;
  font-family: var(--hand-font-handwriting);
  font-size: 1rem;
  color: var(--hand-text);
  background: var(--hand-yellow);
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  box-shadow: 2px 2px 0 var(--hand-shadow-color);
  transform: rotate(1deg);
}

/* Vibe modifiers */
.vibe-minimal .stat-card {
  transform: none;
  box-shadow: none;
  border-width: 1px;
  background: var(--hand-bg-cream);
}

.vibe-minimal .stat-pin,
.vibe-minimal .stat-corner {
  display: none;
}

.vibe-minimal .footer-note {
  background: transparent;
  box-shadow: none;
  transform: none;
}

.vibe-playful .stat-card:hover {
  transform: scale(1.05) rotate(0deg);
}

.vibe-decorated .stat-card::before {
  content: '✨';
  position: absolute;
  top: 0.5rem;
  left: 0.5rem;
  font-size: 1rem;
}
</style>
