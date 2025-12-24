<!--
  stats-showcase.vue - Duolingo Style Statistics Display
  
  Purpose: Stunning display of key metrics with Duolingo's gamified style
  Perfect for XP/streak-style stats, achievements, or impressive numbers
  
  Slots: title, stat-1, stat-2, stat-3, stat-4 (EXACTLY same as slidev-project - note the hyphen!)
  Parameters: columns: 2 | 3 | 4
-->
<template>
  <SlideShell :theme="theme" :vibe="vibe" :header="header" :footer="footer">
    <div class="stats-showcase-layout" :class="[`cols-${columns}`, `vibe-${vibe}`]">
      <!-- Section title -->
      <div v-if="$slots.title" class="section-title">
        <slot name="title" />
      </div>
      
      <!-- Stats grid -->
      <div class="stats-grid">
        <div 
          v-for="i in 6" 
          :key="i" 
          class="stat-item"
          v-show="$slots[`stat-${i}`]"
          :style="{ '--stat-color': statColors[(i-1) % statColors.length] }"
        >
          <div class="stat-icon">{{ statIcons[(i-1) % statIcons.length] }}</div>
          <div class="stat-content">
            <slot :name="`stat-${i}`" />
          </div>
          <div class="stat-badge"></div>
        </div>
      </div>
      
      <!-- Background decorations -->
      <div class="stats-background">
        <div class="confetti confetti-1">🎉</div>
        <div class="confetti confetti-2">🏆</div>
        <div class="confetti confetti-3">⚡</div>
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
}>(), {
  theme: 'duolingo',
  vibe: 'playful',
  columns: 3
})

// Duolingo-style stat colors and icons
const statColors = ['#58CC02', '#1CB0F6', '#FF9600', '#CE82FF', '#FF4B4B', '#FFC800']
const statIcons = ['🔥', '⚡', '🎯', '💎', '🏆', '⭐']
</script>

<style scoped>
.stats-showcase-layout {
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

.stats-grid {
  flex: 1;
  display: grid;
  gap: 1rem;
  align-content: center;
}

.cols-2 .stats-grid { grid-template-columns: repeat(2, 1fr); }
.cols-3 .stats-grid { grid-template-columns: repeat(3, 1fr); }
.cols-4 .stats-grid { grid-template-columns: repeat(4, 1fr); }

.stat-item {
  background: var(--theme-bg-card);
  border: 3px solid var(--stat-color, var(--theme-primary));
  border-radius: var(--radius-xl);
  padding: 1.5rem;
  text-align: center;
  position: relative;
  box-shadow: 0 4px 0 color-mix(in srgb, var(--stat-color, var(--theme-primary)) 60%, black);
}

.stat-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.stat-content :deep(h1),
.stat-content :deep(h2),
.stat-content :deep(h3),
.stat-content :deep(.big-num) {
  color: var(--stat-color, var(--theme-primary));
  font-weight: 900;
  font-size: 3rem;
  margin: 0;
  line-height: 1;
}

.stat-content :deep(p),
.stat-content :deep(.label) {
  color: var(--theme-text-muted);
  font-weight: 700;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0.5rem 0 0 0;
}

.stat-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  background: var(--stat-color, var(--theme-primary));
  border-radius: 50%;
  border: 3px solid white;
}

/* Background decorations */
.stats-background {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.confetti {
  position: absolute;
  font-size: 1.5rem;
  opacity: 0.3;
}

.confetti-1 { top: 10%; right: 10%; }
.confetti-2 { bottom: 15%; left: 8%; }
.confetti-3 { top: 20%; left: 15%; }

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
  gap: 1rem;
}

.vibe-minimal .stats-grid {
  gap: 0.75rem;
}

.vibe-minimal .stat-item {
  border-radius: var(--radius-md);
  border-width: 1px;
  padding: 1rem;
  box-shadow: none;
}

.vibe-minimal .stat-icon {
  font-size: 1.25rem;
}

.vibe-minimal .stat-content :deep(h1),
.vibe-minimal .stat-content :deep(h2),
.vibe-minimal .stat-content :deep(h3),
.vibe-minimal .stat-content :deep(.big-num) {
  font-size: 2rem;
}

.vibe-minimal .stat-badge {
  display: none;
}

.vibe-minimal .stats-background {
  display: none;
}

/* === VIBE: CLEAN === */
.vibe-clean .stat-item {
  border-width: 2px;
  box-shadow: 0 2px 0 color-mix(in srgb, var(--stat-color, var(--theme-primary)) 50%, transparent);
}

.vibe-clean .stat-badge {
  width: 20px;
  height: 20px;
  top: -6px;
  right: -6px;
}

.vibe-clean .confetti {
  opacity: 0.15;
}

/* === VIBE: PLAYFUL === */
.vibe-playful .stat-item {
  border-radius: var(--radius-xl);
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--stat-color) 10%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.vibe-playful .stat-item:nth-child(odd) {
  transform: rotate(-1deg);
}

.vibe-playful .stat-item:nth-child(even) {
  transform: rotate(1deg);
}

.vibe-playful .stat-icon {
  font-size: 2.5rem;
}

.vibe-playful .stat-content :deep(h1),
.vibe-playful .stat-content :deep(h2),
.vibe-playful .stat-content :deep(h3),
.vibe-playful .stat-content :deep(.big-num) {
  font-size: 3.5rem;
}

.vibe-playful .confetti {
  opacity: 0.5;
  font-size: 2rem;
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 2rem;
  gap: 2rem;
}

.vibe-expressive .stats-grid {
  gap: 1.5rem;
}

.vibe-expressive .stat-item {
  border-width: 4px;
  border-radius: var(--radius-xl);
  padding: 2rem;
  box-shadow: 0 6px 0 color-mix(in srgb, var(--stat-color, var(--theme-primary)) 50%, black);
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--stat-color) 15%, var(--theme-bg-card)),
    var(--theme-bg-card)
  );
}

.vibe-expressive .stat-item:nth-child(odd) {
  transform: rotate(-2deg);
}

.vibe-expressive .stat-item:nth-child(even) {
  transform: rotate(2deg);
}

.vibe-expressive .stat-icon {
  font-size: 3rem;
}

.vibe-expressive .stat-content :deep(h1),
.vibe-expressive .stat-content :deep(h2),
.vibe-expressive .stat-content :deep(h3),
.vibe-expressive .stat-content :deep(.big-num) {
  font-size: 4rem;
}

.vibe-expressive .stat-badge {
  width: 32px;
  height: 32px;
  top: -12px;
  right: -12px;
  border-width: 4px;
}

.vibe-expressive .confetti {
  font-size: 2.5rem;
  opacity: 0.6;
}
</style>
