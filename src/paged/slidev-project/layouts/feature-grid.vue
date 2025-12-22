<script setup lang="ts">
/**
 * Feature Grid Layout
 * 
 * 3-column grid for up to 6 features.
 * Inherits from SlideShell for consistent header/footer/theme/vibe.
 * 
 * Frontmatter:
 *   layout: feature-grid
 *   header: "..."    # Optional header text
 *   footer: "..."    # Optional footer text
 *   theme: dark-professional
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

// Get vibe from SlideShell injection or props
const injectedVibe = inject('vibe', computed(() => props.vibe || 'balanced'))
const currentVibe = computed(() => props.vibe || injectedVibe.value || 'balanced')

// Vibe class
const vibeClass = computed(() => `vibe-${currentVibe.value}`)
</script>

<template>
  <SlideShell :header="header" :footer="footer" :theme="theme" :vibe="vibe">
    <div class="feature-grid" :class="vibeClass">
      <header v-if="$slots.title" class="feature-title">
        <slot name="title" />
      </header>
      
      <div class="features-container">
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

.feature-title {
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 600;
  color: var(--theme-text);
}

.feature-title :deep(h1),
.feature-title :deep(h2),
.feature-title :deep(h3) {
  color: var(--theme-primary);
  margin: 0;
}

.features-container {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.feature-box {
  padding: 1.5rem;
  border-radius: var(--radius-md);
  background: var(--theme-bg-surface);
  border: 1px solid var(--theme-border-subtle);
  color: var(--theme-text);
  box-shadow: var(--shadow-sm);
  position: relative;
}

/* Accent bar at top */
.feature-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--theme-primary);
  border-radius: var(--radius-md) var(--radius-md) 0 0;
}

.feature-box:nth-child(3n+2)::before {
  background: var(--theme-accent);
}

.feature-box:nth-child(3n+3)::before {
  background: var(--theme-success);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
}

.vibe-minimal .features-container {
  gap: 0.75rem;
}

.vibe-minimal .feature-box {
  padding: 1rem;
  border-radius: var(--radius-sm);
  background: transparent;
  border: 1px solid var(--theme-border);
  box-shadow: none;
}

.vibe-minimal .feature-box::before {
  height: 2px;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  padding: 1.5rem;
}

.vibe-clean .features-container {
  gap: 1rem;
}

.vibe-clean .feature-box {
  padding: 1.25rem;
  border-radius: var(--radius-sm);
}

/* === VIBE: BALANCED (default) === */
/* Base styles above */

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  padding: 2.5rem;
}

.vibe-decorative .features-container {
  gap: 2rem;
}

.vibe-decorative .feature-box {
  padding: 2rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-bg-surface) 95%, var(--theme-primary))
  );
  border: none;
}

.vibe-decorative .feature-box::before {
  height: 4px;
  box-shadow: 0 2px 8px color-mix(in srgb, var(--theme-primary) 50%, transparent);
}

/* Slight variations */
.vibe-decorative .feature-box:nth-child(odd) {
  transform: translateY(-4px) rotate(-0.3deg);
}

.vibe-decorative .feature-box:nth-child(even) {
  transform: translateY(4px) rotate(0.3deg);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 3rem;
}

.vibe-expressive .features-container {
  gap: 2.5rem;
}

.vibe-expressive .feature-box {
  padding: 2.5rem;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg), var(--shadow-glow);
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-bg-elevated) 70%, var(--theme-primary))
  );
  border: none;
}

.vibe-expressive .feature-box::before {
  height: 5px;
  background: linear-gradient(90deg, var(--theme-primary), var(--theme-accent));
  box-shadow: 0 2px 12px color-mix(in srgb, var(--theme-primary) 60%, transparent);
}

/* Dramatic variations */
.vibe-expressive .feature-box:nth-child(odd) {
  transform: translateY(-8px) rotate(-0.5deg);
}

.vibe-expressive .feature-box:nth-child(even) {
  transform: translateY(8px) rotate(0.5deg);
}

/* Asymmetric radii */
.vibe-expressive .feature-box:nth-child(3n+1) {
  border-radius: var(--radius-xl) var(--radius-sm) var(--radius-xl) var(--radius-sm);
}

.vibe-expressive .feature-box:nth-child(3n+2) {
  border-radius: var(--radius-sm) var(--radius-xl) var(--radius-sm) var(--radius-xl);
}

/* Corner accent */
.vibe-expressive .feature-box::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 50px;
  height: 50px;
  background: radial-gradient(
    circle at bottom right,
    color-mix(in srgb, var(--theme-primary) 10%, transparent) 0%,
    transparent 70%
  );
  border-radius: 0 0 var(--radius-xl) 0;
}
</style>
