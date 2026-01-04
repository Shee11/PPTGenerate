<script setup lang="ts">
/**
 * Stats Showcase Layout - Business Project
 * 
 * Large statistics/numbers display.
 * 
 * Slots:
 *   - title: Section title
 *   - stat1, stat2, stat3, stat4: Statistic boxes
 * 
 * Frontmatter:
 *   layout: stats-showcase
 *   header: "..."
 *   footer: "..."
 *   theme: business_professional
 *   vibe: balanced
 */
import { computed, inject } from 'vue'
import SlideShell from './SlideShell.vue'

const props = defineProps<{
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'decorative' | 'expressive'
}>()

const injectedVibe = inject('vibe', computed(() => props.vibe || 'balanced'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'balanced')
const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="stats-showcase" :class="vibeClass">
      <header v-if="$slots.title" class="showcase-title">
        <slot name="title" />
      </header>
      
      <div class="stats-container">
        <div v-if="$slots.stat1" class="stat-box">
          <slot name="stat1" />
        </div>
        <div v-if="$slots.stat2" class="stat-box">
          <slot name="stat2" />
        </div>
        <div v-if="$slots.stat3" class="stat-box">
          <slot name="stat3" />
        </div>
        <div v-if="$slots.stat4" class="stat-box">
          <slot name="stat4" />
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.stats-showcase {
  height: 100%;
  width: 100%;
  padding: 2rem;
  display: flex;
  flex-direction: column;
}

.showcase-title {
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 600;
  color: var(--theme-text);
}

.showcase-title :deep(h1),
.showcase-title :deep(h2),
.showcase-title :deep(h3) {
  color: var(--theme-primary);
  margin: 0;
}

.stats-container {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  align-content: center;
}

.stat-box {
  padding: 2rem;
  border-radius: var(--radius-md);
  background: var(--theme-bg-surface);
  border: 1px solid var(--theme-border);
  box-shadow: var(--shadow-sm);
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* Large number */
.stat-box :deep(h2),
.stat-box :deep(.stat-value) {
  font-size: 3rem;
  font-weight: 700;
  color: var(--theme-primary);
  margin: 0;
  line-height: 1.1;
}

/* Label */
.stat-box :deep(p),
.stat-box :deep(.stat-label) {
  font-size: 0.875rem;
  color: var(--theme-text-muted);
  margin: 0.75rem 0 0 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Color variations */
.stat-box:nth-child(1) :deep(h2),
.stat-box:nth-child(1) :deep(.stat-value) {
  color: var(--theme-primary);
}

.stat-box:nth-child(2) :deep(h2),
.stat-box:nth-child(2) :deep(.stat-value) {
  color: var(--theme-accent);
}

.stat-box:nth-child(3) :deep(h2),
.stat-box:nth-child(3) :deep(.stat-value) {
  color: var(--theme-success);
}

.stat-box:nth-child(4) :deep(h2),
.stat-box:nth-child(4) :deep(.stat-value) {
  color: var(--theme-warning);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1.5rem;
}

.vibe-minimal .stats-container {
  gap: 1rem;
}

.vibe-minimal .stat-box {
  padding: 1.25rem;
  border-radius: var(--radius-sm);
  box-shadow: none;
}

.vibe-minimal .stat-box :deep(h2),
.vibe-minimal .stat-box :deep(.stat-value) {
  font-size: 2.5rem;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  padding: 1.75rem;
}

.vibe-clean .stats-container {
  gap: 1.25rem;
}

.vibe-clean .stat-box :deep(h2),
.vibe-clean .stat-box :deep(.stat-value) {
  font-size: 2.75rem;
}

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  padding: 2.5rem;
}

.vibe-decorative .stats-container {
  gap: 2rem;
}

.vibe-decorative .stat-box {
  padding: 2.5rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: none;
}

.vibe-decorative .stat-box :deep(h2),
.vibe-decorative .stat-box :deep(.stat-value) {
  font-size: 3.5rem;
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 3rem;
}

.vibe-expressive .stats-container {
  gap: 2.5rem;
}

.vibe-expressive .stat-box {
  padding: 3rem;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    var(--theme-bg-elevated)
  );
}

.vibe-expressive .stat-box :deep(h2),
.vibe-expressive .stat-box :deep(.stat-value) {
  font-size: 4rem;
}
</style>
