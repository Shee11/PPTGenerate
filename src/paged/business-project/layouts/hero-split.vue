<script setup lang="ts">
/**
 * Hero Split Layout - Business Project
 * 
 * Two-panel split layout with configurable ratio.
 * 
 * Slots:
 *   - left: Left panel content
 *   - right: Right panel content
 * 
 * Frontmatter:
 *   layout: hero-split
 *   ratio: 50-50       # Split ratio (e.g., "60-40", "70-30")
 *   header: "..."
 *   footer: "..."
 *   theme: business_professional
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

const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="hero-split" :class="vibeClass">
      <div class="split-panel split-left" :style="{ width: splitRatio.left }">
        <slot name="left" />
      </div>
      
      <div class="split-divider"></div>
      
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
  gap: 2rem;
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

.split-panel :deep(ul),
.split-panel :deep(ol) {
  padding-left: 1.5rem;
  margin: 0;
}

.split-panel :deep(li) {
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.split-panel :deep(p) {
  margin-bottom: 1rem;
  line-height: 1.6;
}

.split-left {
  padding-right: 1rem;
}

.split-right {
  padding-left: 1rem;
}

.split-divider {
  width: 2px;
  background: linear-gradient(
    180deg,
    transparent,
    var(--theme-border),
    var(--theme-primary),
    var(--theme-border),
    transparent
  );
  flex-shrink: 0;
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  gap: 1rem;
  padding: 1.5rem;
}

.vibe-minimal .split-divider {
  width: 1px;
  background: var(--theme-border);
}

/* === VIBE: CLEAN === */
.vibe-clean {
  gap: 1.5rem;
  padding: 1.75rem;
}

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  gap: 2.5rem;
  padding: 2.5rem;
}

.vibe-decorative .split-divider {
  width: 3px;
  background: linear-gradient(
    180deg,
    transparent,
    var(--theme-primary),
    var(--theme-accent),
    var(--theme-primary),
    transparent
  );
}

.vibe-decorative .split-left {
  padding: 1.5rem;
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--theme-primary) 3%, var(--theme-bg-surface)),
    var(--theme-bg-surface)
  );
  border-radius: var(--radius-md);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  gap: 3rem;
  padding: 3rem;
}

.vibe-expressive .split-panel {
  padding: 2rem;
  background: var(--theme-bg-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.vibe-expressive .split-divider {
  width: 4px;
  background: linear-gradient(
    180deg,
    var(--theme-primary),
    var(--theme-accent)
  );
  border-radius: 2px;
}
</style>
