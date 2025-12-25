<script setup lang="ts">
/**
 * Feature Grid Layout - Business Project
 * 
 * Grid of feature boxes with icons/titles.
 * 
 * Slots:
 *   - title: Grid title
 *   - feature1, feature2, feature3, feature4, feature5, feature6: Feature boxes
 * 
 * Frontmatter:
 *   layout: feature-grid
 *   cols: 3          # Number of columns (2-3)
 *   header: "..."
 *   footer: "..."
 *   theme: business_professional
 *   vibe: balanced
 */
import { computed, inject } from 'vue'
import SlideShell from './SlideShell.vue'

const props = defineProps<{
  cols?: number
  header?: string
  footer?: string
  theme?: string
  vibe?: 'minimal' | 'clean' | 'balanced' | 'decorative' | 'expressive'
}>()

const injectedVibe = inject('vibe', computed(() => props.vibe || 'balanced'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'balanced')

const columnCount = computed(() => {
  const cols = props.cols || 3
  return Math.max(2, Math.min(3, cols))
})

const gridStyle = computed(() => ({
  gridTemplateColumns: `repeat(${columnCount.value}, 1fr)`
}))

const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="feature-grid" :class="vibeClass">
      <header v-if="$slots.title" class="grid-title">
        <slot name="title" />
      </header>
      
      <div class="grid-container" :style="gridStyle">
        <div v-if="$slots.feature1" class="feature-box">
          <slot name="feature1" />
        </div>
        <div v-if="$slots.feature2" class="feature-box">
          <slot name="feature2" />
        </div>
        <div v-if="$slots.feature3" class="feature-box">
          <slot name="feature3" />
        </div>
        <div v-if="$slots.feature4" class="feature-box">
          <slot name="feature4" />
        </div>
        <div v-if="$slots.feature5" class="feature-box">
          <slot name="feature5" />
        </div>
        <div v-if="$slots.feature6" class="feature-box">
          <slot name="feature6" />
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.feature-grid {
  height: 100%;
  width: 100%;
  padding: 2rem;
  display: flex;
  flex-direction: column;
}

.grid-title {
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 600;
  color: var(--theme-text);
}

.grid-title :deep(h1),
.grid-title :deep(h2),
.grid-title :deep(h3) {
  color: var(--theme-primary);
  margin: 0;
}

.grid-container {
  flex: 1;
  display: grid;
  gap: 1.5rem;
  align-content: center;
}

.feature-box {
  padding: 1.5rem;
  border-radius: var(--radius-md);
  background: var(--theme-bg-surface);
  border: 1px solid var(--theme-border);
  box-shadow: var(--shadow-sm);
  text-align: center;
}

.feature-box :deep(h3),
.feature-box :deep(h4) {
  color: var(--theme-primary);
  margin-top: 0;
  margin-bottom: 0.75rem;
  font-family: var(--font-heading);
}

.feature-box :deep(p) {
  color: var(--theme-text-muted);
  font-size: 0.9rem;
  margin: 0;
  line-height: 1.5;
}

/* Icon styling */
.feature-box :deep(.icon),
.feature-box :deep(svg) {
  width: 3rem;
  height: 3rem;
  margin-bottom: 1rem;
  color: var(--theme-primary);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1.5rem;
}

.vibe-minimal .grid-container {
  gap: 1rem;
}

.vibe-minimal .feature-box {
  padding: 1rem;
  border-radius: var(--radius-sm);
  box-shadow: none;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  padding: 1.75rem;
}

.vibe-clean .grid-container {
  gap: 1.25rem;
}

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  padding: 2.5rem;
}

.vibe-decorative .grid-container {
  gap: 2rem;
}

.vibe-decorative .feature-box {
  padding: 2rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: none;
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    var(--theme-bg-elevated)
  );
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 3rem;
}

.vibe-expressive .grid-container {
  gap: 2.5rem;
}

.vibe-expressive .feature-box {
  padding: 2.5rem;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.vibe-expressive .feature-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--theme-primary), var(--theme-accent));
}
</style>
