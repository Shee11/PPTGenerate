<script setup lang="ts">
/**
 * Timeline Layout
 * 
 * Vertical timeline with up to 5 steps.
 * Inherits from SlideShell for consistent header/footer/theme/vibe.
 * 
 * Frontmatter:
 *   layout: timeline
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
    <div class="timeline" :class="vibeClass">
      <header v-if="$slots.title" class="timeline-title">
        <slot name="title" />
      </header>
      
      <div class="timeline-container">
        <div v-if="$slots.step1" class="timeline-step">
          <div class="step-marker">1</div>
          <div class="step-content">
            <slot name="step1" />
          </div>
        </div>
        
        <div v-if="$slots.step2" class="timeline-step">
          <div class="step-marker">2</div>
          <div class="step-content">
            <slot name="step2" />
          </div>
        </div>
        
        <div v-if="$slots.step3" class="timeline-step">
          <div class="step-marker">3</div>
          <div class="step-content">
            <slot name="step3" />
          </div>
        </div>
        
        <div v-if="$slots.step4" class="timeline-step">
          <div class="step-marker">4</div>
          <div class="step-content">
            <slot name="step4" />
          </div>
        </div>
        
        <div v-if="$slots.step5" class="timeline-step">
          <div class="step-marker">5</div>
          <div class="step-content">
            <slot name="step5" />
          </div>
        </div>
      </div>
    </div>
  </SlideShell>
</template>

<style scoped>
.timeline {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
}

.timeline-title {
  margin-bottom: 1rem;
  text-align: center;
  font-weight: 600;
  color: var(--theme-text);
}

.timeline-title :deep(h1),
.timeline-title :deep(h2),
.timeline-title :deep(h3) {
  color: var(--theme-primary);
  margin: 0;
}

.timeline-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding-left: 1rem;
  min-height: 0;
}

.timeline-step {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  flex: 1 1 auto;
  min-height: 2.5rem;
  position: relative;
}

/* Connecting line */
.timeline-step:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 1rem;
  top: 2.5rem;
  width: 2px;
  bottom: 0;
  background: linear-gradient(
    180deg,
    var(--theme-primary) 0%,
    var(--theme-border) 100%
  );
  opacity: 0.5;
}

.step-marker {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  flex-shrink: 0;
  background: var(--theme-primary);
  color: var(--theme-bg-base);
  box-shadow: var(--shadow-sm);
  position: relative;
  z-index: 2;
}

.step-content {
  flex: 1;
  padding: 0.5rem 0.75rem;
  background: var(--theme-bg-surface);
  border-radius: var(--radius-sm);
  border-left: 2px solid var(--theme-primary);
  color: var(--theme-text);
}

/* === VIBE: MINIMAL === */
.vibe-minimal {
  padding: 1rem;
}

.vibe-minimal .timeline-container {
  padding-left: 0.5rem;
}

.vibe-minimal .step-marker {
  width: 1.5rem;
  height: 1.5rem;
  font-size: 0.75rem;
  background: var(--theme-border);
  color: var(--theme-text);
}

.vibe-minimal .step-content {
  padding: 0.25rem 0.5rem;
  background: transparent;
  border-radius: 0;
  border-left: 1px solid var(--theme-border);
}

.vibe-minimal .timeline-step:not(:last-child)::after {
  width: 1px;
  opacity: 0.3;
}

/* === VIBE: CLEAN === */
.vibe-clean {
  padding: 1.25rem;
}

.vibe-clean .step-marker {
  width: 1.75rem;
  height: 1.75rem;
  font-size: 0.8rem;
}

.vibe-clean .step-content {
  padding: 0.375rem 0.625rem;
}

/* === VIBE: BALANCED (default) === */
/* Base styles above */

/* === VIBE: DECORATIVE === */
.vibe-decorative {
  padding: 2rem;
}

.vibe-decorative .timeline-container {
  padding-left: 1.5rem;
}

.vibe-decorative .step-marker {
  width: 2.5rem;
  height: 2.5rem;
  font-size: 1rem;
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-accent));
  box-shadow: var(--shadow-md), 0 0 0 4px color-mix(in srgb, var(--theme-primary) 20%, transparent);
}

.vibe-decorative .step-content {
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  border-left: 3px solid var(--theme-primary);
  box-shadow: var(--shadow-sm);
  background: linear-gradient(
    135deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-bg-surface) 95%, var(--theme-primary))
  );
}

.vibe-decorative .timeline-step:not(:last-child)::after {
  width: 3px;
  background: linear-gradient(
    180deg,
    var(--theme-primary) 0%,
    var(--theme-accent) 100%
  );
  opacity: 0.6;
}

/* Alternating positioning */
.vibe-decorative .timeline-step:nth-child(odd) .step-content {
  transform: translateX(4px);
  border-radius: var(--radius-md) var(--radius-lg) var(--radius-md) var(--radius-sm);
}

.vibe-decorative .timeline-step:nth-child(even) .step-content {
  transform: translateX(-4px);
  border-radius: var(--radius-lg) var(--radius-md) var(--radius-sm) var(--radius-md);
}

/* === VIBE: EXPRESSIVE === */
.vibe-expressive {
  padding: 2.5rem;
}

.vibe-expressive .timeline-container {
  padding-left: 2rem;
}

.vibe-expressive .step-marker {
  width: 3rem;
  height: 3rem;
  font-size: 1.125rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-accent));
  box-shadow: 
    var(--shadow-lg),
    0 0 0 6px color-mix(in srgb, var(--theme-primary) 15%, transparent),
    var(--shadow-glow);
}

/* Glow effect */
.vibe-expressive .step-marker::after {
  content: '';
  position: absolute;
  inset: -6px;
  border-radius: 50%;
  background: radial-gradient(circle, color-mix(in srgb, var(--theme-primary) 30%, transparent) 0%, transparent 70%);
  z-index: -1;
}

.vibe-expressive .step-content {
  padding: 1rem 1.25rem;
  border-radius: var(--radius-lg);
  border-left: 4px solid var(--theme-primary);
  box-shadow: var(--shadow-md);
  background: linear-gradient(
    145deg,
    var(--theme-bg-surface),
    color-mix(in srgb, var(--theme-bg-elevated) 80%, var(--theme-primary))
  );
}

.vibe-expressive .timeline-step:not(:last-child)::after {
  width: 4px;
  background: linear-gradient(
    180deg,
    var(--theme-primary) 0%,
    var(--theme-accent) 50%,
    var(--theme-primary) 100%
  );
  opacity: 0.8;
  box-shadow: var(--shadow-glow);
}

/* More dramatic alternating */
.vibe-expressive .timeline-step:nth-child(odd) .step-content {
  transform: translateX(8px) rotate(-0.5deg);
}

.vibe-expressive .timeline-step:nth-child(even) .step-content {
  transform: translateX(-8px) rotate(0.5deg);
}
</style>
