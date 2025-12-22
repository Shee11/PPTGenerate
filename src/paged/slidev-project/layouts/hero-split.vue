<script setup lang="ts">
/**
 * Hero Split Layout
 * 
 * Two-panel split layout with configurable ratio.
 * Inherits from SlideShell for consistent header/footer/theme/vibe.
 * 
 * Frontmatter:
 *   layout: hero-split
 *   ratio: 50-50       # Split ratio (e.g., "60-40", "70-30")
 *   header: "..."      # Optional header text
 *   footer: "..."      # Optional footer text
 *   theme: dark-professional
 *   vibe: balanced
 */
import { computed, inject } from 'vue'
import SlideShell from './SlideShell.vue'

const props = defineProps<{
  ratio?: string
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'decorative' | 'expressive'
}>()

// Get vibe from SlideShell injection or props
const injectedVibe = inject('vibe', computed(() => props.vibe || 'balanced'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'balanced')

// Parse ratio parameter (e.g., "60-40", "50-50", "70-30")
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

// Vibe class
const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="hero-split" :class="vibeClass">
      <!-- Left panel -->
      <div class="split-panel split-left" :style="{ width: splitRatio.left }">
        <slot name="left" />
      </div>
      
      <!-- Divider -->
      <div class="split-divider"></div>
      
      <!-- Right panel -->
      <div class="split-panel split-right" :style="{ width: splitRatio.right }">
        <slot name="right" />
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.hero-split {
  display: flex;
  width: 100%;
  height: 100%;
  gap: 1.5rem;
  padding: 2rem;
}

.split-panel {
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
  color: var(--theme-text);
}

.split-panel :deep(h1),
.split-panel :deep(h2),
.split-panel :deep(h3) {
  color: var(--theme-primary);
  font-family: var(--font-heading);
  margin-bottom: 1rem;
}

.split-left {
  padding-right: 1rem;
}

.split-right {
  padding-left: 1rem;
}

.split-divider {
  width: 2px;
  align-self: stretch;
  background: linear-gradient(
    180deg,
    transparent 0%,
    var(--theme-border) 20%,
    var(--theme-primary) 50%,
    var(--theme-border) 80%,
    transparent 100%
  );
  opacity: 0.5;
  flex-shrink: 0;
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  gap: 1rem;
  padding: 1rem;
}

.vibe-minimal .split-divider {
  width: 1px;
  background: var(--theme-border);
  opacity: 0.3;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  gap: 1.25rem;
  padding: 1.5rem;
}

.vibe-clean .split-divider {
  width: 1px;
  opacity: 0.4;
}

/* === VIBE: BALANCED (default) === */
/* Base styles above */

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  gap: 2rem;
  padding: 2.5rem;
}

.vibe-decorative .split-left {
  background: linear-gradient(
    135deg,
    transparent 0%,
    color-mix(in srgb, var(--theme-primary) 5%, transparent) 100%
  );
  border-radius: var(--radius-lg);
  padding: 2rem;
}

.vibe-decorative .split-divider {
  width: 4px;
  background: linear-gradient(
    180deg,
    var(--theme-primary) 0%,
    var(--theme-accent) 100%
  );
  opacity: 0.6;
  border-radius: 2px;
  box-shadow: var(--shadow-glow);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  gap: 3rem;
  padding: 3rem;
}

.vibe-expressive .split-left {
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--theme-primary) 8%, transparent) 0%,
    color-mix(in srgb, var(--theme-accent) 5%, transparent) 100%
  );
  border-radius: var(--radius-xl);
  padding: 2.5rem;
  box-shadow: var(--shadow-md);
}

.vibe-expressive .split-right {
  background: linear-gradient(
    -135deg,
    color-mix(in srgb, var(--theme-accent) 5%, transparent) 0%,
    transparent 100%
  );
  border-radius: var(--radius-lg);
  padding: 2rem;
}

.vibe-expressive .split-divider {
  width: 6px;
  background: linear-gradient(
    180deg,
    transparent 0%,
    var(--theme-primary) 20%,
    var(--theme-accent) 50%,
    var(--theme-primary) 80%,
    transparent 100%
  );
  opacity: 0.8;
  border-radius: 3px;
  box-shadow: var(--shadow-glow), 0 0 30px color-mix(in srgb, var(--theme-accent) 50%, transparent);
}
</style>
