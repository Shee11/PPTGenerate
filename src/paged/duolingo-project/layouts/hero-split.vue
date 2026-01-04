<script setup lang="ts">
/**
 * Hero Split Layout - Duolingo Style
 * 
 * Two-panel split layout with configurable ratio.
 * Features Duolingo's playful design with rounded corners and clean divisions.
 * 
 * Slots: left, right (EXACTLY these names - same as slidev-project)
 * Parameters: ratio: "50-50" | "60-40" | "70-30"
 */
import { computed, inject } from 'vue'
import SlideShell from './SlideShell.vue'

const props = defineProps<{
  ratio?: string
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'playful' | 'expressive'
}>()

const injectedVibe = inject('vibe', computed(() => props.vibe || 'playful'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'playful')

// Parse ratio parameter
const splitRatio = computed(() => {
  const ratio = props.ratio || '50-50'
  const parts = ratio.split('-').map(Number)
  
  if (parts.length === 2 && !parts.some(isNaN)) {
    const [left, right] = parts
    const total = left + right
    return {
      left: `${(left / total) * 100}%`,
      right: `${(right / total) * 100}%`
    }
  }
  
  return { left: '50%', right: '50%' }
})

const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="hero-split" :class="vibeClass">
      <!-- Left panel -->
      <div class="split-panel split-left" :style="{ width: splitRatio.left }">
        <div class="panel-content">
          <slot name="left" />
        </div>
      </div>
      
      <!-- Divider with Duolingo style -->
      <div class="split-divider">
        <div class="divider-dot"></div>
      </div>
      
      <!-- Right panel -->
      <div class="split-panel split-right" :style="{ width: splitRatio.right }">
        <div class="panel-content">
          <slot name="right" />
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.hero-split {
  display: flex;
  width: 100%;
  height: 100%;
  gap: 1rem;
  padding: 1.5rem;
  align-items: stretch;
}

.split-panel {
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
  color: var(--theme-text);
  background: var(--theme-bg-card);
  border-radius: var(--radius-lg);
  border: 2px solid var(--theme-border);
  box-shadow: var(--shadow-card);
}

.panel-content {
  padding: 2rem;
}

.split-panel :deep(h1),
.split-panel :deep(h2),
.split-panel :deep(h3) {
  color: var(--theme-text);
  font-family: var(--font-heading);
  font-weight: 800;
  margin-bottom: 1rem;
}

.split-panel :deep(h1) {
  font-size: 2.5rem;
  color: var(--theme-primary);
}

.split-panel :deep(h2) {
  font-size: 1.75rem;
}

.split-panel :deep(p) {
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--theme-text-muted);
}

.split-left {
  background: linear-gradient(135deg, #F0FFF0, var(--theme-bg-card));
  border-color: var(--theme-primary);
}

.split-right {
  background: var(--theme-bg-card);
}

/* Divider */
.split-divider {
  width: 4px;
  background: var(--theme-border);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.divider-dot {
  width: 12px;
  height: 12px;
  background: var(--theme-primary);
  border-radius: 50%;
  box-shadow: 0 2px 0 var(--theme-primary-dark);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  gap: 0.5rem;
  padding: 1rem;
}

.vibe-minimal .split-panel {
  border-radius: var(--radius-sm);
  box-shadow: none;
  border: 1px solid var(--theme-border);
  background: var(--theme-bg-card);
}

.vibe-minimal .split-left {
  background: var(--theme-bg-card);
  border-color: var(--theme-border);
}

.vibe-minimal .split-divider {
  width: 2px;
}

.vibe-minimal .divider-dot {
  display: none;
}

/* === VIBE: CLEAN === */
.vibe-clean .split-panel {
  border-width: 1px;
}

.vibe-clean .split-left {
  background: var(--theme-bg-surface);
  border-color: var(--theme-border);
}

/* === VIBE: PLAYFUL === */
.vibe-playful .split-left {
  background: linear-gradient(135deg, #E8FFE0, #DFFFCC);
  border-color: var(--theme-primary);
  border-width: 3px;
}

.vibe-playful .split-right {
  background: linear-gradient(135deg, #E0F4FF, #CCF0FF);
  border-color: var(--theme-accent);
  border-width: 3px;
}

.vibe-playful .divider-dot {
  width: 16px;
  height: 16px;
  background: var(--theme-warning);
  box-shadow: 0 3px 0 var(--theme-warning);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 2rem;
  gap: 1.5rem;
}

.vibe-expressive .split-panel {
  border-radius: var(--radius-xl);
  border-width: 4px;
  box-shadow: var(--shadow-lg);
}

.vibe-expressive .split-left {
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-primary-light));
  border-color: var(--theme-primary-dark);
}

.vibe-expressive .split-left :deep(h1),
.vibe-expressive .split-left :deep(h2),
.vibe-expressive .split-left :deep(h3),
.vibe-expressive .split-left :deep(p) {
  color: white;
}

.vibe-expressive .split-right {
  background: linear-gradient(135deg, var(--theme-accent), #4DC8FF);
  border-color: var(--theme-accent-dark);
}

.vibe-expressive .split-right :deep(h1),
.vibe-expressive .split-right :deep(h2),
.vibe-expressive .split-right :deep(h3),
.vibe-expressive .split-right :deep(p) {
  color: white;
}

.vibe-expressive .divider-dot {
  width: 20px;
  height: 20px;
  background: var(--theme-golden);
  box-shadow: 0 4px 0 #E6B300;
}
</style>
